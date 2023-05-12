# Setup smoothing parameters
window_length = 10
readings = [0] * window_length
read_index = 0
total = 0
moving_avg = 0

# perform smoothing by taking simple moving average (SMA)
# this does have slow start tho which isnt ideal
def smoothing():
    global moving_avg, read_index, readings, index
    reading # hall sensor reading  
    print(f'Hall sensor value: {reading}')

    moving_avg += (1/window_length)*(reading - readings[read_index])
    readings[read_index] = reading

    read_index += 1
    if read_index >= window_length:
        read_index = 0
    
    return reading, moving_avg