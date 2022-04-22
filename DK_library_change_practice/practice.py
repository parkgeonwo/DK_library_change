
# class MyStatus: 
#     def __init__(self,age,name,height,weight): 
#         # self.age = age 
#         # self.name = name
#         # self.height = height
#         # self.weight = weight 
#     def print_name(self):
#         print(self.name)
#     def print_age(self):
#         print(self.age)
#     def print_height(self):
#         print(self.height)
#     def print_weight(self):
#         print(self.weight)

# a = MyStatus(34,"yamada",170,78)

# a.print_age()






import cv2
import mediapipe as mp
from dynamikontrol import Module

ANGLE_STEP = 1

module = Module()

mp_drawing = mp.solutions.drawing_utils
mp_face_detection = mp.solutions.face_detection

face_detection = mp_face_detection.FaceDetection(
    min_detection_confidence=0.5)

cap = cv2.VideoCapture("video2.mp4")
angle = 0 # motor current angle

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    img = cv2.flip(img, 1) # mirror image

    results = face_detection.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(img, detection)

            x1 = detection.location_data.relative_bounding_box.xmin # left side of face bounding box
            x2 = x1 + detection.location_data.relative_bounding_box.width # right side of face bounding box

            cx = (x1 + x2) / 2 # center of the face

            # if cx < 0.4: # left -> clockwise
            #     angle += ANGLE_STEP
            #     module.motor.angle(angle)
            # elif cx > 0.6: # right -> counter clockwise
            #     angle -= ANGLE_STEP
            #     module.motor.angle(angle)

            cv2.putText(img, '%d deg' % (angle), org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=255, thickness=2)

            

    cv2.imshow('Face Cam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
face_detection.close()
module.disconnect()


list = [1,3,5,-1]
print( list.index(max(list)) )










