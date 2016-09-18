import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
SAMPLED_DATA_DIR = os.path.join(DATA_DIR, 'sampled')

ACCELEROMETER_RESULT_SMARTPHONE = 'accelerometer_phone.csv'
BAROMETER_RESULT_SMARTPHONE = 'barometer_phone.csv'
GRAVITY_RESULT_SMARTPHONE = 'gravity_phone.csv'
GYROSCOPE_RESULT_SMARTPHONE = 'gyroscope_phone.csv'
LINEAR_ACCELEROMETER_RESULT_SMARTPHONE = 'linear_accelerometer_phone.csv'
MAGNETIC_RESULT_SMARTPHONE = 'magnetic_phone.csv'

ACCELEROMETER_RESULT_SMARTWATCH = 'accelerometer_watch.csv'
GYROSCOPE_RESULT_SMARTWATCH = 'gyroscope_watch.csv'
LIGHT_RESULT_SMARTWATCH = 'light_watch.csv'
PRESSURE_RESULT_SMARTWATCH = 'pressure_watch.csv'
MAGNETIC_RESULT_SMARTWATCH = 'magnetic_watch.csv'
ULTRAVIOLET_RESULT_SMARTWATCH = 'ultraviolet_watch.csv'
