
###################################### 

# import Camera_module

# camera = Camera_module.Camera()
# # camera = Camera_module.Camera(cam_index="/home/matrix/Desktop/code/video2.mp4")

# while camera.is_opened():         # window_close_key default : esc 
#     frame = camera.get_frame()    # mirror_mode default : True
#     camera.show(frame)            # window_name default : Web Cam 


######################################

# from dynamikontrol import Module
# import Camera_module

# module = Module()
# camera = Camera_module.Camera(cam_index='/home/matrix/Desktop/code/video.mp4')
# camera = Camera_module.Camera()

# angle = 0

# while camera.is_opened():               # cancel_key default : esc 
#     frame = camera.get_frame()          # mirror_mode default : True

#     face = camera.detect_face(frame)
#     lips = camera.detect_lip(frame)

    # if face:
    #     if face.left():
    #         angle += 3
    #         module.motor.angle(angle)
    #     elif face.right():
    #         angle -= 3
    #         module.motor.angle(angle)

    # camera.show(frame)        # cam_name default : "Web Cam"



############################################

from dynamikontrol import Module
import Camera_module2

module = Module()
camera = Camera_module2.Camera(cam_index='/home/matrix/Desktop/code/video.mp4')
# camera = Camera_module2.Camera()

angle = 0

while camera.is_opened():               # cancel_key default : esc 
    frame = camera.get_frame()          # mirror_mode default : True

    face = camera.detect_face(frame)

    # if face:
    #     if face.mouth_open():
    #         angle += 3
    #         module.motor.angle(angle)
    #     elif face.mouth_close():
    #         angle -= 3
    #         module.motor.angle(angle)

    camera.show(frame)        # cam_name default : "Web Cam"











