# -*- coding: utf-8 -*-
"""Untitled31.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tOYNXHhIObo93GduxR-KfRBqrilfZ0Wq
"""

import cv2
import sys
from tensorflow.keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
from google.colab.patches import cv2_imshow

# Loading  the pre-trained model
model = load_model('model.h5')

img_width, img_height = 150, 150

cascade_path = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)


if face_cascade.empty():
    print(f"Error: Unable to load the face cascade from {cascade_path}")
    sys.exit(1)


video_path = 'video.mp4'
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"Error: Unable to open video file {video_path}")
    sys.exit(1)

img_count_full = 0


font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
thickness = 2

while True:
    img_count_full += 1
    response, color_img = cap.read()

    if not response:
        break

    scale = 50
    width = int(color_img.shape[1] * scale / 100)
    height = int(color_img.shape[0] * scale / 100)
    dim = (width, height)

    color_img = cv2.resize(color_img, dim, interpolation=cv2.INTER_AREA)
    gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_img, 1.1, 6)

    img_count = 0
    for (x, y, w, h) in faces:
        org = (x - 10, y - 10)
        img_count += 1
        color_face = color_img[y:y+h, x:x+w]
        face_filename = f'input/{img_count_full}{img_count}face.jpg'
        cv2.imwrite(face_filename, color_face)

        img = load_img(face_filename, target_size=(img_width, img_height))
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)
        prediction = model.predict(img)

        class_label = "Mask" if prediction[0][0] == 0 else "No Mask"
        color = (255, 0, 0) if prediction[0][0] == 0 else (0, 255, 0)

        cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 0, 255), 3)
        cv2.putText(color_img, class_label, org, font, fontScale, color, thickness, cv2.LINE_AA)

    cv2_imshow(color_img)  # Using cv2_imshow() to display the image in Colab
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()