# coding: UTF-8
import numpy as np
import cv2

# カメラからのキャプチャ指定
cap = cv2.VideoCapture(0)

# コーデックの指定
fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')

# 保存ファイルとフレームレートとサイズの指定
out = cv2.VideoWriter('output.m4v', fourcc, 30, (760, 760))

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
        # Adaptive Gaussian Thresholding
        agt = cv2.adaptiveThreshold(frame,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        cv2.imwrite("face.jpg",frame)
        cv2.imwrite("agtFace.jpg",agt)
        break

# 後始末
cap.release()
out.release()
cv2.destroyAllWindows()

