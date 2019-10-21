
from contacting import ContactingClassifier
import numpy as np


clf = ContactingClassifier("contacting/model/contact.h5", 'sentiment/model/vocab.json')
labels = ['question', 'review']


while True:
    text = input("test input or 'quit': ")
    if text == "quit":
        break
    
    p = clf.predict(text)
    i = np.argmax(p)
    l = labels[i]

    print("Predict", l, p)
