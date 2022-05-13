from dynamikontrol import Module
from dynamikontrol_toolkit import Camera

module = Module()
# camera = Camera(path='/home/matrix/Desktop/code/DK_library_change/video2.mp4')
camera = Camera()

while camera.is_opened():
    frame = camera.get_frame()

    # hand = camera.detect_hand(frame,write_shape=True, write_hand_distance=True)
    # if hand:
    #     print(hand.fingers.get_distance(2,3))

    face = camera.detect_face(frame)

    if face:
        print(face.landmark_list[1])
    #     if face.direction == "up":
    #         print("wow")

    camera.show(frame)

module.disconnect()











