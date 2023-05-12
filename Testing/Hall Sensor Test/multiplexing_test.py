from machine import Pin, ADC
from time import sleep
from utime import time_ns


# Calculate the simple moving average for each joint
def calculate_SMA_MCP(key, window_size=10):
    global mcp_joints
    if len(mcp_joints[key]["raw"]) > window_size:
        mcp_joints[key]["raw"].pop(0)
    mcp_joints[key]["current_avg"] =  sum(mcp_joints[key]["raw"]) / len(mcp_joints[key]["raw"])

def calculate_SMA_MCP_rev(key, window_size=10):
    global mcp_joints_rev
    if len(mcp_joints_rev["raw"][key]) > window_size:
        mcp_joints_rev["raw"][key].pop(0)
    mcp_joints_rev["current_avg"][key] =  sum(mcp_joints_rev["raw"][key]) / len(mcp_joints_rev["raw"][key])

fingers = ("pinky", "ring", "middle", "index")
# first mux will track mcp joints, second mux will track pip joints
mcp_joints = { "pinky": {"raw": [], "current_avg": 0}, "ring": {"raw": [], "current_avg": 0}, "middle": {"raw": [], "current_avg": 0}, "index": {"raw": [], "current_avg": 0 }}

mcp_joints_rev = { "raw": { "pinky": [], "ring": [], "middle": [], "index": [] }, "current_avg": { "pinky": 0, "ring": 0, "middle": 0, "index": 0 } }

pip_joints = { "pinky": [], "ring": [], "middle": [], "index": [] }
sampling_time = 1000 #n

select_pin_nums_mux_1 = [22, 21, 20]    # S0~GP22, S1~GP21, S2~GP20

select_pin_nums_mux_2 = [19, 18, 17]    # S0~GP19, S1~GP18, S2~GP17

select_pins_mux_1 = [Pin(i, Pin.OUT) for i in select_pin_nums_mux_1]
z_mux_1 = ADC(Pin(27))    # Z1~GP27

select_pins_mux_2 = [Pin(i, Pin.OUT) for i in select_pin_nums_mux_2]
z_mux_2 = ADC(Pin(26))    # Z2~GP26

'''
# select pin should range bewteen 0 and 4
def select_pin(p, pins): 
    for i in range(3): 
        pins[i].value((p >> i) & 1)
'''
'''
def select_pin(pin, select_pins):
    if pin > 5:
        return
    
    for i in range(3):
        if pin & ( 1 << i ):
            select_pins[i].high()
        else:
            select_pins[i].low()
'''

def select_pin(pin, select_pins):
    if pin == 0:
        select_pins[0].value(0)
        select_pins[1].value(0)
        select_pins[2].value(0)
    elif pin == 1:
        select_pins[0].value(1)
        select_pins[1].value(0)
        select_pins[2].value(0)
    elif pin == 2:
        select_pins[0].value(0)
        select_pins[1].value(1)
        select_pins[2].value(0)
    elif pin == 3:
        select_pins[0].value(1)
        select_pins[1].value(1)
        select_pins[2].value(0)
    elif pin == 4:
        select_pins[0].value(0)
        select_pins[1].value(0)
        select_pins[2].value(1)    

def read_sensors(): 
    sleep(0.1)
    i=0
    while i < len(fingers):
    #for i, key in enumerate(fingers):
        select_pin(i, select_pins_mux_1) 
        mcp_joints[fingers[i]]["raw"].append(z_mux_1.read_u16())
         
        # select_pin(i, select_pins_mux_2)
        # pip_value = z_mux_2.read_u16()

        
        # Calculate the simple moving average for each joint
        calculate_SMA_MCP(fingers[i])
        # pip_avg = calculate_SMA(pip_joints[fingers[i]], pip_value)
        
        
        # Append the average to the list of averages for each joint 
        # mcp_joints[fingers[i]][].append(mcp_avg)
        # pip_joints[fingers[i]].append(pip_avg)
        if time_ns()%sampling_time < sampling_time/2:
            i+=1

    return mcp_joints, pip_joints 

def read_sensors_rev(): 
    sleep(0.1)
    i=0
    while i < len(fingers):
    #for i, key in enumerate(fingers):
        select_pin(i, select_pins_mux_1) 
        mcp_joints_rev["raw"][fingers[i]].append(z_mux_1.read_u16())
         
        # select_pin(i, select_pins_mux_2)
        # pip_value = z_mux_2.read_u16()

        
        # Calculate the simple moving average for each joint
        calculate_SMA_MCP_rev(fingers[i])
        # pip_avg = calculate_SMA(pip_joints[fingers[i]], pip_value)
        
        
        # Append the average to the list of averages for each joint 
        # mcp_joints[fingers[i]][].append(mcp_avg)
        # pip_joints[fingers[i]].append(pip_avg)
        if time_ns()%sampling_time < sampling_time/2:
            i+=1

    # return mcp_joints_rev, pip_joints 


while True:
    # mcp_joints_, pip_joints = 
    read_sensors_rev()
    print(mcp_joints_rev["current_avg"])
    #print(pip_joints,end='\r')
