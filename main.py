import time

from DataGenerator import DataGenerator
import cv2 as cv
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
from PIL import ImageFont, Image, ImageDraw
import random
from datetime import datetime

import GameUi

GameUi.show_logo()

dg = DataGenerator()
model2 = load_model("./model/model2.hdf5")

cam = cv.VideoCapture(0)
cv.namedWindow("webcam", cv.WND_PROP_FULLSCREEN)
cv.setWindowProperty("webcam", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles

gameCount = 0

def gesturesPredict(landmark):
    deg = dg.imageGetDeg(landmark)
    predict = model2.predict([deg], verbose=None)[0]
    return np.argmax(predict)

def gameInit():
    global startTime, userGestures, userLabel, aiGestures, aiLabel, gameCount

    startTime = datetime.now()

    userGestures = None
    aiGestures = random.randrange(0, 2)

    gameCount += 1


if __name__ == '__main__':
    with mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:

        while True:
            gameInit()

            while cam.isOpened():
                success, img = cam.read()
                height, width, _ = img.shape

                if (not success):
                    continue

                img = cv.flip(img, 1)
                img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
                results = hands.process(img_rgb)

                if (results.multi_hand_landmarks != None):
                    hand_landmarks = results.multi_hand_landmarks[0]
                    mp_drawing.draw_landmarks(
                        img,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )

                    gestures = gesturesPredict(hand_landmarks)
                    label = dg.getLabel(gestures)
                    img = GameUi.show_header_pil(f"현재 손동작 : {label}", img)
                else:
                    gestures = None
                    img = GameUi.show_header_pil(f"현재 손동작 : 없음", img)

                currentTime = datetime.now()
                timeDiff = currentTime - startTime

                if (timeDiff.seconds < 1):
                    if (gameCount == 1):
                        img = GameUi.show_title_pil("[시작]", (0, 0, 0), img)
                    else:
                        img = GameUi.show_title_pil("[다시 시작]", (0, 255, 0), img)

                elif(timeDiff.seconds < 3):
                    img = GameUi.show_title_pil("안 내 면", (0, 0, 0), img)

                elif(timeDiff.seconds < 5):
                    img = GameUi.show_title_pil("진다", (0, 0, 0), img)

                elif(timeDiff.seconds < 7):
                    img = GameUi.show_title_pil(f"가위 바위 보!!!!!!!", (0, 0, 0), img)

                elif (timeDiff.seconds < 10):
                    if(gestures == None): #사용자가 낸게 없는 경우
                        break

                    else: # 사용자가 낸게 있는 경우
                        if(userGestures == None):
                            userGestures = gestures

                        img = GameUi.show_title_pil(f"사용자 : {dg.getLabel(userGestures)}", (0, 255, 0), img)

                elif (timeDiff.seconds < 13):
                    img = GameUi.show_title_pil(f"인공지능 : {dg.getLabel(aiGestures)}", (0, 255, 0), img)

                elif (timeDiff.seconds < 16):
                    if aiGestures == userGestures:
                        img = GameUi.show_title_pil("무승부", (0, 0, 0), img)
                    elif (aiGestures - userGestures) % 3 == 1:
                        img = GameUi.show_title_pil("승리!!!", (255, 0, 0), img)
                    else:
                        img = GameUi.show_title_pil("패배", (0, 0, 255), img)
                else:
                    break

                cv.imshow("webcam", img)

                if cv.waitKey(1) & 0xff == 27: # esc키 누르면 종료
                    print("종료")
                    exit(0)