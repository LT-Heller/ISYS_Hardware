from PyQt5 import QtWidgets, uic, QtCore, QtGui
from pyqtgraph import PlotWidget
import sys
from plot import graphPlot
from QtSerial import *
import threading
from time import sleep
from recorder import recorder
import os

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        self.currentPath = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(self.currentPath + '/main.ui', self)
        
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
        self.timer.setInterval(20)
        self.timer.timeout.connect(self.getSerialData)
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
        
    def getSerialData(self):    #liste raus machen
        times = []
        value = [[],[],[],[]]
        while not self.st.queue.empty():
            data = self.st.queue.get()
            time = data['time']
            values = data['values']
            try:
                if(int(values[0]) > 1024 or int(values[1]) > 1024 or int(values[2]) > 1024 or int(values[3]) > 1024):
                    continue
                if(int(values[0]) < 0 or int(values[1]) < 0 or int(values[2]) < 0 or int(values[3]) < 0):
                    continue
            except:
                continue
            times.append(data['time'])
            value[0].append(int(values[0]))
            value[1].append(int(values[1]))
            value[2].append(int(values[2]))
            value[3].append(int(values[3]))
            try:
                self.textBrowserSerial.setText("{:.3f}:\t{}  {}  {}  {}".format(time,values[0],values[1],values[2],values[3]))
                self.record.addData(int(values[0]),int(values[1]),int(values[2]),int(values[3]))
                self.labelInfotext.setText(self.record.getInfoText())
                self.setPicture()
            except:
                pass
        self.graph.addAndPlot(times,(value[0]),(value[1]),(value[2]),(value[3]))
        
    def plot(self, time, value):
        self.graph.addAndPlot(time, value, value, value, value)
        
    def setPicture(self):
        pixmap = QtGui.QPixmap(self.currentPath + os.sep + str(self.record.lable) + ".jpg")
        self.labelPicture.setPixmap(pixmap)
        self.labelPicture.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    status = app.exec_()
    sys.exit(status)

if __name__ == '__main__':
    main()