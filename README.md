# pyCKY
Implementation of the CKY (Cocke-Kasami-Younger) algorithm

## Usage

```
python recognizer.py <grammar file> <sentence> [--tree]
```

## Documentation

### greader.py

This code file contains the functions to parse the grammar file. 
The expected grammar is a CNF (Chomsky Normal Form) grammar. 
That kind of grammar only have rules of the form:
 
```
A -> B C
A -> a
```

where *A, B, C* are non terminal symbols and *a* are terminal symbols. 
Note that all CFG (Context Free Grammar) can be convert in a CNF.

An example of grammar file is:

```
S
S -> NP VP
VP -> VP PP | V NP | eats
PP -> P NP
NP -> DET N | she
V -> eats
P -> with
N -> fish | fork
DET -> a
```

Note: the first line must be indicate a list of root symbols.

### cky.py

It is the **cky** implementation and the tree parser generator. 
The principal function *cky* have the follow required parameters:

- *Roots*: list of root non terminal symbols
- *NT*: list of non terminal symbols of the grammar
- *T*: list of terminal symbols of the grammar
- *GT*: list of terminal rules of type: A -> a
- *GNT*: list of non therminal rules of type: A -> B C
- *words*: list of words that form part of sentence to recognize/analyze

The parameter *Roots*, NT, T, GT, GNT are all genereted by the **parse_cnf** function.

Additionally, the function *cky* can receive two optional parameters *show_table* and *gettree* 
to display the generated cky table and the tree parsers.

### recognizer.py

It is the command line to invoke the above *cky* function and described in the usage section 
of this document.

### G1.g, G2.g, G3.g

Three toy grammars to test this implementation. 

## Examples

That are some execution samples of this work:

An grammar to recognize the language defines by the regular expresion a+b+ 
(a list of a's follow a list of b's):

```
$ python recognize.py G1.g 'a a a a a b' --tree

   a     a     a     a     a     b    
2  A     A     A     A     A     B    
3  A     A     A     A     S     .    
4  A     A     A     A,S   .     .    
5  A     A     A,S   .     .     .    
6  A     A,S   .     .     .     .    
7  A,S   .     .     .     .     .    

Tree
S
├── A
│   ├── A (a)
│   └── A
│       ├── A (a)
│       └── A
│           ├── A (a)
│           └── A
│               ├── A (a)
│               └── A (a)
└── B (b)

a a a a a b is member of the language
```


An typical example in grammar recognition:
```
$ python recognize.py G2.g 'she eats a fish with a fork' --tree

   she    eats   a      fish   with   a      fork  
2  NP     VP,V   DET    N      P      DET    N     
3  S      .      NP     .      .      NP     .     
4  .      VP     .      .      PP     .      .     
5  S      .      .      .      .      .      .     
6  .      .      .      .      .      .      .     
7  .      VP     .      .      .      .      .     
8  S      .      .      .      .      .      .     

Tree
S
├── NP (she)
└── VP
    ├── VP
    │   ├── V (eats)
    │   └── NP
    │       ├── DET (a)
    │       └── N (fish)
    └── PP
        ├── P (with)
        └── NP
            ├── DET (a)
            └── N (fork)

 she eats a fish with a fork is member of the language
```

In the last example is used an ambiguety grammar and show two tree parsers to recognize 
the sentence 'a + a - a':

```
$ python recognize.py G3.g 'a + a - a' --tree

   a    +    a    -    a   
2  A    OP   A    OP   A   
3  .    R    .    R    .   
4  A    .    A    .    .   
5  .    R    .    .    .   
6  A    .    .    .    .   

Tree
A
├── A (a)
└── R
    ├── OP (+)
    └── A
        ├── A (a)
        └── R
            ├── OP (-)
            └── A (a)

Tree
A
├── A
│   ├── A (a)
│   └── R
│       ├── OP (+)
│       └── A (a)
└── R
    ├── OP (-)
    └── A (a)

 a + a - a is member of the language
```