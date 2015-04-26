import sys
from cky import *

def main(args=None):
    if args is None:
        args = sys.argv

    if len(args) < 3:
        print "Usage:"
        print "cky.py <grammar file> <sentence>"

    else:
        R, NT, T, Gt, GT, valid = parse_cnf(open(args[1]))

        if valid:
            #print (R, NT, T, Gt, GT)
            if cky(R, NT, T, Gt, GT, args[2].split(" "), True, True):
                print "\n %s is member of the language"%args[2]
            else:
                print "\n %s is not member of the language"%args[2]


#### MAIN
if __name__ == "__main__":
    sys.exit(main())
