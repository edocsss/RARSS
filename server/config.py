import os

# DATA SELECTION CONFIGURATIONS
FULL_SUBJECT_LIST = [
    'edwin',
    'shelina',
    'mellita',
    'nikolas',
    'samuel',
    'elmo',
    'monica',
    'inge',
    'andri',
    'arianto',
    'orlin',
    'valerie',
    'nathania',
    'albert',
    'james'
]

# Select whose data to pre-process
PREPROCESS_DATA_SOURCE_SUBJECT = 'james'

# Select whose data to use for MODEL TRAINING DATA --> the data for the subject/s must have been pre-processed
TRAINING_DATA_SOURCE_SUBJECT = [
    'shelina',
    'mellita',
    'nikolas',
    'samuel',
    'elmo',
    'monica',
    'inge',
    'andri',
    'arianto',
    'orlin',
    'valerie',
    'nathania',
    'albert',
    'james'
]

# Select whose data to use for MODEL TESTING DATA --> the data for the subject/s must have been pre-processed
TESTING_DATA_SOURCE_SUBJECT = ['edwin']

# Select whose data to use for the K-FOLD CROSS VALIDATION --> the data for the subject/s must have been pre-processed
KFOLD_DATA_SOURCE_SUBJECT = [
    'edwin',
    'shelina',
    'mellita',
    'nikolas',
    'samuel',
    'elmo',
    'monica',
    'inge',
    'andri',
    'arianto',
    'orlin',
    'valerie',
    'nathania',
    'albert',
    'james'
]

# Select whose data to use for the REAL TIME MONITORING MODEL BUILDING --> the dta for the subject/s must have been pre-processed
REAL_TIME_MONITORING_TRAINING_DATA_SOURCE_SUBJECT = [
    'edwin',
    'shelina',
    'mellita',
    'nikolas',
    'samuel',
    'elmo',
    'monica',
    'inge',
    'andri',
    'arianto',
    'orlin',
    'valerie',
    'nathania',
    'albert',
    'james'
]

SENSOR_SOURCES = {
    'sp': ['sp_accelerometer'], # Change this to include other sensors in the data pre-processing
    'sw': ['sw_accelerometer'], # Change this to include other sensors in the data pre-processing
    'sp_full': [
        'sp_accelerometer',
        'sp_barometer',
        'sp_gravity',
        'sp_gyroscope',
        'sp_linear_accelerometer',
        'sp_magnetic'
    ],
    'sw_full': [
        'sw_accelerometer',
        'sw_gyroscope',
        'sw_light',
        'sw_pressure',
        'sw_magnetic',
        'sw_ultraviolet'
    ]
}

######################################################################################

# DIRECTORY PATH CONFIGURATIONS
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
    'sp': 'benchmark_smartwatch_based_activity_recognition_a_machine_learning_approach_combined_smartphone.csv',
    'sw': 'benchmark_smartwatch_based_activity_recognition_a_machine_learning_approach_combined_smartwatch.csv',
    'sp_sw': 'benchmark_smartwatch_based_activity_recognition_a_machine_learning_approach_combined_sp_sw.csv',
    'full': 'benchmark_smartwatch_based_activity_recognition_a_machine_learning_approach_combined_full_[{}].csv'.format('+'.join(SENSOR_SOURCES['sp'] + SENSOR_SOURCES['sw']))
}

FEATURES_DATA_RESULT = {
    'sp': 'features_smartphone_combined.csv',
    'sw': 'features_smartwatch_combined.csv'
}

######################################################################################

# DATA PREPROCESSING CONFIGURATIONS
SAMPLING_FREQUENCY = 10 # in Hz
WINDOW_SIZE = 2000
WINDOW_OVERLAP = 0.5
STARTING_OUTLIER_REMOVAL_SIZE = 7000
ENDING_OUTLIER_REMOVAL_SIZE = 7000

SAMPLING_INTERVAL = int(1000 / SAMPLING_FREQUENCY)
N_ROWS_PER_WINDOW = int(WINDOW_SIZE / SAMPLING_INTERVAL)
FILE_NAME_SUFFIX = '{}_{}_{}_'.format(SAMPLING_FREQUENCY, WINDOW_SIZE, WINDOW_OVERLAP)

######################################################################################

# MODEL BUILDING CONFIGURATIONS
TRAIN_SIZE = 0.8
TEST_SIZE = 1.0 - TRAIN_SIZE

CLASSIFIER_DIR = os.path.join(ROOT_DIR, 'classifier')
MODEL_DIR = os.path.join(CLASSIFIER_DIR, 'model')
MODEL_NAMES = {
    'minmax_scaler': 'minmax_scaler.p',
    'real_time_monitoring_minmax_scaler': 'real_time_monitoring_minmax_scaler.p',
    'real_time_monitoring_rf_model': 'real_time_monitoring_rf_model.p',
    'real_time_monitoring_svm_model': 'real_time_monitoring_svm_model.p'
}