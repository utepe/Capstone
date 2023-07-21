import json
from machine import Pin, ADC, reset
from time import sleep, sleep_ms
from utime import time_ns
import network
import socket

'''Global variables'''
Mode = ("IDLE", "CALIBRATION", "UNITY", "WBA")

fingers = ("thumb", "index", "middle", "ring", "pinky")

sampling_time = 1000 # in nanoseconds

'''Can use same select pins for both muxes, can remove select_pins_mux_2 and select_pin_nums_mux_2'''
select_pin_nums = [22, 21, 20]    # S0~GP22, S1~GP21, S2~GP20

select_pins = [Pin(i, Pin.OUT) for i in select_pin_nums]

z_mux_1 = ADC(Pin(27))    # Z1~GP27
z_mux_2 = ADC(Pin(26))    # Z2~GP26

WBA_pin = Pin(14, mode=Pin.IN, pull=Pin.PULL_UP)
led = Pin("LED", Pin.OUT)

# NOTE: This SSID and password should be changed based on the network being used
ssid = "Truva"
password = "bizimevimiz"

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        led.toggle()
        sleep(1e-2)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    led.on()
    return ip

def open_socket(ip):
    address = (ip, 80)
    sock = socket.socket()
    sock.bind(address)
    sock.listen()
    return sock

# first check if the glove is connected to WBA to enter that mode
# If the glove is not in WBA mode then accept the socket and handle the socket requests 
def serve(sock, glove):
    currentMode = Mode[0]
    client_socket, client_address = sock.accept()
    print('Connected to client:', client_address)
    while True:
        if currentMode == "CALIBRATION":
            glove.calibrate(client_socket)
            currentMode = Mode[0]
        elif currentMode == "UNITY":
            glove.send_data_to_VR(client_socket)
            # TODO: poll Unity and see if "stopSending" message is recieved, if it is switchMode back to IDLE
        elif currentMode == "WBA":
            glove.send_data_to_WBA()
        else:  # IDLE mode
            unityData = client_socket.recv(1024).decode("utf-8")
            if unityData == "calibration":  # CALIBRATION mode
                currentMode = Mode[1]
            elif unityData == "unityMode":  # UNITY mode
                currentMode = Mode[2]
            else:  # remain in IDLE mode
                currentMode = Mode[0]

