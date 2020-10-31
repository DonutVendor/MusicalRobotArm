import serial
import cv2
import time

class SerialWrapper:

    def __init__(self, device):
        self.ser = serial.Serial('COM4')

    def sendData(self, data):
        data += "\r\n"
        self.ser.write(data.encode())

def main():
    notes = ["C", "D", "E", "D", "C", "C", "C", "E", "E", "E", "E"]

    ser = SerialWrapper('COM4')
    
    #Runs code sequence. This is the loop()
    while 1:
        for x in notes:
            ser.sendData(letterToNote(x))
            time.sleep(1)
            ser.sendData("D")
            time.sleep(1)

def letterToNote(letter):
    if letter == "A":
        return noteA()
    elif letter == "B":
        return noteB()
    elif letter == "C":
        return noteC()
    elif letter == "D":
        return noteD()
    elif letter == "E":
        return noteE()

def noteA():
    return "M-80,20,100,"

def noteB():
    return "M-40,20,100,"

def noteC():
    return "M0,20,100,"

def noteD():
    return "M40,20,100,"

def noteE():
    return "M80,20,100,"
    
if __name__ == "__main__":
    main()