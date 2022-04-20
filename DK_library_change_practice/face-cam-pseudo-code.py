
###############################
# //작성순서3 :
# //1. 파일의 끝이 아닌 동안 방복한다.(반복)
# //  1.1 이름 국어, 영어점수를 입력받는다.
# //  1.2 번호를 매긴다.
# //  1.3 총점을 구한다.
# //  1.4 평균을 구한다.
# //  1.5 평균이 70점 이상인지 판단한다.(선택/분기)
# //    1.5.1 참이면 통과한 것으로 판단
# //    1.5.2 거짓이면 실패인 것으로 판단
# //  1.6 평가를 출력한다.
# //2. 끝낸다.
###############################

###############################
# //작성순서2 :
# //1. n까지 반복하여 더한다.
# //  1.1 반환할 변수 sum 을 선언하고 0을 대입한다.
# //  1.2 n을 입력받는다.
# //  1.3 sum에 0부터 1씩 더한다.
# //  1.4 n번째 1을 더했을 때 멈춘다.
# //2. 저장된 sum 값을 반환한다.
###############################


from dynamikontrol import Module
module = Module()       # dk 모듈 불러오기


# 캠시작하기 cam.start( cam_index,  mirror_mode , cam_name , quit_string )         # cam size까지 넣을지 말지는 고민
# 캠시작하기 cam.start( 0 or 1,  o or 1, "Face Cam", 알파벳 )    # 캠만 키는거
                                                                # 웹캠을킬지 카메라를 킬지 / 좌우반전을 할지 안할지 / webcam 이름 / 알파벳 뭘누르면 꺼질지 

# output 이 img = cv2.cvtColor( img, cv2.COLOR_BGR2RGB ) 까지 진행한 img


# cam = Camera(id=0, width=400, height=300)

# 브레드의 예시
while cam.is_opened():
    img = cam.read()

    x, y, w, h = cam.detect_face(img)

    if x > 0.4:
        module.motor.angle(12310)
    elif x < 0.6:
        module.motor.angle(12313)

    cam.show(img)

cam.release()



############################## 변경 전 코드 #############################

import cv2

cap = cv2.VideoCapture(0)    # 웹캠 키기

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    img = cv2.flip(img, 1) # mirror image

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    cv2.imshow('title', img)     # img를 실시간으로 출력 / 제목은 "arg"
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 캠 끄기 cam.end()
cap.release()



################################## 변경 후 코드 #########################

# 한 줄로 캠을 킬 수 있으면 좋겠지만 캠에 얼굴인식, 손인식등을 넣으려면 나눠야할것 같다.

from dynamikontrol import Module, cam

cam = cam.start("cam_index = 0 or 1")              # 캠시작

cam.size( width = 300, height = 400 )              # 캠사이즈 변경

while cam.open():                                     # 캠 오픈
    img = cam.to_img( "mirror_mode = 0 or 1" )        # 캠 --> img
    cam.show( img , "cam_name", "quit_string" )       # 보여주기

cam.end()




############################### 2차 변경 ######################################


from dynamikontrol import Module, Camera

Camera = Camera.start()           # cam_choice = 0,1 기본값 0 / width 기본값 600 / height 기본값 500
## setup 수정

while Camera.isOpened():
    img = Camera.read()        # mirror_mode = 0 or 1 기본값 1 / 기본값 BGR  선택사항 RGB, GRAY, HSV 등등
    Camera.imshow(img)           #  img / cam_name 기본값 "WebCam" / quit_string 기본값 "q"


## 다른사람 라이브러리 많이 참고 해보자 / 메이저한 라이브러리 참고
## 직관적, 많이사용하는 라이브러리 따라가보기
## 코드가 사용자들에게 보이기때문에 신경을 쓰자























################################## 변경전 코드 #########################

import cv2
import mediapipe as mp

ANGLE_STEP = 1     # 1도 단위로 움직이게 만들기

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




################################## 변경후 코드 #########################

from dynamikontrol import Module, cam

ANGLE_STEP = 1     # 1도 단위로 움직이게 만들기

face_cam = cam.face.start(min_detection_confidence=0.7)        # output = face_detection

cam = cam.start("cam_index = 0 or 1")   

while cam.open():
    img = cam.to_img(  "mirror_mode = 0 or 1" )

    results = face_cam.detect(img)
    x1 , x2 , cx = results.location

    if cx < 0.4:
        angle += ANGLE_STEP
        module.motor.angle(angle)


    results.move( ANGLE_STEP, "direction = x or y or xy", angle ) 

    cam.show( img , "cam_name", "quit_string" )

cam.end()

# 로직 얼굴의 위치가 어딘지 알수있다.







######################## 변경 후 : 모듈이 두개에 x y 방향으로 둘다 움직일때 #################

from dynamikontrol import Module, cam

ANGLE_STEP = 1

module_yaw = Module(serial_no='aa000000') # Put your module Serial No.
module_pitch = Module(serial_no='ab000000') # Put your module Serial No.

face_cam = cam.face.start(min_detection_confidence=0.7)        # output = face_detection

cam = cam.start("cam_index = 0 or 1")   


