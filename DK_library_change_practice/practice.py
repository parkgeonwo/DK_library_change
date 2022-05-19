
###################################### 

# import Camera_module

# camera = Camera_module.Camera()
# # camera = Camera_module.Camera(path="/home/matrix/Desktop/code/video2.mp4")

# while camera.is_opened(): 
#     frame = camera.get_frame()
#     camera.show(frame)


############################################

from dynamikontrol import Module
from Camera import Camera
# from dynamikontrol_toolkit import Camera

module = Module()
camera = Camera(path='/home/matrix/Desktop/code/DK_library_change/squat.mp4')
# camera = Camera()
# pTime = 0

count = 0
position = None

while camera.is_opened():
    frame = camera.get_frame()

    body = camera.detect_body(frame)
    camera.show_text(30,50,"blue",count)

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

    # cTime = time.time()
    # fps = 1 / (cTime-pTime)
    # pTime = cTime
    # print(fps)

    # face = camera.detect_face(frame)
    # hand = camera.detect_hand(frame)

    camera.show(frame)

module.disconnect()





