import os, sys
import numpy as np

from modules.EMGDataPreprocessing import EMGDataPreprocessing

FrameLen = 150
dataPrePro = EMGDataPreprocessing(100, 200)

inputfile = "./recordJanNew.csv"
outputfile = "featuresJanNew.csv"

def main():
    record = np.loadtxt(inputfile, delimiter=';')
    values = np.array([x[0:4] for x in record])
    lable = np.array([int(x[4])for x in record])
    featuresList = []
    lableList = []

    print("Testing outputfile...")
    try:
        output = open(outputfile, "w")
    except IOError:
        print("Outputfile error! Permission denied?")
        sys.exit()

    frame = [[] for _ in range(4)]
    for v, value in enumerate(values):
        for c in range(4):
            frame[c].append(value[c])
        if len(frame[0]) >= FrameLen:
            if(lable[v] == lable[v - FrameLen]):
                features = dataPrePro.prepareDataGetFeatures(frame)
                if features:
                    featuresList.append(features)
                    lableList.append(lable[v])
            frame = [[] for _ in range(4)]

    print("Writing Outputfile...")
    output.truncate()
    for row, features in enumerate(featuresList):
        for feature in features:
            output.write(f"{feature};")
        output.write(f"{lableList[row]}\n")
    output.close()



if __name__ == "__main__":
    main()