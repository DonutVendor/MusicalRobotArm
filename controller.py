import serial
import cv2
import time

ser = None

class SerialWrapper:

    def __init__(self, device):
        self.ser = serial.Serial('COM4')

    def sendData(self, data):
        data += "\r\n"
        self.ser.write(data.encode())

def playSong(notes):
    ser = SerialWrapper('COM4')

    print(notes)
    time.sleep(2)
    ser.sendData("E\r\n")
    time.sleep(2)
    ser.sendData("M0,0,200,\r\n")
    time.sleep(5)

    for x in notes:
            ser.sendData(letterToNote(x))
            time.sleep(0.66)

    ser.sendData("M0,0,0,\r\n")
    time.sleep(2)
    ser.sendData("R\r\n")

def main():
    ser = SerialWrapper('COM4')

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
    elif letter == "F":
        return noteF()
    elif letter == "G":
        return noteG()

def noteA():
    return "M30,0,200,D" #

def noteB():
    return "M60,0,200,D"

def noteC():
    return "M-90,0,200,D"

def noteD():
    return "M-60,0,200,D" #

def noteE():
    return "M-30,0,200,D" #

def noteF():
    return "M0,0,200,D" #

def noteG():
    return "M0,0,200,D" #
    
if __name__ == "__main__":
    main()