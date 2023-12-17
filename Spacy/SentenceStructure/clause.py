import spacy
import lemminflect
import logging
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
    'account for': None,
    'add up to': None,
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

        Returns
        -------
        None.

        """
        if adverbials is None:
            adverbials = []

        self.subject = subject
        self.verb = verb
        self.indirect_object = indirect_object
        self.direct_object = direct_object
        self.complement = complement
        self.adverbials = adverbials
        if(self.subject):
            self.doc = self.subject.doc
        else:
            self.doc = None
        self.type = self._get_clause_type()
        
        
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
        return "<{}, {}, {}, {}, {}, {}, {}>".format(
            self.type,
            self.subject,
            self.verb,
            self.indirect_object,
            self.direct_object,
            self.complement,
            self.adverbials,
        )

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
                if self.type in ["SV", "SVA"]:
                    if self.adverbials:
                        for a in self.adverbials:
                            propositions.append(tuple(prop + [a]))
                        propositions.append(tuple(prop + self.adverbials))
                    else:
                        propositions.append(tuple(prop))

                elif self.type == "SVOO":
                    for iobj in indirect_objects:
                        for dobj in direct_objects:
                            propositions.append((subj, verb, iobj, dobj))
                elif self.type == "SVO":
                    for obj in direct_objects + indirect_objects:
                        propositions.append((subj, verb, obj))
                        for a in self.adverbials:
                            propositions.append((subj, verb, obj, a))
                elif self.type == "SVOA":
                    for obj in direct_objects:
                        if self.adverbials:
                            for a in self.adverbials:
                                propositions.append(tuple(prop + [obj, a]))
                            propositions.append(
                                tuple(prop + [obj] + self.adverbials))

                elif self.type == "SVOC":
                    for obj in indirect_objects + direct_objects:
                        if complements:
                            for c in complements:
                                propositions.append(tuple(prop + [obj, c]))
                            propositions.append(
                                tuple(prop + [obj] + complements))
                elif self.type == "SVC":
                    if complements:
                        for c in complements:
                            propositions.append(tuple(prop + [c]))
                        propositions.append(tuple(prop + complements))

        # Remove doubles
        propositions = list(set(propositions))

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
