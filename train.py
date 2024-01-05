# libraries
import random
import numpy as np
import pickle
import json
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.optimizers import SGD
from keras.layers import Dense, Dropout
from keras.models import Sequential, load_model

# Download NLTK resources
nltk.download('omw-1.4')
nltk.download("punkt")
nltk.download("wordnet")

# Initialize NLTK lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents data from JSON file
data_file = open("C:\Python Flask\AI-Chatbot\intents.json").read()
intents = json.loads(data_file)


# Initialize lists for words, classes, and documents
words = []
classes = []
documents = []
ignore_words = ["?", "!"]

# Extract words, classes, and documents from intents data
for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        # Tokenize each word and add to the list
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        # Add documents
        documents.append((w, intent["tag"]))
        # Add classes to the list
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

# Lemmatize words, remove duplicates, and sort
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

# Print information about the data
print(len(documents), "documents")
print(len(classes), "classes", classes)
print(len(words), "unique lemmatized words", words)


# Save words and classes to pickle files
pickle.dump(words, open("words.pkl", "wb"))
pickle.dump(classes, open("classes.pkl", "wb"))

# Initialize training data
training = []
output_empty = [0] * len(classes)

for doc in documents:
    # initializing bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # lemmatize each word - create base word, in attempt to represent related words
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    # create our bag of words array with 1, if word match found in current pattern
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # output is a '0' for each tag and '1' for current tag (for each pattern)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

# Shuffle the training data
random.shuffle(training)

# training = np.array(training)
# # create train and test lists. X - patterns, Y - intents
# train_x = list(training[:, 0])
# train_y = list(training[:, 1])

#updated

# Separate bag-of-words representations and output labels
train_x = [item[0] for item in training]
train_y = [item[1] for item in training]

# Convert to NumPy arrays
train_x = np.array(train_x)
train_y = np.array(train_y)
print("Training data created")

# Create and compile the model
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation="softmax"))
model.summary()

# Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model

# sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
# model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

#Updated (Removed decayIt seems like you're using a deprecated argument, decay, in the instantiation of the SGD optimizer from Keras. The decay argument has been deprecated in newer versions of Keras. To address this issue, 
# you can switch to using the newer format for specifying learning rate schedules in the optimizer.)

# Compile model using SGD optimizer
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])



# for choosing an optimal number of training epochs to avoid underfitting or overfitting use an early stopping callback to keras
# based on either accuracy or loos monitoring. If the loss is being monitored, training comes to halt when there is an 
# increment observed in loss values. Or, If accuracy is being monitored, training comes to halt when there is decrement observed in accuracy values.

# from keras import callbacks 
# earlystopping = callbacks.EarlyStopping(monitor ="loss", mode ="min", patience = 5, restore_best_weights = True)
# callbacks =[earlystopping]

# fitting and saving the model
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

# Save the model
model.save("chatbot_model.h5", hist)
print("Model created and trained")
