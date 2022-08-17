import itertools, re, string, argparse, logging

#set parser
parser = argparse.ArgumentParser( description = "Generate password",\
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
parser.add_argument('-li',"--limit", default = -1, nargs = "?", type=int, help = "How many password you want to generate (default ==> all possible combination)")
parser.add_argument("--digit", "-d", nargs="+", type=str, help = "digits of password (default ==> [a-z], [A-Z], [0-9] and symbols")
parser.add_argument("--length", "-l", default = 8, nargs = "?", type=int, help = "length of password (default ==> 8 )")
parser.add_argument("--output", "-o", default = 'password.txt', nargs = "?", type=str, help = "name of output file (default ==> password.txt) ")
arg = parser.parse_args()

#set logger
class_log_format = logging.Formatter("%(asctime)ss %(levelname)s %(funcName)s: %(message)s")
logger = logging.getLogger("my_logger")

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(class_log_format)

logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

#main
digit = list(string.ascii_letters + string.digits + "!@#$%^&*()")
if arg.digit != None:
    digit = arg.digit
pass_length = arg.length


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

    
with open(arg.output,'a') as f:
    limit_cnt = arg.limit
    generated_cnt = 0
    for digit in itertools.combinations_with_replacement(digit,pass_length):
        if len(digit) == pass_length:
            pw = ''.join(str(i) for i in digit)
            if check(pw):

                comb = set(itertools.permutations(list(pw), pass_length))
                if arg.limit == -1:
                    for ele in comb:
                        f.write(''.join(i for i in ele))
                        f.write('\n')
                        generated_cnt += 1
                else:
                
                    for ele in comb:
                        if limit_cnt > 0:
                            f.write(''.join(i for i in ele))
                            f.write('\n') 
                            limit_cnt -= 1
                            generated_cnt += 1
    if limit_cnt == 0 or limit_cnt == -1:
        logger.log(logging.INFO, f"{generated_cnt} passwords are generated")
    elif limit_cnt != 0:
        logger.log(logging.WARNING, "not enough combination add more digits or check digit type")

                    
