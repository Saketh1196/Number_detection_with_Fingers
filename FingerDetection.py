import cv2
import os
import time
import HandTrackingModule as htm

WCam, HCam = 1080, 780

cap = cv2.VideoCapture(0)
cap.set(3, WCam)
cap.set(4, HCam)

folderPath = "Fingers"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    #print(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))
pTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipIDs = [4, 8, 12, 16, 20]
while True:

    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    #print(lmList)

    if len(lmList)!=0:
        fingers = []

        #Thumb
        if lmList[tipIDs[0]][1] > lmList[tipIDs[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #Fingers
        for id in range(1,5):
            if lmList[tipIDs[id]][2] < lmList[tipIDs[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        #print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)

        h, w, c = overlayList[0].shape
        img[0:h, 0:w] = overlayList[totalFingers-1]

        cv2.rectangle(img, (20,250), (170,450), (0,255,0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45,400), cv2.FONT_HERSHEY_PLAIN, 10, (255,0,110), 10)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (300,70), cv2.FONT_ITALIC, 2, (255,255,0), 4)

    cv2.imshow("Image",img)
    cv2.waitKey(1)
