import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.pyplot as plt

headers = ['value', 'degrees']
data = pd.read_csv('Sample_Data\Hall_Sensor_Data_Reverse_LUT.csv', skiprows=1, names=headers)

def func(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

x = data['value']
y = data['degrees']

popt, _ = curve_fit(func, x, y)
a, b, c, d = popt
print(f"y = {a:0.3f} * x**3 + {b:0.3f} * x**2 + {c:0.3f} * x + {d:0.3f}")

plt.plot(x, y, 'o', label='raw data')

x_line = np.arange(min(x), max(x), 0.01)
y_line = func(x_line, a, b, c, d)

plt.plot(x_line, y_line, label="curve")
plt.legend()

plt.show()
