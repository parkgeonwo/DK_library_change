import cv2
import mediapipe as mp
import time
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# ### For webcam input:     # pose with를 안에넣은것  # fps 9
# cap = cv2.VideoCapture(0)
# pTime = 0

# while cap.isOpened():
#   success, image = cap.read()
#   if not success:
#     print("Ignoring empty camera frame.")
#     continue

#   with mp_pose.Pose(
#       model_complexity=0,
#       min_detection_confidence=0.5,
#       min_tracking_confidence=0.5) as pose:

#         image.flags.writeable = False
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         start = time.time()
#         results = pose.process(image)
#         print("time : ", time.time() - start)

#         image.flags.writeable = True
#         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#         mp_drawing.draw_landmarks(
#             image,
#             results.pose_landmarks,
#             mp_pose.POSE_CONNECTIONS,
#             landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

#   cTime = time.time()
#   fps = 1 / (cTime-pTime)
#   pTime = cTime
#   print(fps)

#   cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
#   if cv2.waitKey(5) & 0xFF == 27:
#     break
# cap.release()



# # For webcam input:      # pose 원본 코드 fps 30
import time
import cv2
cap = cv2.VideoCapture(0)
pTime = 0

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue

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

    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime
    print(fps)

    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()




####### hand with 안에 넣은것   ## fps 19~20

# import cv2
# import mediapipe as mp
# import time
# mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
# mp_hands = mp.solutions.hands

# pTime = 0

# # For webcam input:
# cap = cv2.VideoCapture(0)

# while cap.isOpened():
#   success, image = cap.read()
#   if not success:
#     print("Ignoring empty camera frame.")
#     continue

#   with mp_hands.Hands(
#   model_complexity=0,
#   min_detection_confidence=0.5,
#   min_tracking_confidence=0.5) as hands:
#       image.flags.writeable = False
#       image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#       results = hands.process(image)

#       image.flags.writeable = True
#       image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#       if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#           mp_drawing.draw_landmarks(
#               image,
#               hand_landmarks,
#               mp_hands.HAND_CONNECTIONS,
#               mp_drawing_styles.get_default_hand_landmarks_style(),
#               mp_drawing_styles.get_default_hand_connections_style())

#   cTime = time.time()
#   fps = 1 / (cTime-pTime)
#   pTime = cTime
#   print(fps)

#   cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
#   if cv2.waitKey(5) & 0xFF == 27:
#     break
# cap.release()







# For webcam input:       # fps 30

# import cv2
# import mediapipe as mp
# import time
# mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
# mp_hands = mp.solutions.hands

# pTime = 0

# cap = cv2.VideoCapture(0)
# with mp_hands.Hands(
#     model_complexity=0,
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5) as hands:
#   while cap.isOpened():
#     success, image = cap.read()
#     if not success:
#       print("Ignoring empty camera frame.")
#       # If loading a video, use 'break' instead of 'continue'.
#       continue

#     # To improve performance, optionally mark the image as not writeable to
#     # pass by reference.
#     image.flags.writeable = False
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     results = hands.process(image)

#     # Draw the hand annotations on the image.
#     image.flags.writeable = True
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#     if results.multi_hand_landmarks:
#       for hand_landmarks in results.multi_hand_landmarks:
#         mp_drawing.draw_landmarks(
#             image,
#             hand_landmarks,
#             mp_hands.HAND_CONNECTIONS,
#             mp_drawing_styles.get_default_hand_landmarks_style(),
#             mp_drawing_styles.get_default_hand_connections_style())
#       cTime = time.time()
#       fps = 1 / (cTime-pTime)
#       pTime = cTime
#       print(fps)
#     cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
#     if cv2.waitKey(5) & 0xFF == 27:
#       break
# cap.release()










