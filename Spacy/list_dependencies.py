import spacy

# Load a spaCy model
nlp = spacy.load("en_core_web_sm")

# Get the list of dependency labels
dependency_labels = nlp.get_pipe("parser").labels

# Print the list of dependency labels
print(dependency_labels)
