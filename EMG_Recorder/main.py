from PyQt5 import QtWidgets, uic, QtCore, QtGui
from pyqtgraph import PlotWidget
import sys
from functions.plot import graphPlot
from functions.QtSerial import *
import threading
from time import sleep
from functions.recorder import recorder
import os

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi('./ui/main.ui', self)
        
        self.st = serialTools(self)
        self.serialPorts = self.st.serial_ports()
        if not self.serialPorts:
            self.serialPorts = ["None"]
        self.comboBoxPorts.addItems(self.serialPorts)
        
        self.time = 0
        self.RecorderIsRunning = False
        self.loggerIsRunning = False
        self.recordThread = threading.Thread(target=self.getSerialData)
        self.record = recorder()
        self.graph = graphPlot(self)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.getSerialData)
        self.currentPath = os.getcwd()
        self.setPicture()
        
    def __del__(self):
        pass
        #self.st.stopThread()
        
    def connectSerial(self):
        port = self.comboBoxPorts.currentText()
        print("Selected Port: ", port)
        self.st.connectPort(port)
        if self.st.isConnected:
            #self.st.serialReset()
            #if  not self.st.threadIsRunnning:
            #    self.st.startThread()
            self.timer.start()
            self.loggerIsRunning = True
            
    def disconnectSerial(self):
        if self.st.isConnected:
            self.timer.stop()
            self.loggerIsRunning = False
            self.st.disconnect()
        
    def startRecord(self):
        #self.textBrowserSerial.append(str(self.time))
        #self.time += 1
        if self.loggerIsRunning:
            self.RecorderIsRunning = True
            self.record.startRecorder()
            #self.recordThread.start()
            #self.getSerialData()
            
    def stopRecord(self):
        self.RecorderIsRunning = False
        self.record.stopRecorder()
        #self.recordThread.join()
        
    def getSerialData(self):
        while not self.st.queue.empty():
            data = self.st.queue.get()
            time = data['time']
            values = data['values']
            try:
                if(int(values[0]) > 1024 or int(values[1]) > 1024 or int(values[2]) > 1024 or int(values[3]) > 1024):
                    return
                if(int(values[0]) < 0 or int(values[1]) < 0 or int(values[2]) < 0 or int(values[3]) < 0):
                    return
            except:
                return
            try:
                self.textBrowserSerial.append("{:.3f}:\t{}  {}  {}  {}".format(time,values[0],values[1],values[2],values[3]))
                self.graph.addAndPlot(time,int(values[0]),int(values[1]),int(values[2]),int(values[3]))
                self.record.addData(int(values[0]),int(values[1]),int(values[2]),int(values[3]))
                self.labelInfotext.setText(self.record.getInfoText())
                self.setPicture()
            except:
                pass
        
    def plot(self, time, value):
        self.graph.addAndPlot(time, value, value, value, value)
        
    def setPicture(self):
        pixmap = QtGui.QPixmap(self.currentPath + os.sep + "pictures" + os.sep + str(self.record.lable) + ".jpg")
        self.labelPicture.setPixmap(pixmap)
        self.labelPicture.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    status = app.exec_()
    #main.st.stopThread()
    sys.exit(status)

if __name__ == '__main__':
    main()