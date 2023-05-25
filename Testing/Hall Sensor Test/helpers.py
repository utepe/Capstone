# Calculate the simple moving average for each joint
def calculate_SMA(data, current_value, window_size=10):
    data.append(current_value)
    if len(data) > window_size:
        data.pop(0)
    return sum(data) / len(data)