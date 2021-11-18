
from threading import Thread
import serial
import time
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import pandas as pd


class serialReciever:
    def __init__(self, serialPort = 'COM5', serialBaud = 115200, logLength = 1000, channels = 2):
        self.port = serialPort
        self.baud = serialBaud
        self.logMaxLength = logLength
        self.channels = channels
        self.rawData = bytearray(2)
        self.data = collections.deque(maxlen=logLength)
        self.isRun = True
        self.isReceiving = False
        self.thread = None
        self.logTimer = 0
        self.previousTimer = 0
        self.initTime = time.time()
        self.line = bytes()
        # self.csvData = []

        print('Trying to connect to: ' + str(serialPort) + ' at ' + str(serialBaud) + ' BAUD.')
        try:
            self.serialConnection = serial.Serial(serialPort, serialBaud, timeout=4)
            print('Connected to ' + str(serialPort) + ' at ' + str(serialBaud) + ' BAUD.')
        except:
            print("Failed to connect with " + str(serialPort) + ' at ' + str(serialBaud) + ' BAUD.')
            
    def changePort(self, port):
        self.port = port

    def readSerialStart(self):
        if self.thread == None:
            self.thread = Thread(target=self.backgroundThread)
            self.thread.start()
            # Block till we start receiving values
            while self.isReceiving != True:
                time.sleep(0.1)

    def getSerialData(self):
        return list(self.data)

    def backgroundThread(self):    # retrieve data
        #time.sleep(1.0)  # give some buffer time for retrieving data
        self.serialConnection.reset_input_buffer()
        oldtime = self.initTime
        while (self.isRun):
            #time.sleep(0.001)
            self.line = self.serialConnection.readline()
            try:
                value = str(self.line, 'ascii').split("\t")
            #    print(value[0])
            except:
                pass
            dat = {'value':value,'time':time.time() - self.initTime, 'timeDifferenz':time.time() - oldtime}
            oldtime = time.time()
            self.data.append(dat)
            self.isReceiving = True
            #print(self.rawData)

    def close(self):
        self.isRun = False
        self.thread.join()
        self.serialConnection.close()
        print('Disconnected...')
        # df = pd.DataFrame(self.csvData)
        # df.to_csv('/home/rikisenia/Desktop/data.csv')
