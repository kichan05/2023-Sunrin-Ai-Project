import time

from DataGenerator import DataGenerator
import cv2 as cv
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
import random
from datetime import datetime

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

def showTitle(text, color):
    global width, height, img
    text_size, _ = cv.getTextSize(text, cv.FONT_HERSHEY_DUPLEX, 2, cv.LINE_AA)

    box_width = text_size[0] + 10
    box_height = text_size[1] + 10

    box_x = (img.shape[1] - box_width) // 2
    box_y = (img.shape[0] - box_height) // 2
    cv.rectangle(img, (box_x, box_y), (box_x + box_width, box_y + box_height), (255, 255, 255), -1)

    text_x = (width - text_size[0]) // 2
    text_y = (height + text_size[1]) // 2
    cv.putText(img, text, (text_x, text_y), cv.FONT_HERSHEY_DUPLEX, 2, color, 1, cv.LINE_AA)


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
                img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
                results = hands.process(img)
                img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

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
                    img = cv.putText(img, label, (0, 50), cv.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 1, cv.LINE_AA)
                else:
                    gestures = None

                currentTime = datetime.now()
                timeDiff = currentTime - startTime

                if (timeDiff.seconds < 1):
                    if (gameCount == 1):
                        showTitle("[START]", (0, 0, 0))
                    else:
                        showTitle("[RESTART]", (0, 255, 0))

                if (timeDiff.seconds < 2):
                    pass

                elif (timeDiff.seconds < 7):
                    showTitle(str(7 - timeDiff.seconds), (0, 0, 0))

                elif (timeDiff.seconds < 9):
                    if(gestures == None): #사용자가 낸게 없는 경우
                        break

                    else: # 사용자가 낸게 있는 경우
                        userGestures = gestures
                        showTitle(f"Player : {dg.getLabel(userGestures)}", (0, 0, 0))


                elif (timeDiff.seconds < 10):
                    showTitle(f"Ai : {dg.getLabel(aiGestures)}", (0, 0, 0))

                elif (timeDiff.seconds < 14):
                    if aiGestures == userGestures:
                        showTitle("DRAW", (0, 0, 0))
                    elif (aiGestures - userGestures) % 3 == 1:
                        showTitle("WIN", (255, 0, 0))
                    else:
                        showTitle("DEFEAT", (0, 0, 255))
                else:
                    break

                cv.imshow("webcam", img)

                if cv.waitKey(1) & 0xFF == ord('q'): # q누르면 종료
                    exit(0)