import cv2
import numpy as np
import csv
#Load file csv

data = np.genfromtxt('data.csv', delimiter=',', dtype=str, encoding='utf-8')
ids_to_text = {int(row[0]): row[1] for row in data}

# Initialize the webcam
cap = cv2.VideoCapture()

# Initialize the ArUco dictionary
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_250)

# Initialize the ArUco parameters
aruco_params = cv2.aruco.DetectorParameters_create()

while True:
    # Đọc webcam
    ret, frame = cap.read()
    # Nhận diện thẻ marker
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=aruco_params)

    # vẽ id và text
    if ids is not None:
        ids = np.array(ids).reshape(-1, 1)
        frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Combine the text corresponding to the detected markers
        detected_text = ''.join([ids_to_text[id] for id in ids.flatten()])
        print(detected_text)
        cv2.putText(frame, detected_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('frame', frame)

    # Exit if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()