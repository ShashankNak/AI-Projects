import cv2
import mediapipe as mp
import math


class FindHands:
    def __init__(self, mode=False, max_hands=2, detection_con=0.5, tracking_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=mode, max_num_hands=max_hands,
                                        min_detection_confidence=detection_con, min_tracking_confidence=tracking_con)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def get_position(self, img, hand_no=0, draw=True):
        lst = []
        xlist = []
        ylist = []
        bbox = []
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        if results.multi_hand_landmarks:
            if len(results.multi_hand_landmarks) >= hand_no + 1:
                for ID, lm in enumerate(results.multi_hand_landmarks[hand_no].landmark):
                    h, w, c = img.shape
                    x, y = int(lm.x * w), int(lm.y * h)
                    xlist.append(x)
                    ylist.append(y)
                    lst.append((ID, x, y))
                    # if draw:
                        # cv2.circle(img, (x, y), 5, (255, 0, 255), cv2.FILLED)

                # if draw:
                #     self.mpDraw.draw_landmarks(img, results.multi_hand_landmarks[hand_no],
                #                                self.mpHands.HAND_CONNECTIONS)
            x_min, x_max = min(xlist), max(xlist)
            y_min, y_max = min(ylist), max(ylist)
            bbox = x_min, y_min, x_max, y_max
            # if draw:
            #     cv2.rectangle(img, (x_min - 20, y_min - 20), (x_max + 20, y_max + 20),
            #                   (0, 255, 0), 2)
        return lst, bbox

    def fingers_up(self, lm_list):
        fingers = []
        # Thumb
        if lm_list[self.tipIds[0]][1] > lm_list[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for ID in range(1, 5):

            if lm_list[self.tipIds[ID]][2] < lm_list[self.tipIds[ID] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # totalFingers = fingers.count(1)

        return fingers

    @staticmethod
    def find_distance(lm_list, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = lm_list[p1][1:]
        x2, y2 = lm_list[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # if draw:
        #     cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
        #     cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
        #     cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
        #     cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]
