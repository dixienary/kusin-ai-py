# libraries
import random
import numpy as np
import pickle
import json
from flask import Flask, render_template, request

import mysql.connector
from user_management import create_user, login_user

import nltk
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()


# Connect to MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='kusin-ai' 
)

# # Check if the connection is successful
# if conn.is_connected():
#     print("Connected to the MySQL database.")
# else:
#     print("Not connected to the MySQL database.")
    
# Chat initialization
model = load_model("chatbot_model.h5")
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))

# Load and process the intents JSON file
data_file = open("C:\Python Flask\AI-Chatbot\\intents.json").read()


app = Flask(__name__)
# run_with_ngrok(app) 

# Flask app routes

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/homepage/about")
def about():
    return render_template("about.html")

@app.route("/homepage/contact")
def contact():
    return render_template("contact.html")

@app.route("/homepage/generator")
def generator():
    return render_template("generator.html")

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    return create_user(email, password)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    return login_user(email, password)


@app.route("/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]

    # Load and process the intents JSON file
    data_file = open("C:\Python Flask\AI-Chatbot\\intents.json").read()
    intents = json.loads(data_file)

    # Rest of your existing code
    if msg.startswith('my name is'):
        name = msg[11:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        res = res1.replace("{n}", name)
    elif msg.startswith('hi my name is'):
        name = msg[14:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        res = res1.replace("{n}", name)
    else:
        ints = predict_class(msg, model)
        res = getResponse(ints, intents)
    return res

# Chat functionalities
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            break
    return result


if __name__ == "__main__":
    app.run()

