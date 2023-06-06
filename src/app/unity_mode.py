# TODO: maybe switch this to use UART serial comm
# handles the data processing and sending to Unity
from app import helpers, processing_readings as processing

def sendData(mcp_joints, pip_joints, relationships):
    processing.read_sensors()

    thumb_mcp_reading = helpers.linear_func(mcp_joints["current_avg"]["thumb"], *relationships["thumb_mcp"])
    thumb_pip_reading = helpers.linear_func(pip_joints["current_avg"]["thumb"], *relationships["thumb_pip"])
    index_mcp_reading = helpers.linear_func(mcp_joints["current_avg"]["index"], *relationships["index_mcp"])
    index_pip_reading = helpers.linear_func(pip_joints["current_avg"]["index"], *relationships["index_pip"])
    middle_mcp_reading = helpers.linear_func(mcp_joints["current_avg"]["middle"], *relationships["middle_mcp"])
    middle_pip_reading = helpers.linear_func(pip_joints["current_avg"]["middle"], *relationships["middle_pip"])
    ring_mcp_reading = helpers.linear_func(mcp_joints["current_avg"]["ring"], *relationships["ring_mcp"])
    ring_pip_reading = helpers.linear_func(pip_joints["current_avg"]["ring"], *relationships["ring_pip"])
    pinky_mcp_reading = helpers.linear_func(mcp_joints["current_avg"]["pinky"], *relationships["pinky_mcp"])
    pinky_pip_reading = helpers.linear_func(pip_joints["current_avg"]["pinky"], *relationships["pinky_pip"])

    data_to_send = str(thumb_mcp_reading) + ", " + str(thumb_pip_reading) + str(index_mcp_reading) + ", " + str(index_pip_reading) + str(middle_mcp_reading) + ", " + str(middle_pip_reading) + str(ring_mcp_reading) + ", " + str(ring_pip_reading) + str(pinky_mcp_reading) + ", " + str(pinky_pip_reading) + "\n"

    print(data_to_send)
