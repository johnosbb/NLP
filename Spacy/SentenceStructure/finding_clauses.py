
import spacy
from spacy.tokens import Span, Doc
from spacy.matcher import Matcher
import libnlp as lnlp
from clause import Clause
from spacy.language import Language

sample_sentences = [
    "The boy has walked to the school and has eaten his lunch.",
    "The cat and the dog are playful, and the bird is singing on the tree.",
    "The red car sped down the highway.",
    "The boy walked to the school, ate his lunch and then had taken a nap.",
    "She spoke eloquently at the conference.",
    "She considers him a friend.",
    "Chester is a banker by trade, but is dreaming of becoming a great dancer.",
    " A cat , hearing that the birds in a certain aviary were ailing dressed himself up as a physician , and , taking his cane and a bag of instruments becoming his profession , went to call on them .",
    "I consider Kris a fool",
    "It was a letter that she wrote.",
    "It was a dog that she killed."
    
    
]

def find_clause(sentence: Doc):
    clauses = []
    # verb_matches = lnlp.get_verb_matches_for_span(sentence)
    unique_verb_spans = lnlp.get_unique_verb_spans(sentence)
    for verb_span in unique_verb_spans:            
        subject_span = lnlp.extract_subjects(verb_span, sentence)
        # Check if there are phrases of the form, "AE, a scientist of ..."
        # If so, add a new clause of the form:
        # <AE, is, a scientist>
        if (subject_span):
            for c in subject_span.root.children:
                if c.dep_ == "appos":  # In spaCy, the dependency label "appos" stands for "appositional modifier." An appositional modifier is a grammatical construction in which two noun phrases, often called noun "apposites," are placed next to each other, and one provides additional information or clarification about the other.
                    # this creates a span based on the tokens subtree
                    complement = lnlp.find_span_for_token(c)
                    clause = Clause(subject_span,complement)
                    clauses.append(clause)
        compliment_span = lnlp.find_compliment_as_span_for_token(verb_span.root)
        indirect_object_span = lnlp.find_matching_child_span(verb_span.root, ["dative"]) # the term "dative" typically refers to a grammatical case or construction that marks the recipient or indirect object of an action.
        direct_object_span = lnlp.find_matching_child_span(verb_span.root, ["dobj"]) 
        adverbial_spans = [
            lnlp.find_span_for_token(c)
            for c in verb_span.root.children
            if c.dep_ in ("prep", "advmod", "agent")
        ]
        if(subject_span): # A clause must have a subject
            clause = Clause(subject_span, verb_span,indirect_object_span,direct_object_span,compliment_span, adverbial_spans)
            clauses.append(clause)
    clause_number = 1    
    for clause in clauses:
        print(f"\tClause {clause_number}: {clause} Type : {clause.type}")
        print(f"\t\t{clause.to_propositions(as_text=True,inflect=None,capitalize=True)}") 
        clause_number = clause_number + 1   


def process_sample_sentences(nlp : Language):

    for sample_sentence in sample_sentences:        
        sentence = nlp(
            sample_sentence)
        print(f"Sentence: {sample_sentence}")
        find_clause(sentence)
        
if __name__ == "__main__":    
    nlp = spacy.load("en_core_web_lg")
    # process_sample_sentences(nlp)
    sentence = nlp(sample_sentences[10])
    print(f"Sentence: {sentence}")
    lnlp.show_sentence_parts_as_md(sentence)
    find_clause(sentence)

        


