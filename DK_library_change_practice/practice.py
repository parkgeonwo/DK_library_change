
# class MyStatus: 
#     def __init__(self,age,name,height,weight): 
#         # self.age = age 
#         # self.name = name
#         # self.height = height
#         # self.weight = weight 
#     def print_name(self):
#         print(self.name)
#     def print_age(self):
#         print(self.age)
#     def print_height(self):
#         print(self.height)
#     def print_weight(self):
#         print(self.weight)

# a = MyStatus(34,"yamada",170,78)

# a.print_age()






class Camera():

    def __init__(self):
        
        pass
        
    def is_opened():
        # self.camera_open = self.camera.isOpend()
        # return self.camera_open
        
        return camera.isOpened()





import cv2

cap = cv2.VideoCapture(0)    # 웹캠 키기

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    img = cv2.flip(img, 1) # mirror image

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    cv2.imshow('title', img)     # img를 실시간으로 출력 / 제목은 "arg"
    if cv2.waitKey(1) == ord('q'):
        break

# 캠 끄기 cam.end()
cap.release()



