import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.pyplot as plt

# define the true objective function (3rd degree polynomial)
def func(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

# load dataset
headers = ['value', 'angle']
data = pd.read_csv('Sample_Data\Hall_Sensor_Data_Reverse_LUT.csv', skiprows=1, names=headers)

'''data will be an averaged value from aorund 100 samples from the sensor for each angle'''
x = data['value']
y = data['angle']

# curve fit, popt contains the coefficients of the polynomial
popt, _ = curve_fit(func, x, y)
a, b, c, d = popt
print(f"y = {a:0.3f} * x**3 + {b:0.3f} * x**2 + {c:0.3f} * x + {d:0.3f}")

x_line = np.arange(min(x), max(x), 0.01)
y_line = func(x_line, a, b, c, d)

plt.plot(x, y, 'o', label='raw data')
plt.plot(x_line, y_line, label="curve")
plt.legend()

plt.show()
