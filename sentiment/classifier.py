import tensorflow as tf
import json
import numpy as np
import keras


class SentimentClassifier():
    sequence_length = 256

    def __init__(self, model_json_path, model_weights_path, vocab_path, sequence_length=256):
        with open(model_json_path) as json_f:
            self.model = tf.keras.models.model_from_json(json_f.read())
            self.model.load_weights(model_weights_path)

        print(self.model.summary())
        self.vocab = json.load(open(vocab_path))
        self.sequence_length = sequence_length

    
    def predict(self, text):
        text = self._encode(text)
        p = self.model.predict(text, batch_size=1)
        return p


    def _encode(self, text):
        text = list(text)
        encoded = [self.vocab[c] for c in text]
        if len(encoded) < self.sequence_length:
            encoded += [0] * (self.sequence_length - len(encoded))
        if len(encoded) > self.sequence_length:
            encoded = encoded[:self.sequence_length]
        return np.array([encoded])


if __name__ == "__main__":
    classifier = SentimentClassifier(
        "./model/model.json",
        "./model/model.h5",
        "./model/vocab.json"
    )
    labels = ['pos', 'neg', 'nat']

    while True:
        text = input("sample text(or 'quit'): ")
        if text == "quit":
            break
        
        p = classifier.predict(text)
        i = np.argmax(p)
        l = labels[i]

        print("Predict", l, p)
