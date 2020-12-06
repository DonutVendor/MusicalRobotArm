import numpy as np
import cv2
import serial
import time
from controller import *

D1 = [385, 392]
E1 = [377, 384]
F1 = [369, 376]
G1 = [361, 368]
A1 = [353, 360]
B1 = [345, 352]
C1 = [337, 344]
D2 = [329, 336]
E2 = [321, 328]
F2 = [313, 320]
G2 = [305, 312]

listOfAllLines = []

listOfLetters = []
listToSend = []

def sortOrder(e):
    return e

def getLetter(height):
    num = 0

    #Top line 2 - Top line 1 - 8
    barMeasureOffset = 199
    for x in range(10):
        if height >= G2[0] + (num * barMeasureOffset) and height < G2[1] + (num * barMeasureOffset):
            return "G{}".format(num)
        elif height >= F2[0] + (num * barMeasureOffset) and height <= F2[1] + (num * barMeasureOffset):
            return "F{}".format(num)
        elif height >= E2[0] + (num * barMeasureOffset) and height <= E2[1] + (num * barMeasureOffset):
            return "E{}".format(num)
        elif height >= D2[0] + (num * barMeasureOffset) and height <= D2[1] + (num * barMeasureOffset):
            return "D{}".format(num)
        elif height >= C1[0] + (num * barMeasureOffset) and height <= C1[1] + (num * barMeasureOffset):
            return "C{}".format(num)
        elif height >= B1[0] + (num * barMeasureOffset) and height <= B1[1] + (num * barMeasureOffset):
            return "B{}".format(num)
        elif height >= A1[0] + (num * barMeasureOffset) and height <= A1[1] + (num * barMeasureOffset):
            return "A{}".format(num)
        elif height >= G1[0] + (num * barMeasureOffset) and height <= G1[1] + (num * barMeasureOffset):
            return "G{}".format(num)
        elif height >= F1[0] + (num * barMeasureOffset) and height <= F1[1] + (num * barMeasureOffset):
            return "F{}".format(num)
        elif height >= E1[0] + (num * barMeasureOffset) and height <= E1[1] + (num * barMeasureOffset):
            return "E{}".format(num)
        elif height >= D1[0] + (num * barMeasureOffset) and height <= D1[1] + (num * barMeasureOffset):
            return "D{}".format(num)

        num += 1

    return "ERROR"

def findAndRemove(source, target, threshold):
    h, w = target.shape[:-1]

    res = cv2.matchTemplate(source, target, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):  # Switch collumns and rows
        source = cv2.rectangle(source, pt, (pt[0] + w, pt[1] + h), (255, 255, 255), -1)
        
def notInList(lists, obj):
    for i in lists:
        if(i['locy'] == obj['locy']):
            if((i['locx']-obj['locx']) * (i['locx']-obj['locx']) >= 2):
                return False
    return True

def main():
    img = cv2.imread('songs/yougotafriendinme.png')
    trebleclef = cv2.imread('detection_images/trebleclef.png')
    quarterrest = cv2.imread('detection_images/quarter_rest.png')
    #ret,img = cap.read()
    listOfLetters = []
    listToSend = []

    findAndRemove(img, trebleclef, 0.8)

    #findAndRemove(img, quarterrest, 0.8)
    #Find quarter notes and add to Music List
    h, w = quarterrest.shape[:-1]

    res = cv2.matchTemplate(img, quarterrest, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.8)
    for pt in zip(*loc[::-1]):  # Switch collumns and rows
        #img = cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (255, 255, 255), -1)
        a = pt[0] + w
        b = pt[1] + h
        obj = {'letter': "R", 'locx': a, 'locy': getLetter(b)[1]}
        if(notInList(listOfLetters, obj)):
            #cv2.putText(img, "R:{}".format(getLetter(b)[1]), (a, b), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 255), 1)
            #cv2.putText(img, getLetter(b), (a, b), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            listOfLetters.append(obj)
        

    # Convert to grayscale. 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

    edges = cv2.Canny(gray, 50, 150, apertureSize = 3)
    lines = cv2.HoughLines(edges, 1, np.pi/180, 10)

    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 2000*(-b))
        y1 = int(y0 + 2000*(a))
        x2 = int(x0 - 2000*(-b))
        y2 = int(y0 - 2000*(a))

        # Filter vertical lines
        if np.abs(y1-y2) < 20:
            #cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 4)
            listOfAllLines.append(y1)
    
    listOfAllLines.sort(key=sortOrder)
    linesList = listOfAllLines[::2]
    print(linesList)

    # Blur using 3 * 3 kernel. 
    gray_blurred = cv2.blur(gray, (1, 1)) 
    
    # Apply Hough transform on the blurred image. 
    detected_circles = cv2.HoughCircles(gray_blurred,  
                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 100, 
                param2 = 12, minRadius = 1, maxRadius = 10) 

    if detected_circles is not None: 
    
        # Convert the circle parameters a, b and r to integers. 
        detected_circles = np.uint16(np.around(detected_circles)) 
    
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2] 
    
            # Draw the circumference of the circle. 
            cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
    
            # Draw a small circle (of radius 1) to show the center. 
            cv2.circle(img, (a, b), 1, (0, 0, 255), 3) 

            #cv2.putText(img, "{}".format(b), (a, b), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(img, "{}:{}".format(getLetter(b), b), (a, b), cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 255), 1)
            #cv2.putText(img, getLetter(b), (a, b), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            listOfLetters.append({'letter': getLetter(b), 'locx': a, 'locy': getLetter(b)[1]})
    
    img_sized = cv2.resize(img, (960, 1800)) 
    cv2.imshow('img',img_sized)

    #Send data to controller
    sortedListOfLetters = sorted(listOfLetters, key=lambda x: (x['locy'], x['locx']))
    for x in sortedListOfLetters:
        listToSend.append(x['letter'][0])

    print(listToSend)
    #playSong(listToSend)
 
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()

#cap.release()
