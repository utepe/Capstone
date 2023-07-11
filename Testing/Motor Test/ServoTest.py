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

'''try:
    while True:
        new_pipAngle = input("Enter angle: ")
        if new_pipAngle == "q":
            mcp.stop()
            pip.stop()
            GPIO.cleanup()
            break
        elif new_pipAngle == 'h': # Hold position
            mcpDutyCycle = 0
            pipDutyCycle = 0
        else:
            new_pipAngle = float(new_pipAngle)
            pipAngle = new_pipAngle
            pipDutyCycle = (pipAngle/22.5)+2
        mcp.ChangeDutyCycle(pipDutyCycle)
        pip.ChangeDutyCycle(pipDutyCycle)

except KeyboardInterrupt:
    mcp.stop()
    GPIO.cleanup()'''

try:
    while True:
        angle = input("Enter angle: ")
        if angle == "q":
            break
        elif angle == 'h': # Hold position
            mcpDutyCycle = 0
            pipDutyCycle = 0
        else:
            if 'mp' in angle:
                mcpAngle = float(angle.split('mp')[1].split(' ')[0])
                mcpDutyCycle = int((6000*mcpAngle/180)+2000)

                pipAngle = float(angle.split('mp')[1].split(' ')[1])
                pipDutyCycle = int((6000*pipAngle/180)+2000)
            elif 'm' in angle:
                mcpAngle = float(angle.split('m')[1])
                mcpDutyCycle = int((6000*mcpAngle/180)+2000)
                
            elif 'p' in angle:
                pipAngle = float(angle.split('p')[1])
                pipDutyCycle = int((6000*pipAngle/180)+2000)
            else:
                new_mcpAngle = float(angle)
                pipAngle += (new_mcpAngle - mcpAngle) / 2
                mcpAngle = new_mcpAngle
                mcpDutyCycle = int((6000*mcpAngle/180)+2000)
                pipDutyCycle = int((6000*pipAngle/180)+2000)
        mcp.duty_u16(mcpDutyCycle)
        pip.duty_u16(pipDutyCycle)
        print("MCP: " + str(mcpAngle) + " | PIP: " + str(pipAngle))

except KeyboardInterrupt:
    print("Interrupted")