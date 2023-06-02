import json
from machine import Pin
from enum import Enum
from time import sleep
from app import processing_readings as processing

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
buttonPin = Pin(XX, Pin.IN, Pin.PULL_UP)

def callback(pin):
    global currentMode
    currentMode = mode.IDLE

buttonPin.irq(trigger=Pin.IQR_FALLING, handler=callback)    

with open('relationships.json') as f:
    file_data = f.read()
relationships = json.loads(file_data)
f.close()

while True:
    if currentMode is mode.CALIBRATION:
        print(mode.CALIBRATION)
        # do something
    elif currentMode is mode.UNITY:
        processing.read_sensors()
        index_mcp_reading = processing.linear_func(mcp_joints["current_avg"]["index"], *relationships["index_mcp"])
        index_pip_reading = processing.linear_func(pip_joints["current_avg"]["index"], *relationships["index_pip"])
        data_to_send = str(index_mcp_reading) + ", " + str(index_pip_reading) + "\n"
        print(data_to_send)
    elif currentMode is mode.WBA:
        print(mode.WBA)
    else:
        print(mode.IDLE)
    sleep(0.1)