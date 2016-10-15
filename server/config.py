import os
import math

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
SAMPLED_DATA_DIR = os.path.join(DATA_DIR, 'sampled')
WINDOWED_DATA_DIR = os.path.join(DATA_DIR, 'windowed')
COMBINED_DATA_DIR = os.path.join(DATA_DIR, 'combined')
FEATURES_DATA_DIR = os.path.join(DATA_DIR, 'features')

RAW_DATA_RESULT = {
    'sp_accelerometer': 'raw_accelerometer_phone.csv',
    'sp_barometer': 'raw_barometer_phone.csv',
    'sp_gravity': 'raw_gravity_phone.csv',
    'sp_gyroscope': 'raw_gyroscope_phone.csv',
    'sp_linear_accelerometer': 'raw_linear_accelerometer_phone.csv',
    'sp_magnetic': 'raw_magnetic_phone.csv',

    'sw_accelerometer': 'raw_accelerometer_watch.csv',
    'sw_gyroscope': 'raw_gyroscope_watch.csv',
    'sw_light': 'raw_light_watch.csv',
    'sw_pressure': 'raw_pressure_watch.csv',
    'sw_magnetic': 'raw_magnetic_watch.csv',
    'sw_ultraviolet': 'raw_ultraviolet_watch.csv'
}

SAMPLED_DATA_RESULT = {
    'sp_accelerometer': 'sampled_accelerometer_phone.csv',
    'sp_barometer': 'sampled_barometer_phone.csv',
    'sp_gravity': 'sampled_gravity_phone.csv',
    'sp_gyroscope': 'sampled_gyroscope_phone.csv',
    'sp_linear_accelerometer': 'sampled_linear_accelerometer_phone.csv',
    'sp_magnetic': 'sampled_magnetic_phone.csv',

    'sw_accelerometer': 'sampled_accelerometer_watch.csv',
    'sw_gyroscope': 'sampled_gyroscope_watch.csv',
    'sw_light': 'sampled_light_watch.csv',
    'sw_pressure': 'sampled_pressure_watch.csv',
    'sw_magnetic': 'sampled_magnetic_watch.csv',
    'sw_ultraviolet': 'sampled_ultraviolet_watch.csv'
}

WINDOWED_DATA_RESULT = {
    'sp_accelerometer': 'windowed_accelerometer_phone.csv',
    'sp_barometer': 'windowed_barometer_phone.csv',
    'sp_gravity': 'windowed_gravity_phone.csv',
    'sp_gyroscope': 'windowed_gyroscope_phone.csv',
    'sp_linear_accelerometer': 'windowed_linear_accelerometer_phone.csv',
    'sp_magnetic': 'windowed_magnetic_phone.csv',

    'sw_accelerometer': 'windowed_accelerometer_watch.csv',
    'sw_gyroscope': 'windowed_gyroscope_watch.csv',
    'sw_light': 'windowed_light_watch.csv',
    'sw_pressure': 'windowed_pressure_watch.csv',
    'sw_magnetic': 'windowed_magnetic_watch.csv',
    'sw_ultraviolet': 'windowed_ultraviolet_watch.csv'
}

COMBINED_DATA_RESULT = {
    'sp': 'combined_smartphone.csv',
    'sw': 'combined_smartwatch.csv',
    'sp_sw': 'combined_sp_sw.csv',
    'full': 'combined_full.csv'
}

FEATURES_DATA_RESULT = {
    'sp': 'features_smartphone_combined.csv',
    'sw': 'features_smartwatch_combined.csv'
}

SAMPLING_FREQUENCY = 10 # in Hz
SAMPLING_INTERVAL = int(1000 / SAMPLING_FREQUENCY)
OUTLIER_REMOVAL_SIZE = 5000

THRESHOLD_WEIRD_TIMESTAMP_DETECTION = 10
SENSOR_SAMPLING_FREQUENCY = 250 # by observation in the reading logs
N_SAMPLE_WEIRD_TIMESTAMP_REPLACEMENT = math.ceil(SENSOR_SAMPLING_FREQUENCY / SAMPLING_INTERVAL)

WINDOW_SIZE = 2000
WINDOW_OVERLAP = 0.5
N_ROWS_PER_WINDOW = int(WINDOW_SIZE / SAMPLING_INTERVAL)