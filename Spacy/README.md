# Spacy

## Tokens

A "token" is the smallest unit of text that can be processed and analyzed. Tokens are individual words or characters, or sometimes even subword units, into which a text is divided for various NLP tasks. Tokenization is the process of breaking down a text into these individual tokens.


- Word Tokens: In most NLP applications, tokens are typically words. For example, in the sentence "I love natural language processing," the tokens are "I," "love," "natural," "language," and "processing."
- Character Tokens: In some cases, especially in character-level NLP tasks or for languages without clear word boundaries, tokens can be individual characters. For example, the tokenization of "abc" would result in three character tokens: "a," "b," and "c."
- Subword Tokens: In languages with complex morphology or for machine learning models that operate on subword units, tokenization can be done at the subword level. For example, in English, the word "unhappiness" might be tokenized into "un," "happi," and "ness."
- Whitespace and Punctuation: Tokenization often involves splitting text based on whitespace (spaces, tabs, line breaks) and punctuation marks (e.g., periods, commas, hyphens).
- Tokenization Rules: Tokenization can be language-specific, and the rules for splitting text into tokens may vary based on the language and the specific task.
- Token Objects: In NLP libraries like spaCy, tokens are often represented as objects that include not only the text of the token but also various attributes, such as part-of-speech tags, lemma forms, and more. These attributes are useful for linguistic analysis and other NLP tasks.
- Tokenization Challenges: Tokenization can be challenging for certain languages, especially those with agglutinative or morphologically rich features, as well as for handling contractions, compound words, and other linguistic phenomena.
- Tokenization is a fundamental step in many NLP pipelines, as it serves as the basis for tasks such as part-of-speech tagging, named entity recognition, syntactic parsing, and text classification. Accurate tokenization is crucial for ensuring that NLP models can understand and process text effectively.

## Spans

In spaCy, a "span" refers to a continuous sequence of tokens within a Doc object. A span can represent a portion of the text in a document, which can include one or more adjacent tokens. Spans are often used to extract or manipulate specific segments of text within a larger document.

Key characteristics of spans in spaCy include:

- Continuous Sequence: A span consists of a sequence of tokens that appear consecutively in the text. These tokens are usually adjacent to each other.
- Immutable: Spans are immutable, meaning you cannot modify the text they represent directly. However, you can create new spans based on existing ones.
- Index-Based: Spans can be indexed to access individual tokens within the span.
- Text and Context: A span retains information about the text it represents and its position within the document.


## Sentences

A "sentence" is a linguistic unit that represents a complete and independent thought or statement within a text. SpaCy provides tools for sentence segmentation, which is the process of identifying and separating text into individual sentences. Each sentence is composed of one or more tokens (words or subword units) that form a grammatical and semantic unit.

- Sentence Objects: SpaCy represents sentences as individual objects within a Doc object. A Doc object is created by processing a text using a spaCy language model. You can access sentences within a Doc using the sents attribute.
- Sentence Tokenization: SpaCy performs sentence tokenization by identifying sentence boundaries based on punctuation marks (such as periods, exclamation marks, and question marks) and other language-specific rules. It aims to accurately identify where one sentence ends and the next begins.
- Sentence-Level Attributes: You can access various attributes at the sentence level, such as the text of the sentence, the start and end token indices, and the sentence's root token.

## Understand Ancestors and Children

Consider the sentence:

- The cat sat on the mat.


![image](https://github.com/johnosbb/ProgrammingInPyQT/assets/12407183/57794b3d-59d4-41d5-944c-3b26eb2f1192)


This has the following structure.



| Text         | Index  | POS      | Dep      | Dep Detail               | Ancestors            | Children   |
| ------------ | -------- | ------ | -------- | ------------------- |-------------- | --------- |
| The          | 0      | DET      | det      | determiner               | cat sat              |            |
| cat          | 1      | NOUN     | nsubj    | nominal subject          | sat                  | The        |
| sat          | 2      | VERB     | ROOT     | root                     |                      | cat on .   |
| on           | 3      | ADP      | prep     | prepositional modifier   | sat                  | mat        |
| a            | 4      | DET      | det      | determiner               | mat on sat           |            |
| mat          | 5      | NOUN     | pobj     | object of preposition    | on sat               | a          |
| .            | 6      | PUNCT    | punct    | punctuation              | sat                  |            |




```

Constituent tree:

(S (NP The cat)
   (VP sat
       (PP on
           (NP a mat)))
   .)

```

- 'The' has ancestors 'cat' and 'sat', but it has no children as seen on the graph, there is no arrow starting from 'The and travelling to another token.
- 'cat' has an ancestor 'sat' as seen in the arrow that starts from sat and points back to 'sat'. 'cat' also has a 'The' with the arrow originating at 'sat and pointing back to 'cat'.
- 'sat' the ROOT has no ancestors, but it does have two children, one on each side.
- Similarly 'sat' is an ancestor of 'on'
- 'mat' has ancestors 'on' through a direct dependency and sat indirectly via 'on's relationship with 'sat'. 'mat' also has a child 'a'.


## Extracting Clauses from a Sentence

Due to the richness and variety of the English language extracting clauses from a sentence can be a complex process. The process can be accomplished in a number of discrete steps.

We first find the Verbs (including any auxiliary verbs) in the sentence. Some sample code is provided for that.
### Find the Verbs and Auxilary Verbs in a Sentence

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


``````

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


## Entending Spacys

- [Entending Spacy through Custom Factories and Components](./NER/custom_factory_example/ExtendingSpacy.md)
- [Training Spacy 3.0 for Entity Recognition](./NER/ner_model_training.md)

## References

- [Extracting verbs using Spacy](https://stackoverflow.com/questions/47856247/extract-verb-phrases-using-spacy)
https://spacy.pythonhumanities.com
https://spacy.pythonhumanities.com/01_04_pipelines.html

https://www.youtube.com/watch?v=dIUTsFT2MeQ&t=3382s
