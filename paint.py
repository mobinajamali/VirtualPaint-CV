import cv2 as cv
import numpy as np

# CAPTURE WEBCAM
cap = cv.VideoCapture(0)

# SET CAPTURE PARAMETERS
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
cap.set(3, FRAME_WIDTH)
cap.set(4, FRAME_HEIGHT)
cap.set(10, 150)

# DEFINE COLOR MIN AND MAX FOR HUE ND SATURATION (values found using the color_picker.py)
# [h_min, s_min, v_min, h_max, s_max, v_max]
myColors = [[5, 107, 0, 19, 255, 255], # FOR ORANGE
            [157, 76, 128, 179, 255, 255],  # FOR PINK
            [90, 48, 0, 118, 255, 255],  # FOR BLUE
            [27, 0, 0, 177, 255, 184]]  # FOR BLACK

# CORRESPONDING RGB COLOR CODES FOR THE ABOVE PARAMETERS
# NOTE: YOU HAVE TO WRITE IT IN THE FORMAT OF BGR
myColorValues = [[51, 153, 255],
                 [153, 51, 255],
                 [255, 0, 0],
                 [0, 0, 0]]

myPoints = []   # [x, y, colorIndex (aka count)]

# DEFINE A FUNCTION TO FIND THE COLOR USING MASK
def findColor(img, myColors, myColorValues):
    # CONVERT TO HSV
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    count = 0
    newPoints = []

    # USE UPPER & LOWER LIMIT
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        # CREATE A MASK
        mask = cv.inRange(hsv, lower, upper)
        x,y = getContours(mask) # CHECK THE CONTOUR(*)
        # DRAW CIRCLE AROUND IT (NOTE: DRAW THE COLOR OF THE CIRCLE BASED ON COLOR VALUES)
        cv.circle(result, (x,y), 10, myColorValues[count], cv.FILLED)
        # ONLY IF X, Y ARE DEFINED
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count += 1
        #cv.imshow(str(color[0]), mask)
    return newPoints

# GET THE LOCATION OF THE COLOR USING CONTOUR
def getContours(img):
    contours, hierachy = cv.findContours(img, cv.RETR_EXTERNAL, cv. CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0 # IN CASE IF IT IS NOT DETECTED
    for cnt in contours:
        # FIND THE AREA OF THE CONTOUR
        area = cv.contourArea(cnt)
        # DRAW IT OUT
        cv.drawContours(result, cnt, -1, (255, 0, 0), 3)
        # GIVE MIN THRESHOLD TO PREVENT CAPTURING NOISES
        if area > 500:
            # CALCULATE CURVE LENGTH (TO APPROXIMATE THE CORNERS OF THE EDGES)
            peri = cv.arcLength(cnt, True)
            # APPROX NUM CORNER POINTS FOR EACH SHAPE
            approx = cv.approxPolyDP(cnt, 0.02*peri, True)
            # CREATE BOUNDING BOX AROUND DETECTED OBJ
            x,y,w,h = cv.boundingRect(approx)

    # TO DRAW FROM THE TIP OF THE PEN NOT THE CENTER
    return x+w//2, y

# DRAW THE POINTS
def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv.circle(result, (point[0],point[1]), 10, myColorValues[point[2]], cv.FILLED)

# READ FRAMES
while True:
    success, frame = cap.read()
    result = frame.copy()  # IMG CONTAINING ALL THE INFO
    newPoints = findColor(frame, myColors, myColorValues)  # CALL THE FUNC
    if len(newPoints) != 0:
        for newPoint in newPoints:
            myPoints.append(newPoint)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)

    cv.imshow('Result', result)
    if cv.waitKey(1) & 0xFF==ord('q'):
        break

