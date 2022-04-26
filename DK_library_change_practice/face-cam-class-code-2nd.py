import cv2
import mediapipe as mp
import time

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


    def __repr__(self):   # Face() 객체의 인자를 보기좋게 만듬.
        return 'x1: %.2f, y1: %.2f, width: %.2f, height: %.2f' % (self.c_x, self.c_y, self.width, self.height)


class Camera():
    def __init__(self, cam_index = 0, width = None, height = None ):     # TODO : CAM_NUM 바꾸기

        self.cam_index = cam_index

        self.camera = cv2.VideoCapture(cam_index)    # web cam start

        if width is None or height is None:     
            self.width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))      # camera default frame size 
            self.height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        else:
            self.width = int(width)
            self.height = int(height)

            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)


        ### mediapipe drawing 
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles      # TODO : 그려지는지 확인


    def is_opened(self, window_close_key = 27): # window_close_key = "string" default : esc
        if not self.camera.isOpened():          # if self.camera.isOpened == False
            return False

        ret, img = self.camera.read()

        if not ret:     # 더이상 받을 ret이 없을때
            return False

        if len(str(window_close_key)) == 1:
            window_close_key = ord(window_close_key)
            print(window_close_key)
            if cv2.waitKey(15) & 0xFF == window_close_key:
                return False
        else:
            if cv2.waitKey(15) & 0xFF == window_close_key:
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

    # def detect_face(self, frame, draw_box = True):      # 얼굴한개 찾기
    #     return self.detect_faces(frame, max_num_faces = 1, draw_boxes = draw_box )

    # def detect_faces(self, frame, max_num_faces = 99, draw_boxes = True): # max_num_faces defalut : 99,  mediapipe default : 1  / draw_boxes default : True
    #     mp_face_detection = mp.solutions.face_detection
    #     face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

    #     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #     results = face_detection.process(frame_rgb)

    #     faces = []    # return 할 list

    #     if results.detections:
    #         for detection in results.detections:
    #             width = detection.location_data.relative_bounding_box.width      # box width
    #             height = detection.location_data.relative_bounding_box.height     # box height

    #             x1 = detection.location_data.relative_bounding_box.xmin # left
    #             y1 = detection.location_data.relative_bounding_box.ymin # top

    #             faces.append( Face(x1, y1, width, height) )

    #     faces = sorted(faces, key=lambda face: face.height, reverse=True)  # faces에서 face를 정렬할건데 기준은 face.height이다.
    #     faces = faces[:max_num_faces]    # 정렬된 faces에 max_num_faces 만큼만 할당

    #     if draw_boxes:
    #         self.draw_faces(faces)
    #     else:
    #         pass

    #     return faces


    def detect_face(self, frame, draw_mesh = True):      # 얼굴한개 찾기
        return self.detect_faces(frame, max_num_faces = 1, draw_mesh = draw_mesh )

    def detect_faces(self, frame, max_num_faces = 99, draw_mesh = True, draw_boxes =True):
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces = max_num_faces,    # detect face mesh number
            refine_landmarks = True,          # 정교 landmarks
            min_detection_confidence = 0.5,
            min_tracking_confidence = 0.5)        # TODO : 설정해야하는지 어느정도가 적당한지 조사해보기

        drawing_spec = self.mp_drawing.DrawingSpec(thickness=2, circle_radius=2)
        
        # 필요에 따라 성능 향상을 위해 이미지 작성을 불가능함으로 기본 설정합니다.
        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame)

        # 이미지 위에 얼굴 그물망 주석을 그립니다.
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        faces = []    # return 할 list

        # TODO : 그림그려지는거 큰것만 그려주는지 / 모두다그려지는지
        # 미디어파이프 객체가 한번걸러주는과정 수정필요
        # 바운딩박스있는지 확인
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # self.mp_drawing.draw_landmarks(
                #     image=frame,
                #     landmark_list=face_landmarks,
                #     connections=mp_face_mesh.FACEMESH_TESSELATION,
                #     landmark_drawing_spec=None,
                #     connection_drawing_spec=self.mp_drawing_styles
                #     .get_default_face_mesh_tesselation_style())
                # self.mp_drawing.draw_landmarks(
                #     image=frame,
                #     landmark_list=face_landmarks,
                #     connections=mp_face_mesh.FACEMESH_CONTOURS,
                #     landmark_drawing_spec=None,
                #     connection_drawing_spec=self.mp_drawing_styles
                #     .get_default_face_mesh_contours_style())
                # self.mp_drawing.draw_landmarks(
                #     image=frame,
                #     landmark_list=face_landmarks,
                #     connections=mp_face_mesh.FACEMESH_IRISES,      # TODO: 홍채도 넣으면 좋다.
                #     landmark_drawing_spec=None,
                #     connection_drawing_spec=self.mp_drawing_styles
                #     .get_default_face_mesh_iris_connections_style())

                face_left = face_landmarks.landmark[227].x
                face_right = face_landmarks.landmark[454].x
                face_upper = face_landmarks.landmark[10].y
                face_lower = face_landmarks.landmark[152].y


                face_width = face_right - face_left
                face_height = - ( face_upper - face_lower )

                faces.append( Face(x1=face_left, y1=face_upper, width=face_width, height=face_height) )


        faces = sorted(faces, key=lambda face: face.height, reverse=True)  # faces에서 face를 정렬할건데 기준은 face.height이다.
        faces = faces[:max_num_faces]    # 정렬된 faces에 max_num_faces 만큼만 할당

        if draw_boxes:
            self.draw_faces(faces)
        else:
            pass


        return faces


