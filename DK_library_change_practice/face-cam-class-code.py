################################################## pseudo code ###################################################

# from dynamikontrol import Module, Camera

# camera = Camera.start()           # cam_num = 0,1 기본값 0 / width 화면 최대 / height 화면 최대

# while camera.is_opened():
#     img = camera.read()        # mirror_mode = 1 기본값 1 
#     camera.show(img)           #  img / cam_name 기본값 "WebCam" / #cam_cancel_key 기본값 "esc"


# #######################################
# from dynamikontrol import Module, Camera

# camera = Camera.start()           # cam_num = 0,1 기본값 0 / width 기본값 최대값 / height 기본값 최대값 / 동영상 추가

# angle = 0 # motor current angle

# while camera.is_opened():
#     img = camera.read()        # mirror_mode = 0 or 1 기본값 1 /# 굳이,, 기본값 BGR  선택사항 RGB, GRAY, HSV 등등
    
#     c_x, c_y, w, h = camera.detect_faces(img)         # img / max_num_faces = 1, 2,, 기본값 1 / draw_boxes = 0 or 1 기본값 1

#     if c_x < 0.4:
#         angle += 1
#         module.motor.angle( angle ) 
#     elif c_x > 0.6:
#         angle -= 1
#         module.motor.angle( angle ) 

#     Camera.show(img)           #  img / cam_name 기본값 "WebCam" / #cam_cancel_key 기본값 "esc"



#####################################################################################################################

import cv2
import mediapipe
import autopy

class Camera():

    # max screen size
    wScr, hScr = autopy.screen.size()     # max_width, max_height 

    def __init__(cam_num = 0, width = wScr, height = hScr):
        
        cam_num = cam_num
        width = width
        height = height

        camera = cv2.VideoCapture(cam_num)    # web cam start

        camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
    def is_opened():
        # self.camera_open = self.camera.isOpend()
        # return self.camera_open
        results = camera.isOpened()
        return results



camera = Camera()

while camera.is_opened():
    ret, img = camera.read()
    if not ret:
        break

    img = cv2.flip(img, 1) # mirror image

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    cv2.imshow('title', img)     # img를 실시간으로 출력 / 제목은 "arg"
    if cv2.waitKey(1) == ord('q'):
        break










