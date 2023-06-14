import numpy as np
import matplotlib.pyplot as plt

# Set the angle of separation between vectors in degrees
angle = 10

# Define the initial vectors
v1 = np.array([1, 0])
v2 = np.array([0, 1])

# Calculate the rotation matrix
rotation_matrix = np.array([[np.cos(np.radians(angle)), -np.sin(np.radians(angle))],
                            [np.cos(np.radians(angle)), np.sin(np.radians(angle))]])

# Rotate the second vector by the specified angle
rotated_v2 = rotation_matrix.dot(v2)

# Set up the figure and axes
fig, ax = plt.subplots()

# Plot the vectors
ax.quiver(0, 0, v1[0], v1[1], angles='xy', scale_units='xy', scale=1, color='red', label='Vector 1')
ax.quiver(0, 0, rotated_v2[0], rotated_v2[1], angles='xy', scale_units='xy', scale=1, color='blue', label='Vector 2')

# Set the plot limits
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])

# Set the aspect ratio of the plot
ax.set_aspect('equal')

# Add a legend
ax.legend()

# Show the plot
plt.show()
