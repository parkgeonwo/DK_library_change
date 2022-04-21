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


# 변수 받기 흐르기
# set / get 해보고
# 흐르게 

#####################################################################################################################

import cv2
import mediapipe as mp
import autopy

class Camera():

    # max screen size
    wScr, hScr = autopy.screen.size()     # max_width, max_height 

    def __init__(self, cam_num = 0, width = wScr, height = hScr):
        
        self.cam_num = cam_num
        self.width = width
        self.height = height

        self.camera = cv2.VideoCapture(cam_num)    # web cam start

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)    # web cam width control
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)   # web cam height control

        ### mideapipe drawing
        self.mp_drawing = mp.solutions.drawing_utils             # mediapipe drawing

        ### mediapipe face_detection
        self.mp_face_detection = mp.solutions.face_detection   
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.5)
        
    def start(self):
        while camera.is_opened():
            frame, img = camera.read()
            if not frame:
                break
            return img


    def is_opened(self):

        return self.camera.isOpened()

    def read(self, mirror_mode = 1):
        
        frame, img = self.camera.read()
        img = cv2.flip(img,mirror_mode)    # mirror_mode = 1

        return frame, img

    def show(self, img, cam_name = "Web Cam"):

        cv2.imshow(cam_name, img)
    
    def cancel(self):

        return cv2.waitKey(1) & 0xFF == 27   # cancel_key : esc

    def detect_faces(self, img ):     # max_num_faces = 1 , draw_boxes = 1

        results = self.face_detection.process(img)       

        if results.detections:
            for detection in results.detections:
                self.mp_drawing.draw_detection(img, detection)

                x1 = detection.location_data.relative_bounding_box.xmin # left
                x2 = x1 + detection.location_data.relative_bounding_box.width # right

                y1 = detection.location_data.relative_bounding_box.ymin # top
                y2 = y1 + detection.location_data.relative_bounding_box.height # bottom

                c_x = (x1 + x2) / 2 # horizontal center of the face
                c_y = (y1 + y2) / 2 # vertical center of the face
                w = detection.location_data.relative_bounding_box.width      # box width
                h = detection.location_data.relative_bounding_box.height     # box-height
        
        return c_x, c_y, w, h





######################################

 
camera = Camera()

# while camera.is_opened():
#     frame, img = camera.read()
#     if not frame:
#         break   

#     camera.show(img)
#     if camera.cancel():
#         break

img = camera.start()
camera.show(img)


######################################


# camera = Camera()           

# angle = 0 

# while camera.is_opened():
#     frame, img = camera.read()
#     if not frame:
#         break   

#     c_x, c_y, w, h = camera.detect_faces(img)         

#     print(c_x, c_y, w, h)

#     camera.show(img)

#     if camera.cancel():
#         break

######################################















