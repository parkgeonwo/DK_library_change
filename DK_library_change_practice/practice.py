

# import cv2



# def func1(num):
#     return cv2.VideoCapture(num)

# def func2(cam, num):
#     while cam.isOpened():
#         ret, img = cam.read()
#         if not ret:
#             break

#         img = cv2.flip(img, num) # mirror image

#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#         cv2.imshow('title', img)     # img를 실시간으로 출력 / 제목은 "arg"
#         if cv2.waitKey(1) == ord('q'):
#             break
















############################## 변경 전 코드 #############################



# cap = cv2.VideoCapture(0)    # 웹캠 키기
# cap = func1(0)


# while cap.isOpened():
#     ret, img = cap.read()
#     if not ret:
#         break

#     img = cv2.flip(img, 1) # mirror image

#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# func2(1)

#     cv2.imshow('title', img)     # img를 실시간으로 출력 / 제목은 "arg"
#     if cv2.waitKey(1) == ord('q'):
#         break

# 캠 끄기 cam.end()
# cap.release()





# from dynamikontrol import Module, cam

# cam = cam.start("cam_index = 0 or 1")             # size 

# while cam.open():
#     img = cam.to_img(  "mirror_mode = 0 or 1" )
#     cam.show( img , "cam_name", "quit_string" )

# cam.end()



from dynamikontrol import Module

module = Module()

module.motor.angle(0)

module.disconnect()












