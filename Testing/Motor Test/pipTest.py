from machine import Pin, PWM
from time import sleep

pip = PWM(Pin(1))
pip.freq(50)

print("Waiting for 1 second")
sleep(1)
mcpDutyCycle = 2000
pipDutyCycle = 2000
pip.duty_u16(pipDutyCycle)
pipAngle = 0

try:
    while True:
        angle = input("Enter angle: ")
        if angle == "q":
            break
        elif angle == 'h': # Hold position
            pipDutyCycle = 0
        else:
            pipAngle = float(angle)
            print(pipAngle)
            pipDutyCycle = int((6000*pipAngle/180)+2000)


        pip.duty_u16(pipDutyCycle)
        print(pipDutyCycle)

except KeyboardInterrupt:
    print("Interrupted")