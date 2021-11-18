from tkinter.constants import END, FALSE, LEFT, RIGHT, Y
import serial
import sys 
import tkinter as tk
#import matplotlib
#matplotlib.use("TkAgg")
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
#from matplotlib.figure import Figure
from functions.plotwindow import Plotwindow
import time
from functions.serialReciever import serialReciever
import threading

RUN = True

def serial_ports():
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

def chosePortAction():
    try:
        port = selectedPort.get()
        if port != 'None':
            sr.changePort(port)
            sr.readSerialStart()
            time.sleep(1)
            thread.start()
    except:
        pass

def loop():
    global plotTime
    line = str()
    string = str()
    value = [0]
    try:
        line = ser.readline()
    except (OSError, serial.SerialException):
        app.after(4, loop)
        return
    try:
        value = str(line, 'ascii').split("\t")
        string = str(line, 'ascii')
    except:
        pass
    if value[0]:
        pw.addplotxy(round(time.time()*1000),int(value[0]))
    plotTime += 0.04
    serMon.insert(END, string)
    serMon.yview_moveto(1)
    app.after(1, loop)                  #default 4ms
    
def plot():
    data = list(sr.getSerialData())
    times = []
    values = []
    string = str()
    for dat in data:
        try:
            times.append(dat['time'])#times.append(round(dat['time'] * 1000))
            values.append(int(dat['value'][0]))
            string += str(dat) + '\n'
        except:
            pass
    serMon.insert(END, string)
    serMon.yview_moveto(1)
    pw.plotxy(times, values)
    app.after(1000, plot)
    
def refreshSerMon():
    global RUN
    while(RUN):
        try:
            line = str(sr.line, 'ascii')
        except:
            pass
        serMon.insert(END, line)
        serMon.yview_moveto(1)
        
#sr = serialReciever()
#while True:
#    sr.readSerialStart()
#    data = list(sr.getSerialData())
#    for dat in data:
#        print (dat)
#        print('\n')
#    time.sleep(1)

#ser = serial.Serial()
#ser.timeout = 0.4
#ser.baudrate = 115200

# Ein Fenster erstellen
app = tk.Tk()
# Den Fenstertitle erstellen
app.title("EMG Recorder")

app.geometry('1000x500')

portList = list(serial_ports())
if not portList:
    portList = ["None"]

selectedPort = tk.StringVar(app)
selectedPort.set(portList[0])

opt = tk.OptionMenu(app, selectedPort, *portList)
opt.config(width=90, font=('Helvetica', 12))
opt.pack()

chosePort = tk.Button(app, text="Port wählen", command=chosePortAction)
chosePort.pack(side=RIGHT)

serScroll = tk.Scrollbar(app)
serMon = tk.Text(app, height=10, width=50)
serMon.pack(side=LEFT, fill=Y)
serScroll.pack(side=LEFT, fill=Y)
serScroll.config(command=serMon.yview)
serMon.config(yscrollcommand=serScroll.set)

mf = tk.Frame(master = app)
pw = Plotwindow(mf,(200,150))
mf.pack()
plotTime = 0

sr = serialReciever()
    
#app.after(0, loop)
#app.after(10, plot)

thread = threading.Thread(target = refreshSerMon)

app.mainloop()

RUN=False
sr.close()
thread.join()