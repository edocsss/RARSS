import os
import pandas as pd
import config as CONFIG


def sample_data_by_frequency(frequency=10):
    print("SAMPLING DATA AT {}Hz!".format(frequency))


def read_smartphone_accelerometer_data():
    return read_csv_data(os.path.join(CONFIG.RAW_DATA_DIR, CONFIG.ACCELEROMETER_RESULT_SMARTPHONE))


def read_smartwatch_accelerometer_data():
    return read_csv_data(os.path.join(CONFIG.RAW_DATA_DIR, CONFIG.ACCELEROMETER_RESULT_SMARTWATCH))





def read_csv_data(file_path):
    return pd.read_csv(file_path)


if __name__ == '__main__':
    print(CONFIG.RAW_DATA_DIR)