import cv2
import mediapipe as mp
from numpy import mirr

class Face():
    def __init__(self, x1, y1, width, height):
        self.x1 = x1
        self.y1 = y1
        self.width = width
        self.height = height
        self.x2 = self.x1 + width
        self.y2 = self.y1 + height

        self.c_x = (self.x1 + self.x2) / 2
        self.c_y = (self.y1 + self.y2) / 2

    def __repr__(self):   # Face() 객체의 인자를 보기좋게 만들 수 있음.
        return 'x1: %.2f, y1: %.2f, width: %.2f, height: %.2f' % (self.c_x, self.c_y, self.width, self.height)



class Camera():

    def __init__(self, cam_num = 0, width = None, height = None ):

        self.cam_num = cam_num

        self.camera = cv2.VideoCapture(cam_num)    # web cam start

        if width is None or height is None:     
            self.width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))      # camera default frame size 
            self.height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        else:
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        ### mediapipe face_detection
        self.mp_face_detection = mp.solutions.face_detection   
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.5)
        
    def is_opened(self, window_close_key = 27): # window_close_key = "string" default : esc
        if not self.camera.isOpened():          # self.camera.isOpened가 False 라면
            return False

        ret, img = self.camera.read()

        if not ret:     # 더이상 받을 ret이 없을때
            return False

        if len(str(window_close_key)) == 1:
            window_close_key = ord(window_close_key)
            print(window_close_key)
            if cv2.waitKey(30) & 0xFF == window_close_key:
                return False
        else:
            if cv2.waitKey(30) & 0xFF == window_close_key:
                return False

        self.frame = img

        return True

    def get_frame(self, mirror_mode = True):   # mirror_mode default : True 

        if mirror_mode is True:
            self.frame = cv2.flip(self.frame, 1)
        elif mirror_mode is False:
            pass

        return self.frame

    def show(self, frame, window_name = "Web Cam"):
        return cv2.imshow(window_name, frame)

    def draw_faces(self, faces):   # face 여러개 그려주는 method
        for face in faces:
            cv2.rectangle(self.frame, (int(round(self.width*face.x1)), int(round(self.height*face.y1))),
                    (int(round(self.width*face.x2)),int(round(self.height*face.y2))),
                    (0,255,0), 3)     # face 그리기

    def detect_face(self, frame, draw_box = True):      # 얼굴한개 찾기
        return self.detect_faces(frame, max_num_faces = 1, draw_boxes = draw_box )

    def detect_faces(self, frame, max_num_faces = 99, draw_boxes = True): # max_num_faces defalut : 99,  mediapipe default : 1  / draw_boxes default : True
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(frame_rgb)

        faces = []    # return 할 list

        if results.detections:
            for detection in results.detections:
                w = detection.location_data.relative_bounding_box.width      # box width
                h = detection.location_data.relative_bounding_box.height     # box height

                x1 = detection.location_data.relative_bounding_box.xmin # left
                y1 = detection.location_data.relative_bounding_box.ymin # top

                faces.append( Face(x1, y1, w, h) )

        faces = sorted(faces, key=lambda face: face.height, reverse=True)  # faces에서 face를 정렬할건데 기준은 face.height이다.
        faces = faces[:max_num_faces]    # 정렬된 faces에 max_num_faces 만큼만 할당

        if draw_boxes:
            self.draw_faces(faces)
        else:
            pass

        return faces




###################################### 

# /home/matrix/Desktop/code/video2.mp4

# camera = Camera()

# while camera.is_opened():         # window_close_key 기본 esc 
#     frame = camera.get_frame()    # mirror_mode 기본 True
#     camera.show(frame)            # window_name 기본 Web Cam


######################################

# from dynamikontrol import Module

# module = Module()
# camera = Camera(cam_num='/home/matrix/Desktop/code/video2.mp4')
camera = Camera()

# angle = 0

while camera.is_opened():               # cancel_key default esc 
    frame = camera.get_frame()          # mirror_mode default True

    face = camera.detect_face(frame)     # draw_box default True
    
    # if face.c_x < 0.4:
    #     angle += 3
    #     module.motor.angle(angle)
    # elif face.c_x > 0.6:
    #     angle -= 3
    #     module.motor.angle(angle)

    camera.show(frame)        # cam_name default "Web Cam"




######################################

# from dynamikontrol import Module

# module = Module()
# camera = Camera(cam_num='/home/matrix/Desktop/code/video2.mp4')
# camera = Camera()

# angle = 0

# while camera.is_opened():               # cancel_key default esc 
#     frame = camera.get_frame()          # mirror_mode default True

#     faces = camera.detect_faces(frame)
#     print(faces)
    
#     if face.c_x < 0.4:
#         angle += 3
#         module.motor.angle(angle)
#     elif face.c_x > 0.6:
#         angle -= 3
#         module.motor.angle(angle)

#     camera.show(frame)        # cam_name default "Web Cam"















