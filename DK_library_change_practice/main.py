from dynamikontrol import Module
from dynamikontrol_toolkit import Camera

module = Module()
camera = Camera()

while camera.is_opened():
    frame = camera.get_frame()
    face = camera.detect_face(frame, draw_face=False, draw_lips=False )
    if face:
        if face.eyes.is_look_left():
            module.motor.angle(-50)
            module.motor.angle(50, period = 2)
    camera.show(frame)




