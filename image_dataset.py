import cv2
import mediapipe as mp
import glob

imageFile = glob.glob("./data/image dataset 1/*")

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles


for idx, fieldFile in enumerate(imageFile):
    imageFile = glob.glob(fieldFile + "/*")

    with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        with mp_hands.Hands(
                static_image_mode=True,
                max_num_hands=2,
                min_detection_confidence=0.5) as hands:

            for idx, file in enumerate(imageFile):
                image = cv2.imread(file) # 이미지 불러오기
                image = cv2.flip(image, 1)
                image_RGB= cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image_RGB) # 관절 인식

                cv2.imshow("Hello", image)
                cv2.waitKey(0)

                if not results.multi_hand_landmarks:
                    continue

                # image_height, image_width, _ = image.shape
                annotated_image = image.copy()
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        annotated_image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

                    print(hand_landmarks.landmark[0])

                cv2.imshow("Hello", annotated_image)
                cv2.waitKey(0)

                break