
import spacy
from spacy.tokens import Span, Doc
from spacy.matcher import Matcher
from verbfinder import get_verb_chunks
import libnlp as lnlp
from clause import Clause


if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    sentence = nlp(
        "The boy has walked to the school and has eaten his lunch.")
    sentence = nlp(
        "The boy walked to the school, ate his lunch and then had taken a nap.")
    lnlp.show_sentence_parts(sentence)
    # these represent verbs and verb phrases so they are not tokens but matches that will correlate with a span
    matches = lnlp.get_verb_matches_for_span(sentence)
    unique_matches = lnlp.get_unique_verb_phrases(sentence)
    print(unique_matches)
    # verb = nlp("walked")
    # clause = Clause(subject, verb)
    # print(clause)
