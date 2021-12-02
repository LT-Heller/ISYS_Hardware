import serial
import time
import sys

zahl = 10
if type(zahl) == type(int()):
    print("ja")
    
sys.exit(0)

ser = serial.Serial()
ser = serial.Serial()
ser.baudrate = 2000000#115200
ser.timeout = 0.01
ser.port = "COM5"

ser.open()

liste = []
i = 0

while(i < 20000):
    liste.append(ser.readline())
    i += 1
    
f = open("test.txt", "a")
for lines in liste:
    string = str(lines, 'ascii')
    f.write(string)
f.close()