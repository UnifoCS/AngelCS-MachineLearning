import tensorflow as tf
import json
import numpy as np


class ContactingClassifier:
    sequence_length = 256

    def __init__(self, model_path, vocab_path, sequence_length=256):
        self.model = tf.keras.models.load_model(model_path)
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
