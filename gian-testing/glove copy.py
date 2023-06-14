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

class WBA_Glove:
    
    def __init__(self) -> None:
        # first mux will track mcp joints, second mux will track pip joints
        self.mcp_joints = {
            # [max, min, m, b]
            "calibration": { "thumb": [0, 1e6, 0, 0], "index": [0, 1e6, 0, 0], "middle": [0, 1e6, 0, 0], "ring": [0, 1e6, 0, 0], "pinky": [0, 1e6, 0, 0] }, 
            "raw": { "thumb": [], "index": [], "middle": [], "ring": [], "pinky": [] },
            "current_avg": { "thumb": 0, "index": 0, "middle": 0, "ring": 0, "pinky": 0 },
            "angle": { "thumb": 0, "index": 0, "middle": 0, "ring": 0, "pinky": 0 },
            }
        
        self.pip_joints = { 
            # [max, min, m, b]
            "calibration_0": { "thumb": [0, 1e6, 0, 0], "index": [0, 1e6, 0, 0], "middle": [0, 1e6, 0, 0], "ring": [0, 1e6, 0, 0], "pinky": [0, 1e6, 0, 0] },
            # [max, min, m, b]
            "calibration_90": { "thumb": [0, 1e6, 0, 0], "index": [0, 1e6, 0, 0], "middle": [0, 1e6, 0, 0], "ring": [0, 1e6, 0, 0], "pinky": [0, 1e6, 0, 0] }, 
            # [m, b]
            "adjusted": { "thumb": [0, 0], "index": [0, 0], "middle": [0, 0], "ring": [0, 0], "pinky": [0, 0] },
            "raw": { "thumb": [], "index": [], "middle": [], "ring": [], "pinky": [] },
            "current_avg": { "thumb": 0, "index": 0, "middle": 0, "ring": 0, "pinky": 0 },
            "angle": { "thumb": 0, "index": 0, "middle": 0, "ring": 0, "pinky": 0 },
            "adjusted_angle": { "thumb": 0, "index": 0, "middle": 0, "ring": 0, "pinky": 0 }
            }
        
        self.pip_readings = { "thumb": [], "index": [], "middle": [], "ring": [], "pinky": [] }
    
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
                
    def calibrate(self):
        state = ["CLOSE", "OPEN"]
        
        print("MCP, PIP @ 90")

        # Gather data to create MCP model
        i=0
        time = time_ns()
        while i < 3:
            self.read()
            self.update_MCP_extrema()
            
            if time_ns() - time > 2e9:
                time = time_ns()
                print(state[i % 2])
                i += 1

        input("Press any key to continue...")

        for finger in fingers:
            self.mcp_joints["calibration"][finger][2] = self.linear_fit(90, 0, self.mcp_joints["calibration"][finger][0],
                                                                        self.mcp_joints["calibration"][finger][1])[0]
            self.mcp_joints["calibration"][finger][3] = self.linear_fit(90, 0, self.mcp_joints["calibration"][finger][0],
                                                                        self.mcp_joints["calibration"][finger][1])[1]

            self.pip_joints["raw"][finger] = []

        print("PIP, MCP @ 0")

        # Gather data to create PIP model
        i=0
        time = time_ns()
        while i < 3:
            self.read()
            for finger in fingers:
                self.pip_joints["calibration_0"][finger][0] = max(self.pip_joints["calibration_0"][finger][0], 
                                                                self.pip_joints["current_avg"][finger])
                self.pip_joints["calibration_0"][finger][1] = min(self.pip_joints["calibration_0"][finger][1], 
                                                                self.pip_joints["current_avg"][finger])
            
            if time_ns() - time > 2e9:
                time = time_ns()
                print(state[i % 2])
                i += 1

        input("Press any key to continue...")

        for finger in fingers:
            self.pip_joints["calibration_0"][finger][2] = self.linear_fit(90, 0, self.pip_joints["calibration_0"][finger][0],
                                                                        self.pip_joints["calibration_0"][finger][1])[0]
            self.pip_joints["calibration_0"][finger][3] = self.linear_fit(90, 0, self.pip_joints["calibration_0"][finger][0],
                                                                        self.pip_joints["calibration_0"][finger][1])[1]
            self.pip_joints["raw"][finger] = []

        print(self.pip_joints["calibration_0"]["index"])

        print("PIP, MCP @ 90")

        # Gather data to create PIP model
        i=0
        time = time_ns()
        while i < 3:
            self.read()
            for finger in fingers:
                self.pip_joints["calibration_90"][finger][0] = max(self.pip_joints["calibration_90"][finger][0], 
                                                                self.pip_joints["current_avg"][finger])
                self.pip_joints["calibration_90"][finger][1] = min(self.pip_joints["calibration_90"][finger][1], 
                                                                self.pip_joints["current_avg"][finger])
            
            if time_ns() - time > 2e9:
                time = time_ns()
                print(state[i % 2])
                i += 1
        
        input("Press any key to continue...")

        for finger in fingers:
            self.pip_joints["calibration_90"][finger][2] = self.linear_fit(90, 0, self.pip_joints["calibration_90"][finger][0],
                                                                        self.pip_joints["calibration_90"][finger][1])[0]
            self.pip_joints["calibration_90"][finger][3] = self.linear_fit(90, 0, self.pip_joints["calibration_90"][finger][0],
                                                                        self.pip_joints["calibration_90"][finger][1])[1]
            self.pip_joints["raw"][finger] = []

        print(self.pip_joints["calibration_90"]["index"])
        
        for finger in fingers:
            self.pip_joints["adjusted"][finger][0] = (self.pip_joints["calibration_90"][finger][2] - self.pip_joints["calibration_0"][finger][2]) / 90
            self.pip_joints["adjusted"][finger][1] = (self.pip_joints["calibration_90"][finger][3] - self.pip_joints["calibration_0"][finger][3]) / 90

        print(self.pip_joints["adjusted"]["index"])
                
    def update_MCP_extrema(self):
        for finger in fingers:
            self.mcp_joints["calibration"][finger][0] = max(self.mcp_joints["calibration"][finger][0], 
                                                            self.mcp_joints["current_avg"][finger])
            self.mcp_joints["calibration"][finger][1] = min(self.mcp_joints["calibration"][finger][1], 
                                                            self.mcp_joints["current_avg"][finger])
            
    def linear_fit(self, y2, y1, x2, x1):
        m = (y2 - y1) / (x2 - x1)
        b = y2 - m * x2
        
        return [m, b]
    
    def linear_func(self, x, m, b):
        return m * x + b

    def update_mcp_angles(self, key):
        self.mcp_joints["current_avg"][key] = (sum(self.mcp_joints["raw"][key]) / len(self.mcp_joints["raw"][key]) + 99) // 100 * 100
        
        x1 = self.mcp_joints["current_avg"][key]
        m1 = self.mcp_joints["calibration"][key][2]
        b1 = self.mcp_joints["calibration"][key][3]
        
        mcp = (m1*x1 + b1)

        self.mcp_joints["angle"][key] = mcp
        
    def update_pip_angles(self, key):
        self.pip_joints["current_avg"][key] = (sum(self.pip_joints["raw"][key]) / len(self.pip_joints["raw"][key]) + 99) // 100 * 100
        self.mcp_joints["current_avg"][key] = (sum(self.mcp_joints["raw"][key]) / len(self.mcp_joints["raw"][key]) + 99) // 100 * 100

        mcp = self.mcp_joints["angle"][key]
        pip = self.pip_joints["current_avg"][key]

        m1 = self.pip_joints["adjusted"][key][0] * mcp
        b1 = self.pip_joints["adjusted"][key][1] * mcp

        m2 = self.pip_joints["calibration_0"][key][2]
        b2 = self.pip_joints["calibration_0"][key][3]

        m3 = self.pip_joints["calibration_90"][key][2]
        b3 = self.pip_joints["calibration_90"][key][3]
        
        adjusted_angle = m1 * pip + b1
        angle_mcp_0 = m2 * pip + b2
        angle_mcp_90 = m3 * pip + b3

        self.pip_readings[key] = [mcp, adjusted_angle, angle_mcp_0, angle_mcp_90, angle_mcp_0 - adjusted_angle]
        self.pip_joints["angle"][key] = 1.3* (angle_mcp_90 - 0.15 * mcp)

if __name__ == "__main__":
    glove = WBA_Glove()    
    
    glove.calibrate()

    while True:
        glove.read()
        print(glove.mcp_joints["angle"]["index"], glove.pip_joints["angle"]["index"], end="\r")
        sleep(1e-2)
