import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import os



path = os.path.join('brushing', '1302edwin_raw_accelerometer_phone.csv')
df = pd.read_csv(path)

x = df['ax']
y = df['ay']
z = df['az']

plt.plot(x, y)
plt.show()