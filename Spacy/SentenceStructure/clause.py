import spacy
import lemminflect
import logging
from typing import Union,List, Tuple  # Import the Union type
import typing
from spacy.tokens import Span, Doc
from spacy.matcher import Matcher
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



# DO NOT SET MANUALLY
MOD_CONSERVATIVE = False

# "non_ext_copular" - This category contains words that are typically used as non-extended copular verbs.
# In English, copular verbs are often used to link the subject of a sentence with a subject complement 
# (e.g., "She is happy"). The words in this list, 
# like "die" and "walk," are often not used in this way and are not extended copular verbs.
# "ext_copular" - This category contains words that can function as extended copular verbs.
# Extended copular verbs are used to link the subject of a sentence with a subject complement.
# They include common verbs like "be," "become," and "seem." 
# These words are often used in sentences like "She became a doctor."
# A complex transitive verb is a type of verb that requires both a direct object and an object complement. 
dictionary = {
    "non_ext_copular": ["die", "walk"],
    "ext_copular": [
        "act", "appear", "be", "become", "come", "come out", "end up",
        "get", "go", "grow", "fall", "feel", "keep", "leave", "look",
        "prove", "remain", "seem", "smell", "sound", "stay", "taste",
        "turn", "turn up", "wind up", "live", "come", "go", "stand",
        "lie", "love", "do", "try"
    ],
    "complex_transitive": [
        "bring", "catch", "drive", "get", "keep", "lay", "lead", "place",
        "put", "set", "sit", "show", "stand", "slip", "take"
    ],
    "adverbs_ignore": ["so", "then", "thus", "why", "as", "even"],
    "adverbs_include": [
        "hardly", "barely", "scarcely", "seldom", "rarely"
    ]
}

prepositional_verbs = {
    'abstain from' : None,
    'accuse [someone] of [something]' : None,
    'adapt to' : None,
    'account for': None,
    'add to' : None,
    'agree on' : None,
    'agree with' : None,
    'apologize for' : None,
    'apologize to' : None,
    'add up to': None,
    'apply to': None,
    'approve of': None,
    'argue about': None,
    'arrest for': None,
    'arrive at': None,
    'arrive in': None,
    'ask about': None,
    'ask for': None,
    'attend to': None,
    'believe in': None,
    'belong to': None,
    'care about': None,
    'care for': None,
    'charge with': None,
    'complain about': None,
    'concentrate on': None,
    'confide in': None,
    'connect to': None,
    'consent to': None,
    'consist of': None,
    'contribute to': None,
    'count on': None,
    'come from': None,
    'convert to': None,
    'deal with': None,
    'dedicate to': None,
    'depend on': None,
    'disagree with': None,
    'discuss with': None,
    'dream about': None,
    'dream of': None,
    'elaborate on': None,
    'excel at': None,
    'fear for': None,
    'focus on': None,
    'forget about': None,
    'forgive for': None,
    'get sick with': None,
    'get tired of': None,
    'go to': None,
    'graduate from': None,
    'happen to': None,
    'hear about': None,
    'hear of': None,
    'help with': None,
    'hint at': None,
    'hope for': None,
    'insist on': None,
    'interfere with': None,
    'laugh at': None,
    'laugh about': None,
    'lead to': None,
    'look at': None,
    'listen to': None,
    'look for': None,
    'object to': None,
    'pay for': None,
    'point at': None,
    'pray for': None,
    'prepare for': None,
    'prevent from': None,
    'prohibit from': None,
    'react to': None,
    'recover from': None,
    'believe in': None,
    'call off': None,
    'deal with': None,
    'fall for': None,
    'get across': None,
    'hold on to': None,
    'invite to': None,
    'look into': None,
    'make up for': None,
    'opt for': None,
    'put up with': None,
    'run out of': None,
    'stick to': None,
    'take care of': None,
    'wait for': None,
    'shut down': None,
    'turn away': None,
    'warm up': None,
    'cut off': None,
    'put down': None,
    'wipe out': None,
    'plug in': None,
    'try on': None,
    'face up to': None,
    'dig in': None,
    'bank on': None,
    'come through': None,
    'drift off': None,
    'check in': None,
    'lean on': None,
    'break into': None,
    'chime in': None,
    'pick up on': None,
    'figure out': None,
    'spin off': None,
    'strike out': None,
    'tap into': None,
    'wean off': None,
    'get on with': None,
    'peck at': None,
    'cave in': None,
    'buzz off': None,
    'flare up': None,
    'fly off': None,
    'gear up': None,
    'sail through': None,
    'bankroll': None,
    'chime in': None,
    'bail out': None,
    'count on': None,
    'dial in': None,
    'ease up': None,
    'flare up': None,
    'gear up': None,
    'hammer out': None,
    'keel over': None,
    'settle down': None,
    'tune up': None,  
    'refer to': None,
    'rely on': None,
    'remind of': None,
    'reply to': None,
    'respond to': None,
    'resign from': None,
    'smile at': None,
    'specialize in': None,
    'stare at': None,
    'stem from': None,
    'subscribe to': None,
    'suffer from': None,
    'talk about': None,
    'talk to': None,
    'tell about': None,
    'thank for': None,
    'think about': None,
    'think of': None,
    
}

