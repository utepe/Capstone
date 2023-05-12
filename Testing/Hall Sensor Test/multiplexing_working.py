from machine import Pin, ADC
from time import sleep
from utime import time_ns


# Calculate the simple moving average for each joint
def calculate_SMA_MCP(key, window_size=10):
    global mcp_joints
    if len(mcp_joints["raw"][key]) > window_size:
        mcp_joints["raw"][key].pop(0)
    mcp_joints["current_avg"][key] =  sum(mcp_joints["raw"][key]) / len(mcp_joints["raw"][key])

# Calculate the simple moving average for each joint
def calculate_SMA_PIP(key, window_size=10):
    global pip_joints
    if len(pip_joints["raw"][key]) > window_size:
        pip_joints["raw"][key].pop(0)
    pip_joints["current_avg"][key] =  sum(pip_joints["raw"][key]) / len(pip_joints["raw"][key])


fingers = ("pinky", "ring", "middle", "index")

# first mux will track mcp joints, second mux will track pip joints
mcp_joints = { "raw": { "pinky": [], "ring": [], "middle": [], "index": [] }, "current_avg": { "pinky": 0, "ring": 0, "middle": 0, "index": 0 } }
pip_joints = { "raw": { "pinky": [], "ring": [], "middle": [], "index": [] }, "current_avg": { "pinky": 0, "ring": 0, "middle": 0, "index": 0 } }

sampling_time = 1000 # in nanoseconds


'''Can use same select pins for both muxes, can remove select_pins_mux_2 and select_pin_nums_mux_2'''
select_pin_nums_mux_1 = [22, 21, 20]    # S0~GP22, S1~GP21, S2~GP20

select_pin_nums_mux_2 = [19, 18, 17]    # S0~GP19, S1~GP18, S2~GP17

select_pins_mux_1 = [Pin(i, Pin.OUT) for i in select_pin_nums_mux_1]
z_mux_1 = ADC(Pin(27))    # Z1~GP27

select_pins_mux_2 = [Pin(i, Pin.OUT) for i in select_pin_nums_mux_2]
z_mux_2 = ADC(Pin(26))    # Z2~GP26


# select pin should range bewteen 0 and 4
def select_pin(p, pins): 
    for i in range(3): 
        pins[i].value((p >> i) & 1)

def read_sensors(): 
    i=0
    while i < len(fingers):
        select_pin(i, select_pins_mux_1) 
        mcp_joints["raw"][fingers[i]].append(z_mux_1.read_u16())
         
        # select_pin(i, select_pins_mux_2)
        # pip_joints["raw"][fingers[i]].append(z_mux_2.read_u16())
        
        # Calculate the simple moving average for each joint
        calculate_SMA_MCP(fingers[i])
        # calculate_SMA_PIP(fingers[i])
           
        if time_ns()%sampling_time < sampling_time/2:
            i+=1

while True:
    # mcp_joints_, pip_joints = 
    read_sensors()
    print(mcp_joints["current_avg"],end='\r')
    #print(pip_joints,end='\r')