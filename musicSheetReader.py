import numpy as np
import cv2
import serial
import time
from controller import *

D1 = [116, 125]
E1 = [106, 115]
F1 = [96, 105]
G1 = [86, 95]
A1 = [76, 85]
B1 = [66, 75]
C1 = [56, 65]
D2 = [46, 55]
E2 = [36, 45]
F2 = [26, 35]
G2 = [16, 25]

listOfLetters = []
listToSend = []

def sortOrder(e):
    return e['loc']

def getLetter(height):

    if height > G2[0] and height < G2[1]:
        return "G"
    elif height > F2[0] and height < F2[1]:
        return "F"
    elif height > E2[0] and height < E2[1]:
        return "E"
    elif height > D2[0] and height < D2[1]:
        return "D"
    elif height > C1[0] and height < C1[1]:
        return "C"
    elif height > B1[0] and height < B1[1]:
        return "B"
    elif height > A1[0] and height < A1[1]:
        return "A"
    elif height > G1[0] and height < G1[1]:
        return "G"
    elif height > F1[0] and height < F1[1]:
        return "F"
    elif height > E1[0] and height < E1[1]:
        return "E"
    elif height > D1[0] and height < D1[1]:
        return "D"
    else:
        return "ERROR"

def main():
    img = cv2.imread('music.png')
    #ret,img = cap.read()
    listOfLetters = []
    listToSend = []
    
    # Convert to grayscale. 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    
    # Blur using 3 * 3 kernel. 
    gray_blurred = cv2.blur(gray, (1, 1)) 
    
    # Apply Hough transform on the blurred image. 
    detected_circles = cv2.HoughCircles(gray_blurred,  
                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 100, 
                param2 = 20, minRadius = 1, maxRadius = 30) 
    
    if detected_circles is not None: 
    
        # Convert the circle parameters a, b and r to integers. 
        detected_circles = np.uint16(np.around(detected_circles)) 
    
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2] 
    
            # Draw the circumference of the circle. 
            cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
    
            # Draw a small circle (of radius 1) to show the center. 
            cv2.circle(img, (a, b), 1, (0, 0, 255), 3) 

            cv2.putText(img, getLetter(b), (a, b), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            listOfLetters.append({'letter': getLetter(b), 'loc': a})
        
    #Send data to controller
    listOfLetters.sort(key=sortOrder)
    for x in listOfLetters:
        listToSend.append(x['letter'])

    cv2.imshow('img',img)

    playSong(listToSend)
 
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()

#cap.release()
