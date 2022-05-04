from dynamikontrol import Module, Timer
import time

t1 = Timer()

module_push = Module(serial_no='AC000023')

module_push.motor.angle(-75)
t1.callback_after(func=module_push.motor.angle, args=(75,), after=3)
t1.callback_after(func=module_push.motor.angle, args=(-45,), after=5)



