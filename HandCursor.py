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
    vSmooth = 10

    capture = cv2.VideoCapture(0)
    capture.set(3, wCam)
    capture.set(4, Hcam)
    handsense = hs.HandSense(maxHands=1)

    m = alsaaudio.Mixer()
    wScr, hScr = pyautogui.size()

    while True:
        success, img = capture.read()
        # miniImage = pyautogui.screenshot()
        handsense.detectHands(img)
        lmks, volumeBox = handsense.handLandmarks(img, draw=False)

        if len(lmks) != 0:
            xT, yT = lmks[4][1:]
            xI, yI = lmks[8][1:]
            xM, yM = lmks[12][1:]

            fingerup = handsense.fingerUp(img, draw=False)
            if fingerup[1] == 1 and fingerup.count(1) == 1:
                cv2.putText(img, 'Mouse Controller', (wCam -300, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
                cv2.rectangle(img, (mouseFrame, mouseFrame), (wCam - mouseFrame, Hcam - mouseFrame), (255, 0, 0), 3)
                xconv = np.interp(xI, (mouseFrame, wCam - mouseFrame), (0, wScr))
                yconv = np.interp(yI, (mouseFrame, Hcam - mouseFrame), (0, hScr))
                curX = prevX + (xconv - prevX) / smooth
                curY = prevY + (yconv - prevY) / smooth
                mouse.move(wScr - curX, curY)
                prevX, prevY = curX, curY


            # clicking
            if fingerup[1] == 1 and fingerup[2] == 1 and fingerup.count(1) == 2:
                cv2.putText(img, 'Mouse Controller', (wCam - 300, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
                cv2.rectangle(img, (mouseFrame, mouseFrame), (wCam - mouseFrame, Hcam - mouseFrame), (255, 0, 0), 3)
                length = handsense.fingerDistance(8, 12)
                if length < 40:
                    cv2.circle(img, (xM, yM), 20, (255, 255, 255), cv2.FILLED)
                    pyautogui.click()



            # volume setting
            if fingerup[0] == 1 and fingerup[1] == 1 and fingerup.count(1) == 2:
                areaBox = ((volumeBox[0]-volumeBox[2])*(volumeBox[1]-volumeBox[3]))//100
                print(areaBox)
                if 200<areaBox<1000:

                    cx, cy = (xT + xI) // 2, (yT + yI) // 2
                    length = handsense.fingerDistance(8, 12)
                    color1 = int(np.interp(length, [50, 250], [0, 255]))
                    cv2.putText(img, 'Volume Controller', (wCam -300, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
                    cv2.line(img, (xT, yT), (xI, yI), (0, 0, 255), 2)
                    cv2.circle(img, (cx, cy), 9, (0, 255 - color1, color1), cv2.FILLED)

                    volume = int(np.interp(length, [50, 200], [0, 100]))
                    volume = vSmooth* round(volume/vSmooth)
                    volumeBox = int(np.interp(length,[50,200],[400,150]))
                    volumePercent = int(np.interp(length,[50,200],[0,100]))
                    curV = int(prevV + (volume - prevV) / smooth)
                    m.setvolume(volume)
                    prevV = curV

                    cv2.rectangle(img,(50,150),(85,400),(255,0,0),3)
                    cv2.rectangle(img, (50, volumeBox), (85, 400), (0, 255 - color1, color1), cv2.FILLED)
                    cv2.putText(img,f'{volumePercent}%', (50,450),cv2.FONT_HERSHEY_TRIPLEX,1,(255,0,0),3)

                else:
                    cv2.putText(img, 'Bring Your hand Close', (50, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 3)


        cv2.imshow('HandSense', img)
        cv2.waitKey(1)


if __name__ == '__main__':
    activate()
