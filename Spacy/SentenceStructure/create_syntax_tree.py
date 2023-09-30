# Import required libraries
import spacy
from nltk import Tree
from nltk import pos_tag, word_tokenize, RegexpParser
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


# https://lin-tree-solver.adambcomer.com/
# https://www.bu.edu/linguistics/UG/course/lx522-f01/handouts/lx522-2-trees.pdf
# https://study.com/skill/learn/how-to-identify-noun-and-verb-phrases-explanation.html


def convert_element_tree(element):
    converted_element = f"[{element.label()} "
    for part in element:
        if isinstance(part, Tree):
            converted_tree = convert_element_tree(part)
            converted_element = converted_element + converted_tree + "]"
        elif isinstance(part, tuple):
            modifiers = ""
            value, identifier = part
            modifier_formatted = f"[{identifier} {value}]"
            modifiers += modifier_formatted
            converted_element = converted_element + modifiers
    return converted_element


def show(node):
    if isinstance(node, Tree):
        print(f"tree node = {node} label = {node.label()}")
        for child in node:
            show(child)
    else:  # otherwise it is just a tuple representing a leaf
        # print(f"node = {node}")
        print(f"non tree node = {node}")

# [S  [NNP John]
#   [MD may]
#   [VP    [VB eat]
#   ]
#   [NNS apples]
#   [. .]
# ]


# Example text

sample_text = "Bell, a telecommunication company, which is based in Los Angeles, makes and distributes electronic, computer and building products."
sample_text = "She walked to the park."
sample_text = "She painted a beautiful landscape with a palette of vibrant colors."
sample_text = "John may eat apples."
sample_text = "The quick brown fox jumps over the lazy dog"

# Find all parts of speech in above sentence
tagged = pos_tag(word_tokenize(sample_text))

print(f"tagged = {tagged}")
# Extract all parts of speech from any text
chunker = RegexpParser("""
                       NP: {<DT|PRP\$>?<JJ>*<NN>}    # This rule identifies noun phrases (NPs) and looks for a determiner (DT) or a possessive determiner (PRP$), followed by zero or more adjectives (JJ), and ending with a noun (NN).
                       # This rule identifies prepositions (P) and looks for words tagged as prepositions (IN)
                       P: {<IN>}
                       # This rule identifies verbs (V) and matches any word that has a tag starting with "V" (e.g., VB, VBD, VBG, etc.). This is a broad rule to capture various forms of verbs.
                       V: {<V.*>}
                       # This rule identifies prepositional phrases (PP) and looks for a word labeled as "P" (which stands for preposition) followed by an NP, which is defined by our first rule.
                       PP: {<P|TO> <NP>}
                       # To extract Verb Phrases # This rule identifies verb phrases (VP) and looks for a verb (defined by the third rule) followed by zero or more NPs or PPs.
                       VP: {<V> <NP|PP>*}
                       """)

# Print all parts of speech in above sentence
output = chunker.parse(tagged)
print("After Extracting\n", output)
converted = convert_element_tree(output) + "]"
print(converted)
# for node in output:
#     parse_node(node)
# for node in output:
#     show(output)

# To draw the parse tree
# output.draw()
