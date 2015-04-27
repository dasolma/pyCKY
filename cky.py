import numpy as np
from greader import *
from treelib import Node, Tree

###############################################################
#### CKY ALGORITHM
###############################################################
#Pseudocode from wikipedia
def cky(Roots, NT, T, Gt, GT, words, show_table=False, gettree=False):
    #The input string s consist of n letters, a1... an.
    n = len(words)
    #The grammar contain r terminal and nonterminal symbols R1... Rr.
    r = len(NT)
    #Let P[n,n,r] be an array of booleans. Initialize all elements of P to false.
    P = np.zeros((n,n,r))
    if gettree:
        BP = np.empty((n,n), dtype=object)
        for i in range(0, n):
            for j in range(0, n):
                BP[i,j] = []


    #For each i = 1 to n
    for i in range(0,n):
        # For each unit production Rj -> ai, set P[i,1,j] = true.
        for R,A in Gt.iteritems():
            w = words[i]
            for a in A:
                if words[i] == a[0]:
                    P[0, i, NT.index(R)] = 1
                    if gettree: BP[0,i].append(BackPointer(R, data=a[0]))

    #For each i = 2 to n -- Length of span
    for i in range(2, n+1):
        #For each j = 1 to n-i+1 -- Start of span
        for j in range(1, n-i+2):
            #For each k = 1 to i-1 -- Partition of span
            for k in range(1, i):
                #For each production RA -> RB RC
                for l,R in GT.iteritems():
                    for r in R:
                        #if P[k,j,B] and P[i-k,j+k,C] then set P[i,j,A] = true
                        if P[k-1, j-1, NT.index(r[0])] == 1 and \
                            P[i-k-1,j+k-1, NT.index(r[1])] == 1:
                            P[i-1,j-1,NT.index(l)] = 1

                            if gettree:
                                BP[i-1,j-1].append(BackPointer(l,
                                        p1=getBP(BP[k-1, j-1], r[0]),
                                        p2=getBP(BP[i-k-1,j+k-1], r[1])))


    # if any of P[n,1,x] is true (x is iterated over the set s, where s are all the indices for Rs) then
    #   Then string is member of language
    #   Else string is not member of language
    if show_table: display_table(P, T, NT, words)
    create_trees(BP, Roots, NT, n)

    for r in Roots:
        j = NT.index(r)
        if P[n-1,0,j] == 1: return True

    return False

def getBP(BP, NT):
    for bp in BP:
        if bp.name == NT:
            return bp

    return None

def display_table(P, T, NT, words):
    d = P.shape

    ##calculate the padding and the cells content
    cells = words

    for i in range(d[0]):
        for j in range(0, d[1]):
            c = []
            for k in range(0, d[2]):
                if P[i,j, k] != 0:
                    c.append(NT[k])

            if len(c) != 0:
                cells.append(','.join(c))
            else:
                cells.append(".")

    padding = max([len(c) for c in cells]) + 2


    ##print the table
    print '\n   ' + ' '.join([("%-*s" % (padding, cells[i])) for i in range(0, d[0])])
    for i in range(1,d[0]+1):
        print "%d " %(i+1),
        print ' '.join([("%-*s" % (padding, cells[i])) for i in range(i*d[0], (i+1)*d[0]) ])
        #break


###############################################################
#### BACK POINTER
###############################################################
class BackPointer:

    def __init__(self, name, data=None, p1 = None, p2 = None):
        self.name = name
        self.data = data
        self.pointers = []
        if not p1 is None: self.pointers.append(p1)
        if not p2 is None: self.pointers.append(p2)

###############################################################
#### TREE PARSER
###############################################################
def create_trees(BP, Roots, NT, n):

    for r in Roots:
        j = NT.index(r)
        for bp in BP[n-1,0]:
            print '\nTree'
            t = Tree()
            create_tree(t, bp, 0, 1)
            t.show(key=lambda x: x.identifier)


def create_tree(t, bp, pid, nid):

    if pid == 0:
        t.create_node(bp.name, nid)
    else:
        tag = bp.name
        if not bp.data is None: tag = "%s (%s)"%(tag, bp.data)
        t.create_node(tag, nid, pid)

    if len(bp.pointers) > 0:
        pid = nid
        #left
        #print len(bp.pointers[0])
        nid = create_tree(t, bp.pointers[0], pid, nid+1)
        #right
        #print len(bp.pointers[1])
        nid = create_tree(t, bp.pointers[1], pid, nid+1)

    return nid


