# chatbot.py

import json
import random
import sys

import numpy as np
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Make sure the tokenizer data is available
nltk.download("punkt", quiet=True)

FALLBACK_RESPONSE = "Sorry, I don't understand yet — I'm still learning 🤖"
CONFIDENCE_THRESHOLD = 0.1  # below this, we use fallback


def validate_intents(data: dict) -> None:
    """
    Basic validation for intents.json structure.
    Exits the program with a clear message if something is wrong.
    """
    if "intents" not in data:
        print("❌ ERROR: 'intents' key missing in intents.json")
        sys.exit(1)

    if not isinstance(data["intents"], list):
        print("❌ ERROR: 'intents' must be a list in intents.json")
        sys.exit(1)

    for item in data["intents"]:
        if not isinstance(item, dict):
            print(f"❌ ERROR: intent item is not an object: {item}")
            sys.exit(1)

        missing = [k for k in ("tag", "patterns", "responses") if k not in item]
        if missing:
            print(f"❌ ERROR: Missing fields {missing} in intent: {item}")
            sys.exit(1)

        if not isinstance(item["patterns"], list) or not isinstance(
            item["responses"], list
        ):
            print(
                f"❌ ERROR: 'patterns' and 'responses' must be lists "
                f"in intent with tag='{item.get('tag')}'"
            )
            sys.exit(1)


# 1️⃣ Load intents
with open("intents.json", encoding="utf-8") as file:
    data = json.load(file)

# Validate structure before proceeding
validate_intents(data)

# 2️⃣ Prepare training data
patterns: list[str] = []
tags: list[str] = []
responses: dict[str, list[str]] = {}

for intent in data["intents"]:
    tag = intent["tag"]
    for pattern in intent["patterns"]:
        patterns.append(pattern.lower())
        tags.append(tag)
    responses[tag] = intent["responses"]

# Tokenize and vectorize patterns
vectorizer = CountVectorizer(tokenizer=nltk.word_tokenize)
X = vectorizer.fit_transform(patterns)
y = np.array(tags)

# 3️⃣ Train classifier
clf = MultinomialNB()
clf.fit(X, y)


def predict_intent(text: str) -> tuple[str, float]:
    """
    Predict intent tag and return (tag, confidence).

    Confidence is the max probability from the classifier.
    """
    text = text.strip().lower()
    X_test = vectorizer.transform([text])
    proba = clf.predict_proba(X_test)[0]  # shape: (n_classes,)
    max_idx = np.argmax(proba)
    max_proba = float(proba[max_idx])
    pred_tag = clf.classes_[max_idx]
    return pred_tag, max_proba


# 5️⃣ Get response with fallback
def get_response(user_input: str) -> str:
    # empty or whitespace-only input → fallback
    if not user_input or not user_input.strip():
        return FALLBACK_RESPONSE

    try:
        tag, confidence = predict_intent(user_input)
    except Exception as e:
        print(f"❌ ERROR while predicting intent: {e}")
        return FALLBACK_RESPONSE

    # low-confidence → fallback
    if confidence < CONFIDENCE_THRESHOLD:
        return FALLBACK_RESPONSE

    # safety: if tag not in responses dict → fallback
    resp_list = responses.get(tag)
    if not resp_list:
        return FALLBACK_RESPONSE

    return random.choice(resp_list)