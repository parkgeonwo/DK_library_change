
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

module = Module()
# camera = Camera(path='/home/matrix/Desktop/code/video2.mp4')
camera = Camera()

while camera.is_opened():
    frame = camera.get_frame()

    face = camera.detect_face(frame)

    if face:
        if face.look_left() or face.look_right():
            module.motor.angle(-50)
            module.motor.angle(50, period = 2)

    # if face:
    #     if face.is_located_left():
    #         angle += 3
    #         module.motor.angle(angle)
    #     elif face.is_located_right():
    #         angle -= 3
    #         module.motor.angle(angle)

    camera.show(frame)

module.disconnect()


###########################################

# import cv2
# import mediapipe as mp
# mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
# mp_face_mesh = mp.solutions.face_mesh

# # For webcam input:
# drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
# cap = cv2.VideoCapture(0)
# with mp_face_mesh.FaceMesh(
#     max_num_faces=1,
#     refine_landmarks=True,
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5) as face_mesh:
#   while cap.isOpened():
#     success, image = cap.read()
#     if not success:
#       print("Ignoring empty camera frame.")
#       # If loading a video, use 'break' instead of 'continue'.
#       continue

#     image = cv2.flip(image, 1) # mirror image

#     # To improve performance, optionally mark the image as not writeable to
#     # pass by reference.
#     image.flags.writeable = False
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     results = face_mesh.process(image)

#     # Draw the face mesh annotations on the image.
#     image.flags.writeable = True
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#     if results.multi_face_landmarks:
#       for face_landmarks in results.multi_face_landmarks:
#         mp_drawing.draw_landmarks(
#             image=image,
#             landmark_list=face_landmarks,
#             connections=mp_face_mesh.FACEMESH_TESSELATION,
#             landmark_drawing_spec=None,
#             connection_drawing_spec=mp_drawing_styles
#             .get_default_face_mesh_tesselation_style())
#         mp_drawing.draw_landmarks(
#             image=image,
#             landmark_list=face_landmarks,
#             connections=mp_face_mesh.FACEMESH_CONTOURS,
#             landmark_drawing_spec=None,
#             connection_drawing_spec=mp_drawing_styles
#             .get_default_face_mesh_contours_style())
#         mp_drawing.draw_landmarks(
#             image=image,
#             landmark_list=face_landmarks,
#             connections=mp_face_mesh.FACEMESH_IRISES,
#             landmark_drawing_spec=None,
#             connection_drawing_spec=mp_drawing_styles
#             .get_default_face_mesh_iris_connections_style())

#         # left_eye
#         eye_upper = face_landmarks.landmark[159].y
#         eye_lower = face_landmarks.landmark[145].y
#         eye_left = face_landmarks.landmark[33].x
#         eye_right = face_landmarks.landmark[133].x

#         eye_width = eye_right-eye_left
#         eye_height = abs(eye_upper - eye_lower)

#         eye_center = eye_left + eye_width * (1/2)

#         # right iris 473, 474, 475, 476, 477       center / right / lower / left / up
#         # left iris 468, 469, 470, 471, 472      center / right / lower / left / up

#         ir1 = face_landmarks.landmark[468].x
#         # ir2 = face_landmarks.landmark[469].x
#         # ir3 = face_landmarks.landmark[470].x
#         # ir4 = face_landmarks.landmark[471].x
#         # ir5 = face_landmarks.landmark[472].x

#         print(ir1, eye_left, eye_width*0.3)

#         if ir1 <= eye_left + eye_width*0.35:        # face.left_eye.x1 + face.left_eye.width*0.35
#             print("공부해라1")
#         elif ir1 >= eye_right - eye_width*0.35:
#             print("공부해라2")



#     # Flip the image horizontally for a selfie-view display.
#     cv2.imshow('MediaPipe Face Mesh', image)
#     if cv2.waitKey(5) & 0xFF == 27:
#       break
# cap.release()






