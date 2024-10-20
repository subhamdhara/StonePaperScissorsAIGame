import cv2
import time
from cvzone.HandTrackingModule import HandDetector
import cvzone
import random_choice
import desision as d


def game(detector, cap):
    stateResult = True
    initialTime = 0
    move, comp_img = None, None
    score = [0, 0]
    while True:
        imgBg = cv2.imread("resources/Rock Paper Scissors.png")
        _, img = cap.read()
        img = cv2.flip(img, 180)
        hands, img = detector.findHands(img, flipType=False, draw=True)
        img = img[0:463, 0:487]
        imgBg[170:633, 691:1178] = img
        if stateResult is False:
            timer = int(time.time() - initialTime)
            cv2.putText(imgBg, str(timer), (615, 405), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)
            if timer > 3:
                stateResult = True 
                if hands:
                    state = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 1, 1, 0, 0]:
                        state = 3
                    elif fingers == [1, 1, 1, 1, 1]:
                        state = 2
                    elif fingers == [0, 0, 0, 0, 0]:
                        state = 1
                    # print(state)
                    move, comp_img = random_choice.comp_choice(4)
                    imgBg = cvzone.overlayPNG(imgBg, comp_img, (150,200))
                    de = d.determine_winner(state, move)
                    if de != 0:
                        if de == 1:
                            score = [score[0], score[1]+1]
                        if de == 2:
                            score = [score[0]+1, score[1]]

        if stateResult and comp_img is not None:
            imgBg = cvzone.overlayPNG(imgBg, comp_img, (150,200))
        cv2.putText(imgBg, str(score[0]), (440, 155), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 4)
        cv2.putText(imgBg, str(score[1]), (1035, 155), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 4)

        cv2.imshow("game", imgBg)
        key = cv2.waitKey(1)
        if key == ord("s"):
            initialTime = time.time()
            stateResult = False
def splash(detector, cap):
    # run = True
    while True:
        imgBg = cv2.imread("resources/splash.png")
        _, img = cap.read()
        img = cv2.flip(img, 180)
        hands, img = detector.findHands(img, flipType=False, draw=True)
        tipIds = [4, 8, 12, 16, 20]
        if hands:
            hand = hands[0]
            myLmList = hand["lmList"]
            myHandType = hand["type"]
            fingers = []

            if myLmList[tipIds[0]][1] < myLmList[tipIds[0] - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            if myHandType == "Right":
                for id in range(1, 5):
                    if myLmList[tipIds[id]][0] < myLmList[tipIds[id] - 2][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
            else:
                for id in range(1, 5):
                    if myLmList[tipIds[id]][0] > myLmList[tipIds[id] - 2][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
            # print(fingers)
            if fingers == [1, 0, 0, 0, 0]:
                break
        cv2.imshow("game", imgBg)
        cv2.waitKey(1)


cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)

if __name__ == "__main__":
    splash(detector, cap)
    game(detector, cap)
