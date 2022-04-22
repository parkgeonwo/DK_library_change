import cv2
import mediapipe as mp
  
class Face():
    def __init__(self, x1, y1, w, h):
        self.x1 = x1
        self.y1 = y1
        self.w = w
        self.h = h
        self.x2 = self.x1 + w
        self.y2 = self.y1 + h

        self.c_x = (self.x1 + self.x2) / 2
        self.c_y = (self.y1 + self.y2) / 2

    def __repr__(self):
        return 'c_x: %.2f, c_y: %.2f, width: %.2f, height: %.2f' % (self.c_x, self.c_y, self.w, self.h)

class Camera():

    def __init__(self, cam_num = 0, width = 640, height = 480 ):
        ### TODO : width, height None 으로 기본셋팅 / 입력하면 바뀌게
        ### opencv에서 카메라 해상도 받아오기 사용해서 self.width none 안나오게

        self.cam_num = cam_num

        self.camera = cv2.VideoCapture(cam_num)    # web cam start

        self.width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

        ### TODO : cv2.prop~~ 로 바꾸기
        # self.camera.set(3, self.width)    # web cam width control
        # self.camera.set(4, self.height)   # web cam height control

        ### mediapipe face_detection
        self.mp_face_detection = mp.solutions.face_detection   
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.5)
        
    def is_opened(self, cancel_key = 27):
        ### TODO : cancelkey 이름 바꾸기
        if not self.camera.isOpened():  # self.camera.isOpened가 False 라면
            return False

        ret, img = self.camera.read()

        if not ret:     # 더이상 받을 ret이 없을때
            return False
        if len(str(cancel_key)) == 1:
            cancel_key = ord(cancel_key)
            if cv2.waitKey(30) & 0xFF == cancel_key:  # cancel_key : esc
                return False
        else:
            if cv2.waitKey(30) & 0xFF == cancel_key:  # cancel_key : esc
                return False

        self.frame = img

        return True

    def get_frame(self, mirror_mode = 1):
        ### TODO : True / False
        # True false를 검사해서 함수 안쓰게 / 연산시간 감축
        self.frame = cv2.flip(self.frame, mirror_mode)

        return self.frame

    def show(self, frame, cam_name = "Web Cam"):    # TODO : window_name
        return cv2.imshow(cam_name, frame)

    def draw_faces(self, faces):   # face 여러개 그려주는 method
        for face in faces:
            cv2.rectangle(frame, (int(round(self.width*face.x1)), int(round(self.height*face.y1))),
                    (int(round(self.width*face.x2)),int(round(self.height*face.y2))),
                    (0,255,0), 3)     # face 그리기

    def detect_face(self, frame, draw_box = 1):      # 얼굴한개 찾기
        return self.detect_faces(frame, max_num_faces = 1, draw_boxes = draw_box )

    def detect_faces(self, frame, max_num_faces = 99, draw_boxes = 1): # max_num = mediapipe 기본값과 같게 / draw_boxes = 1
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

        faces = sorted(faces, key=lambda face: face.h, reverse=True)
        faces = faces[:max_num_faces]

        if draw_boxes:
            self.draw_faces(faces)

        return faces




###################################### 


# camera = Camera()

# while camera.is_opened():         # cancel_key 기본 esc 
#     frame = camera.get_frame()    # mirror_mode 기본 1
#     camera.show(frame)            # cam_name 기본 Web Cam


######################################

# from dynamikontrol import Module

# module = Module()
camera = Camera(cam_num='video2.mp4')

# angle = 0

while camera.is_opened():               # cancel_key 기본 esc 
    frame = camera.get_frame()          # mirror_mode 기본 1

    # face = camera.detect_face(frame)     # draw_box 기본 1
    faces = camera.detect_faces(frame, draw_boxes=1)  # max_num_faces 기본 3 / draw_boxes 기본 1 
    #print(face.c_x)
    # print(faces)
    # if face.c_x < 0.4:
    #     angle += 3
    #     module.motor.angle(angle)
    # elif face.c_x > 0.6:
    #     angle -= 3
    #     module.motor.angle(angle)

    camera.show(frame)        # cam_name 기본 Web Cam




















