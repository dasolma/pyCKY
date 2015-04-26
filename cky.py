import sys
import numpy as np
from parser import *

def main(args=None):
    if args is None:
        args = sys.argv

    if len(args) != 3:
        print "Usage:"
        print "cky.py <grammar file> <sentence>"

    else:
        R, NT, T, Gt, GT, valid = parse_cnf(open(args[1]))

        if valid:
            print (R, NT, T, Gt, GT)
            if cky(R, NT, T, Gt, GT, args[2].split(" ")):
                print "%s is member of the language"%args[2]
            else:
                print "%s is not member of the language"%args[2]




###############################################################
#### CKY ALGORITHM
###############################################################
#Pseudocode from wikipedia
def cky(Roots, NT, T, Gt, GT, words):
    #The input string s consist of n letters, a1... an.
    n = len(words)
    #The grammar contain r terminal and nonterminal symbols R1... Rr.
    r = len(NT)
    #Let P[n,n,r] be an array of booleans. Initialize all elements of P to false.
    P = np.zeros((n,n,r))
    #For each i = 1 to n
    for i in range(0,n):
        # For each unit production Rj -> ai, set P[i,1,j] = true.
        for R,a in Gt.iteritems():
            w = words[i]
            if words[i] == a[0]: P[0, i, NT.index(R)] = 1

    #For each i = 2 to n -- Length of span
    for i in range(2, n+1):
        #For each j = 1 to n-i+1 -- Start of span
        for j in range(1, n-i+2):
            #For each k = 1 to i-1 -- Partition of span
            for k in range(1, i):
                #For each production RA -> RB RC
                for l,r in GT.iteritems():
                    #if P[k,j,B] and P[i-k,j+k,C] then set P[i,j,A] = true
                    if P[k-1, j-1, NT.index(r[0])] == 1 and \
                        P[i-k-1,j+k-1, NT.index(r[1])] == 1:
                        P[i-1,j-1,NT.index(l)] = 1

    # if any of P[n,1,x] is true (x is iterated over the set s, where s are all the indices for Rs) then
    #   Then string is member of language
    #   Else string is not member of language
    for r in Roots:
        print r
        j = NT.index(r)
        if P[n-1,0,j] == 1: return True

    return False


#### MAIN
if __name__ == "__main__":
    sys.exit(main())

