import cv2
import numpy as np

# Min Area a color area must have to be tracked
MIN_AREA = 25000

# Blue + Green + Red + Yellow + Cyan + Magenta 
colors_lower = [[110,100,100],[50,100,100],[170,100,100],[20,100,100],[80,100,100],[140,100,100]]
colors_upper = [[130,255,255],[70,255,255],[180,255,255],[40,255,255],[100,255,255],[160,255,255]]

cap = cv2.VideoCapture(0)

while(1):
    _, frame = cap.read()
    
    # Create List for tracked objects
    objIndex = 0
    objectList = []

    # Iterate color ranges
    for index in range(len(colors_lower)):
        
        # Track objects
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_color = np.array(colors_lower[index])
        upper_color = np.array(colors_upper[index])
        mask = cv2.inRange(hsv, lower_color, upper_color)
        contours, hierarchy = cv2.findContours(mask, 1, 2)

        # Iterate tracked objects of the current color
        for contour in contours:

            # Only save if tracked area is large enough
            area = cv2.contourArea(contour)
            if area>MIN_AREA:

                # Draw Rectangle, calculate center points and put coords to the rectangle
                x,y,w,h = cv2.boundingRect(contour)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),2)
                center_x = x+(w/2)
                center_y = y+(h/2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame,str(center_x) + ";" + str(center_y),(x+w,y+h), font, 1,(255,255,255),2,8)

                # Update coords in the objectlist
                if (objIndex==len(objectList)):
                    objectList.append([]);
                objectList[objIndex] = [center_x,center_y]
                objIndex+=1
                    
    # print list of tracked objects      
    print objectList

    cv2.imshow('frame',frame)
    k = cv2.waitKey(5) & 0xFF

cap.release()
cv2.destroyAllWindows()