
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

# module = Module()
# camera = Camera(path='/home/matrix/Desktop/code/DK_library_change/video2.mp4')
camera = Camera()

while camera.is_opened():
    frame = camera.get_frame()

    face = camera.detect_face(frame)

    # if face:
    #     if face.eyes.is_look_left():
    #         print("left")
    #     elif face.eyes.is_look_right():
    #         print("right")

    camera.show(frame)

# module.disconnect()










