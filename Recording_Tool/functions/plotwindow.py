import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation

class Plotwindow():
    def __init__(self, masterframe, size):

        (w,h)=size
        inchsize=(w/25.4, h/25.4)
        self.figure = Figure(inchsize)
        self.axes = self.figure.add_subplot(111)
        self.axes.set_ylim(0,1024)
        self.xlist = []
        self.ylist = []

        # create canvas as matplotlib drawing area
        self.canvas = FigureCanvasTkAgg(self.figure, master=masterframe)
        self.canvas.get_tk_widget().pack()

    def plotxy(self, x, y):
        self.axes.cla()
        self.axes.set_ylim(0,1024)
        self.axes.plot(x,y)
        self.canvas.draw()

    def addplotxy(self, x, y):
        self.xlist.append(x)
        self.ylist.append(y)
        if(len(self.xlist) > 50):
            self.xlist.pop(0)
            self.ylist.pop(0)
        self.axes.cla()
        self.axes.set_ylim(0,1024)
        self.axes.plot(self.xlist,self.ylist)
        self.canvas.draw()
        
    def clearplot(self):
        self.axes.cla()
        self.canvas.draw() 