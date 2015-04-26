###############################################################
#### SIMPLE GRAMMAR PARSING
###############################################################
def parse_cnf(file):
    lines = [line.strip() for line in file]
    G = {}
    valid = True

    R = filter(None, lines[0].split(" "))
    for line in lines[1:]:
        if line.strip() != "":
            l, r, valid = parse_rule(line)

            if valid:
                if not l in G.keys():
                    G[l] = []
                G[l] = G[l] + r

    #check if we have the start simbol 'S'
    if not 'S' in G.keys():
        print "Grammar invalid. Not found start symbol 'S'"
        valid = False



    Gt = filter_dict(G, 1)
    GT = filter_dict(G, 2)
    print GT

    return (R, G.keys(), find_terminals(G), Gt, GT, valid)

def filter_dict(d, l):
    r = {}
    for k, values in d.iteritems():
        r[k] = []
        for v in values:
            if len(v) == l: r[k] = r[k] + [v]

        if len(r[k]) == 0: del r[k]

    return r

def parse_rule(line):
    rule = [x.strip() for x in line.split("->")]
    #print line
    if len(rule) != 2:
        print "Rule no valid: " + line
        l = None
        r = None
        valid = False
    else:
        l, r = rule
        r = filter(None, [x.strip().split(' ') for x in r.split(" | ")])
        valid = validate_rule(l, r, line)

    return l, r, valid

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


def find_terminals(G):
    t = []
    for nt in G.keys():
        for r in G[nt]:
            for s in r:
                if not s in G.keys() and \
                    not s in t:
                    t = t + [s]

    return t