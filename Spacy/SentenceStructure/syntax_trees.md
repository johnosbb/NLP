# Syntax Trees


There are two different forms of syntax used to represent syntax trees. The choice of format often depends on the tool or library used to generate or visualize the syntax tree. 


## Bracketed Notation

This form represents the syntax tree using bracketed notation. Each node in the tree is enclosed within parentheses, and child nodes are nested within their parent nodes.
The format is typically used in linguistic and parsing literature for clear and detailed representations of syntax trees.
It explicitly shows the structure of the tree with nested brackets and includes part-of-speech tags (e.g., NNP for proper nouns), word tokens, and phrase labels (e.g., NP for noun phrases, VP for verb phrases).


```txt
[S  [NNP John]
  [MD may]
  [VP    [VB eat]
  ]
  [NNS apples]
  [. .]
]
```

```txt
[S 
    [NP [DT The][JJ quick][NN brown]]
    [NP [NN fox]]
    [VP [V [VBZ jumps]]
    [PP [P [IN over]]
    [NP [DT the][JJ lazy][NN dog]]]]

]
```

```txt
[S [PP [P [IN After]][NP [DT the][NN boy]]][VP [V [VBD finished]][NP [PRP$ his][NN homework]]][, ,][PRP he][VP [V [VBD went]][PP [TO to][NP [DT the][NN park]]]][. .]]
```

## Indented Text Notation

The second form represents the syntax tree using indented text. It is a more human-readable format that uses indentation to indicate the hierarchy of nodes. It is often used in programming and scripting contexts where a more compact and visually accessible representation is preferred.
It focuses on the hierarchical structure of the tree. Dependencies and relations between words are often implied rather than explicitly labeled.


```txt
(
    S John/NNP
    may/MD 
    (VP (V eat/VB))
    apples/NNS
    ./.
)
```

A node can be a subtree
or it can just contain a tuple
If it is a subtree then it has a label and one of more tuples

```txt
 (S
      Bell/NNP
      ,/,
      ( NP a/DT telecommunication/NN)
      (NP company/NN)
      ,/,
      which/WDT
      ( VP 
          (
             V is/VBZ
          )
      )
      ( VP 
          ( V
               based/VBN
          )
      )
      (P in/IN)
      Los/NNP
      Angeles/NNP
      ,/,
      ( VP 
           ( V 
                makes/VBZ
           )
      )
      and/CC
      ( VP 
           ( V 
               distributes/VBZ
           )
      )
      electronic/JJ
      ,/,
      ( NP
          computer/NN
      )
      and/CC
      ( NP 
          building/NN
      )
      products/NNS
      ./.
)
```


```txt
 (S
  (PP (P After/IN) (NP the/DT boy/NN))
  (VP (V finished/VBD) (NP his/PRP$ homework/NN))
  ,/,
  he/PRP
  (VP (V went/VBD) (PP to/TO (NP the/DT park/NN)))
  ./.)
```