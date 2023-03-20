import cv2 as cv
import time
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cam = cv.VideoCapture(0)

with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cam.isOpened():
        success, img = cam.read()

        if (not success):
            continue

        img = cv.flip(img, 1)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        results = hands.process(img)

        results_object = face_mesh.process(img)

        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

        # cv.imshow("Iamge", img)

        if (results.multi_hand_landmarks):
            for hand_landmarks in results.multi_hand_landmarks:
                print(hand_landmarks)
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv.imshow("Image", img)

        # time.sleep(1)

        cv.waitKey(0)

cam.release()
