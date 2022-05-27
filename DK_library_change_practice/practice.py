
###################################### 

# import Camera_module

# camera = Camera_module.Camera()
# # camera = Camera_module.Camera(path="/home/matrix/Desktop/code/video2.mp4")

# while camera.is_opened(): 
#     frame = camera.get_frame()
#     camera.show(frame)


############################################

# from dynamikontrol import Module
# # from Camera import Camera
# from dynamikontrol_toolkit import Camera

# # module = Module()
# # camera = Camera(path='/home/matrix/Desktop/code/DK_library_change/squat.mp4')
# camera = Camera()

# count = 0
# position = None

# while camera.is_opened():
#     frame = camera.get_frame()

#     # body = camera.detect_body(frame)
#     # camera.show_text(30,50,1,"blue",count)

#     # if body:
#     #     if body.is_squat() == "down":
#     #         position = "down"
#     #     if position == "down" and body.is_squat() == "up":
#     #         position = "up"
#     #         count += 1

#     face = camera.detect_face(frame)
#     if face:
#         print(face.left_eye.is_closed())

#     # hand = camera.detect_hand(frame)
#     # if hand:
#     #     print(hand.fingers.is_up())

#     camera.show(frame)

# # module.disconnect()


from dynamikontrol import Module
from dynamikontrol_toolkit import Camera
# from Camera import Camera

module = Module()
camera = Camera()

while camera.is_opened():
    frame = camera.get_frame()
    hand = camera.detect_hand(frame,show_gesture=True)
    if hand:
        if hand.gesture == "one":
            module.motor.speed(100)
        if hand.gesture == "scissors":
            module.motor.speed(200)
        if hand.gesture == "three":
            module.motor.speed(300)
        if hand.gesture == "paper":
            module.motor.stop()
    camera.show(frame)


