
import spacy
from spacy.tokens import Span, Doc
from spacy.matcher import Matcher
import libnlp as lnlp
from clause import Clause
from spacy.language import Language
import sys


SILENT_MODE=False

sample_sentences = [
    {"example": "The boy has walked to the school and has eaten his lunch.", "classification": ["SV","SVO"], "comments": ""},
    {"example": "The cat and the dog are playful, and the bird is singing on the tree.", "classification": ["SVC","SV"], "comments": ""},
    {"example": "The red car sped down the highway.", "classification": ["SV"], "comments": ""},
    {"example": "The boy walked to the school, ate his lunch and then had taken a nap.", "classification": [], "comments": ""},
    {"example": "She spoke eloquently at the conference.", "classification": [], "comments": ""},
    {"example": "She considers him a friend.", "classification": [], "comments": ""},
    {"example": "Chester is a banker by trade, but is dreaming of becoming a great dancer.", "classification": [], "comments": ""},
    {"example": "A cat, hearing that the birds in a certain aviary were ailing dressed himself up as a physician, and, taking his cane and a bag of instruments becoming his profession, went to call on them.", "classification": [], "comments": ""},
    {"example": "I consider Kris a fool", "classification": [], "comments": ""},
    {"example": "It was a letter that she wrote.", "classification": [], "comments": ""},
    {"example": "It was a dog that she killed.", "classification": [], "comments": ""},
    {"example": "The foul ball hit a car parked outside.", "classification": [], "comments": ""},
    {"example": "I waited for hours last night with this dreadful headache, but eventually gave up and left.", "classification": [], "comments": ""},
    {"example": "But even a tough old tree will eventually die", "classification": [], "comments": ""},
    {"example": "The trail of digital data you leave (both online and offline) is what makes you especially valuable.", "classification": [], "comments": ""},
    {"example": "This happens because onions release an irritating chemical that makes your eyes sting.", "classification": [], "comments": ""},
    {"example": "We know that the earth has had at least five major ice ages.", "classification": [], "comments": ""},
    {"example": "Hoaxes, similar to disinformation, are created to persuade people that things that are unsupported by facts are true", "classification": [], "comments": ""},
    {"example": "I wonder what time the movie starts.", "classification": [], "comments": ""},
    {"example": "The teacher asked who had finished their homework.", "classification": [], "comments": ""},
    {"example": "Can you tell me where the nearest coffee shop is?", "classification": [], "comments": ""},
    {"example": "I don't know when the train will arrive.", "classification": [], "comments": ""},
    {"example": "The woman asked the man why he was so sad.", "classification": [], "comments": ""},
    {"example": "I'm not sure how to solve this equation.", "classification": [], "comments": ""},
    {"example": "The answer to this question lies in how our brains are hardwired to think.", "classification": [], "comments": ""},
    {"example": "The first ice age happened about two billion years ago and lasted about 300 million years.", "classification": [], "comments": ""},
    {"example": "She drove the team crazy.", "classification": [], "comments": ""},
    {"example": "There is a book on the table", "classification": [], "comments": ""},
    {"example": "John's book is on the table.", "classification": [], "comments": ""},
    {"example": "That she won the award is surprising.", "classification": [], "comments": ""},
    {"example": "When they arrive is uncertain.", "classification": [], "comments": "Features an adjectival complement in 'uncertain'"},
    {"example": "Wherever you go, I will follow.", "classification": [], "comments": ""},
    {"example": "Wherever you go, whatever you do, I will follow.", "classification": [], "comments": ""},
    {"example": "Whatever you do, I will always be there for you.", "classification": [], "comments": ""},
    {"example": "Wherever you go, I will always be there for you.", "classification": [], "comments": ""},
    {"example": "The winner of the contest.", "classification": [], "comments": "This is not a clause"},
    {"example": "He cries because he is sad.", "classification": ["SV","SVC"], "comments": "The second clause is a causal clause"},
    {"example": "He cries frequently because he is sad.", "classification": ["SV","SVC"], "comments": "The second clause is a causal clause"},
    {"example": "If it rains, we will stay indoors.", "classification": ["SV","SVC"], "comments": "The second clause is a causal clause"},
    {"example": "Although it was late, he decided to go for a run.", "classification": ["SV","SVC"], "comments": "Dependent Concession clause"},
    {"example": "What she said surprised me." , "classification": [], "comments": "" },
    {"example": "The letter surprised me." , "classification": [], "comments": "" },
    {"example": "The sun was setting, casting a warm glow over the horizon, and the birds were returning to their nests as the day came to an end.",  "classification": [], "comments": "" },
    {"example": "The rain fell steadily, drumming on the roof, while the wind howled through the trees.", "classification": [], "comments": "" },
    {"example": "She gave him a book that he had been wanting for a long time.", "classification": [], "comments": "" },
    {"example": "He told her that he had written her a letter, and she handed him a pen.", "classification": [], "comments": "" },
    {"example": "He told her that he had written a letter to her, and then she handed him a pen.", "classification": [], "comments": "" },
    {"example": "He told her that he had written a letter to her, and then she handed pen to him.", "classification": [], "comments": "" },
    {"example": "The sun was shining brightly, but a cool breeze made the weather pleasant." , "classification": [], "comments": ""},
    {"example": "She painted the bedroom a soothing blue when her husband gave her a set of new brushes." , "classification": [], "comments": ""},
    {"example": "Most students have found her reasonably helpful." , "classification": [], "comments": ""}
    
    
]


