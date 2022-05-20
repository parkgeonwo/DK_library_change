import cv2
import mediapipe as mp
import numpy as np
import math

class Face():
    def __init__(self, face_landmarks, frame):

        self.face_landmarks = face_landmarks
        self.frame = frame
        self.frame_height, self.frame_width, c = frame.shape

        self.landmark_list = []

        for id, lm in enumerate(self.face_landmarks.landmark):
            x, y = int(lm.x * self.frame_width), int(lm.y * self.frame_height)
            self.landmark_list.append([x, y])

        # face
        left = face_landmarks.landmark[127].x * self.frame_width
        right = face_landmarks.landmark[356].x * self.frame_width
        upper = face_landmarks.landmark[10].y * self.frame_height
        lower = face_landmarks.landmark[377].y * self.frame_height
        width = right - left
        height = abs( upper - lower )

        self.x1 = left
        self.y1 = upper
        self.width = width
        self.height = height
        self.x2 = self.x1 + width
        self.y2 = self.y1 + height
        self.center_x = (self.x1 + self.x2) / 2
        self.center_y = (self.y1 + self.y2) / 2

        # lips
        self.lips_left = face_landmarks.landmark[62].x * self.frame_width
        self.lips_right = face_landmarks.landmark[292].x * self.frame_width
        self.lips_upper = face_landmarks.landmark[13].y * self.frame_height
        self.lips_lower = face_landmarks.landmark[14].y * self.frame_height
        self.lips_width = self.lips_right - self.lips_left
        self.lips_height = abs( self.lips_upper - self.lips_lower )

        self.lips_angle = self.get_angle(13,62,14)

        self.lips = Lips( x1 = self.lips_left, y1 = self.lips_upper,
                        width = self.lips_width, height = self.lips_height,
                        angle = self.lips_angle )

        lipsUpper_list = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 308, 415, 310, 311, 312, 13, 82, 81, 80, 191, 78]
        lipsLower_list = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95, 78]
        # lipsUpperInner = [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308]
        # lipsLowerInner = [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308]

        self.lipsUpper_list = [ [face_landmarks.landmark[i].x, face_landmarks.landmark[i].y ] for i in lipsUpper_list ]
        self.lipsLower_list = [ [face_landmarks.landmark[i].x, face_landmarks.landmark[i].y ] for i in lipsLower_list ]

        ##### left eye
        self.left_eye_left = face_landmarks.landmark[33].x * self.frame_width
        self.left_eye_right = face_landmarks.landmark[133].x * self.frame_width
        self.left_eye_upper = face_landmarks.landmark[159].y * self.frame_height
        self.left_eye_lower = face_landmarks.landmark[145].y * self.frame_height
        self.left_eye_width = self.left_eye_right-self.left_eye_left
        self.left_eye_height = abs(self.left_eye_upper - self.left_eye_lower)

        self.left_eye = Eye( x1 = self.left_eye_left, y1 = self.left_eye_upper
                        , width = self.left_eye_width, height = self.left_eye_height
                        , face_width = self.width, face_height = self.height )

        ##### right eye
        self.right_eye_left = face_landmarks.landmark[362].x * self.frame_width
        self.right_eye_right = face_landmarks.landmark[263].x * self.frame_width
        self.right_eye_upper = face_landmarks.landmark[386].y * self.frame_height
        self.right_eye_lower = face_landmarks.landmark[374].y * self.frame_height
        self.right_eye_width = self.right_eye_right-self.right_eye_left
        self.right_eye_height = abs(self.right_eye_upper - self.right_eye_lower)

        self.right_eye = Eye( x1 = self.right_eye_left, y1 = self.right_eye_upper
                        , width = self.right_eye_width, height = self.right_eye_height
                        , face_width = self.width, face_height = self.height )

        # # left eye index list 
        # LEFT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]
        # # right eye index list 
        # RIGHT_EYE =[ 362, 382, ​​381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]


        #### left iris
        # self.left_iris_center = face_landmarks.landmark[468].x
        self.left_iris_right = face_landmarks.landmark[469].x * self.frame_width
        self.left_iris_left = face_landmarks.landmark[471].x * self.frame_width
        self.left_iris_upper = face_landmarks.landmark[470].y * self.frame_height
        self.left_iris_lower = face_landmarks.landmark[472].y * self.frame_height
        self.left_iris_width = self.left_iris_right-self.left_iris_left
        self.left_iris_height = abs(self.left_iris_upper - self.left_iris_lower)

        self.left_iris = Iris( x1 = self.left_iris_left, y1 = self.left_iris_upper
                        , width = self.left_iris_width, height = self.left_iris_height )

        #### right iris
        # self.right_iris_center = face_landmarks.landmark[473].x
        self.right_iris_right = face_landmarks.landmark[474].x * self.frame_width
        self.right_iris_left = face_landmarks.landmark[476].x * self.frame_width
        self.right_iris_upper = face_landmarks.landmark[475].y * self.frame_height
        self.right_iris_lower = face_landmarks.landmark[477].y * self.frame_height
        self.right_iris_width = self.right_iris_right-self.right_iris_left
        self.right_iris_height = abs(self.right_iris_upper - self.right_iris_lower)

        self.right_iris = Iris( x1 = self.right_iris_left, y1 = self.right_iris_upper
                        , width = self.right_iris_width, height = self.right_iris_height )

        ### eyes
        self.eyes = Eyes( self.left_eye, self.right_eye, self.left_iris, self.right_iris )

        ### face turn estimation
        self.head_pose = head_pose_estimation(self.frame_width, self.frame_height, self.face_landmarks)
        self.direction = self.head_pose.text

    def get_angle(self,p1,p2,p3):
        get_angle = Get_angle_class(self.landmark_list)
        return get_angle.angle(p1,p2,p3) 
    def get_distance(self,p1,p2):
        get_distance = Get_distance_class(self.landmark_list)
        return get_distance.distance(p1,p2) 

    def is_located_left(self):
        return self.center_x <= 0.4 * self.frame_width
    def is_located_right(self):
        return self.center_x >= 0.6 * self.frame_width
    def is_located_top(self):
        return self.center_y <= 0.4 * self.frame_height
    def is_located_bottom(self):
        return self.center_y >= 0.6 * self.frame_height

    def __repr__(self):
        return 'center_x: %.3f, center_y: %.3f, width: %.3f, height: %.3f' % (self.center_x, self.center_y, self.width, self.height)

class Lips():
    def __init__(self,x1,y1,width,height, angle):
        self.x1 = x1
        self.y1 = y1
        self.width = width
        self.height = height
        self.x2 = self.x1 + width
        self.y2 = self.y1 + height
        self.center_x = (self.x1 + self.x2) / 2
        self.center_y = (self.y1 + self.y2) / 2
        self.angle = angle
    def is_opened(self, angle = 80):
        return self.angle >= angle
    def __repr__(self):
        return 'center_x: %.3f, center_y: %.3f, width: %.3f, height: %.3f' % (self.center_x, self.center_y, self.width, self.height)

