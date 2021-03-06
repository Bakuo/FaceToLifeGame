# coding: UTF-8
import numpy as np
import cv2

# カメラからのキャプチャ指定
cap = cv2.VideoCapture(0)

# コーデックの指定
fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')

mirror = True
size = (800, 600)

# カメラオープン中はずっと処理する
while(cap.isOpened()):

    # キャプチャ画像を取り出す
    ret, frame = cap.read()

    # データがなければ抜ける
    if ret == False:
        break

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    if mirror is True:
        frame = frame[:,::-1]

    if size is not None and len(size) == 2:
        frame = cv2.resize(frame, size)


    # 画像を画面に出力する
    cv2.imshow('frame', frame)

    # "q"が押されたら抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite("face.jpg",frame)
        break

# 後始末
cap.release()
cv2.destroyAllWindows()

