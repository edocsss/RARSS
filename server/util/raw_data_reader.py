import os
import pandas as pd
import config as CONFIG
import pprint
from models.data_item import DataItem
from util import text_util


def read_all_raw_data(activity_type, data_subjects):
    smartphone_data = read_smartphone_raw_data(activity_type, data_subjects)
    smartwatch_data = read_smartwatch_raw_data(activity_type, data_subjects)
    return {**smartphone_data, **smartwatch_data}


def read_smartphone_raw_data(activity_type, data_subjects, sensors=CONFIG.SENSOR_SOURCES['sp']):
    file_names = _get_file_names_in_raw_directory_by_activity(activity_type, data_subjects)
    file_name_per_sensor = {
        sensor_key: _get_file_name_by_sensor_and_suffix(
            file_names,
            sensor_key
        ) for sensor_key in sensors
    }

    return _read_raw_data_by_activity_and_source(activity_type, file_name_per_sensor)


def read_smartwatch_raw_data(activity_type, data_subjects, sensors=CONFIG.SENSOR_SOURCES['sw']):
    file_names = _get_file_names_in_raw_directory_by_activity(activity_type, data_subjects)
    file_name_per_sensor = {
        sensor_key: _get_file_name_by_sensor_and_suffix(
            file_names,
            sensor_key
        ) for sensor_key in sensors
    }

    return _read_raw_data_by_activity_and_source(activity_type, file_name_per_sensor)


def _get_file_names_in_raw_directory_by_activity(activity_type, data_subjects):
    raw_activity_dir = os.path.join(CONFIG.RAW_DATA_DIR, activity_type)
    all_file_names = os.listdir(raw_activity_dir)
    return [file_name for file_name in all_file_names for subject_name in data_subjects if subject_name in file_name]


def _get_file_name_by_sensor_and_suffix(file_names, file_key):
    return [file_name for file_name in file_names if CONFIG.RAW_DATA_RESULT[file_key] in file_name]


def _read_raw_data_by_activity_and_source(activity_type, file_name_per_sensor):
    try:
        result = {}
        for k, v in file_name_per_sensor.items():
            data_per_sensor = []
            for file_name in v:
                file_id = file_name.split('_')[0]
                file_path = os.path.join(CONFIG.RAW_DATA_DIR, activity_type, file_name)
                data_per_sensor.append(DataItem(file_id, _read_csv_data(file_path)))

            result[k] = data_per_sensor


        return result

    except:
        return None


def _read_csv_data(file_path):
    return pd.read_csv(file_path)


if __name__ == '__main__':
    pprint.pprint(read_smartphone_raw_data('standing', ['edwin']))
    # pprint.pprint(read_smartwatch_raw_data('standing', ['richsen']))