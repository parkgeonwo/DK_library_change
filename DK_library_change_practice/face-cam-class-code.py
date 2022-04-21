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

    def find_coordinate(self, c_x, c_y, w, h):

        list = []
        self.c_x = c_x
        self.c_y = c_y
        self.w = w
        self.h = h
        list = [ self.c_x, self.c_y, self.w, self.h ]

        return list

class Camera():

    def __init__(self, cam_num = 0, width = 640, height = 480 ):
        
        self.cam_num = cam_num
        self.width = width
        self.height = height

        self.camera = cv2.VideoCapture(cam_num)    # web cam start

        self.camera.set(3, self.width)    # web cam width control
        self.camera.set(4, self.height)   # web cam height control

        ### mideapipe drawing
        self.mp_drawing = mp.solutions.drawing_utils             # mediapipe drawing

        ### mediapipe face_detection
        self.mp_face_detection = mp.solutions.face_detection   
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.5)
        
    def is_opened(self, cancel_key = 27):
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
        self.frame = cv2.flip(self.frame, mirror_mode)

        return self.frame

    def show(self, frame, cam_name = "Web Cam"):
        return cv2.imshow(cam_name, frame)


    def detect_face(self, frame):
        # TODO : 제일 큰 얼굴 1개만 반환
        return self.detect_faces(frame, max_num_faces=1)

    def detect_faces(self, frame, max_num_faces=None):     # max_num_faces = 1 , draw_boxes = 1
        results = self.face_detection.process(frame)       
        
        # TODO : max_num_faces 만큼 큰 얼굴만 검출

        r = []

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

                # h가 가장 큰 한개의 좌표만 r에 할당
                if max_num_faces == 1:             
                    temp_list = []
                    for i in range(len(r)):   # len(r) = 탐지된 얼굴 수
                        temp_list.append(r[i][3])       # temp_list에 탐지된 얼굴들의 h값 추가
                        r = r[temp_list.index(max(temp_list))]    # 탐지된 얼굴들의 h 값중 가장 큰 h를 list에서 index 하여 r에서 index num 해당 부분만 r로 할당
                        face_x1 = r[0] - (1/2) * r[2]
                        face_y1 = r[1] + (1/2) * r[3]
                        face_x2 = r[0] + (1/2) * r[2]
                        face_y2 = r[1] - (1/2) * r[3]

                        cv2.rectangle(frame, (int(round(self.width*face_x1)), int(round(self.height*face_y1))),
                                             (int(round(self.width*face_x2)),int(round(self.height*face_y2))),
                                             (0,255,0), 3)     # 제일큰 face 하나에만 그리기

                    # face2 = Face(r[0], r[1], r[2], r[3])
                    # face2 = face2.find_coordinate( r[0], r[1], r[2], r[3] )
                    # return face2

                elif max_num_faces > 1:
                    temp_list = []
                    for i in range(len(r)):      # len(r) = 탐지된 얼굴 수
                        temp_list.append(r[i][3])      # temp_list에 탐지된 얼굴들의 h값 추가
                        temp_list2 = sorted(temp_list, reverse = True)               # temp_list를 정렬하여 temp_list2에 할당
                        for i in range(max_num_faces):  # 얼굴 탐지수만큼 반복
                            if len(temp_list) == 1:
                                r = r[ temp_list.index( temp_list2[0] ) ]
                                print(r)
                                # face_x1 = r[0] - (1/2) * r[2]
                                # face_y1 = r[1] + (1/2) * r[3]
                                # face_x2 = r[0] + (1/2) * r[2]
                                # face_y2 = r[1] - (1/2) * r[3]

                                # cv2.rectangle(frame, (int(round(self.width*face_x1)), int(round(self.height*face_y1))),
                                #                     (int(round(self.width*face_x2)),int(round(self.height*face_y2))),
                                #                     (0,255,0), 3)     # i번째 face 그리기

                            else:
                                r = r[ temp_list.index( temp_list2[i] ) ]    # temp_list2[i] = h값중 1번째 큰값, 2번째 큰값,,,max_num번째 큰값
                            
                                face_x1 = r[0] - (1/2) * r[2]
                                face_y1 = r[1] + (1/2) * r[3]
                                face_x2 = r[0] + (1/2) * r[2]
                                face_y2 = r[1] - (1/2) * r[3]

                                cv2.rectangle(frame, (int(round(self.width*face_x1)), int(round(self.height*face_y1))),
                                                    (int(round(self.width*face_x2)),int(round(self.height*face_y2))),
                                                    (0,255,0), 3)     # i번째 face 그리기

                        
        return r # [Face(), Face()]






###################################### 

# 문제점 1 : break를 클래스안에 넣어줄수가 없음.
## 클래스를 고쳐서 해결했음 


# camera = Camera()

# while camera.is_opened():         # cancel_key 기본 esc 
#     frame = camera.get_frame()    # mirror_mode 기본 1
#     camera.show(frame)


######################################

from dynamikontrol import Module

module = Module()
camera = Camera()

angle = 0

while camera.is_opened():
    frame = camera.get_frame() 

    # face = camera.detect_face(frame)

    faces = camera.detect_faces(frame,max_num_faces = 2)
    # print(face.c_x)




    # for face in faces:
    #     print(face.cx, face.cy, face.w, face.h)
    # print(cx, cy, width, height)
    
    # if face.cx < 0.4:
    #     angle += 1
    #     module.motor.angle(angle, period = 0.1)
    # elif face.cx > 0.6:
    #     angle -= 1
    #     module.motor.angle(angle, period = 0.1)

    cv2.putText(frame, '%d deg' % (angle), org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=255, thickness=2)
    camera.show(frame)












######################################



# from dynamikontrol import Module

# module = Module()
# camera = Camera()           

# while camera.is_opened():
#     frame, img = camera.read()
#     if not frame:
#         break   

#     cx, cy, w, h = camera.detect_faces(img)         
#     # print(cx, cy, width, height)

#     angle = round( -170*cx +85 )
#     module.motor.angle(angle)

#     camera.show(img)

#     if camera.cancel():
#         break



######################################
# 이렇게 하면 되긴함.

# from dynamikontrol import Module

# camera = Camera()   
# module = Module()         

# while camera.is_opened():
#     frame, img = camera.read()
#     if not frame:
#         break   

#     try:
#         cx, cy, w, h = camera.detect_faces(img)         
#         angle = round( -170*cx +85 )
#         module.motor.angle(angle)

#     except:
#         pass

#     camera.show(img)

#     if camera.cancel():
#         break

#######################################










