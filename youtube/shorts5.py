from dynamikontrol import Module
from dynamikontrol_toolkit import Camera

module = Module()
camera = Camera()

count = 0                      # 초기 count
position = None                # 초기 자세 선언

while camera.is_opened():           # 카메라 오픈
    frame = camera.get_frame()      # 프레임 받아오기

    body = camera.detect_body(frame)     # 프레임에서 detect_body
    camera.show_text(x=30,y=50,color = "blue",text = count)    # window에서 count를 show

    if body:      # 몸이 detect되면
        module.motor.angle(-60)    # 모터 -60도로 회전
        if body.is_squat() == "down":   # 스쿼트 자세중에 내려간 자세라면
            position = "down"           # position을 down으로
        if position == "down" and body.is_squat() == "up":    # position이 down이고 스쿼트 자세에서 일어난 자세라면
            position = "up"     # position을 up으로
            count += 1          # count을 +1
        if count >= 5:          # count가 5이상이면
            module.motor.angle(60)      # 모터 60도로 회전

    camera.show(frame)   # 카메라 show



