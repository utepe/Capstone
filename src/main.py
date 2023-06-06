import json
from machine import Pin, time_ms
from enum import Enum
from time import sleep
from app import processing_readings as processing, unity_mode


mcp_joints = processing.mcp_joints
pip_joints = processing.pip_joints

# # Configure the UART (serial port)
# uart = machine.UART(0, baudrate=9600)

# # Function to send data via serial port
# def send_serial_data(data):
#     uart.write(data)

class mode(Enum):
    IDLE = 0
    CALIBRATION = 1
    UNITY = 2
    WBA = 3

currentMode = mode.IDLE

buttonPin = Pin(18, Pin.IN, Pin.PULL_UP)

# handlers for long and short presses for mode selection
def up(pin):
    global first, currentMode
    buttonPin.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: down(pin))
    first = time_ms()
 
def down(pin):
    global first, currentMode
    second = time_ms()
    buttonPin.irq(trigger=Pin.IRQ_RISING, handler=lambda pin: up(pin))
    if (second - first) >= 3000:
        first = second
        print("Long press")
        currentMode = mode.CALIBRATION
    else:
        print("Short press")
        if currentMode is mode.UNITY:
            currentMode = mode.WBA
        else:
            currentMode = mode.UNITY

buttonPin.irq(trigger=Pin.IRQ_RISING, handler=lambda pin: up(pin))

with open('relationships.json') as f:
    file_data = f.read()
relationships = json.loads(file_data)
f.close()

while True:
    if currentMode is mode.CALIBRATION:
        print(mode.CALIBRATION)
        # run calibration script
        # switch mode to UNITY
        currentMode = mode.UNITY
    elif currentMode is mode.UNITY:
        # unity_mode.sendData(mcp_joints, pip_joints, relationships)
        processing.read_sensors()
        index_mcp_reading = processing.linear_func(mcp_joints["current_avg"]["index"], *relationships["index_mcp"])
        index_pip_reading = processing.linear_func(pip_joints["current_avg"]["index"], *relationships["index_pip"])
        data_to_send = str(index_mcp_reading) + ", " + str(index_pip_reading) + "\n"
        print(data_to_send)
    elif currentMode is mode.WBA:
        # run WBA motor controller script
        print(mode.WBA)
    else:
        print(mode.IDLE)
    sleep(0.1)