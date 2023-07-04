'''
Functions to help with the calibration and data processing
'''

# define the true objective linear function
def linear_func(x, a, b):
    return a * x + b

def linear_fit(x1, x2, y1 = 0, y2 = 90):
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    return m, b

def bound(value, low, high):
    return max(low, min(value, high))

def func_glove(x, a, b, scale=1, offset=0):
    return scale*(a * x + b - offset)

def func_user(x, a, b):
    offset = func_glove(min(x), a, b)
    scale = 90/(func_glove(max(x), a, b) - offset)
    return scale*(func_glove(x, a, b) - offset)

def user_calibration(x, a, b):
    offset = func_glove(min(x), a, b)
    scale = 90/(func_glove(max(x), a, b) - offset)
    return scale, offset