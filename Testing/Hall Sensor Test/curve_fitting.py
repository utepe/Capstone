import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.pyplot as plt

# normalize the data to be between 0 and 1 (min value is 0, max value is 1)
def normalize(data):
    return (data - min(data)) / (max(data) - min(data))

# define the true objective function (3rd degree polynomial)
def func_glove(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

def func_user(x, a, b, c, d):
    offset = func_glove(min(x), a, b, c, d)
    scale = 90/(func_glove(max(x), a, b, c, d) - offset)
    return scale*(func_glove(x, a, b, c, d) - offset)

# load dataset
headers = ['value', 'angle']
data = pd.read_csv('Testing\Hall Sensor Test\Sample_Data\Hall_Sensor_Data_Reverse_LUT.csv', skiprows=1, names=headers)

'''data will be an averaged value from around 100 samples from the sensor for each angle'''
x = data['value']
# x = normalize(data['value'])
y = data['angle']/2

# curve fit, popt contains the coefficients of the polynomial
popt, _ = curve_fit(func_glove, x, y)
a, b, c, d = popt
print(f"y = {a:0.3f} * x**3 + {b:0.3f} * x**2 + {c:0.3f} * x + {d:0.3f}")

x_line = np.arange(min(x), max(x), 0.01)
y_line = func_glove(x_line, *popt)

''' DEPRECATED
if testing on a user, and their min is 0.25 and max is 0.75 so then the curve will be normalized between 0.25 and 0.75
during user calibration we will take these bounded and normalized values again to get range of 0 to 1 mapping to 0 to 180 degrees 
'''
# x_bounded = normalize(np.arange(0.25, 0.75, 0.01))
# y_bounded = func_glove(x_bounded, a, b, c, d)
# plt.plot(x_bounded, y_bounded, label="bounded curve")

# user test -> using func_user method to plot the scaled curve based on the bounded region
# x_bounded = np.arange(0.6, 0.7, 0.001)
# y_bounded = func_user(x_bounded, *popt)
# popt, _ = curve_fit(func_glove, x_bounded, y_bounded)
# e, f, g, h = popt
# print(f"y = {e:0.3f} * x**3 + {f:0.3f} * x**2 + {g:0.3f} * x + {h:0.3f}")
# plt.plot(x_bounded, y_bounded, label="bounded curve")

# plt.plot(x, y, 'o', label='raw data')
# plt.plot(x_line, y_line, label="curve")
# plt.legend()

# plt.show()

 # Open the file in write mode
file = open("Testing\Hall Sensor Test\Sample_Data\sampleAngles.txt", "w")
start = 0.41
end = 0.71
step = 0.01

for i in range(int(start * 100), int(end * 100) + 1, int(step * 100)):
    # Write text to the file
    file.write(f"{func_glove(i/100, *popt)/2}, {func_glove(i/100, *popt)}\n")

# Close the file
file.close()
