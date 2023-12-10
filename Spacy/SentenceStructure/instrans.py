import spacy

nlp = spacy.load("en_core_web_sm")

verb = nlp.vocab["read"]
print(f"read is an intransitive verb {verb.vocab}")