#### Eye
class Eye():
    def __init__(self,x1,y1,width,height,face_width,face_height):
        self.x1 = x1
        self.y1 = y1
        self.width = width
        self.height = height
        self.x2 = self.x1 + width
        self.y2 = self.y1 + height
        self.center_x = (self.x1 + self.x2) / 2
        self.center_y = (self.y1 + self.y2) / 2
        self.face_width = face_width
        self.face_height = face_height
    def is_closed(self, ratio = 0.06):
        return (self.height) <= (self.face_width*ratio)
    def __repr__(self):
        return 'center_x: %.3f, center_y: %.3f, width: %.3f, height: %.3f' % (self.center_x, self.center_y, self.width, self.height)

#### Iris
class Iris():
    def __init__(self,x1,y1,width,height):
        self.x1 = x1
        self.y1 = y1
        self.width = width
        self.height = height
        self.x2 = self.x1 + width
        self.y2 = self.y1 + height
        self.center_x = (self.x1 + self.x2) / 2
        self.center_y = (self.y1 + self.y2) / 2
    def __repr__(self):
        return 'center_x: %.3f, center_y: %.3f, width: %.3f, height: %.3f' % (self.center_x, self.center_y, self.width, self.height)

#### Eyes
class Eyes():
    def __init__(self,left_eye,right_eye,left_iris,right_iris):
        self.left_eye = left_eye
        self.right_eye = right_eye
        self.left_iris = left_iris
        self.right_iris = right_iris
    def is_look_left(self, ratio = 0.4):
        look_left = (self.left_iris.center_x <= (self.left_eye.x1 + self.left_eye.width*ratio)) and (self.right_iris.center_x <= (self.right_eye.x1 + self.right_eye.width*ratio))
        return look_left
    def is_look_right(self, ratio = 0.6):
        look_right = (self.left_iris.center_x >= (self.left_eye.x1 + self.left_eye.width*ratio)) and (self.right_iris.center_x >= (self.right_eye.x1 + self.right_eye.width*ratio))
        return look_right

class head_pose_estimation():
    def __init__(self,frame_width, frame_height,face_landmarks ):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.face_landmarks = face_landmarks

        face_2d = []
        face_3d = []
        for idx, lm in enumerate(self.face_landmarks.landmark):
            if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                if idx == 1:
                    nose_2d = (lm.x * self.frame_width, lm.y * self.frame_height)
                    nose_3d = (lm.x * self.frame_width, lm.y * self.frame_height, lm.z * 3000)

                x, y = int(lm.x * self.frame_width), int(lm.y * self.frame_height)

                # Get the 2D Coordinates
                face_2d.append([x, y])
                # Get the 3D Coordinates
                face_3d.append([x, y, lm.z])

        # Convert it to the NumPy array
        face_2d = np.array(face_2d, dtype=np.float64)
        # Convert it to the NumPy array
        face_3d = np.array(face_3d, dtype=np.float64)
        # The camera matrix
        focal_length = 1 * self.frame_width       # 초점거리 1배
        cam_matrix = np.array([ [focal_length, 0, self.frame_height / 2],
                                [0, focal_length, self.frame_width / 2],
                                [0, 0, 1]])
        # The distortion parameters
        dist_matrix = np.zeros((4, 1), dtype=np.float64)
        # Solve PnP
        success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
        # Get rotational matrix
        rmat, jac = cv2.Rodrigues(rot_vec)
        # Get angles
        angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)
        # Get the y rotation degree
        self.x = angles[0] * 360
        self.y = angles[1] * 360
        self.z = angles[2] * 360
        # See where the user's head tilting
        if self.y < -15:
            self.text = "left"
        elif self.y > 15:
            self.text = "right"
        elif self.x < -10:
            self.text = "down"
        elif self.x > 20:
            self.text = "up"
        else:
            self.text = "forward"

        # # Display the nose direction
        # nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)

        # p1 = (int(nose_2d[0]), int(nose_2d[1]))
        # p2 = (int(nose_2d[0] + y * 10) , int(nose_2d[1] - x * 10))
        
        # cv2.line(image, p1, p2, (255, 0, 0), 3)

        # # Add the text on the image
        # cv2.putText(image, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

class Hand():
    def __init__(self, hand_landmarks, frame, hand_angle_data, hand_knn):
            self.hand_landmarks = hand_landmarks
            self.tipIds = [4,8,12,16,20]

            self.hand_knn = hand_knn
            self.hand_angle_data = hand_angle_data

            self.frame = frame
            self.frame_height, self.frame_width, c = frame.shape

            self.xList = []
            self.yList = []
            self.landmark_list = []
            self.joint = np.zeros((21,3))

            for id, lm in enumerate(self.hand_landmarks.landmark):
                x, y = int(lm.x * self.frame_width), int(lm.y * self.frame_height)
                self.xList.append(x)
                self.yList.append(y)
                self.landmark_list.append([x, y])

                self.joint[id] = [lm.x, lm.y, lm.z]

            xmin, xmax = min(self.xList), max(self.xList)
            ymin, ymax = min(self.yList), max(self.yList)
            self.bbox = xmin, ymin, xmax-xmin, ymax-ymin

            self.gesture_dict = {0:'rock', 1:'one', 2:'two', 3:'three', 4:'four', 5:'paper',
                        6:'six', 7:'rocknroll',8:'spiderman', 9:'scissors',10:'ok'}

            self.gesture = self.detect_gesture()

            self.fingers = Fingers(landmark_list= self.landmark_list, tipIds = self.tipIds)

    def get_angle(self,p1,p2,p3):
        get_angle = Get_angle_class(self.landmark_list)
        return get_angle.angle(p1,p2,p3) 

    def get_distance(self,p1,p2):
        get_distance = Get_distance_class(self.landmark_list)
        return get_distance.distance(p1,p2) 

    def get_webcam_distance(self):
        # x is the raw distance , y is the value in cm
        x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
        y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        coff = np.polyfit(x, y, 2)  # y = Ax^2 + Bx + C     # 이차함수 A,B,C coff 뽑아줌

        x1, y1 = self.landmark_list[5]
        x2, y2 = self.landmark_list[17]
 
        distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
        A, B, C = coff
        distanceCM = A * distance ** 2 + B * distance + C
 
        return distanceCM

    def detect_gesture(self):
        # Compute angles between joints
        v1 = self.joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19],:] # Parent joint
        v2 = self.joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],:] # Child joint
        v = v2 - v1 # [20,3]
        # Normalize v
        v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

        # Get angle using arcos of dot product
        self.hand_angle_data = np.arccos(np.einsum('nt,nt->n',
            v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:], 
            v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:])) # [15,]

        self.hand_angle_data = np.degrees(self.hand_angle_data) # Convert radian to degree

        # Inference gesture
        data = np.array([self.hand_angle_data], dtype=np.float32)
        ret, results, neighbours, dist = self.hand_knn.findNearest(data, 3)
        idx = int(results[0][0])

        text = self.gesture_dict[idx].lower()

        return text

