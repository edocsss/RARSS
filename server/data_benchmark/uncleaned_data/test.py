import pandas as pd


f_path = 'cycling/31235subject101_raw_accelerometer_phone.csv'
df = pd.read_csv(f_path)
print(df['timestamp'] - df['timestamp'].min())