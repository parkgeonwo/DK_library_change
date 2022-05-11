from dynamikontrol import Module
from dynamikontrol_toolkit import Camera

module = Module()
camera = Camera()

while camera.is_opened():
    frame = camera.get_frame()

    hand = camera.detect_hand(frame)
    if hand:
        module.motor.angle(-60, period = 1)

    else:
        module.motor.angle(60, period = 1)

    camera.show(frame)

module.disconnect()