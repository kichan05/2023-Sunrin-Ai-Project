import numpy as np
class DataGenerator:
    def __int__(self):
        pass

    def getFindDegList(self):
        return [
            [4, 3, 2],
            [3, 2, 1],

            [8, 7, 6],
            [7, 6, 5],
            [6, 5, 0],

            [12, 11, 10],
            [11, 10, 9],

            [16, 15, 14],
            [15, 14, 13],

            [20, 19, 18],
            [19, 18, 17],
            [18, 17, 0],

            [6, 5, 9],
            [10, 9, 5],

            [14, 13, 9],
            [18, 17, 13],
        ]

    def getLabel(self, index):
        return list(self.labels().keys())[index]

    def labels(self):
        return {
            "보자기": 0,
            "바위": 1,
            "가위": 2
        }

    def imageGetDeg(self, hand_landmarks, label = None):
        degList = []

        for n, i in enumerate(self.getFindDegList()):
            p1 = hand_landmarks.landmark[i[0]]
            p2 = hand_landmarks.landmark[i[1]]
            p3 = hand_landmarks.landmark[i[2]]

            deg = self.getDeg(p1, p2, p3)

            degList.append(deg)

        if (label != None):
            degList.append(label)

        return degList

    def getDeg(self, p1, p2, p3):
        A = self.landmarkToNparray(p1)
        B = self.landmarkToNparray(p2)
        C = self.landmarkToNparray(p3)

        AB = B - A
        BC = C - B

        dot = np.dot(AB, BC)

        normAB = np.linalg.norm(AB)
        normBC = np.linalg.norm(BC)
        angle_rad = np.arccos(dot / (normAB * normBC))

        angle_deg = np.degrees(angle_rad)

        return min(angle_deg, 180 - angle_deg)


    def landmarkToNparray(self, landmark):
        array = np.array([landmark.x, landmark.y, landmark.z])
        return array
