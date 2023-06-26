import json
from machine import Pin, ADC
from time import sleep
from utime import time_ns
from helpers import linear_func, bound

# Calculate the simple moving average for each joint
def calculate_SMA_MCP(key, window_size=10):
    global mcp_joints
    if len(mcp_joints["raw"][key]) > window_size:
        mcp_joints["raw"][key].pop(0)
    mcp_joints["current_avg"][key] =  round(sum(mcp_joints["raw"][key]) / len(mcp_joints["raw"][key]), -2)

# Calculate the simple moving average for each joint
def calculate_SMA_PIP(key, window_size=10):
    global pip_joints
    if len(pip_joints["raw"][key]) > window_size:
        pip_joints["raw"][key].pop(0)
    pip_joints["current_avg"][key] =  round(sum(pip_joints["raw"][key]) / len(pip_joints["raw"][key]), -2)


fingers = ("thumb", "index", "middle", "ring", "pinky")

# TODO: move all common variables to config.py to have them as shared global variables
# first mux will track mcp joints, second mux will track pip joints
mcp_joints = {
    "calibration": { "thumb": [0, 1e6, 0, 0], "index": [0, 1e6, 0, 0], "middle": [0, 1e6, 0, 0], "ring": [0, 1e6, 0, 0], "pinky": [0, 1e6, 0, 0] },
    "raw": { "thumb": [], "index": [], "middle": [], "ring": [], "pinky": [] }, 
    "current_avg": { "thumb": 0, "index": 0, "middle": 0, "ring": 0, "pinky": 0 },
    "angle": { "thumb": 0, "index": 0, "middle": 0, "ring": 0, "pinky": 0 }
}

pip_joints = {
    "calibration_0": { "thumb": [0, 1e6, 0, 0], "index": [0, 1e6, 0, 0], "middle": [0, 1e6, 0, 0], "ring": [0, 1e6, 0, 0], "pinky": [0, 1e6, 0, 0] },
    "calibration_90": { "thumb": [0, 1e6, 0, 0], "index": [0, 1e6, 0, 0], "middle": [0, 1e6, 0, 0], "ring": [0, 1e6, 0, 0], "pinky": [0, 1e6, 0, 0] },
    "raw": { "thumb": [], "index": [], "middle": [], "ring": [], "pinky": [] }, 
    "current_avg": { "thumb": 0, "index": 0, "middle": 0, "ring": 0, "pinky": 0 },
    "angle": { "thumb": 0, "index": 0, "middle": 0, "ring": 0, "pinky": 0 }
}

sampling_time = 1000 # in nanoseconds

'''Can use same select pins for both muxes, can remove select_pins_mux_2 and select_pin_nums_mux_2'''
select_pin_nums = [22, 21, 20]    # S0~GP22, S1~GP21, S2~GP20

select_pins = [Pin(i, Pin.OUT) for i in select_pin_nums]

z_mux_1 = ADC(Pin(27))    # Z1~GP27
z_mux_2 = ADC(Pin(26))    # Z2~GP26

# select pin should range bewteen 0 and 4
def select_pin(p, pins): 
    for i in range(3): 
        pins[i].value((p >> i) & 1)

def read_sensors(): 
    i=0
    while i < len(fingers):

        select_pin(i, select_pins)
        mcp_joints["raw"][fingers[i]].append(round(z_mux_1.read_u16(), -2))
         
        pip_joints["raw"][fingers[i]].append(round(z_mux_2.read_u16(), -2))
        
        # Calculate the simple moving average for each joint
        calculate_SMA_MCP(fingers[i])
        calculate_SMA_PIP(fingers[i])

        update_mcp_angles(fingers[i])
        update_pip_angles(fingers[i])
           
        if time_ns() % sampling_time < sampling_time / 2:
            i+=1


# TODO: instead of calling the calibration key within the joints dictionaries we will call the relationship file and pull from there
def update_mcp_angles(finger):
    mcp = linear_func(mcp_joints["current_avg"][finger], mcp_joints["calibration"][finger][2], mcp_joints["calibration"][finger][3]) 

    mcp_joints["angle"][finger] = bound(mcp, 0, 90)

def update_pip_angles(finger):
    mcp = mcp_joints["angle"][finger]
    pip = pip_joints["current_avg"][finger]

    angle_pip_0 = linear_func(pip, pip_joints["calibration_0"][finger][2], pip_joints["calibration_0"][finger][3])
    angle_pip_90 = linear_func(pip, pip_joints["calibration_90"][finger][2], pip_joints["calibration_90"][finger][3])

    if mcp < 45 and mcp > 0:
        pip = angle_pip_0
    else:
        pip = angle_pip_90

    pip_joints["angle"][finger] = bound(pip, 0, 90)


