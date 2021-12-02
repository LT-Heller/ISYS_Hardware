import serial
import sys
import time
import collections
import threading
from queue import Queue
from PyQt5 import QtSerialPort, QtCore
import struct
import glob

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
        self.dataType = "BYTE"                                  #STRING or BYTE
        self.state = 1
        self.by = bytes()
        self.time = 0
        
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
        
        while self.serial.bytesAvailable() >= 1:
            if self.dataType == "BYTE":
                chr=self.serial.read(1)
                if (self.state==1): # warten auf StartbitANFANG (0xAAAA)
                    if (chr==b'\xaa'):
                        self.state=2
                    else:
                        print("sync fehler 1")
                elif (self.state==2):   # zweite Hälfte vom Startbit bestätigen
                    if(chr==b'\xaa'):
                        self.state=3
                        # print("Blockanfang gefunden")
                    else:
                        self.state = 1
                        print("sync fehler 2")
                elif (3<=self.state and self.state <=10): # Daten aufnehmen
                        self.state=self.state+1
                        self.by+=chr
                        if self.state%2 == 0 and chr == b'\xaa':  # Startbit während der Aufnahme
                            print("sync fehler 3")
                            self.state = 2
                            self.by = bytes()
                            self.time += 0.001
                if (self.state>10):
                    # print("Daten bekommen")
                    self.state=1
                    values = (0,0,0,0)
                    values = struct.unpack('>HHHH', self.by)
                    self.by = bytes()
                    dat = {'values':values,'time':self.time}
                    self.time += 0.001
                    if len(values) > 3:
                        self.queue.put(dat)
                            
            
                        
                # by= bytes()
                # while by != 0xAA:
                #     by = self.serial.read(1)
                # if (self.serial.read(1) !=0xaa):
                #     continue
                # print("gefunden")
                # by = self.serial.read(8)#self.serial.readLine()
                # by = by[:8]
                # #byy = by.split('\t')
                
            # else:
            #     text = self.serial.readLine().data().decode()
            #     text = text.rstrip('\r\n')
            # try:
            #     if self.dataType == "BYTE":
            #         values = (0,0,0,0)
            #         #for i in range(0,3):
            #             #values[i] = int.from_bytes(byy[i],byteorder='big')
            #         values = struct.unpack('>HHHH', self.by)
            #     else:
            #         values = text.split("\t")
            # except:
            #     pass