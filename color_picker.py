import cv2 as cv
import numpy as np

# Define the codec and create VideoWriter object based on final image size
out = cv.VideoWriter('color_picker.avi',
                     cv.VideoWriter_fourcc(*'XVID'), 
                     20.0, 
                     (1920, 480)) # final hstack image size


# webcam setup capture
frameWidth = 640
frameHeight = 480
cap = cv.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)

# send empty function for the track bar
def empty(a):
    pass

# create track bar
cv.namedWindow("HSV")
cv.resizeWindow("HSV",640,240)
cv.createTrackbar("HUE Min","HSV",0,179,empty)
cv.createTrackbar("SAT Min","HSV",0,255,empty)
cv.createTrackbar("VALUE Min","HSV",0,255,empty)
cv.createTrackbar("HUE Max","HSV",179,179,empty)
cv.createTrackbar("SAT Max","HSV",255,255,empty)
cv.createTrackbar("VALUE Max","HSV",255,255,empty)

# read webcam frames
while True:
    _, img = cap.read()
    # convert frame to hsv
    imgHsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)

    # set track bar positioning
    h_min = cv.getTrackbarPos("HUE Min","HSV")
    h_max = cv.getTrackbarPos("HUE Max", "HSV")
    s_min = cv.getTrackbarPos("SAT Min", "HSV")
    s_max = cv.getTrackbarPos("SAT Max", "HSV")
    v_min = cv.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv.getTrackbarPos("VALUE Max", "HSV")
    print(h_min)

    # set boundaries of the track bar
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])

    mask = cv.inRange(imgHsv,lower,upper)
    result = cv.bitwise_and(img,img, mask = mask)

    # create gray masking
    mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
    hStack = np.hstack([img,mask,result])
    #cv2.imshow('Original', img)
    #cv2.imshow('HSV Color Space', imgHsv)
    #cv2.imshow('Mask', mask)
   #cv2.imshow('Result', result)
    out.write(hStack)
    cv.imshow('Horizontal Stacking', hStack)
    print(hStack.shape)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv.destroyAllWindows()