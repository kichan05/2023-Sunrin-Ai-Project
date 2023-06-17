import cv2
import mediapipe as mp
import glob

import numpy as np
import pandas as pd

from DataGenerator import DataGenerator

dataGenerator = DataGenerator()


count = {}

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles

result = []

for i in glob.glob("./data/*"):
    for label, fieldFile in enumerate(glob.glob(i + "/*")):
        imageFile = glob.glob(fieldFile + "/*")
        label = dataGenerator.labels()[fieldFile.split("\\")[-1]]
        l = fieldFile.split("\\")[-1]
        # print(label)

        if(l in count):
            count[l] += len(imageFile)
        else:
            count[l] = len(imageFile)

        with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
            with mp_hands.Hands(
                    static_image_mode=True,
                    max_num_hands=2,
                    min_detection_confidence=0.5) as hands:

                for idx, file in enumerate(imageFile):
                    image = cv2.imread(file)  # 이미지 불러오기
                    image = cv2.flip(image, 1)
                    image_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    results = hands.process(image_RGB)  # 관절 인식

                    cv2.imshow("Hello", image)
                    # cv2.waitKey(0)

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
                            mp_drawing_styles.get_default_hand_connections_style()
                        )

                        result.append(dataGenerator.imageGetDeg(hand_landmarks, label))

                    cv2.imshow("Hello", annotated_image)
                    if cv2.waitKey(5) & 0xFF == 27:  # 종료 버튼을 누르면 종료
                        break


print(count)

result = np.array(result)
print(result.shape)
pd.DataFrame(result).to_csv("data/data.csv", encoding="utf-8", index_label=False)