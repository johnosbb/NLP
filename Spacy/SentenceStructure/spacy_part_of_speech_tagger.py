import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Your sentence
sentence = "The quick brown fox jumps over the lazy dog"

# Process the sentence with spaCy
doc = nlp(sentence)

# Create a list of tuples in the format (token text, part-of-speech tag)
tagged = [(token.text, token.pos_) for token in doc]

# Print the tagged tokens
print(tagged)