class Fingers():
    def __init__(self, landmark_list, tipIds):
        self.landmark_list = landmark_list
        self.tipIds = tipIds

    def is_thumb_up(self):
        return self.landmark_list[self.tipIds[0]][1] < self.landmark_list[self.tipIds[0] - 2][1]

    def is_index_up(self):
        return self.landmark_list[self.tipIds[1]][1] < self.landmark_list[self.tipIds[1] - 2][1]

    def is_middle_up(self):
        return self.landmark_list[self.tipIds[2]][1] < self.landmark_list[self.tipIds[2] - 2][1]

    def is_ring_up(self):
        return self.landmark_list[self.tipIds[3]][1] < self.landmark_list[self.tipIds[3] - 2][1]

    def is_pinky_up(self):
        return self.landmark_list[self.tipIds[4]][1] < self.landmark_list[self.tipIds[4] - 2][1]

    def is_up(self):
        is_up_list = [ self.is_thumb_up(), self.is_index_up(), self.is_middle_up(), self.is_ring_up(), self.is_pinky_up() ]
        return_list = []
        for i in is_up_list:
            if i is True:
                return_list.append(True)
            else:
                return_list.append(False)

        return return_list

    def get_distance(self, tipId1, tipId2):

        tipId1 = (tipId1 + 1) * 4
        tipId2 = (tipId2 + 1) * 4

        x1, y1 = self.landmark_list[tipId1]
        x2, y2 = self.landmark_list[tipId2]

        distance = math.hypot(x2 - x1, y2 - y1)

        return distance


class Body():
    def __init__(self, pose_landmarks, frame_width, frame_height):

        self.pose_landmarks = pose_landmarks
        self.frame_width, self.frame_height = frame_width, frame_height

        self.landmark_list = []

        for id, lm in enumerate(self.pose_landmarks.landmark):
            x, y = int(lm.x * self.frame_width), int(lm.y * self.frame_height)
            self.landmark_list.append([x, y])
        
        self.left_arm = Arm(self.landmark_list, self.get_angle(12,14,16))
        self.right_arm = Arm(self.landmark_list, self.get_angle(11,13,15))
        self.left_leg = Leg(self.landmark_list, self.get_angle(24,26,28))
        self.right_leg = Leg(self.landmark_list, self.get_angle(23,25,27))

    def get_angle(self,p1,p2,p3):
        get_angle = Get_angle_class(self.landmark_list)
        return get_angle.angle(p1,p2,p3) 
    def get_distance(self,p1,p2):
        get_distance = Get_distance_class(self.landmark_list)
        return get_distance.distance(p1,p2) 

    def is_squat(self):
        left_leg_angle = self.get_angle(24,26,28)
        right_leg_angle = self.get_angle(23,25,27)

        if left_leg_angle <= 130 and right_leg_angle <= 130:
            return "down"
        if left_leg_angle >= 160 and right_leg_angle >= 160:
            return "up"

    def is_pushup(self):
        left_arm_angle = self.get_angle(12,14,16)
        right_arm_angle = self.get_angle(11,13,15)

        if left_arm_angle <= 70 and right_arm_angle <= 70:
            return "down"
        if left_arm_angle >= 150 and right_arm_angle >= 150:
            return "up"

    def is_situp(self):
        left_hip_angle = self.get_angle(12,24,26)
        right_hip_angle = self.get_angle(11,23,25)

        if left_hip_angle >= 125 and right_hip_angle >= 125:
            return "down"
        if left_hip_angle <= 55 and right_hip_angle <= 55:
            return "up"
    
    def is_pullup(self):
        left_arm_angle = self.get_angle(12,14,16)
        right_arm_angle = self.get_angle(11,13,15)

        if left_arm_angle >= 150 and right_arm_angle >= 150:
            return "down"
        if left_arm_angle <= 60 and right_arm_angle <= 60:
            return "up"

class Arm():
    def __init__(self, landmark_list, angle):
        self.landmark_list = landmark_list
        self.angle = angle

    def is_fold(self,angle = 35):
        return self.angle < angle

class Leg():
    def __init__(self, landmark_list, angle):
        self.landmark_list = landmark_list
        self.angle = angle

    def is_fold(self,angle = 40):
        return self.angle < angle

class Get_angle_class():
    def __init__(self, landmark_list):
        self.landmark_list = landmark_list

    def angle(self,p1,p2,p3):
        x1, y1 = self.landmark_list[p1]
        x2, y2 = self.landmark_list[p2]
        x3, y3 = self.landmark_list[p3]

        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -math.atan2(y1 - y2, x1 - x2))

        if angle < 0:
            angle += 360
        if angle > 180:
            angle = 360 - angle

        return angle

class Get_distance_class():
    def __init__(self,landmark_list):
        self.landmark_list = landmark_list

    def distance(self, p1, p2):

        x1, y1 = self.landmark_list[p1]
        x2, y2 = self.landmark_list[p2]

        distance = math.hypot(x2 - x1, y2 - y1)

        return distance


