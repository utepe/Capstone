from time import time_ns
import processing_readings as processing
from helpers import linear_fit

mcp_joints = processing.mcp_joints
pip_joints = processing.pip_joints
fingers = processing.fingers

# update LEDs to indicate calibration mode instead of printing
def calibrate():
    state = ("OPEN", "CLOSE")

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

    input("Press enter to continue...")

    for finger in fingers:
        mcp_joints["calibration"][finger][2], mcp_joints["calibration"][finger][3] = linear_fit(mcp_joints["calibration"][finger][0], mcp_joints["calibration"][finger][1])

        pip_joints["raw"][finger] = []

    print("MCP fixed @ 0, PIP changing")

    i = 0
    time = time_ns()
    while i < 3:
        processing.read_sensors()
        for finger in fingers:
            pip_joints["calibration_0"][finger][0] = max(pip_joints["calibration_0"][finger][0], pip_joints["current_avg"][finger])

            pip_joints["calibration_0"][finger][1] = min(pip_joints["calibration_0"][finger][1], pip_joints["current_avg"][finger])
        
        if time_ns() - time > 2e9:
            print(i)
            time = time_ns()
            print(state[i % 2])
            i += 1

    input("Press enter to continue...")

    for finger in fingers:
        pip_joints["calibration_0"][finger][2], pip_joints["calibration_0"][finger][3] = linear_fit(pip_joints["calibration_0"][finger][0], pip_joints["calibration_0"][finger][1])

        pip_joints["raw"][finger] = []
    
    print("MCP fixed @ 90, PIP changing")

    i = 0
    time = time_ns()
    while i < 3:
        processing.read_sensors()
        for finger in fingers:
            pip_joints["calibration_90"][finger][0] = max(pip_joints["calibration_90"][finger][0], pip_joints["current_avg"][finger])

            pip_joints["calibration_90"][finger][1] = min(pip_joints["calibration_90"][finger][1], pip_joints["current_avg"][finger])
        
        if time_ns() - time > 2e9:
            print(i)
            time = time_ns()
            print(state[i % 2])
            i += 1

    input("Press enter to continue...")

    for finger in fingers:
        pip_joints["calibration_90"][finger][2], pip_joints["calibration_90"][finger][3] = linear_fit(pip_joints["calibration_90"][finger][0], pip_joints["calibration_90"][finger][1])

        pip_joints["raw"][finger] = []

    # TODO: send calibration m and b values to the relationships file
    # ex) { "index_mcp": [m, b], "index_pip_0": [m, b], "index_pip_90": [m, b] } 
    print("Calibration complete")

def update_PIP_extrema():
    for finger in fingers:
        pip_joints["calibration"][finger][0] = max(pip_joints["calibration"][finger][0], pip_joints["current_avg"][finger])

        pip_joints["calibration"][finger][1] = min(pip_joints["calibration"][finger][1], pip_joints["current_avg"][finger]) 

def update_MCP_extrema():
    for finger in fingers:
        mcp_joints["calibration"][finger][0] = max(mcp_joints["calibration"][finger][0], mcp_joints["current_avg"][finger])

        mcp_joints["calibration"][finger][1] = min(mcp_joints["calibration"][finger][1], mcp_joints["current_avg"][finger])