# from dynamikontrol import Module
# import time

# module = Module()

# time.sleep(3)

# module.motor.speed(1500)
# time.sleep(4)
# module.motor.stop()


#########################################

from dynamikontrol import Module
from dynamikontrol_toolkit import Camera

module = Module()
camera = Camera()

while camera.is_opened():
    frame = camera.get_frame()
    hand = camera.detect_hand(frame,show_gesture=True)
    if hand:
        if hand.gesture == "one":
            module.motor.speed(100)
        if hand.gesture == "two":
            module.motor.speed(200)
        if hand.gesture == "three":
            module.motor.speed(300)
        if hand.gesture == "paper":
            module.motor.stop()
    camera.show(frame)




