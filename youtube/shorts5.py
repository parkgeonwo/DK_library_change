from dynamikontrol import Module
from dynamikontrol_toolkit import Camera

module = Module()
camera = Camera()

count = 0
position = None

while camera.is_opened():
    frame = camera.get_frame()

    body = camera.detect_body(frame)
    camera.show_text(x=30,y=50,color = "blue",text = count)

    if body:
        module.motor.angle(-60)
        if body.is_squat() == "down":
            position = "down"
        if position == "down" and body.is_squat() == "up":
            position = "up"
            count += 1
        if count >= 3:
            module.motor.angle(60)
            break

    camera.show(frame)



