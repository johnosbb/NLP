# Find the Verbs and Auxilary Verbs in a Sentence

```python
import spacy
from spacy.matcher import Matcher


text = (
    "The author was staring pensively as she wrote. "
    "She is playing the piano."
    "They have been working on this project for months."
    "I will meet you at the coffee shop."
    "He can swim faster than anyone I know."
    "The cat chased the mouse across the room."
    "We should go for a walk in the park."
    "The students are anxious because they are studying for their final exams."
    "The sun sets in the west."
    "The company announced a new product."
    "It was raining heavily when I left home so I took an umbrella."
    "Breaking the window, he climbed inside the office where the safe was located."
)

# for the given span, get matches for the verb templates.
def get_verb_matches(span):
    # 1. Find verb phrases in the span
    # (see mdmjsh answer here: https://stackoverflow.com/questions/47856247/extract-verb-phrases-using-spacy)
    verb_matcher = Matcher(span.vocab)
    verb_matcher.add("Auxiliary verb phrase aux-adv-verb", [
        [{"POS": "AUX"}, {"POS": "ADV", "OP": "+"}, {"POS": "VERB"}]])
    verb_matcher.add("Auxiliary verb phrase aux-verb", [
        [{"POS": "AUX"}, {"POS": "VERB"}]])
    verb_matcher.add("Auxiliary verb phrase", [[{"POS": "AUX"}]])
    verb_matcher.add("Verb phrase", [[{"POS": "VERB"}]],)
    return verb_matcher(span)

# for each sentence in the document, get the verb forms


def extract_verbs(doc):
    verbs = []
    for sent in doc.sents:
        verb_phrase = get_verb_matches(sent)
        verbs.append((sent, verb_phrase))
    return verbs

# Extract a text representation of the spans from matches


def extract_spans_from_match(sent, match):
    verb_spans = []
    for match_id, start, end in match:
        # Create a span from the match indices
        verb_span = sent[start:end]
        verb_spans.append(verb_span)
    return verb_spans


if __name__ == "__main__":
    import spacy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    verb_matches = extract_verbs(doc)
    for sentence, match in verb_matches:
        verb_spans = extract_spans_from_match(sentence, match)
        for verb_span in verb_spans:
            print(f"{sentence} : {verb_span.text}")


```

This produces the result

| Sentence                                           | Verb Parts           |
| -------------------------------------------------- | -------------------- |
| The author was staring pensively as she wrote.     | was                  |
| The author was staring pensively as she wrote.     | was staring          |
| The author was staring pensively as she wrote.     | staring              |
| The author was staring pensively as she wrote.     | wrote                |
| She is playing the piano.                          | is                   |
| She is playing the piano.                          | is playing           |
| She is playing the piano.                          | playing              |
| They have been working on this project for months. | have                 |
| They have been working on this project for months. | been                 |
| They have been working on this project for months. | been working         |
| They have been working on this project for months. | working              |
| I will meet you at the coffee shop.                | will                 |
| I will meet you at the coffee shop.                | will meet            |
| I will meet you at the coffee shop.                | meet                 |
| He can swim faster than anyone I know.             | can                  |
| He can swim faster than anyone I know.             | can swim             |
| He can swim faster than anyone I know.             | swim                 |
| He can swim faster than anyone I know.             | know                 |
| The cat chased the mouse across the room.          | chased               |
| We should go for a walk in the park.               | should               |
| We should go for a walk in the park.               | should go            |
| We should go for a walk in the park.               | go                   |
| The students are anxious because they are studying for their final exams. | are  |
| The students are anxious because they are studying for their final exams. | are  |
| The students are anxious because they are studying for their final exams. | are studying |
| The students are anxious because they are studying for their final exams. | studying     |
| The sun sets in the west.                          | sets                 |
| The company announced a new product.               | announced            |
| It was raining heavily when I left home so I took an umbrella. | was         |
| It was raining heavily when I left home so I took an umbrella. | was raining |
| It was raining heavily when I left home so I took an umbrella. | raining     |
| It was raining heavily when I left home so I took an umbrella. | left        |
| It was raining heavily when I left home so I took an umbrella. | took        |
| Breaking the window, he climbed inside the office where the safe was located. | Breaking |
| Breaking the window, he climbed inside the office where the safe was located. | climbed  |
| Breaking the window, he climbed inside the office where the safe was located. | was      |
| Breaking the window, he climbed inside the office where the safe was located. | was located |
| Breaking the window, he climbed inside the office where the safe was located. | located   |