# You can continue to extend this list with more verbs and provide meanings, example sentences, etc.


class Clause:
    def __init__(
        self,
        subject: typing.Optional[Span] = None,
        verb: typing.Optional[Span] = None,
        indirect_object: typing.Optional[Span] = None,
        direct_object: typing.Optional[Span] = None,
        complement: typing.Optional[Span] = None,
        adverbials: typing.List[Span] = None,
        subordinator: typing.Optional[Span] = None,
        sentence: typing.Optional[Doc] = None,
        subject_on_same_level: typing.Optional[bool]=None
    ):
        """


        Parameters
        ----------
        subject : Span
            Subject.
        verb : Span
            Verb.
        indirect_object : Span, optional
            Indirect object, The default is None.
        direct_object : Span, optional
            Direct object. The default is None.
        complement : Span, optional
            Complement. The default is None.
        adverbials : list, optional
            List of adverbials. The default is [].
        subordinator : Span, optional
            Subordinator. The default is None.
        Returns
        -------
        None.

        """
        if adverbials is None:
            adverbials = []
        self.summary = ""
        self.subject = subject
        self.verb = verb
        self.indirect_object = indirect_object
        self.direct_object = direct_object
        self.complement = complement
        self.adverbials = adverbials
        self.subordinator = subordinator
        self.sentence = sentence
        self.subject_on_same_level = subject_on_same_level
        self.type = None
        if(self.subject):
            self.doc = self.subject.doc
        else:
            self.doc = None
        self.classification = self._get_clause_type()
        
        
