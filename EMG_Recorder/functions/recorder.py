import time
import os

class recorder:
    def __init__(self):
        self.values = [[] for _ in range(4)]
        self.currentPath = os.path.dirname(os.path.abspath(__file__))
        self.path = self.currentPath + "{0}..{0}data".format(os.sep)
        self.recorderIsRunning = False
        self.recording = False
        self.startTime = time.time()
        self.stopTime = time.time()
        self.recordTime = 10
        self.pauseTime = 10
        self.lable = 0
        self.maxLables = 3
    
    def addData(self, value1, value2, value3, value4):
        self.checkStatus()
        if self.recording:
            self.values[0].append(value1)
            self.values[1].append(value2)
            self.values[2].append(value3)
            self.values[3].append(value4)
            
    def checkStatus(self):
        if self.recorderIsRunning:
            if ((time.time() - self.startTime) > self.recordTime and self.recording):
                self.stopRecording()
            elif ((time.time() - self.stopTime) > self.pauseTime and not self.recording):
                self.startRecording()
                
    def getInfoText(self):
        text = "Recorder Infotext..."
        if(not self.recorderIsRunning):
            text = "Keine Aufnahme"
        elif (self.recording):
            text = "Aufnahme läuft noch: {:.1f}".format(self.startTime + self.recordTime - time.time())
        elif (not self.recording):
            text = "Pause noch: {:.1f}".format(self.stopTime + self.pauseTime - time.time())
        return text
        
    def startRecorder(self):
        self.recorderIsRunning = True
        self.stopTime = time.time()
        
    def stopRecorder(self):
        self.recorderIsRunning = False
        if self.recording:
            self.stopRecording()
    
    def startRecording(self):
        self.recording = True
        self.values = [[] for _ in range(4)]
        self.startTime = time.time()
        
    
    def stopRecording(self):
        self.recording = False
        self.stopTime = time.time()
        if self.recorderIsRunning:
            date = time.strftime("%d.%m.%Y_%H.%M.%S")
            print(date)
            f = open(f"{self.path}{os.sep}{date}_EMGAufzeichnung_Lable_{self.lable}.txt", "a") #f"{self.path}{os.sep}{date}_EMG-Aufzeichnung_Lable:{self.lable}.txt"
            for i in range(0, len(self.values[0])):
                string = str(self.values[0][i]) + "," + str(self.values[1][i]) + "," + str(self.values[2][i]) + "," + str(self.values[3][i]) + "," + str(self.lable) + "\n"
                f.write(string)
            f.close()
        self.values = [[] for _ in range(4)]
        self.lable += 1
        if self.lable > self.maxLables - 1:
            self.lable = 0
        if not self.recorderIsRunning: 
            self.lable = 0