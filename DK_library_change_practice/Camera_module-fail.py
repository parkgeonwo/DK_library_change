import cv2
import mediapipe as mp

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

    def __repr__(self):
        return 'x1: %.2f, y1: %.2f, width: %.2f, height: %.2f' % (self.c_x, self.c_y, self.width, self.height)

class Lips():
    def __init__(self, x1, y1, width, height):
        self.x1 = x1
        self.y1 = y1
        self.width = width
        self.height = height
        self.x2 = self.x1 + width
        self.y2 = self.y1 + height

        self.c_x = (self.x1 + self.x2) / 2
        self.c_y = (self.y1 + self.y2) / 2

    def open(self):
        open = int(abs( self.height ) * 1500) >= 100
        return open
    def close(self):
        close = int(abs( self.height ) * 1500) <= 10
        return close

    def __repr__(self):
        return 'x1: %.2f, y1: %.2f, width: %.2f, height: %.2f' % (self.c_x, self.c_y, self.width, self.height)

class Camera():
    def __init__(self, camera_location = 0, width = None, height = None, percentage = None ):

        self.camera = cv2.VideoCapture(camera_location)

        self.camera.set(cv2.CAP_PROP_FPS, 30.0)
        self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
        self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))

        if width is None or height is None:     
            self.width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))      # camera default frame size 
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

    def draw_boxes(self, faces):
        for face in faces:
            cv2.rectangle(self.frame, (int(round(self.width*face.x1)), int(round(self.height*face.y1))),
                    (int(round(self.width*face.x2)),int(round(self.height*face.y2))),
                    (0,255,0), 3)

    def detect_face(self, frame, draw_face_box = True):
        return self.detect_faces(frame, max_num_faces = 1, draw_face_boxes = draw_face_box )

    def detect_faces(self, frame, max_num_faces = 99, draw_face_boxes =True):
 
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles      # TODO : 그려지는지 확인
        mp_face_mesh = mp.solutions.face_mesh

        faces = []

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

                        faces.append( Face(x1=face_left, y1=face_upper, width=face_width, height=face_height) )

        if draw_face_boxes:
            self.draw_boxes(faces)
        else:
            pass

        if len(faces) == 1 and max_num_faces == 1:
            return faces[0]

        return faces


    def detect_lip(self, frame, draw_lip_box = True):
        return self.detect_lips(frame, max_num_lips = 1, draw_lips_boxes = draw_lip_box)

    def detect_lips(self, frame, max_num_lips = 99, draw_lips_boxes =True):
 
        mp_face_mesh = mp.solutions.face_mesh

        lips = []    # return 할 list

        with mp_face_mesh.FaceMesh(
            max_num_faces=max_num_lips,
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

                        lips_left = face_landmarks.landmark[62].x
                        lips_right = face_landmarks.landmark[292].x
                        lips_upper = face_landmarks.landmark[13].y
                        lips_lower = face_landmarks.landmark[14].y
                        lips_width = lips_right - lips_left
                        lips_height = abs( lips_upper - lips_lower )

                        lips.append( Lips(x1=lips_left, y1=lips_upper, width=lips_width, height=lips_height) )

        if draw_lips_boxes:
            self.draw_boxes(lips)
        else:
            pass

        if len(lips) == 1 and max_num_lips == 1:
            return lips[0]

        return lips

def main():
    pass

if __name__ == "__main__":
    main()











