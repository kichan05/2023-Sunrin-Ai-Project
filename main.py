import cv2 as cv
import mediapipe as mp
from DataGenerator import DataGenerator

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles

dataGenerator = DataGenerator()


cam = cv.VideoCapture(0)  # PC에 연결된 카메라를 연결 한다.

result = []


with mp_hands.Hands(
        max_num_hands=1,  # 인식할 손의 촤대 개수
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cam.isOpened():  # 캠이 켜져있는 동안 무한 반복
        success, img = cam.read()  # 캠의 이미지를 가져온다.
        height, width, _ = img.shape

        if (not success):  # 성공하지 않았으면
            continue

        img = cv.flip(img, 1)  # 이미지를 좌우 반전을 시켜준다.
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)  # 채널을 BGR에서 RGB로 변경 시켜준다.

        results = hands.process(img)  # 이미지의 손을 인식 한다.

        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        # 다시 RGB 채널을 BGR 채널로 변경 시켜준다.

        if (results.multi_hand_landmarks):
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )  # 이미지지에 손의 마디를 표시한다

                degList = []

                for n, i in enumerate(dataGenerator.getFindDegList()):
                    p1 = hand_landmarks.landmark[i[0]]
                    p2 = hand_landmarks.landmark[i[1]]
                    p3 = hand_landmarks.landmark[i[2]]

                    deg = dataGenerator.getDeg(p1, p2, p3)

                    font = cv.FONT_HERSHEY_PLAIN

                    x = int(p2.x * width)
                    y = int(p2.y * height)

                    img = cv.putText(img, str(deg), (x, y), font, 1, (255, 255, 255), 1, cv.LINE_AA)

                    break


                    # degList.append(deg)

                # result.append(degList)

        cv.imshow("캠", img)
        # 만든 이미지를 화면에 보여준다.

        if cv.waitKey(5) & 0xFF == 27:  # 종료 버튼을 누르면 종료
            break

cam.release()