# """
# | Identifier  | Type | Description                                              | Example |
# |-------------|------ | ----------------------------------------------------| ------ |
# | SVC         | Subject-Verb-Compliment | This type of clause consists of a subject and a copular (linking) verb, such as "be," "seem," "appear," etc. It typically doesn't have a direct object. | "She is a doctor." |
# | SVO       | Subject-Verb-Object | This type of clause contains a subject, a transitive verb, and a direct object. It represents an action performed by the subject on the object. | "She eats an apple." |
# | SVOO       | Subject-Verb-Object-Object| This type of clause includes a subject, a transitive verb, and both a direct object and an indirect object. | "She gives the book to him." |
# | SVOC      | Subject-Verb-Object-Complement | In this clause, the subject performs an action (verb) on the direct object, and there's a complement that provides additional information about the object. | "She painted the room blue." |
# | SVA      | Subject-Verb-Adverbial| This type of clause includes a subject, a verb, and an adverbial phrase that provides additional information about the action. | "She runs quickly."  |
# | SVOA      | Subject-Verb-Object-Adverbial | This clause combines a subject, a transitive verb, a direct object, and an adverbial phrase. | "She eats an apple slowly."  |
# | SV      | Subject-Verb | clause type represents a simple sentence structure that contains a subject and a verb but does not have a direct object.  | "She sings."  |
# """
    def __str__(self):
        clause_text = f"Subject: {self.subject}, Subject on same level: {self.subject_on_same_level}, Verb: {self.verb}, Direct Object: {self.direct_object}, Indirect Object: {self.indirect_object}, Complements: {self.complement}, Adverbials: {self.adverbials}, Subordinator: {self.subordinator}"
        return clause_text
    
    
    def _get_clause_type(self):
        has_verb = self.verb is not None
        has_complement = self.complement is not None
        has_adverbial = len(self.adverbials) > 0
        has_ext_copular_verb = (
            has_verb and self.verb.root.lemma_ in dictionary["ext_copular"]
        )
        has_non_ext_copular_verb = (
            has_verb and self.verb.root.lemma_ in dictionary["non_ext_copular"]
        )
        conservative = MOD_CONSERVATIVE
        has_direct_object = self.direct_object is not None
        has_indirect_object = self.indirect_object is not None
        has_object = has_direct_object or has_indirect_object
        complex_transitive = (
            has_verb and self.verb.root.lemma_ in dictionary["complex_transitive"]
        )

        clause_type = "undefined"

        if not has_verb:
            clause_type = "SVC" # SVC: Subject-Verb-Clause
            return clause_type

        if has_object:
            if has_direct_object and has_indirect_object:
                clause_type = "SVOO" # Subject-Verb-Object-Object
            elif has_complement:
                clause_type = "SVOC"  # Subject-Verb-Object-Complement 
            elif not has_adverbial or not has_direct_object:
                clause_type = "SVO" # Subject-Verb-Object
            elif complex_transitive or conservative:
                clause_type = "SVOA" # Subject-Verb-Object-Adverbial
            else:
                clause_type = "SVO" # Subject-Verb-Object
        else:
            if has_complement:
                clause_type = "SVC" # Subject-Verb-Compliment
            elif not has_adverbial or has_non_ext_copular_verb:
                clause_type = "SV" # Subject-Verb
            elif has_ext_copular_verb or conservative:
                clause_type = "SVA" # Subject-Verb-Adverbial
            else:
                clause_type = "SV" # Subject-Verb

        return clause_type

    def __repr__(self):
        return "< {}, {}, {}, {}, {}, {}, {}, {}, {}> ".format(
            self.classification,
            self.type,
            self.subject,
            self.verb,
            self.indirect_object,
            self.direct_object,
            self.complement,
            self.adverbials,
            self.subordinator,
        )

    def arrange_adverbials(self,propositions: List,prop : List):
        if self.adverbials:
            for a in self.adverbials: # remember each "a" is a span
                main_verb = lnlp.find_verb_in_ancestors(a.root)
                if(main_verb and main_verb.dep_ == "advcl"):
                    propositions.append(tuple([a] + prop))
                else:
                    propositions.append(tuple(prop + [a]))
            if lnlp.are_word_tuples_equal(tuple([a] + prop),tuple(prop + self.adverbials)) == False:      
                propositions.append(tuple(prop + self.adverbials))
        else:
            propositions.append(tuple(prop))   
            
    def identify_type(self):
        for token in self.verb.root.children:
            if(token.pos_ == "SCONJ"): # This is a subordinating conjunction
                self.subordinator = lnlp.token_as_span(self.sentence,token)
                if(token.text.lower() in ["why","who","where","when","how","whether","whatever","whichever","which","what"]):
                    self.type="dependent wh-clause"                
                elif(token.text.lower() in ["that"]):
                    # We need to check here to see if that is part of clausal subject construction
                    # Find the verbs and check there children for evidence of a clausal subject
                    if lnlp.is_part_of_clausal_subject(token, self.verb) == False:
                        self.type="dependent th-clause"
                elif(token.text.lower() in ["because","since","as"]):
                    self.type="dependent causal-clause"  
                elif(token.text.lower() in ["if","unless","even if","whether","provided that","in case"]):
                    self.type="dependent conditional-clause"               
                elif(token.text.lower() in ['although', 'though', 'even though', 'while', 'whereas', 'despite', 'in spite of', 'regardless of']):
                    self.type="dependent concession-clause"
                elif(token.text.lower() in ['when', 'where', 'while', 'before', 'after', 'since', 'as', 'as if', 'as though', 'although',
                    'because', 'if', 'unless', 'until', 'so that', 'in order that', 'whenever', 'wherever']):
                        self.type="dependent adverbial-clause"
                elif(token.text.lower() in ['who', 'whom', 'whose', 'which', 'that']):
                        self.type="dependent relative-clause"  
            elif((token.pos_ == "PRON")):                
                if(token.tag_ == "WP"):
                    if(token.text.lower() in ["what," "who," "whom," "whose," "which,"  "that."]):
                        self.type="dependent noun-clause"
                        self.subordinator =  lnlp.token_as_span(self.sentence,token)
            else:
                if(self.type == None):
                    self.type="independent clause"            
                    

        
    def identify_compliment_clause(self):   
        if(self.adverbials): 
            for a in self.adverbials:
                for token in a:
                    if(token.pos_ == "SCONJ"):
                        if(token.text.lower() in ["why","who","where","when","how","whether","whatever","whichever","which","what"]):
                            self.type="wh-clause"
                        elif(token.text.lower() in ["that"]):
                            self.type="th-clause"
                        elif(token.text.lower() in ["because","since","as"]):
                                self.type="causal-clause"
        
    def to_propositions(
        self, as_text: bool = False, inflect: str or None = "VBD", capitalize: bool = False
    ):

        if inflect and not as_text:
            logging.warning(
                "`inflect' argument is ignored when `as_text==False'. To suppress this warning call `to_propositions' with the argument `inflect=None'")
        if capitalize and not as_text:
            logging.warning(
                "`capitalize' argument is ignored when `as_text==False'. To suppress this warning call `to_propositions' with the argument `capitalize=False")

        propositions = []

        subjects = lnlp.extract_ccs_from_token_at_root(self.subject)
        direct_objects = lnlp.extract_ccs_from_token_at_root(
            self.direct_object)
        indirect_objects = lnlp.extract_ccs_from_token_at_root(
            self.indirect_object)
        complements = lnlp.extract_ccs_from_token_at_root(self.complement)
        verbs = [self.verb] if self.verb else []

        for subj in subjects:
            if complements and not verbs:
                for c in complements:
                    propositions.append((subj, "is", c))
                propositions.append((subj, "is") + tuple(complements))

            for verb in verbs:
                prop = [subj, verb]
                if self.classification in ["SV", "SVA"]:
                    self.arrange_adverbials(propositions,prop)
                elif self.classification == "SVOO":
                    for iobj in indirect_objects:
                        for dobj in direct_objects:
                            propositions.append((subj, verb, iobj, dobj))
                elif self.classification == "SVO":                    
                    for obj in direct_objects + indirect_objects: # obj is a span
                        if(obj.root.tag_ == "WDT"):
                            proposition = (obj, subj, verb)
                        else:    
                            proposition = (subj, verb, obj)
                        propositions.append(proposition)
                        for a in self.adverbials:
                            proposition = proposition + (a,)
                            propositions.append(proposition)
                elif self.classification == "SVOA":
                    for obj in direct_objects:
                        if self.adverbials:
                            for a in self.adverbials:
                                propositions.append(tuple(prop + [obj, a]))
                            propositions.append(
                                tuple(prop + [obj] + self.adverbials))

                elif self.classification == "SVOC":
                    for obj in indirect_objects + direct_objects:
                        if complements:
                            for c in complements:
                                propositions.append(tuple(prop + [obj, c]))
                            propositions.append(
                                tuple(prop + [obj] + complements))
                elif self.classification == "SVC":
                    if complements:
                        for c in complements:
                            if self.adverbials and (self.type == "th-clause" or self.type == "wh-clause"):
                                for a in self.adverbials:
                                    propositions.append(tuple([a] + prop + [c]))
                            else:      
                                propositions.append(tuple(prop + [c]))
                        if(self.subordinator) :      
                            propositions.append(tuple([self.subordinator] + prop + complements))
                        else:
                            propositions.append(tuple(prop + complements))

        # Remove doubles
        propositions = list(set(propositions))
        #propositions = lnlp.remove_duplicate_tuples(propositions)


        if as_text:
            return self.convert_clauses_to_text(
                propositions, inflect=inflect, capitalize=capitalize
            )
        return propositions

    def convert_clauses_to_text(self, propositions, inflect, capitalize):
        proposition_texts = []
        for proposition in propositions:
            span_texts = []
            for span in proposition:

                token_texts = []
                for token in span:
                    token_texts.append(lnlp.inflect_token(token, inflect))

                span_texts.append(" ".join(token_texts))
            proposition_texts.append(" ".join(span_texts))

        if capitalize:  # Capitalize and add a full stop.
            proposition_texts = [
                text.capitalize() + "." for text in proposition_texts]

        return proposition_texts
