import serial
import struct

class EMGRecorder:

    def __init__(self, baudrate=2000000, port = "COM3", FrameLen = 150):
        recordedData = [[] for _ in range(4)]
        self.FrameLen = FrameLen
        self.ser = serial.Serial(baudrate=baudrate)
        self.ser.port = port

    def connect(self):
        self.ser.open()

    def recordLine(self):
        state = 1
        receivedBytes = bytes()
        while self.ser.readable() >= 1 and state != 12:
            chr=self.ser.read(1)
            if (state==1): # warten auf StartbitANFANG (0xAAAA)
                if (chr==b'\xaa'):
                    state=2
            elif (state==2):   # zweite Hälfte vom Startbit bestätigen
                if(chr==b'\xaa'):
                    state=3
                    # print("Blockanfang gefunden")
                else:
                    print("sync fehler 2")
                    state = 1
            elif (3<=state and state <=10): # Daten aufnehmen
                    state=state+1
                    receivedBytes+=chr
                    if state%2 == 0:
                        if chr == b'\xaa':  # Startbit während der Aufnahme
                            print("sync fehler 3")
                            state = 2
                            receivedBytes = bytes()
                        elif chr != b'\x00' and chr != b'\x01' and chr != b'\x02' and chr != b'\x03': # fehlerhafte Bits während der Aufnahme
                            print(f"error, while reading bytes! Chr: {chr}\treceivedBytes: {receivedBytes}")
                            receivedBytes = bytes()
                            state = 1
            if (state>10):
                # print("Daten bekommen")
                state=12
                values = (0,0,0,0)
                values = struct.unpack('>HHHH', receivedBytes)
                receivedBytes = bytes()
                return values
        return False

    def recordFrame(self):
        self.ser.flushInput()
        frame = [[] for _ in range(4)]
        while len(frame[0]) < self.FrameLen:
            value = self.recordLine()
            if value:
                for c in range(4):
                    frame[c].append(value[c])
            else:
                frame = [[] for _ in range(4)]
        return frame