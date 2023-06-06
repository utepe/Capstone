import json
from scipy.optimize import curve_fit
import pandas as pd
from helpers import *

# load dataset
headers = ['mcp', 'pip']
data = pd.read_csv('Testing\Hall Sensor Test\Sample_Data\datalogging.csv', skiprows=1, names=headers)

'''data will be an averaged value from around 100 samples from the sensor for each angle'''

# TODO: implement method to remove outliers when processing data
for i in range(len(data["pip"])):
    if(data["pip"][i] > 25000):
        data["pip"].pop(i)

x_index_mcp = [min(data['mcp']), max(data['mcp'])]
y_index_mcp = [0, 90]

x_index_pip = [min(data['pip']), max(data['pip'])]
y_index_pip = [0, 90]

# curve fit, popt contains the coefficients of the polynomial
popt_index_mcp, _ = curve_fit(linear_func, x_index_mcp, y_index_mcp)
a, b = popt_index_mcp
print(f"y = {a:0.3f} * x + {b:0.3f}")

popt_index_pip, _ = curve_fit(linear_func, x_index_pip, y_index_pip)
a, b = popt_index_pip

with open('src/common/relationships.json') as f:
    file_data = f.read()
relationships = json.loads(file_data)

relationships["index_mcp"] = list(popt_index_mcp)
relationships["index_pip"] = list(popt_index_pip)

# print(relationships)
with open('src/common/relationships.json', 'w') as relationship_file:
    relationship_file.write(json.dumps(relationships))