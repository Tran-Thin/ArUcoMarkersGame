import os
import cv2
import keyboard
import numpy as np
import playsound
import pygame
from gtts import gTTS
import random
import time

# Load the CSV data
data = np.genfromtxt('data.csv', delimiter=',', dtype=str, encoding='utf-8')
ids_to_text = {int(row[0]): row[1] for row in data}

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize the ArUco dictionary
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_250)

# Initialize the ArUco parameters
aruco_params = cv2.aruco.DetectorParameters_create()

def generate_speech(text):  # Chuyển số điểm của người chơi thành giọng nói
    output = gTTS(text,lang="vi", slow=False)
    output.save("./data/sound/PointTemp.mp3")
    play('point')

def read_images(dir_path):  # Tạo list chứa các ảnh trong file theo đường dẫn
    img_list = []
    files = os.listdir(dir_path)
    for file in files:
        img_path = os.path.join(dir_path, file)
        image = cv2.imread(img_path)
        img_list.append(image)
    return img_list

def delay(t):
    text = "Bạn có "+ str(t) +" giây để sắp xếp chữ " + answer
    play_text(text)
    time.sleep(t)

IMAGES_LIST = read_images(r'.\data\image_animals')
TOTALTIME = 30 * 120    # 120s
CHECK_FREQ = 30
CHECK_AGAIN_TIME = 30 * 5
REMINDTIME = 30 * 3

#Variables
GameState = 0   # 0=off, 1=start, 2=play, 3=final, 4=error
frameCount = 0
point = 0
timeIdx = 0
timeCheckIdx = 0
remindIdx = 0
questionID = []
checkStatus = 0
markerDetected = set()
answerStatus = 0

soundDict = {
    'intro':'./data/sound/Intro.mp3',
    'start':'./data/sound/Start.mp3',
    'question':'./data/sound/Question_2.mp3',
    'tenSec':'./data/sound/TenSec.mp3',
    'fiveSec':'./data/sound/FiveSec.mp3',
    'timeUp':'./data/sound/Timeup.mp3',
    '3Only':'./data/sound/3Only.mp3',
    'missing1':'./data/sound/missing1.mp3',
    'missing2':'./data/sound/missing2.mp3',
    '1of3':'./data/sound/1of3.mp3',
    '2of3':'./data/sound/2of3.mp3',
    '3of3':'./data/sound/3of3.mp3',
    'false':'./data/sound/False.mp3',
    'end':'./data/sound/End.mp3',
    'cancel':'./data/sound/Cancel.mp3',
    'wrongType':'./data/sound/wrongType.mp3',
    'point':'./data/sound/PointTemp.mp3',
    'error':'./data/sound/Error.mp3',
}



def play_text(text):
    output = gTTS(text, lang="vi", slow=False)
    output.save("./data/sound/text.mp3")
    playsound.playsound("./data/sound/text.mp3")
    os.remove("./data/sound/text.mp3")

def play(sound):    # Chạy các file ấm thanh
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(soundDict[sound])
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.quit()

play('intro')
solan = 3
while True:

    # Đọc webcam
    ret, frame = cap.read()
    # Nhận diện thẻ marker
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=aruco_params)
    markerDetected = set()
    if corners:
        for id in ids:
            markerDetected.add(id[0])
    # gamestate 0
    if GameState == 0:
        point = 0  # reset point
        if keyboard.is_pressed('s') or 0 in markerDetected:
            GameState = 1
            play('start')
        timeIdx = 0
        lanchoi = 3
    # gamestate 1
    elif GameState == 1:
        lanchoi -= 1

        if lanchoi > 0:
            play_text('Lần chơi thứ ' + str(3 - lanchoi))
            # Câu hỏi
            # list chuỗi ký tự
            char_list = ["học",'việt', 'việt nam', 'nam']
            a = ['học', 'học sinh', 'trường', 'trường học', 'lớp', 'lớp học', 'con vật', 'con mèo',
                         'quần áo', 'máy tính', 'vở', 'bút', 'học tập', 'hộp bút', 'sân trường', 'con gà',
                         'hoa', 'bông hoa', 'việt nam', 'điện thoại', 'bố', 'mẹ', 'ông bà', 'bố mẹ']

            # chọn ngẫu nhiên một chuỗi từ list
            answer = random.choice(char_list)
            ques = 'Bạn hãy ghép chữ ' + answer
            print(ques)
            play_text(ques)
            delay(7)
            GameState = 2
        else: GameState = 3

    # gamestate 2
    elif GameState == 2:
        timeIdx += 1
        if TOTALTIME - timeIdx == 30 * 10:  # còn 10s
            play('tenSec')
        if TOTALTIME - timeIdx == 30 * 5:  # còn 5s
            play('fiveSec')
        if TOTALTIME - timeIdx == 0:  # hết giờ
            play('timeUp')
            GameState = 3

        if frameCount % CHECK_FREQ == 0:
            if 0 in markerDetected or (1 in markerDetected and len(markerDetected) > 1):
                play('wrongType')
                continue
            if keyboard.is_pressed('c') or (32 in markerDetected and len(markerDetected) == 1):
                play('cancel')
                GameState = 0
                continue

            # vẽ id và text
            array = []
            if ids is not None:
                ids = np.array(ids).reshape(-1, 1)
                frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)
                for id in range(len(ids)):
                    # Lấy tọa độ góc trái của các marker ArUco
                    corners_left_top = int(corners[id][0][0][0])
                    array.append(corners_left_top)
                sorted_ids = [x[1] for x in sorted(zip(array, ids), key=lambda pair: pair[0])]
                # Combine the text corresponding to the detected markers
                detected_text = ''
                for id in sorted_ids:
                    if id == 11:
                        detected_text = detected_text + ' '
                    elif id == 1:
                        GameState = 3
                        break
                    else:
                        detected_text = detected_text + ids_to_text[int(id)]
                # detected_text = ''.join([ids_to_text[int(id)] for id in sorted_ids])
                detected_text = detected_text.encode('utf-8').decode('utf-8')
                print(detected_text)
                cv2.putText(frame, detected_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Speak the detected_text
                noi = "Câu trả lời của bạn là: " + detected_text
                play_text(noi)

                # thông báo
                if detected_text == answer:
                    dung = "Bạn đúng rồi, bạn được cộng 50 điểm"
                    play_text(dung)
                    point += 50
                    GameState = 1
                    solan = 2
                else:
                    if solan > 0:
                        sai = "Bạn sai rồi, bạn còn " +str(solan) +' lần thử lại'
                        play_text(sai)
                        delay(7)
                        solan -= 1
                    else:
                        thua = "Bạn thua rồi, bạn bị trừ 25 điểm"
                        play_text(thua)
                        point -= 25
                        solan = 3
                        GameState = 1
            if checkStatus == 1:  # Thời gian sửa
                timeCheckIdx += 1
                if CHECK_AGAIN_TIME - timeCheckIdx == 0:
                    checkStatus = 0
                    timeCheckIdx = 0

        # gamestate 3
    elif GameState == 3:
        # thông báo điểm
        # playsound
        play('end')
        generate_speech(str(point))
        GameState = 0

        # gamestate 4
    elif GameState == 4:
        play('error')

        if keyboard.is_pressed('c') or 1 in markerDetected:
            play('cancel')
            GameState = 0

    # Display the frame
    cv2.imshow('frame', frame)

    # Exit if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()