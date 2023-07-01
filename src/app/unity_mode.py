# TODO: maybe switch this to use UART serial comm
# handles the data processing and sending to Unity
from app import processing_readings as processing

mcp_joints = processing.mcp_joints
pip_joints = processing.pip_joints

# TODO: will relationships still be needed with the new method of calibration?
def sendData(client_socket):
    processing.read_sensors()
    data_to_send = str(mcp_joints["angle"]["thumb"]) + ", " + str(pip_joints["angle"]["thumb"]) + str(mcp_joints["angle"]["index"]) + ", " + str(pip_joints["angle"]["index"]) + str(mcp_joints["angle"]["middle"]) + ", " + str(pip_joints["angle"]["middle"]) + str(mcp_joints["angle"]["ring"]) + ", " + str(pip_joints["angle"]["ring"]) + str(mcp_joints["angle"]["pinky"]) + ", " + str(pip_joints["angle"]["pinky"]) + "\n"
    client_socket.send(data_to_send.encode('utf-8'))
    # print(data_to_send)
