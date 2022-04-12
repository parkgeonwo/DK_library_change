from dynamikontrol import Module
import cv2
import mediapipe as mp
# https://github.com/tensorflow/tfjs-models/blob/master/facemesh/mesh_map.jpg

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

cap = cv2.VideoCapture(0)

module = Module()

with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACE_CONNECTIONS,
                    landmark_drawing_spec=drawing_spec,
                    connection_drawing_spec=drawing_spec)

                lip_upper = face_landmarks.landmark[13].y
                lip_lower = face_landmarks.landmark[14].y

                gap = -int(abs(lip_lower - lip_upper) * 1500)
                print(gap)
                module.motor.angle(gap, period=0.1)

        cv2.imshow('Mouth Robot', image)
        if cv2.waitKey(1) == ord('q'):
            break

cap.release()
