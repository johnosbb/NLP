import spacy
from spacy.tokens import Span, Doc
from spacy.matcher import Matcher
from verbfinder import get_verb_chunks

text_complex = (
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
    "After I finished my homework, I went to the park."
)

# Given an entity or token, find the complete span associated with it by finding it children


def extract_span_from_entity(token):
    children = []
    for child in token.subtree:
        children.append(child)
    entity_subtree = sorted(children, key=lambda x: x.i)
    return Span(token.doc, start=entity_subtree[0].i, end=entity_subtree[-1].i + 1)


def extract_subjects(verb):
    root = verb.root
    while root:
        # Can we find subject at current level by looking for Nominal Subjects or a Passive Nominal Subjects?
        for child in root.children:  # examine the children of the verb
            # is it a Nominal Subject or a Passive Nominal Subject
            if child.dep_ in ["nsubj", "nsubjpass"]:
                subject = extract_span_from_entity(child)
                return subject
        # ... otherwise recurse up one level in the sentence tree by looking for dependencies that point towards other clauses
        if (root.dep_ in ["conj", "cc", "advcl", "acl", "ccomp"]
                and root != root.head):
            root = root.head
        else:  # we have a verb with no children or one whose children do not have a nominal or passive nominal subject
            root = None

    return None


if __name__ == "__main__":
    import spacy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    verb_chunks = get_verb_chunks(doc)
    for verb in verb_chunks:
        subject = extract_subjects(verb)
        print(f"Verb: {verb}  Subject: {subject}")