while cam.open():
    img = cam.to_img(  "mirror_mode = 0 or 1" )

    results = face_cam.detect(img)
    results.move( ANGLE_STEP, "direction = x or y or xy", angle_yaw = 0, angle_pitch = 0, module_num = 0, module_num2 = 0 ) 

    cam.show( img , "cam_name", "quit_string" )

cam.end()





# 컨벤션, 클래스, 첫글자 대문자 , Camera라고 명시
####################### 2차 변경 ##############################


from dynamikontrol import Module, Camera

Camera = Camera.start()           # cam_choice = 0,1 기본값 0 / width 기본값 600 / height 기본값 500

face_detection = Camera.face_detection()        # min_detection_confidence 0.5 기본값 / 

# angle 변수 필요
# angle의 변수가 왜필요한지 
# 현재 위치도 모르고 변화하는걸 알려주기위해서

angle = 0 # motor current angle

while Camera.isOpened():
    img = Camera.read()        # mirror_mode = 0 or 1 기본값 1 / 기본값 BGR  선택사항 RGB, GRAY, HSV 등등

    c_x, c_y, w, h = face_detection.process(img)         # max_num_faces = 1, 2,, 기본값 1 / step_angle = 1, 2,, 기본값 1
     

    # face_detection , img 에 들어가는게 이상하다. 따로 모듈을 만들어주던가 camera와 연결
    # 계산최대한 적게
    # 동사 + 명사 형식으로 바꾸기 / 복수 까지 고려해야한다. / detect_faces
    # face 여러개 하는거도 고려해야한다.

    if c_x < 0.4:
        module.motor.angle(  )         # 여길 어떻게할까??????????
    elif c_x > 0.6:
        module.motor.angle(  ) 

    Camera.imshow(img)           #  img / cam_name 기본값 "WebCam" / quit_string 기본값 "q"

# opencv 변수나 함수와도 맞춰보기
# 교과서 만들기




######################## 최종 ###########################


from dynamikontrol import Module, Camera

camera = Camera()           # cam_index = 0,1 기본값 0 / width 화면 최대 / height 화면 최대

while camera.is_opened():
    img = camera.read()        # mirror_mode = 1 기본값 1 
    camera.show(img)           #  img / cam_name 기본값 "WebCam" / #cam_cancel_key 기본값 "esc"


## 다른사람 라이브러리 많이 참고 해보자 / 메이저한 라이브러리 참고
## 직관적, 많이사용하는 라이브러리 따라가보기
## 코드가 사용자들에게 보이기때문에 신경을 쓰자


#####################################################


from dynamikontrol import Module, Camera

camera = Camera.start()           # cam_index = 0,1 기본값 0 / width 기본값 최대값 / height 기본값 최대값 / 동영상 추가
                                    # 변수명

# faces_detection = Camera.faces_detection()        # min_detection_confidence 0.5 기본값 / 

# angle 변수 필요
# angle의 변수가 왜필요한지 
# 현재 위치도 모르고 변화하는걸 알려주기위해서
# 동영상이 들어갈수도있다.

angle = 0 # motor current angle


while camera.is_opened():
    img = camera.read()        # mirror_mode = 0 or 1 기본값 1 /
    
    c_x, c_y, w, h = camera.detect_faces(img,1)         # img / max_num_faces = 1, 2,, 기본값 1 / bounding_box 0 or 1 
    # 옵션 추가 : box 안그리게 / 그리게 , 

    # face_detection , img 에 들어가는게 이상하다. 따로 모듈을 만들어주던가 camera와 연결
    # 계산최대한 적게
    # 동사 + 명사 형식으로 바꾸기 / 복수 까지 고려해야한다. / detect_faces
    # face 여러개 하는거도 고려해야한다.

    if c_x < 0.4:
        angle += 1
        module.motor.angle( angle ) 
    elif c_x > 0.6:
        angle -= 1
        module.motor.angle( angle ) 

    Camera.show(img)           #  img / cam_name 기본값 "WebCam" / quit_string 기본값 "esc"

# 교과서 만들기


###############################################

from dynamikontrol import Module, Camera

camera = Camera.start()           # cam_num = 0,1 기본값 0 / width 화면 최대 / height 화면 최대

while camera.is_opened():
    img = camera.read()        # mirror_mode = 1 기본값 1 
    camera.show(img)           #  img / cam_name 기본값 "WebCam" / #cam_cancel_key 기본값 "esc"


#######################################
from dynamikontrol import Module, Camera

camera = Camera.start()           # cam_num = 0,1 기본값 0 / width 기본값 최대값 / height 기본값 최대값 / 동영상 추가

angle = 0 # motor current angle

while camera.is_opened():
    img = camera.read()        # mirror_mode = 0 or 1 기본값 1 /# 굳이,, 기본값 BGR  선택사항 RGB, GRAY, HSV 등등
    
    c_x, c_y, w, h = camera.detect_faces(img)         # img / max_num_faces = 1, 2,, 기본값 1 / draw_boxes = 0 or 1 기본값 1

    if c_x < 0.4:
        angle += 1
        module.motor.angle( angle ) 
    elif c_x > 0.6:
        angle -= 1
        module.motor.angle( angle ) 

    Camera.show(img)           #  img / cam_name 기본값 "WebCam" / #cam_cancel_key 기본값 "esc"

# 교과서 만들기


