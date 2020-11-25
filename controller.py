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

    for x in notes:
            ser.sendData(letterToNote(x))
            time.sleep(2)

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
        return noteE()
    elif letter == "G":
        return noteE()

def noteA():
    return "M-15,20,100,"

def noteB():
    return "M-30,20,100,"

def noteC():
    return "M-45,20,100,"

def noteD():
    return "M45,20,100,"

def noteE():
    return "M30,20,100,"

def noteF():
    return "M15,20,100,"

def noteG():
    return "M0,20,100,"
    
if __name__ == "__main__":
    main()