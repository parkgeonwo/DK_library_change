from dynamikontrol import Module
import time

m = Module()


m.motor.angle(-60)
time.sleep(1)
# 2초 주기로 120도 원호운동
while True:
    m.motor.angle(60,1)
    time.sleep(1)
    m.motor.angle(-60,1)
    time.sleep(1)

