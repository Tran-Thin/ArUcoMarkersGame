import cv2 as cv
from cv2 import aruco
import numpy as np
import os
import pandas as pd
from playsound import playsound
import pyglet

def image_augmentation(frame, src_image, dst_points):
    src_h, src_w = src_image.shape[:2]
    frame_h, frame_w = frame.shape[:2]
    mask = np.zeros((frame_h, frame_w), dtype=np.uint8)
    src_points = np.array([[0, 0], [src_w, 0], [src_w, src_h], [0, src_h]])
    H, _ = cv.findHomography(srcPoints=src_points, dstPoints=dst_points)
    warp_image = cv.warpPerspective(src_image, H, (frame_w, frame_h))
    cv.imshow("warp image", warp_image)
    cv.fillConvexPoly(mask, dst_points, 255)
    results = cv.bitwise_and(warp_image, warp_image, frame, mask=mask)

#def play_sound(soundids):
    #pyglet.media.load()

def read_images(dir_path):
    img_list = []
    files = os.listdir(dir_path)
    for file in files:
        img_path = os.path.join(dir_path, file)
        image = cv.imread(img_path)
        img_list.append(image)
    return img_list

'''
def read_audio(dir_path):
    audio_list = []
    files = os.listdir(dir_path)
    for file in files:
        audio_path = os.path.join(dir_path, file)
        audio, fs = librosa.load(audio_path, sr = None)
        audio_list.append(audio)
    return audio_list
'''

marker_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)

param_markers = aruco.DetectorParameters_create()

images_list = read_images(r'E:\PycharmProjects\DA3\data\image_animals')


#print(sound_list)
cap = cv.VideoCapture(1)

#df = pd.read_csv('sound.csv')

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers)
    if marker_corners:
        if marker_corners:
            for ids, corners in zip(marker_IDs, marker_corners):
                corners = corners.reshape(4, 2)
                corners = corners.astype(int)
                if ids[0] <= 30:
                    print(ids[0])
                    image_augmentation(frame, images_list[ids[0]], corners)
                    link = r'.\data\sound_animals\s' + str(ids[0]) + '.mp3'
                    playsound(link)
                else:
                    image_augmentation(frame, images_list[0], corners)
            # print(ids, "  ", corners)
    cv.imshow("frame", frame)
    key = cv.waitKey(1)
    if key == ord("q"):
        break
cap.release()
cv.destroyAllWindows()