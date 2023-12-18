import time
import numpy as np
import cv2
import mouse
from MyHandTrackingAlgo import FindHands
from tkinter import *

w_cam, h_cam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, w_cam)
cap.set(4, h_cam)
win = Tk()
smoothening = 6
wScr, hScr = win.winfo_screenwidth(), win.winfo_screenheight()
# print(wScr, hScr)
p_locX, p_locY = 0, 0
c_locX, c_locY = 0, 0

detector = FindHands(max_hands=2)
p_time, length = 0, 0
# Frame Reduction
frame_rd = 100

while True:
    # 1. Find Hand Landmarks
    succeed, img = cap.read()

    lst, bbox = detector.get_position(img)

    # 2. Get the tip of the index and middle finger
    if len(lst) != 0:
        x1, y1 = lst[8][1:]
        x2, y2 = lst[12][1:]
        # print(x1, y1, x2, y2)

        # 3. Check if fingers are up
        fingers = detector.fingers_up(lst)
        # print(fingers)

        cv2.rectangle(img, (frame_rd, frame_rd), (w_cam - frame_rd, h_cam - frame_rd), (255, 0, 255), 2)
        # 4. Only index finger : Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:
            # 5. convert coordinates
            x3 = np.interp(x1, (frame_rd, w_cam - frame_rd), (0, wScr))
            y3 = np.interp(y1, (frame_rd, h_cam - frame_rd), (0, hScr))

            # 6. smoothen values
            c_locX = p_locX + (x3 - p_locX) / smoothening
            c_locY = p_locY + (y3 - p_locY) / smoothening
            cv2.circle(img, (x1, y1), 15, (255, 255, 0), cv2.FILLED)
            p_locX, p_locY = c_locX, c_locY
            # 7. move mouse
            mouse.move(wScr - c_locX, c_locY)

        # 8. Both Index and middle finger are up: Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:
            # 9. Find distance between two fingers
            length, img, lineInfo = detector.find_distance(lst, 8, 12, img)
            print(length)
            # 10 Click mouse if short
            if length < 30:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                mouse.click()
    # 11. Frame Rate
    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord("q"):
        break
