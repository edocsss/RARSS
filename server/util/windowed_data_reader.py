import os
import pandas as pd
import config as CONFIG
import pprint
from models.data_item import DataItem
from util import text_util


def read_all_windowed_data(activity_type):
    smartphone_data = read_smartphone_windowed_data(activity_type)
    smartwatch_data = read_smartwatch_windowed_data(activity_type)
    return {**smartphone_data, **smartwatch_data}


def read_smartphone_windowed_data(activity_type):
    file_names = get_file_names_in_windowed_directory_by_activity(activity_type)
    file_name_per_sensor = {
        sensor_key: _get_file_name_by_sensor_and_suffix(
            file_names,
            sensor_key
        ) for sensor_key in CONFIG.SENSOR_SOURCES['sp']
    }

    return read_windowed_data_by_activity_and_source(activity_type, file_name_per_sensor)


def read_smartwatch_windowed_data(activity_type):
    file_names = get_file_names_in_windowed_directory_by_activity(activity_type)
    file_name_per_sensor = {
        sensor_key: _get_file_name_by_sensor_and_suffix(
            file_names,
            sensor_key
        ) for sensor_key in CONFIG.SENSOR_SOURCES['sw']
    }

    return read_windowed_data_by_activity_and_source(activity_type, file_name_per_sensor)


def get_file_names_in_windowed_directory_by_activity(activity_type):
    windowed_activity_dir = os.path.join(CONFIG.WINDOWED_DATA_DIR, activity_type)
    return [file_name for file_name in os.listdir(windowed_activity_dir) if CONFIG.FILE_NAME_SUFFIX in file_name]


def read_windowed_data_by_activity_and_source(activity_type, file_name_per_sensor):
    try:
        result = {}
        for k, v in file_name_per_sensor.items():
            data_per_sensor = []
            for file_name in v:
                if text_util.check_list_element_in_string(file_name, CONFIG.TRAINING_DATA_SOURCE_SUBJECT):
                    file_id = file_name.split('_')[3]
                    file_path = os.path.join(CONFIG.WINDOWED_DATA_DIR, activity_type, file_name)
                    data_per_sensor.append(DataItem(file_id, read_csv_data(file_path)))

            result[k] = data_per_sensor

        return result

    except:
        return None


def _get_file_name_by_sensor_and_suffix(file_names, file_key):
    return [file_name for file_name in file_names if CONFIG.WINDOWED_DATA_RESULT[file_key] in file_name]


def read_csv_data(file_path):
    return pd.read_csv(file_path)


if __name__ == '__main__':
    pprint.pprint(read_smartphone_windowed_data('testing'))
    pprint.pprint(read_smartwatch_windowed_data('testing'))