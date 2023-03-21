import cv2
import cv2.aruco as aruco
import numpy as np

# Tạo dictionary cho Aruco markers
aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_1000)

# Khởi tạo bộ phát hiện Aruco
parameters = aruco.DetectorParameters_create()

# Khởi tạo đối tượng video capture để lấy khung hình từ webcam
cap = cv2.VideoCapture(1)

while True:
    # Lấy khung hình từ webcam
    ret, frame = cap.read()

    # Tìm và giải mã các marker trong khung hình
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

    # Tìm các marker từ 996 đến 999
    indices = np.where(ids == np.array([[996, 997, 998, 999]]))[1]
    if len(indices) == 4:
        # Lấy góc của các marker
        marker_corners = [corners[i][0] for i in indices]
        # Nối các góc lại với nhau
        rect = np.array([marker_corners[0][0], marker_corners[1][1], marker_corners[2][2], marker_corners[3][3]], np.float32)
        # Vẽ đường biên của hình chữ nhật
        cv2.drawContours(frame, [rect.astype(int)], -1, (0, 255, 0), 2)

    # Hiển thị khung hình kết quả
    cv2.imshow('frame', frame)

    # Nhấn phím 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
