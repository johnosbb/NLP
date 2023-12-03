import spacy
from spacy.tokens import Span, Doc
from spacy.tokens.token import Token  # Import the Token type
from spacy.matcher import Matcher
from typing import Union  # Import the Union type

import libnlp as lnlp

# ## Credits
# This is based on a re-implementation by Emmanouil Theofanis Chourdakis of original research work (and also the dictionaries) is attributed to Luciano Del Corro
# and Rainer Gemulla. If you use it in your code please note that there are slight modifications in the code in order to make it work with the spacy dependency parser, and also cite:
# ```
# Del Corro Luciano, and Rainer Gemulla: "Clausie: clause-based open information extraction." 
# Proceedings of the 22nd international conference on World Wide Web. ACM, 2013.
# ```

# It would be helpful to also cite this specific implementation if you are using it:
# ```
# @InProceedings{chourdakis2018grammar,
# author = {Chourdakis, E.T and Reiss, J.D.},
# title = {Grammar Informed Sound Effect Retrieval for Soundscape Generation},
# booktitle = {DMRN+ 13: Digital Music Research Network One-day Workshop},
# month = {November},
# year = {2018},
# address = {London, UK},
# pages={9}
# }



text_examples = (
    "The author was staring pensively as she wrote."
    "She is playing the piano."
    "They have been working on this project for months."
    "I will meet you at the coffee shop."
    "He can swim faster than anyone I know."
    "The cat chased the mouse across the room."
    "We should go for a walk in the park."
    "The students are anxious because they are studying for their final exams."
    "The sun sets in the west."
    "The company announced a new product."
    "It was raining heavily when I left home so I took an umbrella."
    "Breaking the window, he climbed inside the office where the safe was located."
    "I haven't finished my homework."
    "It was really raining heavily when I left home so I took a cab."
    "Are you coming to the party?"
    "After I finished my homework, I went to the park."
    "She wanted to visit the museum, but he preferred to explore the park."
    "She sings beautifully, and he dances gracefully."
    "Bell, a telecommunication company, which is based in Los Angeles, makes and distributes electronic, computer and building products."
    "The book that he recommended is on the shelf."
    "The cake, which was baked by my sister, was delicious."
    "She is a doctor."
    "She is a talented musician."
    "A cat, hearing that the birds in a certain aviary were ailing dressed himself up as a physician, and, taking his cane and a bag of instruments becoming his profession, went to call on them."
)


text = (
    "She is a talented musician."
)





if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
    sentence = input("Please enter a sentence:\n")
    doc = nlp(sentence)
    lnlp.show_sentence_parts_as_md(doc)
    print(f"Finding the subjects for the sentence: {sentence }")
    verb_spans = lnlp.get_verb_spans(doc)
    for verb_span in verb_spans:
        print(f"Finding the subjects for the verb span: {sentence }")
        subject = lnlp.extract_subjects(verb_span, doc)
        print(f"Verb: {verb_span}  Subject: {subject}")
