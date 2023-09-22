import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

# Define a pattern for the Matcher
pattern = [{"LOWER": "example"}, {"POS": "NOUN"}]

# Add the pattern to the Matcher
matcher.add("ExamplePattern", [pattern])

# Process a text
text = "This is an example sentence. Another example is here."
doc = nlp(text)

# Find matches in the document
matches = matcher(doc)

# Loop through the matches and get token IDs and POS tags
for match_id, start, end in matches:
    matched_tokens = doc[start:end]
    token_ids = [token.i for token in matched_tokens]
    token_pos = [token.pos_ for token in matched_tokens]

    print(f"Match ID: {match_id}")
    print(f"Token IDs: {token_ids}")
    print(f"Token POS tags: {token_pos}")

    for token_id, pos in zip(token_ids, token_pos):
        token = doc[token_id]
        print(
            f"Token Text: {token.text}, Token ID: {token_id}, Token POS: {pos}")
