from machine import Pin, PWM
import time

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
pinkyAngle = 0

try:
    while True:
        angle = input("Enter angle: ")
        if angle == "q":
            break
        elif angle == 'h': # Hold position
            thumbDutyCycle = 0
            indexDutyCycle = 0
            middleDutyCycle = 0
            ringDutyCycle = 0
            pinkyDutyCycle = 0
        else:
            angle = float(angle)
            thumbDutyCycle = int((6000*angle/180)+2000)
            indexDutyCycle = int((6000*angle/180)+2000)
            middleDutyCycle = int((6000*angle/180)+2000)
            ringDutyCycle = int((6000*(180-angle)/180)+2000)
            pinkyDutyCycle = int((6000*(180-angle)/180)+2000)
        thumb.duty_u16(thumbDutyCycle)
        index.duty_u16(indexDutyCycle)
        middle.duty_u16(middleDutyCycle)
        ring.duty_u16(ringDutyCycle)
        pinky.duty_u16(pinkyDutyCycle)

except KeyboardInterrupt:
    print("Interrupted")