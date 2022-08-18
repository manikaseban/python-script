import itertools, re, string, argparse, logging

# set logger
class_log_format = logging.Formatter(
    "%(asctime)ss %(levelname)s %(funcName)s: %(message)s")
logger = logging.getLogger("my_logger")

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(class_log_format)

logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

# main
def check(pw):
    low = re.search(r"[a-z]", pw)
    up = re.search(r"[A-Z]", pw)
    num = re.search(r"[0-9]", pw)
    sym = re.search(r"[!@#$%^&*()]", pw)
    result = False

    if arg.upper:
        if all((up,)) == False:
            return False
        else:
            result = True
    if arg.lower:
        if all((low,)) == False:
            return False
        else:
            result = True
    if arg.number:
        if all((num,)) == False:
            return False
        else:
            result = True
    if arg.symbol:
        if all((sym,)) == False:
            return False
        else:
            result = True

    if result:
        return result
    else:
        return all((low, up, num, sym))


def generate_password(digit, pass_length, limit_cnt, prefix):

    digit = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    if arg.digit != None:
        digit = arg.digit

    if len(prefix) < pass_length:
        pass_length -= len(prefix)
    else:
        logger.log(logging.WARNING,
                    "prefix is too long")
        exit()

    with open(arg.output, 'a') as f:

        generated_cnt = 0
        for comb in itertools.product(digit, repeat=pass_length):

            pw = ''.join(str(i) for i in comb)
            if check(pw):
                if arg.limit == -1:

                    f.write(prefix+pw)
                    f.write('\n')
                    generated_cnt += 1

                if limit_cnt > 0:
                    f.write(prefix+pw)
                    f.write('\n')
                    limit_cnt -= 1
                    generated_cnt += 1
        if limit_cnt == 0 or limit_cnt == -1:
            logger.log(logging.INFO, f"{generated_cnt} passwords are generated")
        elif limit_cnt != 0:
            logger.log(logging.WARNING,
                    "not enough combination add more digits or check digit type")


if __name__ == "__main__":
    # set parser
    parser = argparse.ArgumentParser(description="Generate password",
                                    epilog="""
        you should enter type of passwords character 
        -L/--lower -U/--upper -N/--number -S/--symbol  (default ==> all of them)
        """,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    digit_type = parser.add_argument_group()
    digit_type.add_argument('-U', "--upper", action="store_true")
    digit_type.add_argument('-L', "--lower", action="store_true")
    digit_type.add_argument('-N', "--number", action="store_true")
    digit_type.add_argument('-S', "--symbol", action="store_true")
    parser.add_argument('-li', "--limit", default=-1, nargs="?", type=int,
                        help="How many password you want to generate (default ==> all possible combination)")
    parser.add_argument("--digit", "-d", nargs="+", type=str,
                        help="digits of password (default ==> [a-z], [A-Z], [0-9] and symbols")
    parser.add_argument("--length", "-l", default=8, nargs="?",
                        type=int, help="length of password (default ==> 8 )")
    parser.add_argument("--prefix", "-p", default='', nargs="?",
                        type=str, help="prefix of password")
    parser.add_argument("--output", "-o", default='password.txt', nargs="?",
                        type=str, help="name of output file (default ==> password.txt) ")
    arg = parser.parse_args()

   
    generate_password(arg.digit, arg.length, arg.limit, arg.prefix)