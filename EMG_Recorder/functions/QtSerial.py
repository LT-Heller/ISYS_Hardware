import serial
import sys
import time
import collections
import threading
from queue import Queue
from PyQt5 import QtSerialPort, QtCore

class serialTools:
    
    def __init__(self, QTMainWindow):
        self.serial = QtSerialPort.QSerialPort(
            'COM5',
            baudRate=2000000,#QtSerialPort.QSerialPort.Baud2000000,
            readyRead=self.receive
        )
        self.data = collections.deque(maxlen=1000)
        self.initTime = time.time()
        self.isConnected = False
        self.reading = bytes()
        self.lines = []
        self.dat = {'values':list(),'time':time.time() - self.initTime}
        self.queue = Queue()
        self.counter = 0
        self.QtMainWindow = QTMainWindow
        
    def __del__(self):
        pass
    
    def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def connectPort(self, port):
        try:
            if port != 'None':
                self.serial.setPort(QtSerialPort.QSerialPortInfo(port))
                print(self.serial.open(QtCore.QIODevice.ReadWrite))
                self.isConnected = True
                #time.sleep(1)
                #threadSerMon.start()
                #threadPlot.start()
        except:
            pass
        
    def disconnect(self):
        self.isConnected = False
        self.serial.close()
    
    def receive(self):
        while self.serial.canReadLine():
            text = self.serial.readLine().data().decode()
            text = text.rstrip('\r\n')
            try:
                values = text.split("\t")
                values.pop(0)
            except:
                pass
            dat = {'values':values,'time':time.time() - self.initTime}
            #return(dat['time'], dat['values'])
            if len(values) > 3:
                self.queue.put(dat)