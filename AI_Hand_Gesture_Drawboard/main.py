import cv2 as cv
from tkinter import *
from MyHandTrackingAlgo import FindHands
import time
import numpy as np


cap = cv.VideoCapture(0)
w_cam, h_cam = 640, 480
cap.set(3, w_cam)
cap.set(4, h_cam)
win = Tk()
smoothening = 6
wScr, hScr = win.winfo_screenwidth(), win.winfo_screenheight()
p_locX, p_locY = 0, 0
c_locX, c_locY = 0, 0

detector = FindHands(max_hands=2)
p_time, length = 0, 0
# Frame Reduction
frame_rd = 10

canvas = []


while True:
    succeed, img = cap.read()
    # mirror the frames
    img = cv.flip(img, 1)
    lst, bbox = detector.get_position(img)

    # 2. Get the tip of the index and middle finger
    if len(lst) != 0:
        x1, y1 = lst[8][1:]
        x2, y2 = lst[12][1:]
        t1, t2 = lst[4][1:]
        # print(x1, y1, x2, y2)

        # 3. Check if fingers are up
        fingers = detector.fingers_up(lst)
        
        # white color canvas
        cv.rectangle(img, (frame_rd, frame_rd), (w_cam - frame_rd, h_cam - frame_rd), (0, 255, 0), 15)
        # 4. Only index finger : Draw mode
        if fingers[1] == 1 and fingers[2] == 0:
            # 5. convert coordinates
            x3 = np.interp(x1, (frame_rd, w_cam - frame_rd), (0, wScr))
            y3 = np.interp(y1, (frame_rd, h_cam - frame_rd), (0, hScr))

            # 6. smoothen values
            c_locX = p_locX + (x3 - p_locX) / smoothening
            c_locY = p_locY + (y3 - p_locY) / smoothening
            cv.circle(img, (x1, y1), 15, (255, 255, 0), cv.FILLED)
            p_locX, p_locY = c_locX, c_locY

            # 8. Draw on the canvas
            cv.circle(img, (x1,y1), 15, (0, 0, 0), cv.FILLED)

            canvas.append((x1, y1))
            

        # 8. Both Index and middle finger are up: Eraser
        if fingers[1] == 1 and fingers[2] == 1 :
            # 9. Find distance between two fingers
            length, img, lineInfo = detector.find_distance(lst, 8, 12, img)
            # 10 Click mouse if short
            if length < 30:
                cv.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv.FILLED)
                # find values in the canvas and delete the values
                for i in canvas:
                    # if the values of canvas is in the radius of lineInfo
                    if cv.norm(i, (lineInfo[4], lineInfo[5])) < 15:
                        canvas.remove(i)
        if fingers[1] == 1 and fingers[2] == 1 and fingers[0]==1 and fingers[3] ==1:
            canvas = []


        # only thumb is up
        if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0:
            cv.circle(img, (t1,t2), 15, (0, 255, 255), cv.FILLED)
            # freeze the frame
            cv.waitKey(1)

        
        for i in range(len(canvas)):
            cv.circle(img, canvas[i], 3, (0, 0, 0), cv.FILLED)
        






    # 11. Frame Rate
    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time
    cv.putText(img, str(int(fps)), (20, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv.imshow("Image", img)
    if cv.waitKey(1) == ord("q"):
        cv.destroyAllWindows()
        break



