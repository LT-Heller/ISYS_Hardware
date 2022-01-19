import numpy as np

from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

def create_model(numClasses, numFeatures):
    model = Sequential()

    model.add(Dense(units=15, kernel_initializer="uniform", bias_initializer="zeros", input_shape=(np.shape(range(numFeatures))), activation="relu"))

    model.add(Dense(units=numClasses, kernel_initializer="uniform", bias_initializer="zeros", activation="softmax"))

    model.compile(
    loss="sparse_categorical_crossentropy",
    optimizer=Adam(lr=0.001),
    metrics=["accuracy"])

    return model

class EMGClassifier:
    def __init__(self, numFeatures = 16, numClasses = 3):
        self.numFeatures = numFeatures
        self.numClasses = numClasses
        self.model = create_model(numClasses, numFeatures)

    def printSummary(self):
        self.model.summary()

    def loadWeights(self, pathToWeights):
        self.model.load_weights(pathToWeights)

    def makePrediction(self, features):
        predictions = self.model.predict([features,features])
        classes = np.argmax(predictions, axis = 1)
        return classes[0]