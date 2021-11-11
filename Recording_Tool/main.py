from tkinter.constants import END, LEFT, RIGHT, Y
import serial
import sys 
import tkinter as tk
#import matplotlib
#matplotlib.use("TkAgg")
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
#from matplotlib.figure import Figure
from functions.plotwindow import Plotwindow

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

def loop():
    global plotTime
    line = str()
    try:
        line = str(ser.readline())
    except (OSError, serial.SerialException):
        return
    value = line.split("\t")
    if value[0]:
        pw.addplotxy(plotTime,value[0])
    plotTime += 0.04
    serMon.insert(END, line)
    app.after(4, loop)                  #default 4ms

ser = serial.Serial()
ser.timeout = 0.4
ser.baudrate = 57600

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

app.after(0, loop)
app.mainloop()