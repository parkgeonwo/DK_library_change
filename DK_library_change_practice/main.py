from dynamikontrol import Module
from Camera import Camera

module = Module()
camera = Camera(path =1)

module.motor.angle(60)

while camera.is_opened():
    frame = camera.get_frame()

    hand = camera.detect_hand(frame)
    if hand:
        module.motor.angle(-60, period = 1.5)
    else:
        module.motor.angle(60, period = 1.5)
    
    camera.show(frame)











