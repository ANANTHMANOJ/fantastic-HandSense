import cv2
import mediapipe as mp
import time
import math



class HandSense:
    def __init__(self,img_mode = False,maxHands = 2, min_detect_conf = 0.5, min_track_conf = 0.5):
        self.img_mode =img_mode
        self.maxHands =maxHands
        self.min_detect_conf =min_detect_conf
        self.min_track_conf =min_track_conf
        self.mpHands = mp.solutions.hands
        self.mpH = self.mpHands.Hands( self.img_mode,self.maxHands,
                                  self.min_detect_conf,self.min_track_conf)
        self.mpLandMarks = mp.solutions.drawing_utils

    def detectHands(self,img, draw = True):
        RGB_Image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.result_image = self.mpH.process(RGB_Image)

        if self.result_image.multi_hand_landmarks:
            for HLandMark in self.result_image.multi_hand_landmarks:
                if draw:
                    self.mpLandMarks.draw_landmarks(img,HLandMark, self.mpHands.HAND_CONNECTIONS)
        return img

    def handLandmarks(self, img, handNo = 0, draw=True):
        self.hlm =[]
        xList =[]
        yList =[]
        boundBox =[]
        if self.result_image.multi_hand_landmarks:
            hand = self.result_image.multi_hand_landmarks[handNo]
            for id, lm in enumerate(hand.landmark):
                h, w, channel = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.hlm.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 12, (255, 255, 0), cv2.FILLED)
            xmin,xmax =min(xList),max(xList)
            ymin, ymax = min(xList), max(xList)
            boundBox = xmin,ymin,xmax,ymax
        return self.hlm,boundBox

    def fingerUp(self,img, draw = True):
        lmks,_ = self.handLandmarks(img, draw= draw)
        self.tipIndex= [4,8,12,16,20]
        self.fingerup = []
        if len(lmks) != 0:
            if lmks[4][1] > lmks[3][1]:
                self.fingerup.append(1)
            else:
                self.fingerup.append(0)
            for landmarks in self.tipIndex[1:]:
                if lmks[landmarks][2] < lmks[landmarks-2][2]:
                    self.fingerup.append(1)
                else:
                    self.fingerup.append(0)
        return self.fingerup

    def fingerDistance(self,p1,p2):
        x1,y1 = self.hlm[p1][1:]
        x2,y2 = self.hlm[p2][1:]
        length = math.hypot((x2-x1),(y2-y1))
        return length







def main():
    ctime = 0
    ptime = 0
    capture = cv2.VideoCapture(0)
    handsense = HandSense()
    while True:
        success, img = capture.read()
        img = handsense.detectHands(img)
        lst,_ = handsense.handLandmarks(img)
        if len(lst)!=0:
            print(lst[4])
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
        cv2.imshow("webcam", img)
        cv2.waitKey(1)



if __name__ == '__main__':
    main()