# pyCKY
Implementation of the CKY (Cocke-Kasami-Younger) algorithm

## Usage

```
python recognizer.py <grammar file> <sentence> [--tree]
```

## Documentation

### greader.py

That code file contain the functions to parse the grammar file. 
The expected grammar is a CNF (Chomsky Normal Form) grammar. 
That kind of grammar only have rule of the form:
 
```
A -> B C
A -> a
```

where A, B, C are non terminal symbols and a are terminal symbols. 
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

It is the cky implementation and the tree parser generation. 
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

Three toy grammar to test this implementation. 

## Examples

That are some execution samples of this work:

In the last example is used a ambiguety grammar and show two tree parsers to recognize the sentence 'a + a - a':

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