import spacy
from spacy.tokens import Span, Doc
from spacy.matcher import Matcher
from verbfinder import get_verb_chunks
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
    "The cake, which was baked by my sister, was delicious."
)

# Given an entity or token, find the complete span associated with it by finding its children


def extract_span_from_entity(token):
    children = []
    for child in token.subtree:
        children.append(child)
    # This will sort the list of children based on the values returned by x.i.
    # In other words, it will sort the children in ascending order of their positions in the document.
    entity_subtree = sorted(children, key=lambda x: x.i)
    extracted_span = Span(
        token.doc, start=entity_subtree[0].i, end=entity_subtree[-1].i + 1)  # The -1 index is used to access the last element in the entity_subtree list, which represents the last token in the sorted subtree.
    return extracted_span


def find_determiners_for_noun(noun, doc):
    for child in noun.children:
        if(child.pos_ == "DET"):
            return child
    return None


def find_parent_token_for_child(target_child, doc):
    for token in doc:
        for child in token.children:
            if child == target_child:
                return token
    return None


def find_subject_in_passive_construction(verb_span, doc):
    # print(type(verb_span))
    number_of_parts = len(verb_span)
    if number_of_parts > 1:
        for verb_part in verb_span:
            print(f"verb part: {verb_part.text}")
            if(verb_part.tag_ == "VBN"):
                parent = find_parent_token_for_child(verb_part, doc)
                if(parent):
                    if parent.dep_ == "nsubj":
                        # now we find any determiners
                        determiner = find_determiners_for_noun(parent, doc)
                        if(determiner):
                            parent_as_span = doc[determiner.i: parent.i + 1]
                        else:
                            parent_as_span = doc[parent.i: parent.i + 1]
                        print(
                            f"verb : {verb} has an active voice subject {parent_as_span}")
                        return parent_as_span
    return None


def extract_subjects(verb, doc):
    root = verb.root
    while root:
        if(root.children):
            # Can we find subject at current level by looking for Nominal Subjects or a Passive Nominal Subjects?
            for child in root.children:  # examine the children of the verb
                # is it a Nominal Subject or a Passive Nominal Subject. Note: there are other less common dependencies that can indicate subjects:
                # csubj (Clausal Subject): This label is used to identify clausal subjects, which are entire clauses that function as the subject of the main clause.
                # expl (Expletive Subject): This label is used for expletive subjects, which are placeholders like "it" or "there" that don't have a clear referent.
                # csubjpass (Clausal Subject in Passive): Similar to "csubj," this label is used to identify entire clauses that function as the subject in passive voice sentences.
                if child.dep_ in ["nsubj", "nsubjpass"]:
                    subject = extract_span_from_entity(child)
                    if(child.dep_ == "nsubj"):
                        print(
                            f"The verb phrase that contains [{verb}] has a child dependency [{child.dep_}] that points to a Nominal Subject: [{subject}].")
                    else:
                        print(
                            f"The verb phrase that contains [{verb}] has a child dependency [{child.dep_}] that points to a Passive Nominal Subject: [{subject}].")
                        subject_as_active_voice_construction = find_subject_in_passive_construction(
                            verb, doc)
                        if(subject_as_active_voice_construction):
                            return subject_as_active_voice_construction
                    return subject
        else:
            print(f"The verb [{verb}] has no children")
        # If we cannot find children which are subjects then we recurse up one level in the sentence tree by looking for dependencies that point towards other clauses
        if (root.dep_ in ["conj", "cc", "advcl", "acl", "ccomp", "auxpass"]
                and root != root.head):
            print(
                f"The verb [{verb}] has a dependency [{root.dep_}] that indicates the presence of other clauses.")
            root = root.head
        else:  # we have a verb with no children or one whose children do not have a nominal or passive nominal subject and which does not appear to have other clauses
            root = None

    return None


if __name__ == "__main__":
    import spacy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    lnlp.show_sentence_parts(doc)
    print(f"Finding the subjects for the sentence: {text}")
    verb_chunks = get_verb_chunks(doc)
    for verb in verb_chunks:
        print(f"Finding the subjects for the verb: {verb}")
        subject = extract_subjects(verb, doc)
        print(f"Verb: {verb}  Subject: {subject}")
