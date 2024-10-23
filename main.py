import cv2
import time
from cvzone.HandTrackingModule import HandDetector
import cvzone
import choice
import desision as d

def gesture_horizontal(hand, gesture):
    tipIds = [4, 8, 12, 16, 20]
    fingers = []
    myLmList = hand["lmList"]
    myHandType = hand["type"]
    if myLmList[0][0] - myLmList[9][0] > (myLmList[0][1] - myLmList[9][1])-30:
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
    if fingers == gesture:
        return True
    else:
        return False


def gesture(d, h, g):
    fingers = d.fingersUp(h)
    if fingers == g or gesture_horizontal(h,  g):
        return True
    else:
        return False
    

def game(detector, cap):
    # state = None
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
                    if gesture(detector, hands[0],  [0, 1, 1, 0, 0]):
                        state = 3
                    elif gesture(detector, hands[0],  [1, 1, 1, 1, 1]):
                        state = 2
                    elif gesture(detector, hands[0],  [0, 0, 0, 0, 0]):
                        state = 1
                    move, comp_img = choice.hard_comp_choice(4)
                    imgBg = cvzone.overlayPNG(imgBg, comp_img, (150,200))
                    de = d.determine_winner(state, move)
                    if de != 0:
                        choice.update_plan(state)
                        if de != 1:
                            if de == 2:
                                score = [score[0], score[1]+1]
                            if de == 3:
                                score = [score[0]+1, score[1]]

        if stateResult and comp_img is not None:
            imgBg = cvzone.overlayPNG(imgBg, comp_img, (150,200))
            if hands:
                hand = hands[0]
                if gesture_horizontal(hand, [1, 0, 0, 0, 0]):
                    break

        cv2.putText(imgBg, str(score[0]), (440, 155), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 4)
        cv2.putText(imgBg, str(score[1]), (1035, 155), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 4)

        cv2.imshow("game", imgBg)
        cv2.waitKey(1)
        if hands:
            hand = hands[0]
            if gesture(detector, hands[0], [0, 1, 0, 0, 1]) and stateResult:
                initialTime = time.time()
                stateResult = False
def splash(detector, cap):
    while True:
        imgBg = cv2.imread("resources/splash.png")
        _, img = cap.read()
        img = cv2.flip(img, 180)
        hands, img = detector.findHands(img, flipType=False, draw=True)
        if hands:
            hand = hands[0]
            if gesture_horizontal(hand, [1, 0, 0, 0, 0]):
                break
        cv2.imshow("game", imgBg)
        cv2.waitKey(1)

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)

if __name__ == "__main__":
    splash(detector, cap)
    game(detector, cap)
