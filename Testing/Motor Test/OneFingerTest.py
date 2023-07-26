from machine import Pin, PWM
import time
'''
thumb = PWM(Pin(5))
index = PWM(Pin(6))
middle = PWM(Pin(7))
ring = PWM(Pin(8))
pinky = PWM(Pin(9))

thumb.freq(50)
index.freq(50)
middle.freq(50)
ring.freq(50)
pinky.freq(50)

thumbAngle = 0
indexAngle = 0
middleAngle = 0
ringAngle = 0
pinkyAngle = 0'''

pin = int(input("Enter pin: "))
finger = PWM(Pin(pin))
finger.freq(50)
angle = 0

try:
    while True:
        angle = input("Enter angle: ")
        if angle == "q":
            break
        elif angle == 'h': # Hold position
            fingerDutyCycle = 0
        else:
            angle = float(angle)
            fingerDutyCycle = int((6000*(angle)/180)+2000)
        finger.duty_u16(fingerDutyCycle)

except KeyboardInterrupt:
    print("Interrupted")
    pass