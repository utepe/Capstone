''' 
NOTE: func_glove method is just the name of the 3rd degreee poly method, it will be renamed to something more fitting
def func_glove(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d
'''
'''
Note: micopython does have scipy so alter the func_glove to have default values 
def func_glove(x, a, b, c, d, offset=0, scale=1):
    return scale*(a * x**3 + b * x**2 + c * x + d - offset)
'''

'''
GLOVE CALIBRATION STEPS -> readings to angles
1. Take 100 samples from set angle with the glove for each finger, take average
    store data corresponding to angle in an array of tuples or csv 
2. Repeat step 1 for all angles and array of readings and angles is achieved
    ex) 
    >>> data = [(x = voltage reading, y = angle)] = [(0.41, 0), (0.45, 10), (0.5, 20), ...]
    or
    >>> data = [(voltage readings), (angles)]
3. Pass data for each finger into curve fit method and retrieve coeffiecents of 3rd degree polynomial 
    ex) 
    >>> popt, _ = curve_fit(func_glove, x, y) 
    >>> [a, b, c, d] = popt   
4. Store these coefficients into a dictionary 
    do a json dumps of dict of poly coefficents for each finger, write to file
    ex) 
    >>> relationship = { "thumb_mcp": [],"thumb_pip": [], "index_mcp": [], "index_pip": [], "middle_mcp": [], "middle_pip": [],"ring_mcp": [], "ring_pip": [], "pinky_mcp": [],"pinky_pip": [] }
    >>> relationship["thumb_mcp"] = popt_thumb_mcp
    >>> with open('relationships.txt', 'w') as relationship_file:
    >>>     relationship_file.write(json.dumps(relationships))
'''

'''
USER CALIBRATION STEPS -> new data to angle relationship based on users fingers
1. Load coefficients of calibrated glove function from relationship file as python dict
    ex) 
    >>> with open('relationship_file.txt') as f:
    >>>     data = f.read()
    >>> relationships = json.loads(data)
2. Prompt user to open hands fully and start storing data in array
3. User then closes and opens hand fully to get max bounded ROM for each finger
    ex) 
    >>> userROM_thumb_mcp.append(mcp_joints["raw"]["thumb"])
4. Pass these bounded readings for each finger into func_user method to get bounded angles
    ex) 
    >>> x_bounded_thumb_mcp = np.arange(min(userROM_thumb_mcp), max(userROM_thumb_mcp), 0.001)
    >>> y_bounded_thumb_mcp = func_user(x_bounded, *relationship["thumb_mcp"])
5. Apply curve fitting again to get new coefficients specific for user 
    ex) 
    >>> popt_user_thumb_mcp, _ = curve_fit(func_glove, x_bounded_thumb_mcp, y_bounded_thumb_mcp)
6. User Calibration Complete

When sending data to Unity via Serial Port:

'''

'''
Code Snippet for Writing Serial Port from Pico:
import machine
import time

# Configure the UART (serial port)
uart = machine.UART(0, baudrate=9600)

# Function to send data via serial port
def send_serial_data(data):
    uart.write(data)

# Example usage
while True:
    thumb_mcp_reading = func_glove(mcp_joints["current_avg"]["thumb"], *popt_user_thumb_mcp)
    data_to_send = f"{thumb_reading}, {thumb_pip_reading}... \n"
    send_serial_data(data_to_send)
    time.sleep(1)
'''