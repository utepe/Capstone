# TODO: maybe switch this to use UART serial comm
# handles the data processing and sending to Unity
from app import processing_readings as processing

# TODO: will relationships still be needed with the new method of calibration?
def sendData(mcp_joints, pip_joints, relationships):
    processing.read_sensors()

    data_to_send = str(mcp_joints["angle"]["thumb"]) + ", " + str(pip_joints["angle"]["thumb"]) + str(mcp_joints["angle"]["index"]) + ", " + str(pip_joints["angle"]["index"]) + str(mcp_joints["angle"]["middle"]) + ", " + str(pip_joints["angle"]["middle"]) + str(mcp_joints["angle"]["ring"]) + ", " + str(pip_joints["angle"]["ring"]) + str(mcp_joints["angle"]["pinky"]) + ", " + str(pip_joints["angle"]["pinky"]) + "\n"

    print(data_to_send)
