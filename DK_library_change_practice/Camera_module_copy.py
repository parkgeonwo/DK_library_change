import cv2
import mediapipe as mp

class Face():
    def __init__(self, face_landmarks):

        # face
        face_left = face_landmarks.landmark[227].x
        face_right = face_landmarks.landmark[454].x
        face_upper = face_landmarks.landmark[10].y
        face_lower = face_landmarks.landmark[152].y
        face_width = face_right - face_left
        face_height = abs( face_upper - face_lower )

        self.face_x1 = face_left
        self.face_y1 = face_upper
        self.face_width = face_width
        self.face_height = face_height
        self.face_x2 = self.face_x1 + face_width
        self.face_y2 = self.face_y1 + face_height
        self.face_c_x = (self.face_x1 + self.face_x2) / 2
        self.face_c_y = (self.face_y1 + self.face_y2) / 2

        # lips
        lips_left = face_landmarks.landmark[62].x
        lips_right = face_landmarks.landmark[292].x
        lips_upper = face_landmarks.landmark[13].y
        lips_lower = face_landmarks.landmark[14].y
        lips_width = lips_right - lips_left
        lips_height = abs( lips_upper - lips_lower )

        self.lips_x1 = lips_left
        self.lips_y1 = lips_upper
        self.lips_width = lips_width
        self.lips_height = lips_height
        self.lips_x2 = self.lips_x1 + lips_width
        self.lips_y2 = self.lips_y1 + lips_height
        self.lips_c_x = (self.lips_x1 + self.lips_x2) / 2
        self.lips_c_y = (self.lips_y1 + self.lips_y2) / 2

    def left_side_window(self):
        left = self.face_c_x <= 0.4
        return left
    def right_side_window(self):
        right = self.face_c_x >= 0.6
        return right
    def top_side_window(self):
        up = self.face_c_y <= 0.4
        return up
    def bottom_side_window(self):
        down = self.face_c_y >= 0.6
        return down

    def open_mouth(self):
        open = (self.lips_height) >= (self.face_height*0.1) 
        return open

    def __repr__(self):
        return 'self.face_c_x: %.2f, self.face_c_y: %.2f, self.face_width: %.2f, self.face_height: %.2f' % (self.face_c_x, self.face_c_y, self.face_width, self.face_height)

class Camera():
    def __init__(self, file_or_device=0, width = None, height = None ):

        self.camera = cv2.VideoCapture(file_or_device)

        if width is None or height is None:     
            self.width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        else:
            self.width = int(width)
            self.height = int(height)

    def is_opened(self, window_close_key = 27): # window_close_key = "string" default : esc
        if not self.camera.isOpened():
            return False

        ret, img = self.camera.read()

        if not ret:
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
        self.frame = cv2.resize(self.frame, (self.width, self.height), interpolation=cv2.INTER_CUBIC)

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
            cv2.rectangle(self.frame, (int(round(self.width*face.face_x1)), int(round(self.height*face.face_y1))),
                    (int(round(self.width*face.face_x2)),int(round(self.height*face.face_y2))),
                    (0,255,0), 3)
    
    def draw_lips(self, faces):
        for face in faces:
            cv2.rectangle(self.frame, (int(round(self.width*face.lips_x1)), int(round(self.height*face.lips_y1))),
                    (int(round(self.width*face.lips_x2)),int(round(self.height*face.lips_y2))),
                    (0,255,0), 3)

    def detect_face(self, frame, draw_face_box = True, draw_lips_box = True):
        return self.detect_faces(frame, max_num_faces = 1, draw_face_boxes=draw_face_box, draw_lips_boxes=draw_lips_box )

    def detect_faces(self, frame, max_num_faces = 99, draw_face_boxes =True, draw_lips_boxes = True):
 
        mp_face_mesh = mp.solutions.face_mesh

        faces = []    # return 할 list

        with mp_face_mesh.FaceMesh(
            max_num_faces=max_num_faces,
            refine_landmarks=True,
            min_detection_confidence=0.4, 
            min_tracking_confidence=0.5) as face_mesh:

                frame.flags.writeable = False
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(frame)

                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:  
                        faces.append( Face(face_landmarks) )

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





# 웃는다 / 안웃는다 등 기능 추가
# 릴리즈 플랜을 짜서 
# 소프트웨어 방법론에서 릴리즈 플랜짜는법 있음. --> 릴리즈 노트 
# 0.1 버전 기능들 / 0.2 버전 기능들
# 애자일 개발 방법론 / 스크럼

# 다음번에 어떤 기능을 하겠다 계획세우기


# 버전 0.1.0
# 2022.04.28
# description : 카메라 웹캠 및 이미지를 화면에서 쉽게 띄우고 얼굴과 입을 인식하여 활용할 수 있는 기능을 내포하고 있음.
# (New) 카메라 웹캠 및 이미지 화면에 띄우기 기능
# (New) 얼굴 인식 기능 
# (New) 입 인식 기능
# (Feature) 얼굴, 입 draw_boxes 기능
# (Feature) 얼굴, 입술(한개)의 x1, y1, x2, y2, width, height, c_x, c_y 추출 기능
# (Feature) 얼굴(한개)이 화면상의 top/bottom/left/right side method
# (Feature) 입(한개)를 벌렸을때 method


# 버전 0.2.0
# (New) Face 객체에서 (왼쪽, 오른쪽) 눈 / 홍채 인식 기능 추가
# (Feature) (왼쪽, 오른쪽) 눈 close method 추가
# (Feature) (왼쪽, 오른쪽) 홍채가 눈안에서 top / bottom / left / right side 인지 알려주는 method
# (Feature) (양쪽) 눈 close / (양쪽) 홍채 side

# (Feature) Face 객체에서 입 모양 method 기능 추가
# (Feature) 웃는 입 모양, 슬픈 입모양






