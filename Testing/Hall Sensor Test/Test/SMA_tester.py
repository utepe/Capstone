from helpers import calculate_SMA

# Test case 1: Empty list
data = []
current_value = 10
window_size = 5
average = calculate_SMA(data, current_value, window_size)
assert average == 10 

# Test case 2: Window size greater than the list length
data = [1, 2, 3, 4, 5]
current_value = 6
window_size = 10
average = calculate_SMA(data, current_value, window_size)
assert average == 3.5 

# Test case 3: Window size equal to the list length
data = [1, 2, 3, 4]
current_value = 5
window_size = 5
average = calculate_SMA(data, current_value, window_size)
assert average == 3 

# Test case 4: Window size smaller than the list length
data = [1, 2, 3, 4, 5]
current_value = 6
window_size = 5
average = calculate_SMA(data, current_value, window_size)
assert average == 4

print("Everything passed")