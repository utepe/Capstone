import json
from machine import Pin, ADC
from time import sleep
from utime import time_ns
from helpers import linear_func, bound
from common import config as cfg

# Calculate the simple moving average for each joint
def calculate_SMA_MCP(key, window_size=10):
    if len(cfg.mcp_joints["raw"][key]) > window_size:
        cfg.mcp_joints["raw"][key].pop(0)
    cfg.mcp_joints["current_avg"][key] =  round(sum(cfg.mcp_joints["raw"][key]) / len(cfg.mcp_joints["raw"][key]), -1)

# Calculate the simple moving average for each joint
def calculate_SMA_PIP(key, window_size=10):
    if len(cfg.pip_joints["raw"][key]) > window_size:
        cfg.pip_joints["raw"][key].pop(0)
    cfg.pip_joints["current_avg"][key] =  round(sum(cfg.pip_joints["raw"][key]) / len(cfg.pip_joints["raw"][key]), -1)

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
    while i < len(cfg.fingers):

        select_pin(i, select_pins)
        cfg.mcp_joints["raw"][cfg.fingers[i]].append(round(z_mux_1.read_u16(), -1))
         
        cfg.pip_joints["raw"][cfg.fingers[i]].append(round(z_mux_2.read_u16(), -1))
        
        # Calculate the simple moving average for each joint
        calculate_SMA_MCP(cfg.fingers[i])
        calculate_SMA_PIP(cfg.fingers[i])

        update_mcp_angles(cfg.fingers[i])
        update_pip_angles(cfg.fingers[i])
           
        if time_ns() % sampling_time < sampling_time / 2:
            i+=1

def update_mcp_angles(finger):
    mcp = linear_func(cfg.mcp_joints["current_avg"][finger], *relationships[finger + "_mcp"]) 

    cfg.mcp_joints["angle"][finger] = bound(mcp, 0, 90)

def update_pip_angles(finger):
    mcp = cfg.mcp_joints["angle"][finger]
    pip = cfg.pip_joints["current_avg"][finger]

    angle_pip_0 = linear_func(pip, *relationships[finger + "_pip_0"])
    angle_pip_90 = linear_func(pip, *relationships[finger + "_pip_90"])

    if mcp < 45 and mcp > 0:
        pip = angle_pip_0
    else:
        pip = angle_pip_90

    cfg.pip_joints["angle"][finger] = bound(pip, 0, 90)

def get_relationship():
    global relationships
    with open('src/common/relationships.json') as f:
        file_data = f.read()
    relationships = json.loads(file_data)
    f.close()
