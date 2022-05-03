from dynamikontrol import Module
from dynamikontrol_toolkit import Camera

module = Module()
camera = Camera(path=1)

angle = 0

while camera.is_opened():
    frame = camera.get_frame()

    face = camera.detect_face(frame, draw_lips=False)

    if face:
        if face.is_located_left():
            angle += 5
            module.motor.angle(angle)
        elif face.is_located_right():
            angle -= 5
            module.motor.angle(angle)

    camera.show(frame)

module.disconnect()