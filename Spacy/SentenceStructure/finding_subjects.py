import spacy
from spacy.tokens import Span, Doc
from spacy.matcher import Matcher
from verbfinder import get_verb_chunks
import libnlp as lnlp


text = (
    "After the boy finished his homework, he went to the park."
)

# Given an entity or token, find the complete span associated with it by finding its children


def extract_span_from_entity(token):
    children = []
    for child in token.subtree:
        children.append(child)
    # This will sort the list of children based on the values returned by x.i. In other words, it will sort the children in ascending order of their positions in the document.
    entity_subtree = sorted(children, key=lambda x: x.i)
    extracted_span = Span(
        token.doc, start=entity_subtree[0].i, end=entity_subtree[-1].i + 1)  # The -1 index is used to access the last element in the entity_subtree list, which represents the last token in the sorted subtree.
    return extracted_span


def extract_subjects(verb):
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
        subject = extract_subjects(verb)
        print(f"Verb: {verb}  Subject: {subject}")
