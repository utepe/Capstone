# handles the data processing and sending to Unity
from app import processing_readings as processing
from common import config as cfg

def sendData(client_socket):
    processing.read_sensors()
    data_to_send = str(cfg.mcp_joints["angle"]["thumb"]) + ", " + str(cfg.pip_joints["angle"]["thumb"]) + str(cfg.mcp_joints["angle"]["index"]) + ", " + str(cfg.pip_joints["angle"]["index"]) + str(cfg.mcp_joints["angle"]["middle"]) + ", " + str(cfg.pip_joints["angle"]["middle"]) + str(cfg.mcp_joints["angle"]["ring"]) + ", " + str(cfg.pip_joints["angle"]["ring"]) + str(cfg.mcp_joints["angle"]["pinky"]) + ", " + str(cfg.pip_joints["angle"]["pinky"]) + "\n"
    client_socket.send(data_to_send.encode('utf-8'))
    # print(data_to_send)
