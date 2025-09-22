import cv2
import mediapipe as mp
import math
import serial
import time

ser = serial.Serial('COM3', baudrate=9600, timeout=1)

time.sleep(2)  # Ждем инициализации Arduino

capture = cv2.VideoCapture("media/videos/video_2025-09-21_14-27-40.mp4")

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

with mp_hands.Hands(min_detection_confidence=0.7,
                    min_tracking_confidence=0.7) as hands:
    while True:
        success, image = capture.read()

        if not success or cv2.waitKey(15) == 113: #113 = ord("q")
            break

        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # конвертируем изображение в rgb для работы с ним в mediapipe
        results = hands.process(imageRGB)

        if results.multi_hand_landmarks:
            for landmark in results.multi_hand_landmarks:
                coord_points = [] # список координатов указательного и большого пальца

                mp_drawing.draw_landmarks(image=image,
                                          landmark_list=landmark,
                                          connections=mp_hands.HAND_CONNECTIONS)

                for point_id, point in enumerate(landmark.landmark):
                    width, height, _ = image.shape
                    x, y = int(point.x * height), int(point.y * width)

                    if point_id == 8 or point_id == 4: # если point_id соответствует кончику указательно или большого пальца
                        coord_points.append((x, y)) # добавляем в список координатов кортеж с координатами кончика пальца
                        cv2.circle(image, (x, y), 10, (255, 255, 0), -1)

                x1, x2, y1, y2 = coord_points[0][0], coord_points[1][0], coord_points[0][1], coord_points[1][1]

                length = int(math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))) # вычесление длины между указательным и большим пальцем
                                                                                               # через теорему Пифагора
                length = max(0, min(255, length)) # приводим значение length к диапозону от 0 до 255

                ser.write(("#" + str(abs(length)) + ";").encode()) # оборачиваем строку в конструкцию: #length; и передаем ее в ардуино

        cv2.imshow("Window", image)

capture.release()
cv2.destroyAllWindows()
ser.close()