class Glove():
    def __init__(self):
        self.mcp_joints = {
            "calibration": { "thumb": [0, 1e6, 0, 0], "index": [0, 1e6, 0, 0], "middle": [0, 1e6, 0, 0], "ring": [0, 1e6, 0, 0], "pinky": [0, 1e6, 0, 0] },
            "raw": { "thumb": [], "index": [], "middle": [], "ring": [], "pinky": [] }, 
            "current_avg": { "thumb": 0, "index": 0, "middle": 0, "ring": 0, "pinky": 0 },
            "angle": { "thumb": 0, "index": 0, "middle": 0, "ring": 0, "pinky": 0 }
        }

        self.pip_joints = {
            "calibration_0": { "thumb": [0, 1e6, 0, 0], "index": [0, 1e6, 0, 0], "middle": [0, 1e6, 0, 0], "ring": [0, 1e6, 0, 0], "pinky": [0, 1e6, 0, 0] },
            "calibration_90": { "thumb": [0, 1e6, 0, 0], "index": [0, 1e6, 0, 0], "middle": [0, 1e6, 0, 0], "ring": [0, 1e6, 0, 0], "pinky": [0, 1e6, 0, 0] },
            "raw": { "thumb": [], "index": [], "middle": [], "ring": [], "pinky": [] }, 
            "current_avg": { "thumb": 0, "index": 0, "middle": 0, "ring": 0, "pinky": 0 },
            "angle": { "thumb": 0, "index": 0, "middle": 0, "ring": 0, "pinky": 0 }
        }

        self.relationships = {}

        self.get_relationships()
    
    def select_pin(self, p, pins): 
        for i in range(3): 
            pins[i].value((p >> i) & 1)

    def read_sensors(self): 
        i=0
        while i < len(fingers):

            self.select_pin(i, select_pins)
            self.mcp_joints["raw"][fingers[i]].append(round(z_mux_1.read_u16(), -1))
            
            self.pip_joints["raw"][fingers[i]].append(round(z_mux_2.read_u16(), -1))
            
            # Calculate the simple moving average for each joint
            self.calculate_SMA_MCP(fingers[i])
            self.calculate_SMA_PIP(fingers[i])

            if time_ns() % sampling_time < sampling_time / 2:
                i+=1

    def calibrate(self, client_socket):
        state = ("OPEN", "CLOSE")

        while True:
            calibrationMsg = client_socket.recv(1024).decode("utf-8")
            if calibrationMsg == "calibration_step_1":
                print("calibration step 1 msg received")
                break

        print("MCP changing, PIP fixed @ 0")
        i = 0
        time = time_ns()
        while i < 3:
            self.read_sensors()
            self.update_MCP_extrema()
            if time_ns() - time >= 2e9:
                time = time_ns()
                print(state[i % 2])
                i += 1

        for finger in fingers:
            self.mcp_joints["calibration"][finger][2], self.mcp_joints["calibration"][finger][3] = self.linear_fit(self.mcp_joints["calibration"][finger][0], self.mcp_joints["calibration"][finger][1])

            self.pip_joints["raw"][finger] = []

        client_socket.send("complete".encode('utf-8'))

        while True:
            calibrationMsg = client_socket.recv(1024).decode("utf-8")
            if calibrationMsg == "calibration_step_2":
                break

        print("MCP fixed @ 0, PIP changing")

        i = 0
        time = time_ns()
        while i < 3:
            self.read_sensors()
            for finger in fingers:
                self.pip_joints["calibration_0"][finger][0] = max(self.pip_joints["calibration_0"][finger][0], self.pip_joints["current_avg"][finger])

                self.pip_joints["calibration_0"][finger][1] = min(self.pip_joints["calibration_0"][finger][1], self.pip_joints["current_avg"][finger])
            
            if time_ns() - time > 2e9:
                time = time_ns()
                print(state[i % 2])
                i += 1

        for finger in fingers:
            self.pip_joints["calibration_0"][finger][2], self.pip_joints["calibration_0"][finger][3] = self.linear_fit(self.pip_joints["calibration_0"][finger][0], self.pip_joints["calibration_0"][finger][1])

            self.pip_joints["raw"][finger] = []

        client_socket.send("complete".encode('utf-8'))

        while True:
            calibrationMsg = client_socket.recv(1024).decode("utf-8")
            if calibrationMsg == "calibration_step_3":
                print("calibration step 3 msg received")
                break
            
        print("MCP fixed @ 90, PIP changing")

        i = 0
        time = time_ns()
        while i < 3:
            self.read_sensors()
            for finger in fingers:
                self.pip_joints["calibration_90"][finger][0] = max(self.pip_joints["calibration_90"][finger][0], self.pip_joints["current_avg"][finger])

                self.pip_joints["calibration_90"][finger][1] = min(self.pip_joints["calibration_90"][finger][1], self.pip_joints["current_avg"][finger])
            
            if time_ns() - time > 2e9:
                time = time_ns()
                print(state[i % 2])
                i += 1

        client_socket.send("complete".encode('utf-8'))

        for finger in fingers:
            self.pip_joints["calibration_90"][finger][2], self.pip_joints["calibration_90"][finger][3] = self.linear_fit(self.pip_joints["calibration_90"][finger][0], self.pip_joints["calibration_90"][finger][1])

            self.pip_joints["raw"][finger] = []

        self.write_to_relationships()
        print("Calibration complete")

    def send_data_to_VR(self, client_socket):
        self.read_sensors()
        self.update_angles()
        data_to_send = str(self.mcp_joints["angle"]["thumb"]) + ", " + str(self.pip_joints["angle"]["thumb"]) + ", " + str(self.mcp_joints["angle"]["index"]) + ", " + str(self.pip_joints["angle"]["index"]) + ", " + str(self.mcp_joints["angle"]["middle"]) + ", " + str(self.pip_joints["angle"]["middle"]) + ", " + str(self.mcp_joints["angle"]["ring"]) + ", " + str(self.pip_joints["angle"]["ring"]) + ", " + str(self.mcp_joints["angle"]["pinky"]) + ", " + str(self.pip_joints["angle"]["pinky"]) + " \n"
        client_socket.send(data_to_send.encode('utf-8'))
        # TODO: remove this 10ms sleep and test again
        sleep_ms(10)
    
    # TODO: update this once Stevo is done
    def send_data_to_WBA(self):
        pass

    def update_angles(self):
        for finger in fingers:
            self.update_mcp_angles(finger)
            self.update_pip_angles(finger)

    def update_PIP_extrema(self):
        for finger in fingers:
            self.pip_joints["calibration"][finger][0] = max(self.pip_joints["calibration"][finger][0], self.pip_joints["current_avg"][finger])

            self.pip_joints["calibration"][finger][1] = min(self.pip_joints["calibration"][finger][1], self.pip_joints["current_avg"][finger]) 

    def update_MCP_extrema(self):
        for finger in fingers:
            self.mcp_joints["calibration"][finger][0] = max(self.mcp_joints["calibration"][finger][0], self.mcp_joints["current_avg"][finger])

            self.mcp_joints["calibration"][finger][1] = min(self.mcp_joints["calibration"][finger][1], self.mcp_joints["current_avg"][finger])

    def calculate_SMA_MCP(self, key, window_size=10):
        if len(self.mcp_joints["raw"][key]) > window_size:
            self.mcp_joints["raw"][key].pop(0)
        self.mcp_joints["current_avg"][key] =  round(sum(self.mcp_joints["raw"][key]) / len(self.mcp_joints["raw"][key]), -1)

    def calculate_SMA_PIP(self, key, window_size=10):
        if len(self.pip_joints["raw"][key]) > window_size:
            self.pip_joints["raw"][key].pop(0)
        self.pip_joints["current_avg"][key] =  round(sum(self.pip_joints["raw"][key]) / len(self.pip_joints["raw"][key]), -1)

    def update_mcp_angles(self, finger):
        mcp = self.linear_func(self.mcp_joints["current_avg"][finger], *self.relationships[finger + "_mcp"]) 

        self.mcp_joints["angle"][finger] = round(self.bound(mcp, 0, 90), 2)

    def update_pip_angles(self, finger):
        mcp = self.mcp_joints["angle"][finger]
        pip = self.pip_joints["current_avg"][finger]

        angle_pip_0 = self.linear_func(pip, *self.relationships[finger + "_pip_0"])
        angle_pip_90 = self.linear_func(pip, *self.relationships[finger + "_pip_90"])

        if mcp < 45 and mcp > 0:
            pip = angle_pip_0
        else:
            pip = angle_pip_90

        self.pip_joints["angle"][finger] = round(self.bound(pip, 0, 90), 2)

    def linear_func(self, x, a, b):
        return a * x + b

    def linear_fit(self, x1, x2, y1 = 90, y2 = 0):
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        return m, b

    def bound(self, value, low, high):
        return max(low, min(value, high))
    
    def get_relationships(self):
        try:
            with open('./relationships.json') as f:
                file_data = f.read()
                self.relationships = json.loads(file_data)
        except OSError:
            with open('./relationships.json', 'w+') as f:
                self.set_relationships()
                f.write(json.dumps(self.relationships))

    def write_to_relationships(self):
        self.set_relationships()
        with open('relationships.json', 'w') as f:
            f.write(json.dumps(self.relationships))

    def set_relationships(self):
        # ex) { "index_mcp": [m, b], "index_pip_0": [m, b], "index_pip_90": [m, b] }
        for finger in fingers:
            self.relationships[finger + "_mcp"] = [self.mcp_joints["calibration"][finger][2], self.mcp_joints["calibration"][finger][3]]
            self.relationships[finger + "_pip_0"] = [self.pip_joints["calibration_0"][finger][2], self.pip_joints["calibration_0"][finger][3]]
            self.relationships[finger + "_pip_90"] = [self.pip_joints["calibration_90"][finger][2], self.pip_joints["calibration_90"][finger][3]] 


if __name__ == '__main__':
    try:
        ip = connect()
        sock = open_socket(ip)
        glove = Glove()
        serve(sock, glove)
    except KeyboardInterrupt:
        reset()