from time import time_ns

import json
import processing_readings as processing
from helpers import linear_fit
from common import config as cfg

# update LEDs to indicate calibration mode instead of printing
def calibrate(client_socket):
    state = ("OPEN", "CLOSE")

    while True:
        calibrationMsg = client_socket.recv(1024)
        if calibrationMsg == "calibration_step_1":
            break

    print("MCP changing, PIP fixed @ 0")
    i = 0
    time = time_ns()
    while i < 3:
        processing.read_sensors()
        update_MCP_extrema()
        if time_ns() - time >= 2e9:
            print(i)
            time = time_ns()
            print(state[i % 2])
            i += 1

    client_socket.send("complete".encode('utf-8'))

    while True:
        calibrationMsg = client_socket.recv(1024)
        if calibrationMsg == "calibration_step_2":
            break

    for finger in cfg.fingers:
        cfg.mcp_joints["calibration"][finger][2], cfg.mcp_joints["calibration"][finger][3] = linear_fit(cfg.mcp_joints["calibration"][finger][0], cfg.mcp_joints["calibration"][finger][1])

        cfg.pip_joints["raw"][finger] = []

    print("MCP fixed @ 0, PIP changing")

    i = 0
    time = time_ns()
    while i < 3:
        processing.read_sensors()
        for finger in cfg.fingers:
            cfg.pip_joints["calibration_0"][finger][0] = max(cfg.pip_joints["calibration_0"][finger][0], cfg.pip_joints["current_avg"][finger])

            cfg.pip_joints["calibration_0"][finger][1] = min(cfg.pip_joints["calibration_0"][finger][1], cfg.pip_joints["current_avg"][finger])
        
        if time_ns() - time > 2e9:
            print(i)
            time = time_ns()
            print(state[i % 2])
            i += 1

    client_socket.send("complete".encode('utf-8'))

    while True:
        calibrationMsg = client_socket.recv(1024)
        if calibrationMsg == "calibration_step_3":
            break

    for finger in cfg.fingers:
        cfg.pip_joints["calibration_0"][finger][2], cfg.pip_joints["calibration_0"][finger][3] = linear_fit(cfg.pip_joints["calibration_0"][finger][0], cfg.pip_joints["calibration_0"][finger][1])

        cfg.pip_joints["raw"][finger] = []
    
    print("MCP fixed @ 90, PIP changing")

    i = 0
    time = time_ns()
    while i < 3:
        processing.read_sensors()
        for finger in cfg.fingers:
            cfg.pip_joints["calibration_90"][finger][0] = max(cfg.pip_joints["calibration_90"][finger][0], cfg.pip_joints["current_avg"][finger])

            cfg.pip_joints["calibration_90"][finger][1] = min(cfg.pip_joints["calibration_90"][finger][1], cfg.pip_joints["current_avg"][finger])
        
        if time_ns() - time > 2e9:
            print(i)
            time = time_ns()
            print(state[i % 2])
            i += 1


    for finger in cfg.fingers:
        cfg.pip_joints["calibration_90"][finger][2], cfg.pip_joints["calibration_90"][finger][3] = linear_fit(cfg.pip_joints["calibration_90"][finger][0], cfg.pip_joints["calibration_90"][finger][1])

        cfg.pip_joints["raw"][finger] = []

    # ex) { "index_mcp": [m, b], "index_pip_0": [m, b], "index_pip_90": [m, b] } 
    writeToRelationships()
    print("Calibration complete")

def update_PIP_extrema():
    for finger in cfg.fingers:
        cfg.pip_joints["calibration"][finger][0] = max(cfg.pip_joints["calibration"][finger][0], cfg.pip_joints["current_avg"][finger])

        cfg.pip_joints["calibration"][finger][1] = min(cfg.pip_joints["calibration"][finger][1], cfg.pip_joints["current_avg"][finger]) 

def update_MCP_extrema():
    for finger in cfg.fingers:
        cfg.mcp_joints["calibration"][finger][0] = max(cfg.mcp_joints["calibration"][finger][0], cfg.mcp_joints["current_avg"][finger])

        cfg.mcp_joints["calibration"][finger][1] = min(cfg.mcp_joints["calibration"][finger][1], cfg.mcp_joints["current_avg"][finger])

def writeToRelationships():
    with open('src/common/relationships.json') as f:
        file_data = f.read()
    f.close()
    
    relationships = json.loads(file_data)

    # ex) { "index_mcp": [m, b], "index_pip_0": [m, b], "index_pip_90": [m, b] }
    for finger in cfg.fingers:
        relationships[finger + "_mcp"] = [cfg.mcp_joints["calibration"][finger][2], cfg.mcp_joints["calibration"][finger][3]]
        relationships[finger + "_pip_0"] = [cfg.pip_joints["calibration_0"][finger][2], cfg.pip_joints["calibration_0"][finger][3]]
        relationships[finger + "_pip_90"] = [cfg.pip_joints["calibration_90"][finger][2], cfg.pip_joints["calibration_90"][finger][3]] 

    with open('src/common/relationships.json', 'w') as relationship_file:
        relationship_file.write(json.dumps(relationships))
    
    relationship_file.close()