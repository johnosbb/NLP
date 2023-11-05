import spacy
from spacy.tokens import Span, Doc
from spacy.tokens.token import Token  # Import the Token type
from spacy.matcher import Matcher
from typing import Union  # Import the Union type

import libnlp as lnlp


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
    "A cat, hearing that the birds in a certain aviary were ailing dressed himself up as a physician, and, taking his cane and a bag of instruments becoming his profession, went to call on them."
)


text = (
    "The cake, which was baked by my sister, was delicious."
)





if __name__ == "__main__":
    #import spacy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    lnlp.show_sentence_parts(doc)
    print(f"Finding the subjects for the sentence: {text}")
    verb_spans = lnlp.get_verb_spans(doc)
    for verb in verb_spans:
        print(f"Finding the subjects for the verb: {verb}")
        subject = lnlp.extract_subjects(verb, doc)
        print(f"Verb: {verb}  Subject: {subject}")
