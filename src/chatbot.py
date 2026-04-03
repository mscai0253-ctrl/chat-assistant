import json
import random
from nltk.tokenize import word_tokenize

with open("src/intents.json") as f:
    data = json.load(f)

def get_response(user_input):
    words = word_tokenize(user_input.lower())

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            if pattern in words:
                return random.choice(intent["responses"])

    return "Sorry, I didn't understand that."