def report(text : str):
    global SILENT_MODE
    if(SILENT_MODE == False):
        print(text)

def find_clauses(sentence: Doc, validate: bool=False):
    clauses = []
    unique_verb_spans = lnlp.get_unique_verb_spans(sentence)
    report(f"\n----------------\nSentence: {sentence.text}")
    for verb_span in unique_verb_spans:            
        report(f"\nVerb: {verb_span}")
        subject_span,subject_on_same_level = lnlp.extract_subjects(verb_span, sentence)
        # Check if there are phrases of the form, "AE, a scientist of ..."
        # If so, add a new clause of the form:
        # <AE, is, a scientist>
        if (subject_span):
            report(f"\tSubject of verb {verb_span}: {subject_span}")
            for c in subject_span.root.children:
                if c.dep_ == "appos":  # In spaCy, the dependency label "appos" stands for "appositional modifier." An appositional modifier is a grammatical construction in which two noun phrases, often called noun "apposites," are placed next to each other, and one provides additional information or clarification about the other.
                    # this creates a span based on the tokens subtree
                    complement = lnlp.find_span_for_token(c)
                    clause = Clause(subject_span,complement,sentence=sentence,subject_on_same_level=subject_on_same_level)
                    clauses.append(clause)
        complement_span = lnlp.find_complement_as_span_for_token(verb_span.root) # we look for clausal complement, adjectival complement,open clausal complement or attribute
        if(complement_span):
            report(f"\tcomplement for {verb_span}: {complement_span}")
        indirect_object_span = lnlp.find_matching_child_span(verb_span.root, ["dative"]) # the term "dative" typically refers to a grammatical case or construction that marks the recipient or indirect object of an action.
        if(indirect_object_span):
            report(f"\tIndirect object for {verb_span}: {indirect_object_span}")
        direct_object_span = lnlp.find_matching_child_span(verb_span.root, ["dobj"]) 
        if(direct_object_span):
            report(f"\tDirect object for {verb_span}: {direct_object_span}")
        adverbial_spans = []
        for c in verb_span.root.children:
            if c.dep_ in ("prep", "advmod", "agent"):
                adverbial_spans.append(lnlp.find_span_for_token(c))   
        if(adverbial_spans):
            report(f"There {'is' if len(adverbial_spans) == 1 else 'are'} {len(adverbial_spans)} adverbial{'s:' if len(adverbial_spans) != 1 else ':'}")
            for adverbial_span in adverbial_spans:
                report(f"\t{adverbial_span}")             
        if(subject_span): # A clause must have a subject            
            clause = Clause(subject_span, verb_span,indirect_object_span,direct_object_span,complement_span, adverbial_spans,sentence=sentence,subject_on_same_level=subject_on_same_level)
            clause.identify_complement_clause()
            clauses.append(clause)
    clause_number = 1    
    if(len(clauses) > 0):
        report(f"There {'is' if len(clauses) == 1 else 'are'} {len(clauses)} clause{'s:' if len(clauses) != 1 else ':'}")
        for clause in clauses:
            clause.identify_type()
            report(f"\t{clause_number}: {clause}, Classification : {clause.classification}, Type: {clause.type}, Subordinator {clause.subordinator}")
            report(f"\t\tProposition: {clause.to_propositions(as_text=True,inflect=None,capitalize=True)}") 

            clause_number = clause_number + 1 
    return clauses    

            
  


def process_sample_sentences(nlp : Language):

    for sample_sentence in sample_sentences:        
        sentence = nlp(
            sample_sentence["example"])
        find_clauses(sentence)
        
def profile_sample_sentences(nlp : Language):  
    global SILENT_MODE
    SILENT_MODE=True  
    for sample_sentence in sample_sentences:        
        sentence = nlp(
            sample_sentence["example"])
        clauses = find_clauses(sentence)
        print(sentence)
        for clause in clauses:
            print(clause)
            proposition = clause.to_propositions(as_text=True,inflect=None,capitalize=True)
            print(proposition)
        print("--------")
        
if __name__ == "__main__":  
    nlp = spacy.load("en_core_web_lg") 
    if len(sys.argv) > 1:
        if(sys.argv[1] == "test"):
            process_sample_sentences(nlp)  
        else:
            profile_sample_sentences(nlp)          
    else:

        sentence = input("Please enter a sentence:\n")
        doc = nlp(sentence)
        #process_sample_sentences(nlp)
        #sentence = nlp(sample_sentences[11])
        report(f"Sentence: {sentence}")
        lnlp.show_sentence_parts_as_md(doc,False)
        find_clauses(doc)

        


