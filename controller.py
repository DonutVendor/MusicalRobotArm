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
    ser = SerialWrapper('COM4')
    
    #Runs code sequence. This is the loop()
    while 1:
        ser.sendData("M0,0,100,")
        time.sleep(5)
        ser.sendData("M100,0,100,")
        time.sleep(5)
        ser.sendData("M100,0,0,")
        time.sleep(5)
    
if __name__ == "__main__":
    main()