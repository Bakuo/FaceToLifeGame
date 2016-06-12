# -*- coding: utf-8 -*-
import cv2

cascade_path = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"

image_path = "face.jpg"

color = (255, 5, 5) # kinda red

# Loading file
image = cv2.imread(image_path)

cascade = cv2.CascadeClassifier(cascade_path)

facerect = cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=1, minSize=(1,1))

isFace = True

print "face rectangle"
print facerect

if len(facerect) > 0:
    rectSize = []
    for rect in facerect:
        rectSize.append(rect[2]*rect[3])
    print rectSize
    faceIndex = rectSize.index(max(rectSize))
    print faceIndex
    detectedFace = facerect[faceIndex]
    cv2.rectangle(image, tuple(detectedFace[0:2]),tuple(detectedFace[0:2]+detectedFace[2:4]), color, thickness=2)
    cv2.imwrite("detected.jpg",image)
else:
    isFace = False
    print("no face")

