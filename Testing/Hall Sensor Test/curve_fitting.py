import numpy as np
from scipy.optimize import curve_fit

def func(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

