import spacy
from spacy.matcher import Matcher
import libnlp as lnlp
from spacy.tokens import Span, Doc
from typing import Union  # Import the Union type


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
    "A cat, hearing that the birds in a certain aviary were ailing dressed himself up as a physician, and, taking his cane and a bag of instruments becoming his profession, went to call on them."
)


text = (
    "After the boy finished his homework, he went to the park."
)
# If the match or span includes an adverb then we want to exclude the adverb


def remove_adverbs(match):
    filtered_matches = []
    match_id, start, end = match
    matched_tokens = doc[start:end]
    for token in matched_tokens:
        if token.pos_ == "AUX":
            filtered_matches.append(token)  # this needs to be a span tuple
        if token.pos_ == "ADV":
            filtered_matches.append(token)
        elif token.pos_ == "VERB":
            filtered_matches.append(token)
    return filtered_matches




# for each sentence in the document, get the verb forms

# this returns a list of tuples, the first item being the sentence, the second a series of spans containing the verbs associated with that sentence


def extract_verbs(doc):
    verbs = []
    for sent in doc.sents:
        verb_phrase = lnlp.get_verb_matches_for_span(sent)
        verbs.append((sent, verb_phrase))
    return verbs  # a list of verb matches






def method_1(doc):
    verb_matches = extract_verbs(doc)
    for sentence, matches in verb_matches:  # there may be multiple matches for a sentence
        # for each span we want to remove any adverbs and just retain the verb parts.
        filtered_matches = []
        for match in matches:
            # print(match)
            # filtered = remove_adverbs(match)
            filtered_matches.append(match)
        verb_spans = lnlp.extract_spans_from_matches(sentence, filtered_matches)    
        # verb_spans = extract_spans_from_match(sentence, filtered_matches)
        for verb_span in verb_spans:
            print(f"{sentence} : {verb_span.text}")
    verb_chunks = lnlp.get_verb_spans(doc)
    for chunk in verb_chunks:
        print(f"Verb: {chunk}")


def method_2(doc):
    # doc could be a multi-sentence document
    for sent in doc.sents:
        unique_matches = lnlp.get_unique_verb_spans(sent)
        print(f"Sentence: {sent} Unique verb phrases: {unique_matches}")


if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text_examples)
    method_2(doc)
    method_1(doc)