# class Temp():
#     def __init__(self, faces):
#         if len(faces) >= 1:
#             self.main_face_center_x = faces[0].c_x



###################################### 

# "/home/matrix/Desktop/code/video2.mp4"

# camera = Camera( )

# while camera.is_opened():         # window_close_key default : esc 
#     frame = camera.get_frame()    # mirror_mode default : True
#     camera.show(frame)            # window_name default : Web Cam


######################################

from dynamikontrol import Module

module = Module()
# camera = Camera(cam_num='/home/matrix/Desktop/code/video2.mp4')
camera = Camera()

angle = 0

while camera.is_opened():               # cancel_key default : esc 
    frame = camera.get_frame()          # mirror_mode default : True

    face = camera.detect_face(frame)     # draw_box default : True

    if len(face) >= 1:          # if one face detect
        c_x = face[0].c_x
        print(c_x)

        if c_x < 0.4:
            angle += 3
            module.motor.angle(angle)
        elif c_x > 0.6:
            angle -= 3
            module.motor.angle(angle)

    camera.show(frame)        # cam_name default : "Web Cam"




######################################

# from dynamikontrol import Module

# module = Module()
# camera = Camera(cam_num='/home/matrix/Desktop/code/video2.mp4')
# camera = Camera()

# angle = 0

# while camera.is_opened():               # cancel_key default esc 
#     frame = camera.get_frame()          # mirror_mode default True

#     faces = camera.detect_faces(frame)
#     if len(faces) == 1:              # face가 1개 detect 되면
#         print(faces[0].c_x)
#     elif len(faces) == 2:            # face가 2개 detect 되면
#         print(faces[0].c_x, faces[1].c_x)

#     camera.show(frame)        # cam_name default "Web Cam"


####################################

# from dynamikontrol import Module

# camera = Camera(cam_num='/home/matrix/Desktop/code/video2.mp4')
# # camera = Camera()

# module = Module()
# angle = 0

# while camera.is_opened():               # cancel_key default : esc 
#     frame = camera.get_frame()          # mirror_mode default : True

#     face = camera.face_mesh(frame)     # draw_box default : True
#     print(face)

#     if len(face) >= 1:
#         main_face_center_x = face[0].c_x

#         if main_face_center_x < 0.4:
#             angle += 3
#             module.motor.angle(angle)
#         elif main_face_center_x > 0.6:
#             angle -= 3
#             module.motor.angle(angle)

#     camera.show(frame)        # cam_name default : "Web Cam"

## TODO : 한개 DETECT될때 바꾸기
## TODO : FACEMESH 이름






######################################

# from dynamikontrol import Module

# # camera = Camera(cam_num='/home/matrix/Desktop/code/video2.mp4')
# camera = Camera()

# module = Module()
# angle = 0

# while camera.is_opened():               # cancel_key default : esc 
#     frame = camera.get_frame()          # mirror_mode default : True

#     face = camera.face_mesh(frame)     # draw_box default : True

#     if len(face) >= 1:
#         main_face_center_x = face[0].c_x

#         if main_face_center_x < 0.4:
#             angle += 3
#             module.motor.angle(angle)
#         elif main_face_center_x > 0.6:
#             angle -= 3
#             module.motor.angle(angle)

#     camera.show(frame)        # cam_name default : "Web Cam"












