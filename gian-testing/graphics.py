import serial
from time import sleep
import ast
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.animation as animation

def data_gen(num):
    """Data generation"""
    angle = num * np.pi/36    
    vx, vy, vz = np.cos(angle), np.sin(angle), 1
    ax.cla()
    ax.quiver(0, 0, 0, vx, vy, vz, pivot="tail", color="black")
    ax.quiver(0, 0, 0, vx, vy, 0, pivot="tail", color="black",
              linestyle="dashed")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.view_init(elev=30, azim=60)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
data_gen(0)
ani = animation.FuncAnimation(fig, data_gen, frames = 2000, interval = 10, blit=False)
plt.show()

'''
index = [-10, -10, 10]
v = [0, 5, 4]
q = [7, 8, 10]

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlim([-10, 10])
ax.set_ylim([-10, 10])
ax.set_zlim([0, 10])

start = [0, 0, 0]

ax.quiver(start[0], start[1], start[2], u[0], u[1], u[2], color='r', arrow_length_ratio=0.1)
ax.quiver(start[0], start[1], start[2], v[0], v[1], v[2], color='b', arrow_length_ratio=0.1)
ax.quiver(start[0], start[1], start[2], q[0], q[1], q[2], color='g', arrow_length_ratio=0.1)

plt.show()
'''
'''
ser = serial.Serial("COM7", 9600)    #Open port with baud rate
while True:
    received_data = ser.read()              #read serial port
    sleep(0.03)
    
    data_left = ser.inWaiting()             #check for remaining byte
    received_data += ser.read(data_left)
    received_data = ast.literal_eval(received_data.decode("utf-8"))
'''
    