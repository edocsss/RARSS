import os
import config as CONFIG
import pandas as pd
from util import windowed_data_reader


def combine_data(activity_type):
    merged_smartphone_dfs = _merge_smartphone_data(activity_type)
    merged_smartwatch_dfs = _merge_smartwatch_data(activity_type)

    combined_smartphone_dfs = _combine_data_into_one(merged_smartphone_dfs)
    combined_smartwatch_dfs = _combine_data_into_one(merged_smartwatch_dfs)

    merged_smartphone_dfs = _drop_irrelevant_columns(combined_smartphone_dfs)
    merged_smartwatch_dfs = _drop_irrelevant_columns(combined_smartwatch_dfs)

    _create_combined_data_directory()
    _create_combined_activity_directory(activity_type)

    _write_combined_dataframe_to_csv(activity_type, merged_smartphone_dfs, is_smartphone=True)
    _write_combined_dataframe_to_csv(activity_type, merged_smartwatch_dfs, is_smartphone=False)


def _merge_smartphone_data(activity_type):
    windowed_smartphone_data = windowed_data_reader.read_smartphone_windowed_data(activity_type)
    combined_smartphone_data = _merge_sensory_data_to_one(windowed_smartphone_data)
    return combined_smartphone_data


def _merge_smartwatch_data(activity_type):
    windowed_smartwatch_data = windowed_data_reader.read_smartwatch_windowed_data(activity_type)
    combined_smartwatch_data = _merge_sensory_data_to_one(windowed_smartwatch_data)
    return combined_smartwatch_data


def _merge_sensory_data_to_one(windowed_data):
    first_key = list(windowed_data.keys())[0]
    n_experiment = len(windowed_data[first_key])
    combined_df_result = []

    for i in range(n_experiment):
        timestamps = windowed_data[first_key][0].dataframe['timestamp']
        merged_df = pd.DataFrame(data=timestamps, columns=['timestamp'])

        for sensor_name, values in windowed_data.items():
            df = values[i].dataframe
            merged_df = merged_df.join(df, rsuffix='_r')

        combined_df_result.append(merged_df)

    return combined_df_result


def _combine_data_into_one(merged_dfs):
    combined_df = merged_dfs[0]
    for i in range(1, len(merged_dfs)):
        combined_df = combined_df.append(merged_dfs[i], ignore_index=True)

    return combined_df


def _drop_irrelevant_columns(df):
    return df.drop([
        'Unnamed: 0',
        'Unnamed: 0.1',
        'Unnamed: 0_r',
        'Unnamed: 0.1_r',
        'Unnamed: 0_x',
        'Unnamed: 0.1_x',
        'Unnamed: 0_y',
        'Unnamed: 0.1_y',
        'timestamp_r'
    ], axis=1)


def _create_combined_data_directory():
    dir_path = os.path.join(CONFIG.COMBINED_DATA_DIR)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def _create_combined_activity_directory(activity_type):
    dir_path = os.path.join(CONFIG.COMBINED_DATA_DIR, activity_type)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def _write_combined_dataframe_to_csv(activity_type, dataframe, is_smartphone=True):
    file_name_key = 'sp' if is_smartphone else 'sw'
    file_path = os.path.join(CONFIG.COMBINED_DATA_DIR, activity_type, CONFIG.COMBINED_DATA_RESULT[file_name_key])
    dataframe.to_csv(file_path)


if __name__ == '__main__':
    combine_data('going_downstairs')