class Camera():
    def __init__(self, path:any=0, width:int = None, height:int = None ) -> None:

        self.camera = cv2.VideoCapture(path)

        if width is None or height is None:     
            self.width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        else:
            self.width = int(width)
            self.height = int(height)

        print("Webcam/Video가 시작되었습니다. 현재 Window의 가로는 {} pixel, 세로는 {} pixel입니다.".format( self.width, self.height))

        self.hand_angle_data, self.hand_knn = self.hand_knn_learn()

        self.mp_pose_single = self.mediapipe_pose()
        self.mp_hand_single = self.meidapipe_hand()
        self.mp_face_single = self.meidapipe_face()

    def mediapipe_pose(self):
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        return pose

    def meidapipe_hand(self):
        mp_hands = mp.solutions.hands
        mp_hand_single = mp_hands.Hands(
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.5)
        return mp_hand_single

    def meidapipe_face(self):
        mp_face_mesh = mp.solutions.face_mesh
        mp_face_single = mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.4, 
            min_tracking_confidence=0.5)
        return mp_face_single

    def hand_knn_learn(self):
        hand_gesture_learn_list = [ 32.647995,27.334458,18.777239,32.558145,149.876268,29.578624,37.800344,133.458050,45.085468,32.342115,142.727088,37.366495,26.056262,139.415512,40.519754,0.000000,
        45.166793,26.117019,18.645196,31.567098,138.965945,20.022370,33.176819,132.806630,21.381263,28.201580,138.854737,14.808465,26.329570,128.394781,23.400235,0.000000,
        20.826588,35.926397,39.943409,20.257126,88.651968,29.781060,17.812546,102.683664,16.751548,11.247996,103.264677,18.000063,15.584646,82.515342,23.045704,0.000000,
        31.327256,24.482902,27.073693,22.894414,64.537885,47.775269,16.256466,89.803293,40.146627,9.443338,91.327471,35.448822,14.446064,71.702363,35.047523,0.000000,
        28.164625,31.028619,23.568194,21.468457,141.750809,21.386416,29.323112,129.772949,38.852031,24.264641,138.309162,33.321451,23.231644,129.452243,30.819853,0.000000,
        39.493933,30.825017,37.798715,48.789407,101.569152,29.543310,62.408973,102.175635,65.566150,59.301602,112.161872,55.427656,60.565796,102.860590,49.489659,0.000000,
        46.636410,27.871526,25.808261,22.547515,69.819060,42.556670,16.971363,85.544017,36.496952,11.288500,75.542530,39.251253,16.539423,48.637377,29.019384,0.000000,
        45.042568,19.961871,11.893033,13.603903,32.278803,27.388893,7.747610,17.797417,5.794515,2.940872,16.492116,1.481793,9.127502,8.934992,6.483260,0.000000,
        47.299112,32.659637,25.455925,33.674011,52.766652,43.792789,29.175726,97.063906,24.384931,27.473441,104.583461,24.572468,32.064351,94.460182,22.230902,0.000000,
        46.483112,30.871050,36.277547,40.493482,96.787611,39.591184,38.159227,110.260392,30.181509,30.411843,119.519070,30.006762,26.418003,122.606342,33.310417,0.000000,
        27.792747,27.346865,18.358880,13.459867,12.675573,14.827358,21.851454,94.371765,35.972556,19.283318,104.185629,31.780360,26.073177,81.116557,33.292727,1.000000,
        35.320273,26.381613,20.191984,14.668020,7.185043,4.248832,25.126893,121.084548,26.620646,24.078772,117.775156,30.698631,30.541078,89.432634,37.903796,1.000000,
        26.048195,19.402587,26.436642,6.365824,9.542588,3.241575,28.086456,113.535227,26.468682,20.288474,116.216192,24.670197,26.922405,95.790580,20.527646,1.000000,
        27.221395,15.414500,25.939750,6.623381,7.608257,2.696879,28.052599,108.763997,27.351137,21.551970,108.780979,26.114410,25.929242,91.324413,21.103923,1.000000,
        32.014172,10.991831,28.415461,5.728636,6.481493,0.889479,23.010316,90.874638,34.321755,12.829574,92.857042,35.219209,11.395936,68.408045,41.629204,1.000000,
        35.391177,18.592058,33.007410,4.140826,6.493375,1.912261,25.824411,100.550619,29.616766,19.956852,99.451776,31.702370,24.273458,82.648994,25.282382,1.000000,
        33.667543,32.918064,19.468711,7.488233,2.724066,7.948471,28.506697,49.497494,13.477383,55.206680,70.580958,23.938099,54.585635,72.790658,27.310205,1.000000,
        34.297057,31.368970,12.617624,12.278204,1.644287,8.980053,30.469056,26.478147,7.106024,52.598374,70.892878,25.786772,42.428934,65.808129,34.571704,1.000000,
        37.283942,26.503899,38.901662,12.471588,1.771188,4.433059,38.654754,109.571409,23.595078,35.738030,105.880785,31.167126,25.614191,107.024708,29.663542,1.000000,
        37.309748,20.163841,29.692652,7.735964,3.484735,2.936218,33.402019,102.752624,25.379006,27.139984,100.369156,26.013738,25.387794,95.077939,19.624609,1.000000,
        27.064267,4.116995,11.001622,16.486113,10.552898,11.181537,14.660537,7.230117,6.805212,5.992467,1.279764,12.949280,2.583446,5.751485,12.190489,2.000000,
        31.191134,4.290191,11.017077,14.137684,3.406932,3.979965,14.172432,62.540096,5.982379,4.602033,33.828657,3.623022,7.488203,11.515055,14.876723,2.000000,
        32.675400,6.051246,9.601219,16.191259,6.049887,3.021566,23.574714,34.476614,52.095947,20.944558,28.680245,10.530155,21.732707,9.850545,3.993437,2.000000,
        36.983640,10.596499,14.782542,8.568285,5.152676,2.903961,20.725178,85.560392,20.407994,15.760408,73.182706,27.857098,16.365531,47.081374,18.958339,2.000000,
        28.553979,4.386473,14.044008,14.800291,8.822664,4.434532,12.653980,85.107713,5.685620,4.419841,57.803916,8.104906,9.925122,21.634206,28.194048,2.000000,
        43.905587,4.436173,6.406616,7.984581,3.269949,4.945221,21.120639,23.389945,11.310605,16.343349,24.295424,15.957736,9.628379,15.356038,23.239797,2.000000,
        47.227182,2.093504,13.185004,10.198872,9.016928,4.762649,30.488841,87.460182,19.246491,31.417656,83.437891,35.377278,26.301992,71.631192,41.428162,2.000000,
        38.963707,3.312926,14.764106,13.346643,2.701027,3.122325,15.783439,70.890089,24.271086,16.162595,55.105191,27.125569,14.065205,31.765137,30.163877,2.000000,
        38.235214,9.765067,12.204059,13.054985,3.186906,6.008764,30.496132,105.006685,19.614097,37.621662,101.843967,33.236817,36.027421,96.934316,33.416261,2.000000,
        44.894136,5.703140,18.672275,16.862815,7.250208,1.171276,27.349864,91.238617,15.085455,31.288754,83.884860,30.505573,32.303599,72.093530,33.306199,2.000000,
        33.233165,5.251370,12.361472,7.406677,2.403716,1.809087,14.060716,1.544563,4.514234,31.659243,100.935772,25.510835,35.251030,89.933031,19.148129,3.000000,
        52.796238,11.266403,14.081873,4.255632,1.900488,2.120873,8.555830,4.423145,2.657591,32.922917,102.226827,22.889829,35.501908,85.247861,24.733276,3.000000,
        45.530282,6.599183,2.705272,11.851240,11.457306,8.534295,10.935138,3.143677,7.689091,40.015122,108.650040,20.131360,44.474448,95.466861,23.438341,3.000000,
        40.178526,5.883763,11.293230,9.412355,5.010292,3.067079,17.325150,5.933416,5.999398,39.241775,112.753544,23.859172,37.437907,104.919452,24.762976,3.000000,
        41.220657,6.328683,11.057584,8.445178,5.794255,1.084988,11.758416,8.098485,5.679773,36.361657,116.513918,16.134616,37.406455,101.434675,18.718483,3.000000,
        58.029470,7.936083,18.771053,7.850386,3.486047,9.073247,6.786294,4.949442,3.565229,34.004830,84.326025,32.755850,41.777266,74.807435,32.737475,3.000000,
        47.655365,6.263117,10.347858,4.807681,4.465829,8.093180,5.107651,1.721795,4.607089,33.309515,102.655187,23.337544,38.665966,107.032195,18.660136,3.000000,
        37.110564,9.127239,10.668107,9.388768,7.970887,9.143346,12.781739,13.336964,6.699117,2.049043,44.085116,10.394698,5.635468,36.843559,23.718730,3.000000,
        38.684006,11.977840,10.109062,4.396552,1.626858,0.703276,12.755652,4.171569,4.843316,33.498154,83.193397,31.964912,32.269514,74.880485,33.148861,3.000000,
        37.850077,11.219031,11.298609,4.051946,5.171304,1.238764,9.662268,7.351379,3.868443,29.601931,85.170091,34.670269,24.091245,67.618521,43.369632,3.000000,
        33.375924,45.897643,44.959032,4.206236,2.510320,3.222605,6.785700,5.948434,5.084050,4.488179,10.262063,2.284405,10.728425,9.843519,2.926731,4.000000,
        42.745151,37.643024,50.160862,5.435130,4.830251,6.826986,5.556171,3.002356,0.205582,4.943730,4.228434,1.315191,14.777243,1.532173,2.396397,4.000000,
        36.649501,39.702291,44.822909,3.642930,8.181224,8.751886,3.456824,9.219551,4.474447,5.561067,16.236727,1.138055,18.158290,4.719707,7.470625,4.000000,
        33.732343,45.422586,55.822462,7.638146,2.152629,4.033472,1.464054,4.268573,1.663308,2.984584,7.626433,3.389159,6.941995,4.292772,5.763352,4.000000,
        38.116837,42.441980,54.622501,5.664158,2.892497,5.785950,4.736157,4.173156,2.245456,4.465982,7.503835,2.509713,12.375703,4.960036,2.874021,4.000000,
        24.033897,40.088233,38.787525,9.386012,9.464247,10.413310,5.538884,8.901695,6.428157,5.607933,8.132257,8.182374,12.767122,4.234681,9.934021,4.000000,
        22.047348,48.635157,48.085973,4.204146,8.782940,8.546689,8.453367,8.064216,4.190607,8.495972,9.646204,6.860789,15.861648,9.336959,7.072326,4.000000,
        33.365355,38.958717,46.813890,9.899286,7.299461,2.715544,9.758196,11.715413,5.594981,17.783596,9.339260,5.354658,18.192992,8.105073,12.362090,4.000000,
        38.594702,38.014552,39.186073,10.419738,4.358816,1.884457,3.774121,6.272337,6.311814,4.514871,3.737852,3.404841,16.175068,7.367417,6.986737,4.000000,
        34.595418,45.275342,38.231041,16.250354,8.341614,3.207451,15.948974,17.222175,0.766148,21.815026,15.449771,4.494622,21.761233,9.026763,6.234337,4.000000,
        35.255824,12.681438,12.162714,1.949913,4.178936,2.694380,5.003759,5.714465,4.993314,2.866081,7.437629,5.021466,6.839853,3.950859,7.966758,5.000000,
        35.381951,6.525500,19.199896,3.555485,5.347654,2.759508,1.414179,4.648061,6.142657,1.858605,7.096097,7.531731,6.483093,6.014813,12.057738,5.000000,
        41.645858,15.220567,8.432321,3.891638,2.995404,3.117573,2.547617,4.607339,4.529059,4.610331,8.582590,3.758644,12.137491,3.805865,7.507453,5.000000,
        31.975783,6.425621,27.088570,1.623824,0.324600,3.288059,4.708754,6.496409,2.555214,3.167269,10.568400,3.977490,5.989966,12.268311,8.626645,5.000000,
        52.354737,15.120519,8.159867,12.150277,3.072984,2.300643,6.897060,7.296752,5.010795,13.108232,14.797280,6.259755,33.110258,40.388509,18.435610,5.000000,
        42.999924,9.240689,12.167061,6.017784,5.659045,3.776685,8.656432,8.790815,2.774698,9.226938,7.683244,2.427294,5.585492,5.957392,7.547471,5.000000,
        43.477665,14.105631,13.982119,10.789480,3.810610,5.423428,6.094256,6.136796,5.340599,8.386305,7.252753,1.856217,5.491802,10.913479,5.328268,5.000000,
        20.702271,10.081805,4.982003,23.877205,7.948928,1.551362,19.273723,11.337202,3.647189,20.742387,9.034537,1.285506,19.839281,4.202442,2.836296,5.000000,
        17.150237,8.940540,9.556369,14.012305,6.129931,4.739453,8.193098,13.911509,5.344650,6.554458,10.177747,5.336161,3.375271,4.698845,3.420790,5.000000,
        39.389713,1.117582,18.518180,2.084555,9.091669,5.572484,4.861925,9.557979,1.797316,8.672537,6.123965,4.182991,5.379867,3.624339,9.622453,5.000000,
        32.768108,9.503798,21.593121,70.120588,79.257446,19.285731,62.786166,89.545887,25.282514,35.479257,113.421803,22.441275,2.555735,2.533934,11.763745,6.000000,
        46.482827,7.663155,23.567131,63.902830,93.346809,22.482054,56.086617,100.846042,23.564547,33.851183,117.178513,25.286268,6.500882,2.959386,19.501039,6.000000,
        38.634087,11.621667,12.321092,65.498904,85.213781,26.907686,64.852347,83.909753,32.034636,62.020283,83.323703,34.953183,29.379008,6.594299,10.074840,6.000000,
        36.741209,5.558563,16.938405,62.598507,83.631724,28.465062,62.411796,78.189144,32.007691,54.511854,86.981567,39.002972,30.600811,3.231690,22.656990,6.000000,
        32.129682,4.522638,20.253860,56.993430,92.831512,27.698204,64.360650,95.358514,25.051703,46.830764,114.904887,27.940107,11.182135,6.640856,21.113219,6.000000,
        44.091949,7.621931,10.947011,55.501159,89.272723,24.395429,55.948755,82.842522,30.297209,38.470464,104.984128,27.955863,14.350666,8.625918,9.942533,6.000000,
        27.479936,4.097992,12.034439,54.818352,83.537471,23.730609,48.670413,87.563799,21.889500,49.545667,79.728856,24.308692,24.089367,8.214144,6.436579,6.000000,
        36.959546,8.284973,14.947872,68.824398,94.120399,21.986314,66.216127,86.226797,19.891681,68.870759,84.502687,33.513477,39.479300,6.941457,13.541512,6.000000,
        31.751109,4.022216,18.241775,50.880285,84.077726,26.394814,47.129386,86.697861,22.057838,45.542544,80.530217,21.078212,23.212825,9.845619,9.567523,6.000000,
        32.046934,2.906928,16.507149,65.617373,85.127539,28.785882,59.764329,87.419937,28.859106,55.605317,84.626147,30.414226,24.107689,8.410958,11.024586,6.000000,
        44.811824,2.247344,16.590034,3.907380,1.037199,5.722256,24.259901,79.244223,50.637637,27.387484,89.464871,38.621035,18.931667,12.572601,2.455508,7.000000,
        37.624495,9.248881,15.595617,13.943688,6.967265,3.055396,23.551784,87.673090,25.656546,26.030782,73.236715,36.542141,17.261648,14.773418,0.548913,7.000000,
        46.128234,4.915813,20.525325,18.394542,5.316863,7.119637,36.039645,100.389825,28.537262,32.345505,93.461557,34.594623,16.737188,8.445271,13.111714,7.000000,
        44.808399,4.501318,15.921841,5.676711,2.912810,3.308981,47.062820,107.593445,23.310176,44.997130,102.337257,28.679087,22.346223,1.190159,15.552526,7.000000,
        26.530469,6.008313,17.595035,18.261555,3.655714,3.716061,38.781065,99.707067,33.522438,39.233322,94.661400,30.749988,17.065474,7.716530,4.521263,7.000000,
        25.322479,18.037882,12.067315,32.241247,4.182720,10.241490,64.298837,85.322581,35.394987,66.325426,85.916786,50.186207,33.529981,4.814649,21.073403,7.000000,
        26.159149,11.137073,9.392574,32.497866,5.530923,21.209995,58.690552,88.162466,44.455593,66.220628,82.889458,53.075216,26.491866,8.719384,20.402972,7.000000,
        27.655743,8.826697,10.426987,24.228312,4.138157,1.587366,43.504149,89.435706,34.546310,49.337679,85.551153,39.430488,23.411189,3.340633,15.438018,7.000000,
        36.260453,2.525784,12.413987,6.889512,1.646308,7.154511,41.815285,94.048841,25.811301,32.851651,98.766322,29.309239,13.612372,3.147535,24.566801,7.000000,
        24.798043,8.936647,9.570077,23.075096,20.969004,7.107377,43.418623,85.495565,23.589483,45.492214,78.922022,23.059844,20.685546,13.108988,7.381683,7.000000,
        24.596646,29.736908,25.081947,8.884024,6.559019,0.456588,29.827859,102.927281,18.240074,12.725527,97.401429,17.777858,15.098036,16.796076,6.547921,8.000000,
        50.252621,28.077263,30.040298,22.374885,2.026989,4.306113,48.841783,103.821814,30.767418,54.614023,96.278374,33.056198,26.596671,9.641538,4.516223,8.000000,
        46.720347,25.202566,24.210076,17.260718,9.712490,3.675929,28.947328,75.844410,28.755709,30.145959,65.809682,40.230338,16.848285,4.840667,8.473947,8.000000,
        28.024332,40.119232,25.496783,13.016671,7.596354,14.071081,32.813221,113.327516,27.055776,24.094514,106.255872,24.239304,2.695157,12.629440,4.089145,8.000000,
        34.887251,22.980568,30.863599,3.881194,2.064988,2.772694,38.137402,103.151437,25.618216,29.328686,97.400949,24.351962,5.864652,4.536465,12.272375,8.000000,
        44.262576,27.125702,15.256883,20.713364,3.406373,9.884314,48.267375,88.476030,29.769608,53.448143,86.022664,36.539874,34.193978,5.617906,18.224099,8.000000,
        34.424282,20.819976,23.608225,11.864899,2.669081,5.032476,42.855215,93.195115,35.297608,43.077306,90.292816,43.513382,13.542847,2.543531,21.420034,8.000000,
        23.015253,23.751870,6.535196,3.763148,11.911140,3.379227,11.032025,87.060834,28.273261,6.145853,86.565476,29.938395,12.812652,48.514888,26.460021,8.000000,
        25.593816,27.246954,20.144459,20.815079,5.138932,12.616756,49.827635,88.011111,33.921899,49.312024,90.373766,37.904222,21.777395,2.446046,13.132388,8.000000,
        25.844453,24.825664,26.760306,17.165493,1.734105,12.963703,47.661407,79.048283,33.757782,44.984442,81.283531,35.549849,6.113230,3.008991,13.152020,8.000000,
        37.490134,32.495884,23.745591,10.263570,5.490865,1.261483,15.089296,8.650429,9.230090,48.912789,79.448029,45.186757,67.013845,71.875879,37.987664,9.000000,
        29.998130,43.524030,25.121150,15.417454,5.852091,7.589172,16.529002,0.725466,7.439875,24.380792,120.390560,19.199350,15.767035,114.411769,15.472736,9.000000,
        34.622599,37.017378,27.669637,2.741039,8.577513,2.243323,14.292178,6.378143,11.999477,45.919511,94.120950,44.025584,55.995302,88.266768,37.774801,9.000000,
        46.051695,54.653762,13.225411,14.781907,10.640506,4.251865,26.399216,6.573900,13.331524,71.594673,72.859317,49.275027,84.113429,61.311140,49.315297,9.000000,
        42.190255,30.782101,19.135231,8.149782,0.703450,2.855704,12.872799,7.649640,10.776583,41.484759,94.828726,26.366485,53.216605,91.162535,30.145703,9.000000,
        38.171631,28.749776,23.954708,7.154842,3.578104,5.526701,9.363086,5.571996,12.836742,43.175990,94.345481,30.334696,56.697473,91.082536,34.231611,9.000000,
        33.777163,44.571014,9.712207,2.335842,12.885402,6.266991,6.820075,3.736563,1.888396,65.052365,84.113728,15.254376,46.649516,92.143424,12.844981,9.000000,
        33.079898,42.409666,15.798544,5.416477,5.498882,2.514304,11.149445,1.194875,2.339769,48.673194,98.541595,16.054597,34.371564,104.661793,14.501611,9.000000,
        40.680805,40.801298,8.909207,5.691228,5.981328,2.100842,4.616145,2.721628,1.298055,40.710221,108.934659,12.880654,35.708418,112.317369,14.130233,9.000000,
        36.514748,45.446515,14.760226,4.549033,8.010085,5.285616,6.942849,0.038435,0.997313,46.468994,97.612162,17.154017,36.863595,107.383317,16.551778,9.000000,
        35.166499,10.133535,24.003586,20.414161,65.397661,53.280209,1.070313,10.611034,5.501693,5.086899,6.810580,2.684862,12.257347,2.932739,6.857893,10.000000,
        27.177540,7.165712,7.382681,27.979051,59.310011,43.088365,5.833023,13.201885,5.084093,5.462635,7.353229,7.037985,20.449650,11.142431,6.311775,10.000000,
        34.202671,12.923296,4.436527,7.954484,69.748850,41.098671,3.179318,9.590110,1.405584,8.344494,5.966596,0.871905,10.470855,2.615677,4.257028,10.000000,
        25.280928,15.253511,41.613189,19.461021,79.660231,45.791824,1.437713,7.270879,2.006402,2.456731,6.494313,1.439689,7.423358,3.559971,7.069693,10.000000,
        20.440146,14.117206,39.528597,16.725306,73.608294,36.204705,12.769179,54.409591,18.337170,9.325091,8.840259,3.291002,10.046129,0.961772,5.568736,10.000000,
        42.600813,1.628398,5.641295,29.320372,59.391940,37.741437,2.664271,1.934314,5.444876,8.683744,1.608252,4.105315,14.743984,4.496544,5.945350,10.000000,
        29.871450,9.303312,17.007823,31.072375,81.973636,33.115093,3.079640,6.669931,2.969039,11.754539,10.396972,5.003912,17.389056,5.201686,6.154532,10.000000,
        38.840654,10.783952,14.997242,40.915437,51.729814,31.135298,3.212290,3.550812,4.857939,13.059346,1.997148,4.008071,22.157437,2.847960,3.501141,10.000000,
        36.957795,16.899360,21.456777,49.829542,76.993500,35.017241,8.948312,8.467755,1.604304,6.864062,5.030107,3.714164,20.978079,4.631371,3.630589,10.000000,
        36.359711,12.904628,12.775588,55.680258,67.934220,28.683606,6.375559,0.552467,4.157252,14.441847,1.584075,2.392591,33.491625,6.145185,1.497830,10.000000 ]

        file = np.reshape(hand_gesture_learn_list, (110,16))
        
        hand_angle_data = file[:,:-1].astype(np.float32)
        label = file[:, -1].astype(np.float32)
        knn = cv2.ml.KNearest_create()
        knn.train(hand_angle_data, cv2.ml.ROW_SAMPLE, label)

        return hand_angle_data, knn

    def is_opened(self, close_key: int or str = 27) -> bool:
        if not self.camera.isOpened():
            return False

        ret, img = self.camera.read()

        if not ret:
            return False

        if len(str(close_key)) == 1:
            close_key = ord(close_key)
            if cv2.waitKey(20) & 0xFF == close_key:
                return False
        else:
            if cv2.waitKey(20) & 0xFF == close_key:
                return False

        self.frame = img
        self.frame = cv2.resize(self.frame, (self.width, self.height), interpolation=cv2.INTER_CUBIC)

        return True

    def get_frame(self, mirror_mode = True):

        if mirror_mode is True:
            self.frame = cv2.flip(self.frame, 1)

        return self.frame

    def show(self, frame, window_name = "Window"):
        return cv2.imshow(window_name, frame)

    def get_angle(self,p1,p2,p3):
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -math.atan2(y1 - y2, x1 - x2))

        if angle < 0:
            angle += 360
        if angle > 180:
            angle = 360 - angle

        return angle

    def get_distance(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        distance = math.hypot(x2 - x1, y2 - y1)

        return distance

    def show_text(self, x = 30, y = 50, font_size = 1, color = "black", text = "text"):
        text = str(text)

        if color == "green":
            color = (0,255,0)
        elif color == "blue":
            color = (255,0,0)
        elif color == "red":
            color = (0,0,255)
        elif color == "black":
            color = (0,0,0)
        elif color == "white":
            color = (255,255,255)

        self.frame = cv2.putText(self.frame, text, org=(int(x), int(y)),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=font_size, color=color, thickness=3)

    ### draw face

    def draw_faces(self, faces):
        for face in faces:
            cv2.rectangle(self.frame, (int(round(face.x1)), int(round(face.y1))),
                    (int(round(face.x2)),int(round(face.y2))),
                    (0,255,0), 3)
    
    def draw_lips(self, faces):
        for face in faces:
            for i in range( len( face.lipsUpper_list )):
                face.lipsUpper_list[i][0] =  round(face.lipsUpper_list[i][0] * self.width)
                face.lipsUpper_list[i][1] =  round(face.lipsUpper_list[i][1] * self.height)
                face.lipsLower_list[i][0] =  round(face.lipsLower_list[i][0] * self.width)
                face.lipsLower_list[i][1] =  round(face.lipsLower_list[i][1] * self.height)

            lips_upper_points = np.array( face.lipsUpper_list, np.int32 )
            lips_lower_points = np.array( face.lipsLower_list, np.int32 )

            self.frame = cv2.polylines( self.frame, [lips_upper_points], False, (0,255,0), 2 )
            self.frame = cv2.polylines( self.frame, [lips_lower_points], False, (0,255,0), 2 )

    def draw_eyes(self, faces):
       for face in faces:
            left_eye_c_x = round(face.left_eye.center_x)
            left_eye_c_y = round(face.left_eye.center_y)
            left_eye_width = round(face.left_eye.width*0.5)
            left_eye_height = round(face.left_eye.height*0.5)

            right_eye_c_x = round(face.right_eye.center_x)
            right_eye_c_y = round(face.right_eye.center_y)
            right_eye_width = round(face.right_eye.width*0.5)
            right_eye_height = round(face.right_eye.height*0.5)

            left_eye_points = cv2.ellipse2Poly( (left_eye_c_x, left_eye_c_y),(left_eye_width,left_eye_height), 0, 0, 360, 30 )
            self.frame = cv2.polylines( self.frame, [left_eye_points], False, (0,255,0), 2 )

            right_eye_points = cv2.ellipse2Poly( (right_eye_c_x, right_eye_c_y),(right_eye_width,right_eye_height), 0, 0, 360, 30 )
            self.frame = cv2.polylines( self.frame, [right_eye_points], False, (0,255,0), 2 )

    def draw_irides(self, faces):
       for face in faces:
            self.frame = cv2.circle( self.frame, ( round(face.left_iris.center_x) , round(face.left_iris.center_y) ),
                                round( min( [face.left_iris.width, face.left_iris.height] ) * 0.5 ), (0,255,0), 2 )
            self.frame = cv2.circle( self.frame, ( round(face.right_iris.center_x) , round(face.right_iris.center_y) ),
                                round( min( [face.left_iris.width, face.left_iris.height] ) * 0.5 ), (0,255,0), 2 )

    def show_direction(self, faces):
        for face in faces:
            # self.frame = cv2.putText(self.frame, face.head_pose.text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

            self.frame = cv2.putText(self.frame, face.head_pose.text, org=(int(face.x1), int(face.y1 - 15)),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 0), thickness=2)

    ### draw_hand

    def draw_hands(self, hands):
        thumb_list = [0,1,2,3,4]
        index_list = [0,5,6,7,8]
        middle_list = [9,10,11,12]
        ring_list = [13,14,15,16]
        pinky_list = [0,17,18,19,20]
        bridge_list = [5,9,13,17]

        temp_list = [ thumb_list, index_list, middle_list, ring_list, pinky_list, bridge_list ]

        for hand in hands:
            for j in range(len(temp_list)):
                for i in range(len(temp_list[j])-1):
                    self.frame = cv2.line( self.frame, ( hand.landmark_list[temp_list[j][i]][0] , hand.landmark_list[temp_list[j][i]][1] ),
                                        ( hand.landmark_list[temp_list[j][i+1]][0] , hand.landmark_list[temp_list[j][i+1]][1] ), (0,255,0), 3 )

            for i in range(21):
                self.frame = cv2.circle(self.frame, (hand.landmark_list[i][0] , hand.landmark_list[i][1]), 4, (255, 0, 255), cv2.FILLED)

    def show_gesture(self, hands):
        for hand in hands:
            
            text = hand.detect_gesture()
            gesture = hand.gesture_dict

            if text in gesture.values():
                self.frame = cv2.putText(self.frame, text.lower(), org=(int(hand.landmark_list[0][0]), int(hand.landmark_list[0][1] + 25)),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)
    
    def show_distance(self, hands):
        for hand in hands:
            x,y,w,h = hand.bbox
            distanceCM = hand.get_distance()
            self.frame = cv2.rectangle(self.frame,(x,y), (x+w, y+h), (255,0,255),3 )
            self.frame = cv2.putText(self.frame, text= f'{int(distanceCM)} cm', org=(int(x+5), int(y-10)),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)

    ### draw body

    def draw_body(self, body):
        face_upper_list = [8,6,5,4,0,1,2,3,7]
        face_lower_list = [10,9]
        hand_list = [18,16,14,12,11,13,15,17]
        left_finger_list = [18,20,16,22]
        right_finger_list = [17,19,15,21]
        body_list = [12,24,23,11]
        left_leg = [24,26,28,30,32,28]
        right_leg = [23,25,27,29,31,27]

        temp_list = [ face_upper_list, face_lower_list, hand_list, left_finger_list, right_finger_list, body_list, left_leg, right_leg ]

        for body in body:
            for j in range(len(temp_list)):
                for i in range(len(temp_list[j])-1):
                    self.frame = cv2.line( self.frame, ( body.landmark_list[temp_list[j][i]][0] , body.landmark_list[temp_list[j][i]][1] ),
                                        ( body.landmark_list[temp_list[j][i+1]][0] , body.landmark_list[temp_list[j][i+1]][1] ), (0,255,0), 3 )

            for i in range(33):
                self.frame = cv2.circle(self.frame, (body.landmark_list[i][0] , body.landmark_list[i][1]), 4, (255, 0, 255), cv2.FILLED)



    ### detect face

    def detect_face(self, frame, draw_face = True, draw_lips = True, draw_eyes = True, draw_irides = True,
                        show_direction = True) -> object or None:

        # mp_face_mesh = mp.solutions.face_mesh

        # face = []
        # max_num_face = 1

        # with mp_face_mesh.FaceMesh(
        #     max_num_faces=max_num_face,
        #     refine_landmarks=True,
        #     min_detection_confidence=0.4, 
        #     min_tracking_confidence=0.5) as face_mesh:

        face = []
        max_num_face = 1

        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_face_single.process(frame)

        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:  
                face.append( Face(face_landmarks, frame) )

        if draw_face:
            self.draw_faces(face)
        if draw_lips:
            self.draw_lips(face)
        if draw_eyes:
            self.draw_eyes(face)
        if draw_irides:
            self.draw_irides(face)
        if show_direction:
            self.show_direction(face)

        if len(face) == 1 and max_num_face == 1:
            return face[0]

        return None

    def detect_faces(self, frame, max_num_faces = 99, draw_faces =True, draw_lips = True, draw_eyes = True, draw_irides = True,
                    show_direction = True) -> list:
 
        mp_face_mesh = mp.solutions.face_mesh  

        faces = []

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
                        faces.append( Face(face_landmarks,frame) )

        if draw_faces:
            self.draw_faces(faces)
        if draw_lips:
            self.draw_lips(faces)
        if draw_eyes:
            self.draw_eyes(faces)
        if draw_irides:
            self.draw_irides(faces)
        if show_direction:
            self.show_direction(faces)

        return faces

    ### detect_hand
    def detect_hand(self, frame, draw_hand = True, show_gesture = False, show_distance = False):
        mp_hands = mp.solutions.hands

        hand = []
        max_num_hand = 1

        # with mp_hands.Hands(
        #     max_num_hands=max_num_hand,
        #     model_complexity=0,
        #     min_detection_confidence=0.6,
        #     min_tracking_confidence=0.5) as detect_hands:

        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_hand_single.process(frame)

        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                hand.append( Hand(hand_landmarks, frame, self.hand_angle_data, self.hand_knn) )

        if draw_hand:
            self.draw_hands(hand)
        if show_gesture:
            self.show_gesture(hand)
        if show_distance:
            self.show_distance(hand)

        if len(hand) == 1 and max_num_hand == 1:
            return hand[0]

        return None

    def detect_hands(self, frame, max_num_hands = 99, draw_hands = True, show_gesture = False, show_distance = False):
        mp_hands = mp.solutions.hands

        hands = []

        self.num = max_num_hands

        with mp_hands.Hands(
            max_num_hands=max_num_hands,
            model_complexity=0,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.5) as detect_hands:

                frame.flags.writeable = False
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = detect_hands.process(frame)

                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        hands.append( Hand(hand_landmarks, frame, self.hand_angle_data,self.hand_knn) )

        if draw_hands:
            self.draw_hands(hands)
        if show_gesture:
            self.show_gesture(hands)
        if show_distance:
            self.show_distance(hands)

        return hands


    def detect_body(self, frame, draw_body = True):
        body = []

        # with mp_pose.Pose(
        #     model_complexity=0,
        #     min_detection_confidence=0.5,
        #     min_tracking_confidence=0.5) as pose:

        #         frame.flags.writeable = False
        #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #         results = pose.process(frame) 

        #         frame.flags.writeable = True
        #         frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        #         if results.pose_landmarks:
        #             body.append( Body(results.pose_landmarks, self.width, self.height) )

        # pose = mp_pose.Pose(
        #     model_complexity=0,
        #     min_detection_confidence=0.5,
        #     min_tracking_confidence=0.5)

        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_pose_single.process(frame) 

        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            body.append( Body(results.pose_landmarks, self.width, self.height) )

        if draw_body:
            self.draw_body(body)

        if len(body) == 1:
            return body[0]

        return None


