import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
SAMPLED_DATA_DIR = os.path.join(DATA_DIR, 'sampled')
WINDOWED_DATA_DIR = os.path.join(DATA_DIR, 'windowed')

RAW_ACCELEROMETER_RESULT_SMARTPHONE = 'raw_accelerometer_phone.csv'
RAW_BAROMETER_RESULT_SMARTPHONE = 'raw_barometer_phone.csv'
RAW_GRAVITY_RESULT_SMARTPHONE = 'raw_gravity_phone.csv'
RAW_GYROSCOPE_RESULT_SMARTPHONE = 'raw_roscope_phone.csv'
RAW_LINEAR_ACCELEROMETER_RESULT_SMARTPHONE = 'raw_linear_accelerometer_phone.csv'
RAW_MAGNETIC_RESULT_SMARTPHONE = 'raw_magnetic_phone.csv'

RAW_ACCELEROMETER_RESULT_SMARTWATCH = 'raw_accelerometer_watch.csv'
RAW_GYROSCOPE_RESULT_SMARTWATCH = 'raw_gyroscope_watch.csv'
RAW_LIGHT_RESULT_SMARTWATCH = 'raw_light_watch.csv'
RAW_PRESSURE_RESULT_SMARTWATCH = 'raw_pressure_watch.csv'
RAW_MAGNETIC_RESULT_SMARTWATCH = 'raw_magnetic_watch.csv'
RAW_ULTRAVIOLET_RESULT_SMARTWATCH = 'raw_ultraviolet_watch.csv'

SAMPLED_ACCELEROMETER_RESULT_SMARTPHONE = 'sampled_accelerometer_phone.csv'
SAMPLED_BAROMETER_RESULT_SMARTPHONE = 'sampled_barometer_phone.csv'
SAMPLED_GRAVITY_RESULT_SMARTPHONE = 'sampled_gravity_phone.csv'
SAMPLED_GYROSCOPE_RESULT_SMARTPHONE = 'sampled_roscope_phone.csv'
SAMPLED_LINEAR_ACCELEROMETER_RESULT_SMARTPHONE = 'sampled_linear_accelerometer_phone.csv'
SAMPLED_MAGNETIC_RESULT_SMARTPHONE = 'sampled_magnetic_phone.csv'

SAMPLED_ACCELEROMETER_RESULT_SMARTWATCH = 'sampled_accelerometer_watch.csv'
SAMPLED_GYROSCOPE_RESULT_SMARTWATCH = 'sampled_gyroscope_watch.csv'
SAMPLED_LIGHT_RESULT_SMARTWATCH = 'sampled_light_watch.csv'
SAMPLED_PRESSURE_RESULT_SMARTWATCH = 'sampled_pressure_watch.csv'
SAMPLED_MAGNETIC_RESULT_SMARTWATCH = 'sampled_magnetic_watch.csv'
SAMPLED_ULTRAVIOLET_RESULT_SMARTWATCH = 'sampled_ultraviolet_watch.csv'

COMBINED_SAMPLED_SMARTPHONE_DATA = 'sampled_smartphone_combined.csv'
COMBINED_SAMPLED_SMARTWATCH_DATA = 'sampled_smartwatch_combined.csv'

WINDOWED_SMARTPHONE_DATA = 'windowed_smartphone_combined.csv'
WINDOWED_SMARTWATCH_DATA = 'windowed_smartwatch_combined.csv'

SAMPLING_FREQUENCY = 10 # in Hz
SAMPLING_INTERVAL = int(1000 / SAMPLING_FREQUENCY)
OUTLIER_REMOVAL_SIZE = 1000

WINDOW_SIZE = 2000
WINDOW_OVERLAP = 0.5