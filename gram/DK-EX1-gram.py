from dynamikontrol import Module, Timer
import time

t1 = Timer()

module = Module()

module.motor.angle(-45)
t1.callback_after(func=module.motor.angle, args=(45,), after=2, interval=0.1)




