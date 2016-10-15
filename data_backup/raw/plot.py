import matplotlib.pyplot as plt
import pandas as pd
import os


path = os.path.join('folding', '1_raw_accelerometer_watch.csv')
df = pd.read_csv(path)
x = df['timestamp']
y = df['ax']

plt.plot(x, y)
plt.show()