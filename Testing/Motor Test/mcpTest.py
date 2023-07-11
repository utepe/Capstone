from machine import Pin, PWM
from time import sleep

mcp = PWM(Pin(0))
mcp.freq(50)

print("Waiting for 1 second")
sleep(1)
mcpDutyCycle = 3000
mcp.duty_u16(mcpDutyCycle)
mcpAngle = 0

try:
    while True:
        angle = input("Enter angle: ")
        if angle == "q":
            break
        elif angle == 'h': # Hold position
            mcpDutyCycle = 0
        else:
            mcpAngle = float(angle)
            print(mcpAngle)
            mcpDutyCycle = int((6000*mcpAngle/180)+2000)


        mcp.duty_u16(mcpDutyCycle)
        print(mcpDutyCycle)

except KeyboardInterrupt:
    print("Interrupted")