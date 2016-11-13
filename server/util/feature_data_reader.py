import os
import pandas as pd
import config as CONFIG
import pprint


def read_all_windowed_data(activity_type):
    smartphone_data = read_smartphone_features_data(activity_type)
    smartwatch_data = read_smartwatch_features_data(activity_type)
    return {
        'sp': smartphone_data,
        'sw': smartwatch_data
    }


def read_smartphone_features_data(activity_type):
    file_path = os.path.join(CONFIG.FEATURES_DATA_DIR, activity_type, CONFIG.FILE_NAME_SUFFIX + '_'.join(CONFIG.PREPROCESS_DATA_SOURCE_SUBJECT) + '_' + CONFIG.FEATURES_DATA_RESULT['sp'])
    return read_csv_data(file_path)


def read_smartwatch_features_data(activity_type):
    file_path = os.path.join(CONFIG.FEATURES_DATA_DIR, activity_type, CONFIG.FILE_NAME_SUFFIX + '_'.join(CONFIG.PREPROCESS_DATA_SOURCE_SUBJECT) + '_' + CONFIG.FEATURES_DATA_RESULT['sw'])
    return read_csv_data(file_path)


def read_csv_data(file_path):
    return pd.read_csv(file_path)


if __name__ == '__main__':
    pprint.pprint(read_smartphone_features_data('going_downstairs'))
    pprint.pprint(read_smartwatch_features_data('going_downstairs'))