
###################################### 

# import Camera_module

# camera = Camera_module.Camera()
# # camera = Camera_module.Camera(path="/home/matrix/Desktop/code/video2.mp4")

# while camera.is_opened(): 
#     frame = camera.get_frame()
#     camera.show(frame)


############################################

from dynamikontrol import Module
from Camera import Camera
import time
import mediapipe as mp
import cv2
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# module = Module()
# # camera = Camera(path='/home/matrix/Desktop/code/DK_library_change/video2.mp4')
camera = Camera()
pTime = 0


while camera.is_opened():
    frame = camera.get_frame()

    # body = camera.detect_body(frame)
    hand = camera.detect_hands(frame,max_num_hands = 2)

    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime
    print(fps)

    # face = camera.detect_face(frame)
    # hand = camera.detect_hand(frame)

    camera.show(frame)

# module.disconnect()

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


