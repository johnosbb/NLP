import spacy
import lemminflect
import logging
import typing

from spacy.tokens import Span, Doc
from spacy.matcher import Matcher
import libnlp as lnlp


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

        self.doc = self.subject.doc

        self.type = self._get_clause_type()

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
            clause_type = "SVC"
            return clause_type

        if has_object:
            if has_direct_object and has_indirect_object:
                clause_type = "SVOO"
            elif has_complement:
                clause_type = "SVOC"
            elif not has_adverbial or not has_direct_object:
                clause_type = "SVO"
            elif complex_transitive or conservative:
                clause_type = "SVOA"
            else:
                clause_type = "SVO"
        else:
            if has_complement:
                clause_type = "SVC"
            elif not has_adverbial or has_non_ext_copular_verb:
                clause_type = "SV"
            elif has_ext_copular_verb or conservative:
                clause_type = "SVA"
            else:
                clause_type = "SV"

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
                    token_texts.append(inflect_token(token, inflect))

                span_texts.append(" ".join(token_texts))
            proposition_texts.append(" ".join(span_texts))

        if capitalize:  # Capitalize and add a full stop.
            proposition_texts = [
                text.capitalize() + "." for text in proposition_texts]

        return proposition_texts
