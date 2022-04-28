
###################################### 

# import Camera_module

# camera = Camera_module.Camera()
# # camera = Camera_module.Camera(file_or_device="/home/matrix/Desktop/code/video2.mp4")

# while camera.open(): 
#     frame = camera.get_frame()
#     camera.show(frame)


############################################

from dynamikontrol import Module
from Camera_module import Camera

module = Module()
# camera = Camera(file_or_device='/home/matrix/Desktop/code/video2.mp4')
camera = Camera()

angle = 0

while camera.open():
    frame = camera.get_frame()

    face = camera.detect_face(frame)

    if face:
        if face.left_side_window():
            angle += 3
            module.motor.angle(angle)
        elif face.right_side_window():
            angle -= 3
            module.motor.angle(angle)

    camera.show(frame)

module.disconnect()














