import pyqtgraph as pg

class graphPlot:
    def __init__(self, QTMainWindow):
        self.time = []
        self.values = [[] for _ in range(4)]
        self.QTWindow = QTMainWindow
        self.test = 0
        self.data_line1 =  self.QTWindow.graphWidget.plot(list(range(100)),list(range(100)))
        self.data_line2 =  self.QTWindow.graphWidget.plot(list(range(100)),list(range(100)))
        self.data_line3 =  self.QTWindow.graphWidget.plot(list(range(100)),list(range(100)))
        self.data_line4 =  self.QTWindow.graphWidget.plot(list(range(100)),list(range(100)))
        self.QTWindow.graphWidget.setBackground('w')
        self.QTWindow.graphWidget.setYRange(0, 1024, padding=0)
        self.QTWindow.graphWidget.showGrid(x=True, y=True)
        self.pen1 = pg.mkPen(color=(255, 0, 0))
        self.pen2 = pg.mkPen(color=(0, 255, 0))
        self.pen3 = pg.mkPen(color=(0, 0, 255))
        self.pen4 = pg.mkPen(color=(255, 125, 0))
        self.counter = 0
        
    def plot(self, time, value):
        self.QTWindow.graphWidget.plot(time, value)
        
    def plotGraph(self):
        #self.QTWindow.graphWidget.plot(self.time, self.values[0])
        self.data_line1.setData(self.time, self.values[0], pen=self.pen1, name="Channel 1")
        self.data_line2.setData(self.time, self.values[1], pen=self.pen2, name="Channel 2")
        self.data_line3.setData(self.time, self.values[2], pen=self.pen3, name="Channel 3")
        self.data_line4.setData(self.time, self.values[3], pen=self.pen4, name="Channel 4")
        
    def addAndPlot(self, time, value1, value2, value3, value4):
        if (type(time) == type(list()) and type(value1) == type(list())):
            self.time.extend(time)
            self.values[0].extend(value1)
            self.values[1].extend(value2)
            self.values[2].extend(value3)
            self.values[3].extend(value4)
            while(len(self.time) > 1000):                
                self.time.pop(0)
                self.values[0].pop(0)
                self.values[1].pop(0)
                self.values[2].pop(0)
                self.values[3].pop(0)
        else:
            self.time.append(time)
            self.values[0].append(value1)
            self.values[1].append(value2)
            self.values[2].append(value3)
            self.values[3].append(value4)
            if(len(self.time) > 1000):
                self.time.pop(0)
                self.values[0].pop(0)
                self.values[1].pop(0)
                self.values[2].pop(0)
                self.values[3].pop(0)
        if(self.counter == 1):
            self.plotGraph()
            self.counter = 0
        self.counter += 1