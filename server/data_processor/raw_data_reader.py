import os
import pandas as pd
import config as CONFIG


def read_all_data(activity_type):
    return {
        'sp_accelerometer': read_csv_data(os.path.join(CONFIG.RAW_DATA_DIR, activity_type, CONFIG.RAW_ACCELEROMETER_RESULT_SMARTPHONE)),
        'sp_barometer': read_csv_data(os.path.join(CONFIG.RAW_DATA_DIR, activity_type, CONFIG.RAW_BAROMETER_RESULT_SMARTPHONE)),
        'sp_gravity': read_csv_data(os.path.join(CONFIG.RAW_DATA_DIR, activity_type, CONFIG.RAW_GRAVITY_RESULT_SMARTPHONE)),
        'sp_gyroscope': read_csv_data(os.path.join(CONFIG.RAW_DATA_DIR, activity_type, CONFIG.RAW_GYROSCOPE_RESULT_SMARTPHONE)),
        'sp_linear_accelerometer': read_csv_data(os.path.join(CONFIG.RAW_DATA_DIR, activity_type, CONFIG.RAW_LINEAR_ACCELEROMETER_RESULT_SMARTPHONE)),
        'sp_magnetic': read_csv_data(os.path.join(CONFIG.RAW_DATA_DIR, activity_type, CONFIG.RAW_MAGNETIC_RESULT_SMARTPHONE)),

        'sw_accelerometer': read_csv_data(os.path.join(CONFIG.RAW_DATA_DIR, activity_type, CONFIG.RAW_ACCELEROMETER_RESULT_SMARTWATCH)),
        'sw_gyroscope': read_csv_data(os.path.join(CONFIG.RAW_DATA_DIR, activity_type, CONFIG.RAW_GYROSCOPE_RESULT_SMARTWATCH)),
        'sw_light': read_csv_data(os.path.join(CONFIG.RAW_DATA_DIR, activity_type, CONFIG.RAW_LIGHT_RESULT_SMARTWATCH)),
        'sw_pressure': read_csv_data(os.path.join(CONFIG.RAW_DATA_DIR, activity_type, CONFIG.RAW_PRESSURE_RESULT_SMARTWATCH)),
        'sw_magnetic': read_csv_data(os.path.join(CONFIG.RAW_DATA_DIR, activity_type, CONFIG.RAW_MAGNETIC_RESULT_SMARTWATCH)),
        'sw_ultraviolet': read_csv_data(os.path.join(CONFIG.RAW_DATA_DIR, activity_type, CONFIG.RAW_ULTRAVIOLET_RESULT_SMARTWATCH))
    }


def read_csv_data(file_path):
    return pd.read_csv(file_path)