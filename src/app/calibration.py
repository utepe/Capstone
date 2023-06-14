from time import time_ns
import processing_readings as processing

mcp_joints = processing.mcp_joints
pip_joints = processing.pip_joints
fingers = processing.fingers

# update LEDs to indicate calibration mode instead of printing
def calibration_mode():
    state = ("OPEN", "CLOSE")

    print("MCP")
    i = 0
    time = time_ns()
    while i < 5:
        processing.read_sensors()
        update_MCP_max()
        if time_ns() - time >= 2e9:
            print(i)
            time = time_ns()
            print(state[i % 2])
            i += 1

    print("PIP")
    i = 0
    time = time_ns()
    while i < 5:
        processing.read_sensors()
        update_PIP_max()
        if time_ns() - time >= 2e9:
            print(i)
            time = time_ns()
            print(state[i % 2])
            i += 1

    for finger in fingers:
        mcp_joints["calibration"][finger][2], mcp_joints["calibration"][finger][3] = linear_fit(mcp_joints["calibration"][finger][0], mcp_joints["calibration"][finger][1])

        pip_joints["calibration"][finger][2], pip_joints["calibration"][finger][3] = linear_fit(pip_joints["calibration"][finger][0], pip_joints["calibration"][finger][1])

def linear_fit(x1, x2, y1 = 0, y2 = 90):
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    return m, b

def update_PIP_max():
    pass 

def update_MCP_max():
    pass