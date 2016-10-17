import os
import config as CONFIG
import pandas as pd
from util import sampled_data_reader
from models.data_item import DataItem


def divide_and_store_sampled_data_to_windows(activity_type):
    sampled_data = sampled_data_reader.read_all_sampled_data(activity_type)
    windowed_data = {}

    for k, v in sampled_data.items():
        result = []
        for sampled_data_item in v:
            file_id = sampled_data_item.file_id
            dataframe = sampled_data_item.dataframe

            windowed_dataframe = _divide_dataframe_to_windows(dataframe)
            result.append(DataItem(file_id, windowed_dataframe))

        windowed_data[k] = result

    _store_windowed_data_to_files(windowed_data, activity_type)


def _divide_dataframe_to_windows(df):
    result_df = pd.DataFrame(data=None, columns=df.columns)
    row_step = int(CONFIG.N_ROWS_PER_WINDOW * CONFIG.WINDOW_OVERLAP)
    total_rows = df.shape[0]

    for i in range(0, total_rows, row_step):
        # Ignore the last window if the last window is NOT FULL!
        if i + CONFIG.N_ROWS_PER_WINDOW > total_rows:
            break

        window_df = df[i:i + CONFIG.N_ROWS_PER_WINDOW]
        result_df = result_df.append(window_df, ignore_index=True)

    return result_df


def _create_windowed_data_directory():
    dir_path = os.path.join(CONFIG.WINDOWED_DATA_DIR)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def _create_windowed_activity_directory(activity_type):
    dir_path = os.path.join(CONFIG.WINDOWED_DATA_DIR, activity_type)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def _store_windowed_data_to_files(windowed_data, activity_type):
    print('Writing windowed data to files..')
    _create_windowed_data_directory()
    _create_windowed_activity_directory(activity_type)

    for k, v in windowed_data.items():
        for windowed_data_item in v:
            file_name = CONFIG.FILE_NAME_SUFFIX + windowed_data_item.file_id + '_' + CONFIG.WINDOWED_DATA_RESULT[k]
            _write_windowed_dataframe_to_csv(activity_type, file_name, windowed_data_item.dataframe)

    print('Windowed data stored!')


def _write_windowed_dataframe_to_csv(activity_type, file_name, dataframe):
    file_path = os.path.join(CONFIG.WINDOWED_DATA_DIR, activity_type, file_name)
    dataframe.to_csv(file_path)