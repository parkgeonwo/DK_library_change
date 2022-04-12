import cv2
import mediapipe as mp
from dynamikontrol import Module

ANGLE_STEP = 1     # 1도 단위로 움직이게 만들기

module = Module()       # dk 모듈 불러오기

mp_drawing = mp.solutions.drawing_utils
mp_face_detection = mp.solutions.face_detection

face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.7)       # 검출에 성공한 것으로 간주할 얼굴의 검출 모델의 신뢰값 # 기본값 0.5

cap = cv2.VideoCapture(0)    # 웹캠 키기
angle = 0 # motor current angle

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    img = cv2.flip(img, 1) # mirror image

    results = face_detection.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))     # BGR img를 RGB로 변환합니다. --> 변환 후 face 검출을 진행한것을 results

    if results.detections:      # results의 detections가 탐지되면
        for detection in results.detections:
            mp_drawing.draw_detection(img, detection)     # img에 detection을 그려준다.

            x1 = detection.location_data.relative_bounding_box.xmin # left side of face bounding box
            x2 = x1 + detection.location_data.relative_bounding_box.width # right side of face bounding box
            # print(x1)    # 0.3323525~~            
            # print(x2)    # 

            cx = (x1 + x2) / 2 # center of the face

            if cx < 0.4: # left -> clockwise
                angle += ANGLE_STEP
                module.motor.angle(angle)
            elif cx > 0.6: # right -> counter clockwise
                angle -= ANGLE_STEP
                module.motor.angle(angle)

            cv2.putText(img, '%d deg' % (angle), org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=255, thickness=2)

            break

    cv2.imshow('Face Cam', img)     # img를 실시간으로 출력 / 제목은 "Face Cam"
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
face_detection.close()
module.disconnect()


########### 설명
# x1, x2 를 각각 얼굴 바운딩 박스의 왼쪽 위 좌표, 오른쪽 아래 좌표라고 가정하고, cx 를 얼굴의 중심 좌표라고 가정합시다.
# Mediapipe는 좌표를 입력 이미지의 상대 좌표로 반환하므로 cx 의 값 범위는 0.0 에서 1.0 사이가 될 것입니다.
# 예를 들어 이미지 안에서 얼굴이 정중앙에 위치한다면 cx 의 값은 0.5 가 됩니다.


############ 네이버 카페
# mediapipe를 사용해서 얼굴을 인식하면 그 결과값으로 bounding box (바운딩박스) 가 나오는데요.
# 바운딩 박스란 얼굴의 위치를 표시한 사각형입니다. 바운딩 박스 값의 범위는 0 ~ 1 사이의 값을 가집니다.


# 여기서 우리는 얼굴 사각형의 왼쪽 좌표인 x1 과 오른쪽 좌표인 x2 를 구해서 얼굴의 중심 좌표 cx를 구할거에요.
# 만약 cx의 값이 가 0.5라면 카메라를 기준으로 얼굴은 정중앙에 위치하게 되는 거겠죠?

# cx = (x1 + x2) / 2
# 중심 좌표 cx를 구했다면, 이제 모터를 움직이는 코드만 작성하면 됩니다.
# 만약 얼굴이 왼쪽으로 치우쳐져 있다면 (cx < 0.4), 화면을 왼쪽으로 움직여야 하니, 모터를 시계방향으로 회전하게 하면 되겠죠?

# 반대로 얼굴이 오른쪽으로 치우쳐져 있다면 (cx > 0.6), 화면을 오른쪽으로 움직여야 하니, 모터를 반시계방향으로 돌려줍니다.

# ANGLE_STEP 은 위에서 1로 지정해두었으니 1도 단위로 움직이게 될 거에요. angle 변수에 ANGLE_STEP 을 더해주거나 빼주어서 얼굴 위치를 반영한 각도를 따라가도록 만들어주면 끝!




########## 웹캠 실행

# cap = cv2.VideoCapture(0)
# while cap.isOpened():
#     ret, frame = cap.read()
#     cv2.imshow('Mediapipe Feed', frame)
    
#     if cv2.waitKey(10) & 0xFF == 27: # esc 키를 누르면 닫음
#         break
        
# cap.release()


#############################

















