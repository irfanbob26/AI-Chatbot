# chatbot.py

import json
import random
import numpy as np
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Download NLTK data only if needed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

# 1️⃣ Load intents
with open('intents.json') as file:
    data = json.load(file)

# 2️⃣ Prepare training data
patterns = []
tags = []
responses = {}
for intent in data['intents']:
    for pattern in intent['patterns']:
        patterns.append(pattern)
        tags.append(intent['tag'])
    responses[intent['tag']] = intent['responses']

# Tokenize and vectorize patterns
vectorizer = CountVectorizer(tokenizer=nltk.word_tokenize)
X = vectorizer.fit_transform(patterns)
y = np.array(tags)

# 3️⃣ Train classifier
clf = MultinomialNB()
clf.fit(X, y)

# 4️⃣ Predict intent
def predict_intent(text):
    """Predict the intent of user input text."""
    X_test = vectorizer.transform([text])
    pred_tag = clf.predict(X_test)[0]
    return pred_tag

# 5️⃣ Get response
def get_response(user_input):
    """Generate a response based on user input."""
    if not user_input or not user_input.strip():
        return "Please say something!"

    intent = predict_intent(user_input)
    return random.choice(responses[intent])
