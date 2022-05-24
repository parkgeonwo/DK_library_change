# from dynamikontrol import Module
# import time

# module = Module()

# module.motor.speed(4800)
# time.sleep(3)
# module.motor.stop()

# module.disconnect()


##############################3

import cv2
import mediapipe as mp
import math
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose



# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('/home/matrix/Desktop/code/DK_library_change/squat.mp4')

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      break

    image = cv2.flip(image, 1)

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

    landmark_list = []
    if results.pose_landmarks:
        for id, lm in enumerate(results.pose_landmarks.landmark):
            x, y, z = lm.x, lm.y, lm.y
            landmark_list.append([x, y, z])

        start, middle, end = 23,25,27

        print( landmark_list[start][2], landmark_list[middle][2], landmark_list[end][2] )

        v1 = [ landmark_list[start][i] - landmark_list[middle][i] for i in range(3) ]
        v2 = [ landmark_list[end][i] - landmark_list[middle][i] for i in range(3) ]

        v_in = v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

        s_v1=math.sqrt(pow(v1[0],2)+pow(v1[1],2)+pow(v1[2],2))
        s_v2=math.sqrt(pow(v2[0],2)+pow(v2[1],2)+pow(v2[2],2))

        if v_in == 0:
            print("사이각:0(단위:deg)")
        else:
            print("사이각:%.4g(단위:deg)"%(math.degrees(math.acos(v_in/(s_v1*s_v2)))))

    cv2.imshow('MediaPipe Pose',image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()








