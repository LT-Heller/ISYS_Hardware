import ctypes
from numpy import mean

def detectPeaks(data: list[list[int]], averageCh: list[float], offset: int) -> bool:
    for c, channel in enumerate(data):
        for i, value in enumerate(channel):
            if value > averageCh[c] + offset or value < averageCh[c] - offset:
                return True
    return False

def normData(data: list[list[int]], minCh: list[int], maxCh: list[int]):
    for c, channel in enumerate(data):
        for i, value in enumerate(channel):
            data[c][i] = 2 * ((float(value) - minCh[c]) / (maxCh[c] - minCh[c])) - 1

def getMinMax(data: list[list[int]]) -> tuple[list[int],list[int]]:
    minCh = [0 for _ in range(4)]
    maxCh = [0 for _ in range(4)]
    for c, channel in enumerate(data):
        minCh[c] = min(channel)
        maxCh[c] = max(channel)
    return (minCh, maxCh)

class EMGDataPreprocessing:
    
    def __init__(self, MinMaxListLen = 100, offsetPeaks = 200):
        self.listOfMin = [[] for _ in range(4)]
        self.listOfMax = [[] for _ in range(4)]
        self.listOfAvg = [[] for _ in range(4)]
        self.MinMaxListLen = MinMaxListLen
        self.offsetPeaks = offsetPeaks

        self.feat = ctypes.cdll.LoadLibrary("./libfeatures.so")
        self.feat.EMGfeatures.argtypes = (ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_uint)
        self.feat.EMGfeatures.restype = ctypes.POINTER(ctypes.c_float)

    def extractFeatures(self, array: list[list[float]]) -> list[float]:
        array_type = ctypes.c_float * len(array[0])

        result = self.feat.EMGfeatures(array_type(*array[0]),array_type(*array[1]),array_type(*array[2]),array_type(*array[3]),ctypes.c_uint(len(array[0])))
        features = []
        for i in range(16):
            features.append(round(result[i], 6))
            
        return features

    def refreshMinMaxAvgList(self, data: list[list[int]]):
        (minCh, maxCh) = getMinMax(data)
        avgCh = [mean(data[c]) for c in range(4)]
        for c in range(len(minCh)):
            self.listOfMin[c].append(minCh[c])
            if len(self.listOfMin[c]) > self.MinMaxListLen: del self.listOfMin[c][0]
            self.listOfMax[c].append(maxCh[c])
            if len(self.listOfMax[c]) > self.MinMaxListLen: del self.listOfMax[c][0]
            self.listOfAvg[c].append(avgCh[c])
            if len(self.listOfAvg[c]) > self.MinMaxListLen: del self.listOfAvg[c][0]

    def prepareDataGetFeatures(self, frame: list[list[int]]):
        if detectPeaks(frame, [mean(self.listOfAvg[c]) for c in range(4)], self.offsetPeaks):
            # print("Fehlerhafte Daten")
            return False
        self.refreshMinMaxAvgList(frame)
        minCh = [min(self.listOfMin[c]) for c in range(4)]
        maxCh = [max(self.listOfMax[c]) for c in range(4)]
        normData(frame, minCh, maxCh)
        features = self.extractFeatures(frame)
        return features