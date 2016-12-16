import matplotlib.pyplot as plt
import pandas as pd
import os


path = os.path.join('brushing', '1302edwin_raw_accelerometer_phone.csv')
df = pd.read_csv(path)
x = df['timestamp']
y = df['ax']

plt.plot(x, y)
plt.show()