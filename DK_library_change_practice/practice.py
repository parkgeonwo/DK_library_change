
###################################### 

# import Camera_module

# camera = Camera_module.Camera()
# # camera = Camera_module.Camera(path="/home/matrix/Desktop/code/video2.mp4")

# while camera.is_opened(): 
#     frame = camera.get_frame()
#     camera.show(frame)


############################################

from dynamikontrol import Module
from Camera import Camera
# from dynamikontrol_toolkit import Camera
import time
import mediapipe as mp
import cv2


# module = Module()
# # camera = Camera(path='/home/matrix/Desktop/code/DK_library_change/video2.mp4')
camera = Camera()
# pTime = 0

count = 0

while camera.is_opened():
    frame = camera.get_frame()

    body = camera.detect_body(frame)
    camera.show_text(50,30,"black",count)

    if body:
        print(body.count_squat())

    # cTime = time.time()
    # fps = 1 / (cTime-pTime)
    # pTime = cTime
    # print(fps)

    # face = camera.detect_face(frame)
    # hand = camera.detect_hand(frame)

    camera.show(frame)

# module.disconnect()



