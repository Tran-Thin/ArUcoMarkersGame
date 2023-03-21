import cv2
import cv2.aruco as aruco
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib as mpl
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple
import csv
from gtts import gTTS
import os

def cv2_img_add_text(img, text, left_corner: Tuple[int, int],
                     text_rgb_color=(255, 0, 0), text_size=24,
                     font='./data/font/cmunrm.otf', offsetX=0, offsetY=0,
                     **option):
    pil_img = img
    if isinstance(pil_img, np.ndarray):
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    font_text = ImageFont.truetype(font=font, size=text_size, encoding=option.get('encoding', 'utf-8'))

    textsize = draw.textsize(text=text, font=font_text)


    textX = (img.shape[1] - (AR_SIDE + OFFSET * 2) - textsize[1]) / 2 + (AR_SIDE + OFFSET * 2) + offsetX
    textY = 15 + offsetY
    # textX = 110
    # textY = 0

    draw.text((textX, textY), text, text_rgb_color, font=font_text)
    cv2_img = cv2.cvtColor(np.asarray(pil_img), cv2.COLOR_RGB2BGR)
    if option.get('replace'):
        img[:] = cv2_img[:]
        return None
    return cv2_img


def drawImg(text, text_size, offsetX=0, offsetY=0):
    global AR_CODE, PAIRS
    img = np.zeros((H, W), np.uint8)
    img.fill(255)
    ar = aruco.drawMarker(ARUCO_DICT, AR_CODE, AR_SIDE, (OFFSET, OFFSET))

    img[OFFSET:OFFSET + ar.shape[0], OFFSET:OFFSET + ar.shape[1]] = ar
    img = cv2_img_add_text(img, text, (AR_SIDE + OFFSET * 2, 0), text_rgb_color=(0, 0, 255), text_size=text_size,
                           offsetX=offsetX, offsetY=offsetY)
    PAIRS.append((AR_CODE,text))
    cv2.imwrite("./data/Ar_characters/" + str(AR_CODE) + ".jpg", img)
    AR_CODE += 1


ARUCO_PARAMETERS = aruco.DetectorParameters_create()
ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_5X5_250)

H = 175
W = 370
OFFSET = 15
AR_SIDE = 80
AR_CODE = 11
PAIRS = []
# CAPITAL LETTER 65

listLower = [' ', 'a','à','á','ả','ã','ạ',
             'ă','ằ','ắ','ẳ','ẵ','ặ',
             'â','ầ','ấ','ẩ','ẫ','ậ',
             'b','c','d',
             'đ',
             'e','è','é','ẻ','ẽ','ẹ',
             'ê','ề','ế','ể','ễ','ệ',
             'g','h',
             'i','ì','í','ỉ','ĩ','ị',
             'k','l','m','n',
             'o','ò','ó','ỏ','õ','ọ',
             'ô','ồ','ố','ổ','ỗ','ộ',
             'ơ','ờ','ớ','ở','ỡ','ợ',
             'p','q','r','s','t',
             'u','ù','ú','ủ','ũ','ụ',
             'ư','ừ','ứ','ử','ữ','ự',
             'v','x',
             'y','ỳ','ý','ỷ','ỹ','ỵ']

ghep = ['ch', 'gh', 'gi', 'ng', 'nh', 'ngh', 'kh', 'ph', 'qu', 'th', 'tr']

for i in listLower:
    text = i
    drawImg(text, 150, offsetY=-20)

for i in ghep:
    text = i
    drawImg(text, 160, offsetX=-20, offsetY=-20)

for i in range(12):
    # OFF CARD
    ar = aruco.drawMarker(ARUCO_DICT, i, 256, (OFFSET, OFFSET))
    cv2.imwrite('./data/Ar_characters/' + str(i) + '.jpg', ar)

with open('data.csv', 'w', newline='', encoding='utf-8') as out:
    csv_out = csv.writer(out)
    #csv_out.writerow(['code', 'text'])
    for row in PAIRS:
        csv_out.writerow(row)

# Các ký tự trong bảng chữ cái tiếng Việt
vietnamese_alphabet = " ,a,à,á,ả,ã,ạ,ă,ằ,ắ,ẳ,ẵ,ặ,â,ầ,ấ,ẩ,ẫ,ậ,b,c,d,đ,e,è,é,ẻ,ẽ,ẹ,ê,ề,ế,ể,ễ,ệ,g,h,i,ì,í,ỉ,ĩ,ị,k,l,m,n,o,ò,ó,ỏ,õ,ọ,ô,ồ,ố,ổ,ỗ,ộ,ơ,ờ,ớ,ở,ỡ,ợ,p,q,r,s,t,u,ù,ú,ủ,ũ,ụ,ư,ừ,ứ,ử,ữ,ự,v,x,y,ỳ,ý,ỷ,ỹ,ỵ,"

# Chuyển các ký tự thành một danh sách
characters = vietnamese_alphabet.split(',')
i=12
# Vòng lặp để tạo file âm thanh cho từng chữ cái
for character in characters:
    # Tạo đối tượng gTTS với ngôn ngữ là tiếng Việt
    tts = gTTS(text=character, lang='vi')
    # Lưu file âm thanh với tên tương ứng với chữ cái
    tts.save('./data/sound_abcTV/'+str(i)+'.mp3'.format(character))
    i+=1
