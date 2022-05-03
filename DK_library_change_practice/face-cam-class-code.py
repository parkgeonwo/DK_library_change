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

class Face():
    def __init__(self, c_x, c_y, w, h):
        self.c_x = c_x
        self.c_y = c_y
        self.w = w
        self.h = h

class Camera():

    def __init__(self, cam_num = 0, width = 640, height = 480 ):
        ### TODO : width, height None 으로 기본셋팅 / 입력하면 바뀌게
        ### opencv에서 카메라 해상도 받아오기 사용해서 self.width none 안나오게

        self.cam_num = cam_num
        self.width = width
        self.height = height

        self.camera = cv2.VideoCapture(cam_num)    # web cam start

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
            if cv2.waitKey(1) & 0xFF == cancel_key:  # cancel_key : esc
                return False
        else:
            if cv2.waitKey(1) & 0xFF == cancel_key:  # cancel_key : esc
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

    def draw_face(self, r):       # face 한개 그리는 method
        r = r[ self.temp_list.index( max(self.temp_list) ) ]      # h가 가장 큰 한개의 좌표만 r로 할당
        face_x1 = r[0] - (1/2) * r[2]
        face_y1 = r[1] + (1/2) * r[3]
        face_x2 = r[0] + (1/2) * r[2]
        face_y2 = r[1] - (1/2) * r[3]
        cv2.rectangle(frame, (int(round(self.width*face_x1)), int(round(self.height*face_y1))),
                (int(round(self.width*face_x2)),int(round(self.height*face_y2))),
                (0,255,0), 3)     # face 그리기

    def draw_faces(self,r,num_faces):   # face 여러개 그려주는 method
        self.temp_list2 = sorted(self.temp_list, reverse=True)
        self.face_list = []

        for i in range(num_faces):
            self.face_list.append( r[ self.temp_list.index( self.temp_list2[i]) ] )

            face_x1 = self.face_list[i][0] - (1/2) * self.face_list[i][2]
            face_y1 = self.face_list[i][1] + (1/2) * self.face_list[i][3]
            face_x2 = self.face_list[i][0] + (1/2) * self.face_list[i][2]
            face_y2 = self.face_list[i][1] - (1/2) * self.face_list[i][3]
            cv2.rectangle(frame, (int(round(self.width*face_x1)), int(round(self.height*face_y1))),
                    (int(round(self.width*face_x2)),int(round(self.height*face_y2))),
                    (0,255,0), 3)     # face 그리기

    def detect_face(self, frame, draw_box = 1):      # 얼굴한개 찾기
        draw_box_num = draw_box
        return self.detect_faces(frame, max_num_faces = 1, draw_boxes = draw_box_num )

    def detect_faces(self, frame, max_num_faces = 3, draw_boxes = 1): # max_num = mediapipe 기본값과 같게 / draw_boxes = 1
        results = self.face_detection.process(frame) 

        # TODO : max_num_faces 만큼 큰 얼굴만 검출

        r = []    # return 할 list

        if results.detections: 
            for detection in results.detections:
                # self.mp_drawing.draw_detection(frame, detection)

                w = detection.location_data.relative_bounding_box.width      # box width
                h = detection.location_data.relative_bounding_box.height     # box height

                x1 = detection.location_data.relative_bounding_box.xmin # left
                x2 = x1 + w # right

                y1 = detection.location_data.relative_bounding_box.ymin # top
                y2 = y1 + h # bottom

                c_x = (x1 + x2) / 2 # horizontal center of the face
                c_y = (y1 + y2) / 2 # vertical center of the face

                face = Face(c_x, c_y, w, h)

                r.append( [face.c_x, face.c_y, face.w, face.h] )


        self.temp_list = []     # h의 크기를 비교하기위한 리스트
        self.temp_list2 = []    # face 여러개 있을때 h의 크기를 sort하기 위한 리스트

        if len(r) == 1:     # 얼굴이 한개 detect 됐을때
            self.temp_list.append(r[0][3])
            ### TODO : IF / ELIF 합치기
            if max_num_faces == 1 and draw_boxes == 1:    # 한개만 detect 할때는
                self.draw_face(r)     # h가 가장 큰 얼굴에 rectangle 그리기
            elif max_num_faces >= 2 and draw_boxes == 1:   # max_num_faces가 2이상이라도
                self.draw_face(r)      # 한개만 detect 될때 그려주기

        for i in range(2,6):    # 얼굴 2~5개까지 가능
            if len(r) == i:     # 얼굴이 두개 detect 됐을때
                for j in range(i):
                    self.temp_list.append(r[j][3])

                if max_num_faces == 1 and draw_boxes == 1 :    # 한개만 detect 할때는
                    self.draw_face(r)     # h가 가장 큰 얼굴에 rectangle 그리기
                
                elif max_num_faces >= 2 and draw_boxes == 1:                  # 여러개 detect할때는
                    self.draw_faces(r,num_faces = i)    # 큰 얼굴 순서대로 max_num_faces 만큼 rectangle그리기


        if max_num_faces == 1 and len(r) == 1:     # max_num_faces가 1이고 얼굴이 한개 detect됐을때,
            return face

        elif max_num_faces == 1 and len(r) == 0:   # max_num_faces가 1이고 얼굴이 detect안됐을때,
            face2 = Face(0.5, 0.5, 0, 0)        # c_x, c_y = 0.5 , w, h = 0
            return face2    # face가 감지안되도 face가 1개가 리턴이 된다. 

        elif max_num_faces == 1 and len(r) >= 2:   # max_num_faces가 1이고 얼굴이 2개이상 detect 됐을때,
            face3 = Face(0.5, 0.5, 0, 0)        # c_x, c_y = 0.5 , w, h = 0
            return face3    # face 
        else:
            return r 






###################################### 


camera = Camera()

while camera.is_opened():         # cancel_key 기본 esc 
    frame = camera.get_frame()    # mirror_mode 기본 1
    camera.show(frame)            # cam_name 기본 Web Cam


######################################

# from dynamikontrol import Module

# module = Module()
# camera = Camera()

# angle = 0

# while camera.is_opened():               # cancel_key 기본 esc 
#     frame = camera.get_frame()          # mirror_mode 기본 1

#     #face = camera.detect_face(frame)     # draw_box 기본 1
#     faces = camera.detect_faces(frame, draw_boxes=1)  # max_num_faces 기본 3 / draw_boxes 기본 1 
#     #print(face.c_x)
#     print(faces)
#     # if face.c_x < 0.4:
#     #     angle += 3
#     #     module.motor.angle(angle)
#     # elif face.c_x > 0.6:
#     #     angle -= 3
#     #     module.motor.angle(angle)

#     camera.show(frame)        # cam_name 기본 Web Cam




















