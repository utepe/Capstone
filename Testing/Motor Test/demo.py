from machine import Pin, PWM
import time

mcp = PWM(Pin(0))
pip = PWM(Pin(1))
mcp.freq(50)
pip.freq(50)

print("Waiting for 1 second")
time.sleep(1)
mcpDutyCycle = 5000 # adjusted 0 degrees (90 on the servo)
pipDutyCycle = 5000 # adjusted 0 degrees (90 on the servo)
mcp.duty_u16(mcpDutyCycle)
pip.duty_u16(pipDutyCycle)
mcpAngle = 0
pipAngle = 0

# Straight finger wag
mcpRange = [80, 110]
pipRange = [70, 20]
steps = 50
sleepTime = 0.01
mcpInc = (mcpRange[1]-mcpRange[0])/steps
pipInc = (pipRange[1]-pipRange[0])/steps

pipAngle = pipRange[0]
mcpAngle = mcpRange[0]

while True:
    for i in range(steps):
        time.sleep(sleepTime)
        mcpAngle += mcpInc
        pipAngle += pipInc
        mcpDutyCycle = int((6000*mcpAngle/180)+2000)
        pipDutyCycle = int((6000*pipAngle/180)+2000)
        mcp.duty_u16(mcpDutyCycle)
        pip.duty_u16(pipDutyCycle)

    for i in range(steps):
        time.sleep(sleepTime)
        mcpAngle -= mcpInc
        pipAngle -= pipInc
        mcpDutyCycle = int((6000*mcpAngle/180)+2000)
        pipDutyCycle = int((6000*pipAngle/180)+2000)
        mcp.duty_u16(mcpDutyCycle)
        pip.duty_u16(pipDutyCycle)


mcpDutyCycle = 0
pipDutyCycle = 0

mcp.duty_u16(mcpDutyCycle)
pip.duty_u16(pipDutyCycle)