import sys

def main(args=None):
    if args is None:
        args = sys.argv

    if len(args) != 3:
        print "Usage:"
        print "cky.py <grammar file> <sentence>"

    else:
        G, valid = parse_grammar(open(args[1]))

        if valid:
            print G



#GRAMMAR PARSING
def parse_grammar(file):
    lines = [line.strip() for line in file]
    G = {}
    valid = True

    for line in lines:
        rule = [x.strip() for x in line.split("->")]

        if len(rule) != 2:
            print "Rule no valid: " + l
            valid = False
        else:
            l, r = rule
            r = filter(None, [x.strip() for x in r.split(" | ")])
            valid = validate_rule(l,r, line)

            if valid:
                if not l in G.keys():
                    G[l] = []
                G[l] = G[l] + r

    return (G, valid)

def validate_rule(l, r, rule):
    invalid = False
    if not l.isupper():
        cause = "left side must be a non terminal"
        invalid = True

    if len(r) == 0:
        cause = "right side can't be empty"
        invalid = True

    if invalid:
        print "Rule no valid: %s (%s)"%(rule, cause)

    return not invalid

if __name__ == "__main__":
    sys.exit(main())

