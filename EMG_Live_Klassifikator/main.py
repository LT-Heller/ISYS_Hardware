from copy import deepcopy
import os, sys
import numpy as np

from modules.EMGRecorder import EMGRecorder
from modules.EMGDataPreprocessing import EMGDataPreprocessing
from modules.EMGClassifier import EMGClassifier

currentPath = str(os.getcwd())
osSep = str(os.sep)

recorder = EMGRecorder(2000000, "COM3", 150)
dataPrePro = EMGDataPreprocessing(100, 200)
classifier = EMGClassifier(16, 3)

def main():
    classifier.loadWeights("models/modelJanNew.hdf5")
    classifier.printSummary()

    recorder.connect()

    while True:
        frame = recorder.recordFrame()
        features = dataPrePro.prepareDataGetFeatures(frame)
        if not features:
            print("Fehlerhafte Daten")
            continue
        prediction = classifier.makePrediction(features)

        if prediction == 0: print("Papier\r", end="")
        if prediction == 1: print("Stein \r", end="")
        if prediction == 2: print("Schere\r", end="")

if __name__ == "__main__":
    main()