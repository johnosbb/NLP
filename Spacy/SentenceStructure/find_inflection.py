import spacy
import lemminflect
import libnlp as lnlp


nlp = spacy.load('en_core_web_sm')
test_sentences = [
    'I am testing this example and examining these samples.', 'I walk to the shop.', "I think therefore I am.", "The sun rises in the east.",
    "Water boils at 100 degrees Celsius.", "She knows how to swim.", "The Earth orbits the sun.", "Cats chase mice.", "She likes to run.", "This is your moment to shine.",
    "He loves to read mystery novels.", "The math teacher teaches geometry.", "I am here for you.",
    "This moment feels so perfect.", "White rabbits with pink eyes runs close by her.", "The South Africans are winning the match.",
    "The South Africans are not winning the match.", "They are getting ready.", "We are here.", "I am here."]

expected_sentences = [
    'I was testing this example and examining these samples .', 'I walked to the shop .', "I thought therefore I was .", "The sun rose in the east .",
    "Water boiled at 100 degrees Celsius .", "She knew how to swim .", "The Earth orbited the sun .", "Cats chased mice .", "She liked to run .",
    "This was your moment to shine .",
    "He loved to read mystery novels .", "The math teacher taught geometry .", "I was here for you .", "This moment felt so perfect .",
    "White rabbits with pink eyes ran close by her .", "The South Africans were winning the match .",  "The South Africans were not winning the match .",
    "They were getting ready .", "We were here .", "I was here ."]
# test_sentences = ["The South Africans are winning the match."]
# expected_sentences = ["The South Africans were winning the match ."]
# print(doc[2]._.lemma())
# print(doc[4]._.inflect('NNS'))  # Noun, plural
# print(doc[8]._.inflect('NN'))  # Noun, singular
# print(doc[6]._.inflect('VBD'))  # Verb Past Tense

# replace_token(existing_doc, replacement_word, target_word=None, target_pos=None):
i = 0
for sentence in test_sentences:
    doc = nlp(sentence)
    # lnlp.show_sentence_parts(doc)
    answer = lnlp.convert_to_past_tense(nlp, doc)
    if(expected_sentences[i] == answer.text):
        print(f"Correct: {answer.text}")
    else:
        print(f"Error: expected: {expected_sentences[i]} got:  {answer}")
    i += 1


# new_doc = None
# for token in doc:
#     if(token.pos_ == "VERB"):
#         # print(f"Found verb {token.text}")
#         # Verb Past Tense)
#         new_doc = lnlp.replace_token(nlp,
#                                      doc, token._.inflect('VBD'), None, ["VERB"])
# if new_doc:
#     print(f"New Doc POS: {new_doc}")
# for token in doc:
#     if(token.text == "samples"):
#         # print(f"Found target {token.text}")
#         # Verb Past Tense)
#         new_doc = lnlp.replace_token(nlp, doc, "pieces", "samples", None)
# if new_doc:
#     print(f"New Doc Word Replacement: {new_doc}")
