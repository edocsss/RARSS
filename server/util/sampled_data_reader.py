import os
import pandas as pd
import config as CONFIG
import pprint
from models.data_item import DataItem


def read_all_sampled_data(activity_type):
    smartphone_data = read_smartphone_sampled_data(activity_type)
    smartwatch_data = read_smartwatch_sampled_data(activity_type)
    return {**smartphone_data, **smartwatch_data}


def read_smartphone_sampled_data(activity_type):
    file_names = get_file_names_in_sampled_directory_by_activity(activity_type)
    file_name_per_sensor = {
        'sp_accelerometer': [file_name for file_name in file_names if file_name.find(CONFIG.SAMPLED_DATA_RESULT['sp_accelerometer']) >= 0],
        'sp_barometer': [file_name for file_name in file_names if file_name.find(CONFIG.SAMPLED_DATA_RESULT['sp_barometer']) >= 0],
        'sp_gravity': [file_name for file_name in file_names if file_name.find(CONFIG.SAMPLED_DATA_RESULT['sp_gravity']) >= 0],
        'sp_gyroscope': [file_name for file_name in file_names if file_name.find(CONFIG.SAMPLED_DATA_RESULT['sp_gyroscope']) >= 0],
        'sp_linear_accelerometer': [file_name for file_name in file_names if file_name.find(CONFIG.SAMPLED_DATA_RESULT['sp_linear_accelerometer']) >= 0],
        'sp_magnetic': [file_name for file_name in file_names if file_name.find(CONFIG.SAMPLED_DATA_RESULT['sp_magnetic']) >= 0]
    }

    return read_sampled_data_by_activity_and_source(activity_type, file_name_per_sensor)


def read_smartwatch_sampled_data(activity_type):
    file_names = get_file_names_in_sampled_directory_by_activity(activity_type)
    file_name_per_sensor = {
        'sw_accelerometer': [file_name for file_name in file_names if file_name.find(CONFIG.SAMPLED_DATA_RESULT['sw_accelerometer']) >= 0],
        'sw_gyroscope': [file_name for file_name in file_names if file_name.find(CONFIG.SAMPLED_DATA_RESULT['sw_gyroscope']) >= 0],
        'sw_light': [file_name for file_name in file_names if file_name.find(CONFIG.SAMPLED_DATA_RESULT['sw_light']) >= 0],
        'sw_pressure': [file_name for file_name in file_names if file_name.find(CONFIG.SAMPLED_DATA_RESULT['sw_pressure']) >= 0],
        'sw_magnetic': [file_name for file_name in file_names if file_name.find(CONFIG.SAMPLED_DATA_RESULT['sw_magnetic']) >= 0],
        'sw_ultraviolet': [file_name for file_name in file_names if file_name.find(CONFIG.SAMPLED_DATA_RESULT['sw_ultraviolet']) >= 0]
    }

    return read_sampled_data_by_activity_and_source(activity_type, file_name_per_sensor)


def get_file_names_in_sampled_directory_by_activity(activity_type):
    sampled_activity_dir = os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type)
    return os.listdir(sampled_activity_dir)


def read_sampled_data_by_activity_and_source(activity_type, file_name_per_sensor):
    try:
        result = {}
        for k, v in file_name_per_sensor.items():
            data_per_sensor = []
            for file_name in v:
                file_path = os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, file_name)
                data_per_sensor.append(DataItem(file_name, read_csv_data(file_path)))

            result[k] = data_per_sensor


        return result

    except:
        return None

def read_csv_data(file_path):
    return pd.read_csv(file_path)


if __name__ == '__main__':
    pprint.pprint(read_smartphone_sampled_data('standing'))
    pprint.pprint(read_smartwatch_sampled_data('standing'))