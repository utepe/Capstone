import json
from machine import Pin, ADC
from time import sleep
from utime import time_ns

fingers = ("thumb", "index", "middle", "ring", "pinky")

sampling_time = 1000 # in nanoseconds

'''Can use same select pins for both muxes, can remove select_pins_mux_2 and select_pin_nums_mux_2'''
select_pin_nums = [22, 21, 20]    # S0~GP22, S1~GP21, S2~GP20

select_pins = [Pin(i, Pin.OUT) for i in select_pin_nums]

z_mux_1 = ADC(Pin(27))    # Z1~GP27
z_mux_2 = ADC(Pin(26))    # Z2~GP26

# Configure the UART (serial port)
uart = machine.UART(0, baudrate=9600)

class WBA_Glove:
    
    def __init__(self) -> None:
        # first mux will track mcp joints, second mux will track pip joints
        self.mcp_joints = {
            "calibration": { "thumb": [0, 1e6, 0, 0], "index": [0, 1e6, 0, 0], "middle": [0, 1e6, 0, 0], "ring": [0, 1e6, 0, 0], "pinky": [0, 1e6, 0, 0] }, # [max, min, m, b]
            "raw": { "thumb": [], "index": [], "middle": [], "ring": [], "pinky": [] },
            "current_avg": { "thumb": 0, "index": 0, "middle": 0, "ring": 0, "pinky": 0 },
            "angle": { "thumb": 0, "index": 0, "middle": 0, "ring": 0, "pinky": 0 }
            }
        
        self.pip_joints = {
            "calibration": { "thumb": [0, 1e6, 0, 0], "index": [0, 1e6, 0, 0], "middle": [0, 1e6, 0, 0], "ring": [0, 1e6, 0, 0], "pinky": [0, 1e6, 0, 0] }, # [max, min, m, b]
            "raw": { "thumb": [], "index": [], "middle": [], "ring": [], "pinky": [] },
            "current_avg": { "thumb": 0, "index": 0, "middle": 0, "ring": 0, "pinky": 0 },
            "angle": { "thumb": 0, "index": 0, "middle": 0, "ring": 0, "pinky": 0 }
            }
    
    def select_pin(self, p, pins): 
        for i in range(3): 
            pins[i].value((p >> i) & 1)
                
    def read(self):
        i=0
        while i < len(fingers):
            key = fingers[i]
            
            self.select_pin(i, select_pins)
            
            if len(self.mcp_joints["raw"][key]) > 10:
                self.mcp_joints["raw"][key].pop(0)
            self.mcp_joints["raw"][key].append((z_mux_1.read_u16() + 99) // 100 * 100)
            
            if len(self.pip_joints["raw"][key]) > 10:
                self.pip_joints["raw"][key].pop(0)
            self.pip_joints["raw"][key].append((z_mux_2.read_u16() + 99) // 100 * 100)
            
            self.update_mcp_angles(key)
            self.update_pip_angles(key)
            
            if time_ns() % sampling_time < sampling_time / 2:
                i+=1
                
    def update_calib_data(self):
        for finger in fingers:
            curr_mcp_max = glove.mcp_joints["calibration"][finger][0]
            curr_mcp_min = glove.mcp_joints["calibration"][finger][1]
            self.mcp_joints["calibration"][finger][0] = max(self.mcp_joints["calibration"][finger][0], self.mcp_joints["raw"][finger][-1])
            self.mcp_joints["calibration"][finger][1] = min(self.mcp_joints["calibration"][finger][1], self.mcp_joints["raw"][finger][-1])
            
            curr_pip_max = self.pip_joints["calibration"][finger][0]
            curr_pip_min = self.pip_joints["calibration"][finger][1]
            self.pip_joints["calibration"][finger][0] = max(self.pip_joints["calibration"][finger][0], self.pip_joints["raw"][finger][-1])
            self.pip_joints["calibration"][finger][1] = min(self.pip_joints["calibration"][finger][1], self.pip_joints["raw"][finger][-1])
            
    def curve_fit(self):
        for finger in fingers:
            self.mcp_joints["calibration"][finger][2] = 90 / (self.mcp_joints["calibration"][finger][1] - self.mcp_joints["calibration"][finger][0]) # m
            self.mcp_joints["calibration"][finger][3] = 90 - self.mcp_joints["calibration"][finger][2] * self.mcp_joints["calibration"][finger][1] # b
            
            self.pip_joints["calibration"][finger][2] = 90 / (self.pip_joints["calibration"][finger][1] - self.pip_joints["calibration"][finger][0]) # m
            self.pip_joints["calibration"][finger][3] = 90 - self.pip_joints["calibration"][finger][2] * self.pip_joints["calibration"][finger][1] # b

    def update_mcp_angles(self, key):
        self.mcp_joints["current_avg"][key] =  (sum(self.mcp_joints["raw"][key]) / len(self.mcp_joints["raw"][key]) + 99) // 100 * 100
        
        x = self.mcp_joints["current_avg"][key]
        m = self.mcp_joints["calibration"][key][2]
        b = self.mcp_joints["calibration"][key][3]
        
        self.mcp_joints["angle"][key] = m*x + b
        
    def update_pip_angles(self, key):
        self.pip_joints["current_avg"][key] =  (sum(self.pip_joints["raw"][key]) / len(self.pip_joints["raw"][key]) + 99) // 100 * 100
        
        x = self.pip_joints["current_avg"][key]
        m = self.pip_joints["calibration"][key][2]
        b = self.pip_joints["calibration"][key][3]
        
        self.pip_joints["angle"][key] = m*x + b
        
# Function to send data via serial port
def send_serial_data(data):
    uart.write(data)

if __name__ == "__main__":
    glove = WBA_Glove()
        
    state = ["OPEN", "CLOSE"]
    
    i=0
    time = time_ns()
    while i < 5:
        glove.read()
        glove.update_calib_data()
        
        if time_ns() - time > 2e9:
            time = time_ns()
            print(state[i % 2])
            i += 1
            
    glove.curve_fit()
        
    while True:
        glove.read()
        print(glove.mcp_joints["angle"], end='\r')
        send_serial_data(str("Hi"))
        sleep(2)