import cv2
import HandSense as hs
import numpy as np
import mouse
import pyautogui
import alsaaudio

def activate():
    wCam, Hcam = 648, 488
    mouseFrame = 100
    prevX, prevY = 0, 0
    curX, curY = 0, 0
    curV, prevV = 0, 0
    smooth = 7

    capture = cv2.VideoCapture(0)
    capture.set(3, wCam)
    capture.set(4, Hcam)
    handsense = hs.HandSense(maxHands=1)

    m = alsaaudio.Mixer()
    wScr, hScr = pyautogui.size()

    while True:
        success, img = capture.read()
        handsense.detectHands(img)
        lmks = handsense.handLandmarks(img, draw=False)
        cv2.rectangle(img, (mouseFrame, mouseFrame), (wCam - mouseFrame, Hcam - mouseFrame), (255, 0, 0), 3)
        # mouse.move(1,1)
        if len(lmks) != 0:
            xT, yT = lmks[4][1:]
            xI, yI = lmks[8][1:]
            xM, yM = lmks[12][1:]

            fingerup = handsense.fingerUp(img, draw=False)
            # print(fingerup)
            if fingerup[1] == 1 and fingerup.count(1) == 1:
                xconv = np.interp(xI, (mouseFrame, wCam - mouseFrame), (0, wScr))
                yconv = np.interp(yI, (mouseFrame, Hcam - mouseFrame), (0, hScr))
                curX = prevX + (xconv - prevX) / smooth
                curY = prevY + (yconv - prevY) / smooth
                mouse.move(wScr - curX, curY)
                prevX, prevY = curX, curY

            if fingerup[1] == 1 and fingerup[2] == 1 and fingerup.count(1) == 2:
                length = handsense.fingerDistance(8, 12)
                if length < 40:
                    cv2.circle(img, (xM, yM), 20, (255, 255, 255), cv2.FILLED)
                    pyautogui.click()

            if fingerup[0] == 1 and fingerup[1] == 1 and fingerup.count(1) == 2:
                cx, cy = (xT + xI) // 2, (yT + yI) // 2
                length = handsense.fingerDistance(8, 12)
                cv2.line(img, (xT, yT), (xI, yI), (0, 0, 255), 2)
                cv2.circle(img, (cx, cy), 9, (255, 0, 0), cv2.FILLED)
                volume = np.interp(length, [50, 250], [0, 100]).astype(int)
                curV = int(prevV + (volume - prevV) / smooth)
                print(length, curV, volume)
                m.setvolume(volume)
                prevV = curV

        cv2.imshow('HandSense', img)
        cv2.waitKey(1)



if __name__ == '__main__':
    activate()