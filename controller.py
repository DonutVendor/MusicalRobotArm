import serial

class SerialWrapper:

    def __init__(self, device):
        self.ser = serial.Serial('COM4')

    def sendData(self, data):
        data += "\r\n"
        self.ser.write(data.encode())

def main():
    ser = SerialWrapper('COM4')
    
    while 1:
        ser.sendData("M100,0,100,")
        sleep(1)
    
if __name__ == "__main__":
    main()