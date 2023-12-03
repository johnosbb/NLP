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
    "The mouse was chased by the cat."
    "The cat chased the mouse."
    "With a smile, she talked."
    "She talked with a smile."
    "He wanted to sing a song."
    "He wanted to sing."
    "It is important that we address this issue."
    "That we address this issue is important."
    "She wrote a letter."
    "It was a letter that she wrote."
    "I bought the car that he crashed"
    "It was a letter that she wrote."
    "The seeds were eaten by the bird."
    "She is a doctor."
)


text = (
    "It was a letter that she wrote."
)





if __name__ == "__main__":
    #import spacy
    nlp = spacy.load("en_core_web_sm")
    sentence = input("Please enter a sentence:\n")
    doc = nlp(sentence)
    lnlp.show_sentence_parts_as_md(doc)
    print(f"Finding the objects for the sentence: {sentence}")
    verb_spans = lnlp.get_verb_spans(doc)
    for verb_span in verb_spans:
        print(f"Finding the objects for the verb: {verb_span}")
        indirect_object_span = lnlp.find_matching_child_span(verb_span.root, ["dative"]) # the term "dative" typically refers to a grammatical case or construction that marks the recipient or indirect object of an action.
        direct_object_span = lnlp.find_matching_child_span(verb_span.root, ["dobj"]) 
        prepositional_phrase_objs = lnlp.get_prepositional_phrase_objs(doc)
        print(f"indirect_object_span: {indirect_object_span}")
        print(f"direct_object_span: {direct_object_span}")
        print(f"prepositional_phrase_objs: {prepositional_phrase_objs}")