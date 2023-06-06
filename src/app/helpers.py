'''
Functions to help with the calibration and data processing
'''

# define the true objective linear function
def linear_func(x, a, b):
    return a * x + b

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