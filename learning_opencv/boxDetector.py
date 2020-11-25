import numpy as np
import cv2

#Camera feed for my remote camera (Uses an app on my phone)
cam = 'http://10.0.0.212:4747/mjpegfeed'

cap = cv2.VideoCapture(cam)

while(1):
    ret,img = cap.read()

    # Convert to grayscale. 
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    mask = cv2.inRange(imgray, 110, 255)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)

    probability = 0
    
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours: 
        area = cv2.contourArea(cnt) 
   
        # Shortlisting the regions based on there area. 
        if area > 5000:  
            approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True) 
            probability += 10
            if(probability > 100):
                probability = 100
    
            # Checking if the no. of sides of the selected region is 7. 
            if(len(approx) >= 4 and len(approx) <= 6):  
                cv2.drawContours(img, [approx], 0, (0, 0, 255), 5) 
                probability = 100

    cv2.putText(img, '{}%'.format(probability), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('img', img)
    cv2.imshow('imgray', mask)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
