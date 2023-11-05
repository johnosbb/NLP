
import spacy
from spacy.tokens import Span, Doc
from spacy.matcher import Matcher
import libnlp as lnlp
from clause import Clause


if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    sentence = nlp(
        "The boy has walked to the school and has eaten his lunch.")
    sentence = nlp(
        "The boy walked to the school, ate his lunch and then had taken a nap.")
    # lnlp.show_sentence_parts(sentence)
    # these represent verbs and verb phrases so they are not tokens but matches that will correlate with a span
    verb_matches = lnlp.get_verb_matches_for_span(sentence)
    unique_spans = lnlp.get_unique_verb_spans(sentence)
    for verb_span in unique_spans:
        subject = lnlp.extract_subjects(verb_span, sentence)
        #print(f"verb_span : {verb_span} subject : {subject}")
        clause = Clause(subject, verb_span)
        print(f"Clause : {clause} Type : {clause.type}")
        indirect_object = lnlp.find_matching_child_span(verb_span.root, ["dative"]) # the term "dative" typically refers to a grammatical case or construction that marks the recipient or indirect object of an action.
        direct_object = lnlp.find_matching_child_span(verb_span.root, ["dobj"]) 
        object  = lnlp.find_object_as_span_for_token(verb_span.root)
        print(f" Indirect Object: {indirect_object } Direct Object: {direct_object} Object = {object}")
    # verb = nlp("walked")
    # clause = Clause(subject, verb)
    # print(clause)
