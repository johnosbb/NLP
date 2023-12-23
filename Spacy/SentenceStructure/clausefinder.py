
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
    "It was a dog that she killed.",
    "The foul ball hit a car parked outside.",
    "I waited for hours last night with this dreadful headache, but eventually gave up and left.",
    "But even a tough old tree will eventually die",
    "The trail of digital data you leave (both online and offline) is what makes you especially valuable.",
    "This happens because onions release an irritating chemical that makes your eyes sting.",
    "We know that the earth has had at least five major ice ages.",
    "Hoaxes, similar to disinformation, are created to persuade people that things that are unsupported by facts are true",
    "I wonder what time the movie starts.",
    "The teacher asked who had finished their homework.",
    "Can you tell me where the nearest coffee shop is?",
    "I don't know when the train will arrive.",
    "The woman asked the man why he was so sad.",
    "I'm not sure how to solve this equation.",
    "The answer to this question lies in how our brains are hardwired to think.",
    "The first ice age happened about two billion years ago and lasted about 300 million years.",
    "She drove the team crazy.",
    "There is a book on the table",
    "John's book is on the table.",
    "That she won the award is surprising.",
    "When they arrive is uncertain.",
    "Wherever you go, I will follow.",
    "Wherever you go, whatever you do, I will follow.",
    "Whatever you do, I will always be there for you.",
    "Wherever you go, I will always be there for you."
    
    
]

def find_clauses(sentence: Doc):
    clauses = []
    unique_verb_spans = lnlp.get_unique_verb_spans(sentence)
    print(f"Sentence: {sentence.text}")
    for verb_span in unique_verb_spans:            
        print(f"\nVerb: {verb_span}")
        subject_span = lnlp.extract_subjects(verb_span, sentence)
        # Check if there are phrases of the form, "AE, a scientist of ..."
        # If so, add a new clause of the form:
        # <AE, is, a scientist>
        if (subject_span):
            print(f"\tSubject of verb {verb_span}: {subject_span}")
            for c in subject_span.root.children:
                if c.dep_ == "appos":  # In spaCy, the dependency label "appos" stands for "appositional modifier." An appositional modifier is a grammatical construction in which two noun phrases, often called noun "apposites," are placed next to each other, and one provides additional information or clarification about the other.
                    # this creates a span based on the tokens subtree
                    complement = lnlp.find_span_for_token(c)
                    clause = Clause(subject_span,complement)
                    clauses.append(clause)
        compliment_span = lnlp.find_compliment_as_span_for_token(verb_span.root)
        if(compliment_span):
            print(f"\tCompliment for {verb_span}: {compliment_span}")
        indirect_object_span = lnlp.find_matching_child_span(verb_span.root, ["dative"]) # the term "dative" typically refers to a grammatical case or construction that marks the recipient or indirect object of an action.
        if(indirect_object_span):
            print(f"\tIndirect object for {verb_span}: {indirect_object_span}")
        direct_object_span = lnlp.find_matching_child_span(verb_span.root, ["dobj"]) 
        if(direct_object_span):
            print(f"\tDirect object for {verb_span}: {direct_object_span}")
        adverbial_spans = []
        for c in verb_span.root.children:
            if c.dep_ in ("prep", "advmod", "agent"):
                adverbial_spans.append(lnlp.find_span_for_token(c))   
        if(adverbial_spans):
            print(f"There {'is' if len(adverbial_spans) == 1 else 'are'} {len(adverbial_spans)} adverbial{'s:' if len(adverbial_spans) != 1 else ':'}")
            for adverbial_span in adverbial_spans:
                print(f"\t{adverbial_span}")        
        if(direct_object_span):
                print(f"\tDirect object for {verb_span}: {direct_object_span}")      
        if(subject_span): # A clause must have a subject
            clause = Clause(subject_span, verb_span,indirect_object_span,direct_object_span,compliment_span, adverbial_spans)
            clauses.append(clause)
    clause_number = 1    
    if(clauses):
        print(f"There {'is' if len(clauses) == 1 else 'are'} {len(clauses)} clause{'s:' if len(clauses) != 1 else ':'}")
        for clause in clauses:
            print(f"\t{clause_number}: {clause} Type : {clause.type}")
            print(f"\t\tProposition: {clause.to_propositions(as_text=True,inflect=None,capitalize=True)}") 
            clause_number = clause_number + 1 

            
  


def process_sample_sentences(nlp : Language):

    for sample_sentence in sample_sentences:        
        sentence = nlp(
            sample_sentence)
        print(f"Sentence: {sample_sentence}")
        find_clauses(sentence)
        
if __name__ == "__main__":    
    nlp = spacy.load("en_core_web_lg")
    sentence = input("Please enter a sentence:\n")
    doc = nlp(sentence)
    #process_sample_sentences(nlp)
    #sentence = nlp(sample_sentences[11])
    print(f"Sentence: {sentence}")
    lnlp.show_sentence_parts_as_md(doc,False)
    find_clauses(doc)

        


