import serial
import sys
import time
import collections
import threading
from queue import Queue

class serialTools:
    
    def __init__(self):
        self.sr = serial.Serial()
        self.sr.baudrate = 2000000#115200
        self.sr.timeout = 0.01
        self.data = collections.deque(maxlen=1000)
        self.initTime = time.time()
        self.isConnected = False
        self.reading = bytes()
        self.lines = []
        self.threadIsRunnning = False
        self.thread = threading.Thread(target = self.getDataThread)
        self.dat = {'values':list(),'time':time.time() - self.initTime}
        self.queue = Queue()
        self.counter = 0
        
    def __del__(self):
        self.stopThread()
    
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
                self.sr.port = port
                self.sr.open()
                self.isConnected = True
                #time.sleep(1)
                #threadSerMon.start()
                #threadPlot.start()
        except:
            pass
        
    def disconnect(self):
        self.isConnected = False
        self.sr.close()
        self.reading = bytes()
        self.lines = list()
        
    def serialReset(self):
        self.sr.reset_input_buffer()
        self.initTime = time.time()
        
    def backgroundThread(self):    # retrieve data
        #time.sleep(1.0)  # give some buffer time for retrieving data
        self.sr.reset_input_buffer()
        oldtime = self.initTime
        while (self.isRun):
            #time.sleep(0.001)
            self.line = self.sr.readline()
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
            
    def readlines(self):
        if len(self.lines) < 1:
            reading = self.sr.read(self.sr.in_waiting)
            self.reading += reading
            self.lines = str(self.reading, 'ascii').split('\n')
            self.reading = self.reading[(len(self.lines)*21):]
            
        # print("Testline")
        # #print(str(self.reading, 'ascii'))
        # for lin in lines:
        #     print(lin)
            
    def getData(self):
        #self.line = self.sr.readline()
        self.readlines()
        try:
            #values = str(self.line, 'ascii').split("\t")
            values = self.lines[0].split('\t')
            self.lines.pop(0)
            # self.lines.pop(0)
            # self.lines.pop(0)
            # self.lines.pop(0)
        except:
            pass
        dat = {'values':values,'time':time.time() - self.initTime}
        return(dat['time'], dat['values'])
    
    
    def getDataNew(self):
        self.line = self.sr.readline()
        try:
            values = str(self.line, 'ascii').split("\t")
        except:
            pass
        dat = {'values':values,'time':time.time() - self.initTime}
        #return(dat['time'], dat['values'])
        if len(values) > 3:
            #print(dat)
            self.queue.put(dat)
    
    def getDataThread(self):
        while self.threadIsRunnning:
            time.sleep(0.0001)
            if self.isConnected:
                line = self.sr.readline()
                try:
                    values = str(line, 'ascii').split("\t")
                    #values = [str(self.counter), str(0), str(0), str(0)]
                    self.counter += 10
                    if self.counter > 1024:
                        self.counter = 0
                    values[3] = str(self.counter)
                except:
                    pass
                dat = {'values':values,'time':time.time() - self.initTime}
                #return(dat['time'], dat['values'])
                if len(values) > 3:
                    #print(dat)
                    self.queue.put(dat)
            #    self.getDataNew()
            #     (times, values) = self.getData()
            #     if values[0] != '':
            #         self.dat = {'values':values,'time':times}
            #         self.queue.put(self.dat)
                
    def startThread(self):
        self.threadIsRunnning = True
        self.thread.start()

    def stopThread(self):
        if self.threadIsRunnning:
            self.threadIsRunnning = False
            print("stopping Thread")
            self.thread.join()
        
    def getDat(self):
        #return(self.dat['time'], self.dat['values'])
        if not self.queue.empty():
            data = self.queue.get()
            #print("test", data)
            return(data['time'], data['values'])
        return(0, ['0','0','0','0'])