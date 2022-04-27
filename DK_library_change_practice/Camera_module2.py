import cv2
import mediapipe as mp

class Face():
    def __init__(self, x1, y1, width, height, lips_x1, lips_y1, lips_width, lips_height):
        self.x1 = x1
        self.y1 = y1
        self.width = width
        self.height = height
        self.x2 = self.x1 + width
        self.y2 = self.y1 + height

        self.c_x = (self.x1 + self.x2) / 2
        self.c_y = (self.y1 + self.y2) / 2

        self.lips_x1 = lips_x1
        self.lips_y1 = lips_y1
        self.lips_width = lips_width
        self.lips_height = lips_height
        self.lips_x2 = self.lips_x1 + lips_width
        self.lips_y2 = self.lips_y1 + lips_height

        self.lips_c_x = (self.lips_x1 + self.lips_x2) / 2
        self.lips_c_y = (self.lips_y1 + self.lips_y2) / 2

    def left(self):
        left = self.c_x <= 0.4
        return left
    def right(self):
        right = self.c_x >= 0.6
        return right
    
    def up(self):
        up = self.c_y <= 0.4
        return up
    def down(self):
        down = self.c_y >= 0.6
        return down
    
    def mouth_open(self):
        open = int(abs( self.lips_height ) * 1500) >= 100
        return open
    def mouth_close(self):
        close = int(abs( self.lips_height ) * 1500) <= 10
        return close

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

    def is_opened(self, window_close_key = 27): # window_close_key = "string" default : esc
        if not self.camera.isOpened():          # if self.camera.isOpened == False
            return False

        ret, img = self.camera.read()

        if not ret:     # 더이상 받을 ret이 없을때
            return False

        if len(str(window_close_key)) == 1:
            window_close_key = ord(window_close_key)
            print(window_close_key)
            if cv2.waitKey(20) & 0xFF == window_close_key:
                return False
        else:
            if cv2.waitKey(20) & 0xFF == window_close_key:
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

    def draw_faces(self, faces):
        for face in faces:
            cv2.rectangle(self.frame, (int(round(self.width*face.x1)), int(round(self.height*face.y1))),
                    (int(round(self.width*face.x2)),int(round(self.height*face.y2))),
                    (0,255,0), 3)
    
    def draw_lips(self, faces):
        for face in faces:
            cv2.rectangle(self.frame, (int(round(self.width*face.lips_x1)), int(round(self.height*face.lips_y1))),
                    (int(round(self.width*face.lips_x2)),int(round(self.height*face.lips_y2))),
                    (0,255,0), 3)

    def detect_face(self, frame, draw_face_box = True, draw_lips_box = True):
        return self.detect_faces(frame, max_num_faces = 1, draw_face_boxes=draw_face_box, draw_lips_boxes=draw_lips_box )

    def detect_faces(self, frame, max_num_faces = 99, draw_face_boxes =True, draw_lips_boxes = True):
 
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles      # TODO : 그려지는지 확인
        mp_face_mesh = mp.solutions.face_mesh

        faces = []    # return 할 list

        with mp_face_mesh.FaceMesh(
            max_num_faces=max_num_faces,
            refine_landmarks=True,
            min_detection_confidence=0.5,      # TODO : 설정해야하는지 어느정도가 적당한지 조사해보기
            min_tracking_confidence=0.5) as face_mesh:

                frame.flags.writeable = False
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(frame)

                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        face_left = face_landmarks.landmark[227].x
                        face_right = face_landmarks.landmark[454].x
                        face_upper = face_landmarks.landmark[10].y
                        face_lower = face_landmarks.landmark[152].y
                        face_width = face_right - face_left
                        face_height = abs( face_upper - face_lower )

                        lips_left = face_landmarks.landmark[62].x
                        lips_right = face_landmarks.landmark[292].x
                        lips_upper = face_landmarks.landmark[13].y
                        lips_lower = face_landmarks.landmark[14].y
                        lips_width = lips_right - lips_left
                        lips_height = abs( lips_upper - lips_lower )

                        faces.append( Face(x1=face_left, y1=face_upper, width=face_width, height=face_height,
                                        lips_x1=lips_left, lips_y1=lips_upper, lips_width=lips_width, lips_height=lips_height) )

        if draw_face_boxes:
            self.draw_faces(faces)
        else:
            pass

        if draw_lips_boxes:
            self.draw_lips(faces)
        else:
            pass

        if len(faces) == 1 and max_num_faces == 1:
            return faces[0]

        return faces

def main():
    pass

if __name__ == "__main__":
    main()


###################################### 

# "/home/matrix/Desktop/code/video2.mp4"

# camera = Camera( )

# while camera.is_opened():         # window_close_key default : esc 
#     frame = camera.get_frame()    # mirror_mode default : True
#     camera.show(frame)            # window_name default : Web Cam


######################################

# from dynamikontrol import Module

# module = Module()
# camera = Camera(cam_index='/home/matrix/Desktop/code/video.mp4')
# # camera = Camera()

# angle = 0

# while camera.is_opened():               # cancel_key default : esc 
#     frame = camera.get_frame()          # mirror_mode default : True

#     face = camera.detect_face(frame)
#     lips = camera.detect_lip(frame)

    # if face.left():
    #     angle += 3
    #     module.motor.angle(angle)
    # elif face.right():
    #     angle -= 3
    #     module.motor.angle(angle)

    # camera.show(frame)        # cam_name default : "Web Cam"













