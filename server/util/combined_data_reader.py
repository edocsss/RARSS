import os
import pandas as pd
import config as CONFIG
import pprint


def read_all_combined_data(activity_type):
    smartphone_data = _read_smartphone_combined_data(activity_type)
    smartwatch_data = _read_smartwatch_combined_data(activity_type)

    return {
        'sp': smartphone_data,
        'sw': smartwatch_data
    }


def _read_smartphone_combined_data(activity_type):
    file_path = os.path.join(CONFIG.COMBINED_DATA_DIR, activity_type, CONFIG.FILE_NAME_SUFFIX + '_'.join(CONFIG.PREPROCESS_DATA_SOURCE_SUBJECT) + '_' + CONFIG.COMBINED_DATA_RESULT['sp'])
    return _read_csv_data(file_path)


def _read_smartwatch_combined_data(activity_type):
    file_path = os.path.join(CONFIG.COMBINED_DATA_DIR, activity_type, CONFIG.FILE_NAME_SUFFIX + '_'.join(CONFIG.PREPROCESS_DATA_SOURCE_SUBJECT) + '_' + CONFIG.COMBINED_DATA_RESULT['sw'])
    return _read_csv_data(file_path)


def _read_csv_data(file_path):
    return pd.read_csv(file_path)


if __name__ == '__main__':
    pprint.pprint(_read_smartphone_combined_data('going_downstairs'))
    pprint.pprint(_read_smartwatch_combined_data('going_downstairs'))