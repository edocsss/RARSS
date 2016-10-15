import os
import config as CONFIG
import pandas as pd
from util import windowed_data_reader
from util import feature_data_reader


def combine_all_data_into_one_complete_dataset():
    activities = os.listdir(CONFIG.COMBINED_DATA_DIR)
    combined_dfs = []

    for activity in activities:
        file_path = os.path.join(CONFIG.COMBINED_DATA_DIR, activity, CONFIG.COMBINED_DATA_RESULT['sp_sw'])
        df = pd.read_csv(file_path)

        activity_df = pd.DataFrame(data=[[activity]] * len(df), columns=['activity'])
        df = df.join(activity_df)
        combined_dfs.append(df)

    result_df = pd.DataFrame(data=None, columns=combined_dfs[0].columns)
    result_df = result_df.append(combined_dfs, ignore_index=True)
    _write_full_dataset_dataframe_to_csv(result_df)


def combine_data_sources_into_one(activity_type):
    merged_df = _merge_smartphone_and_smartwatch_data(activity_type)
    _create_combined_data_directory()
    _create_combined_activity_directory(activity_type)
    _write_combined_dataframe_to_csv(activity_type, merged_df, source='sp_sw')


def combine_data_by_source(activity_type):
    merged_smartphone_dfs = _merge_smartphone_data(activity_type)
    merged_smartwatch_dfs = _merge_smartwatch_data(activity_type)

    combined_smartphone_dfs = _combine_data_into_one(merged_smartphone_dfs)
    combined_smartwatch_dfs = _combine_data_into_one(merged_smartwatch_dfs)

    combined_smartphone_dfs = _drop_irrelevant_columns(combined_smartphone_dfs)
    combined_smartwatch_dfs = _drop_irrelevant_columns(combined_smartwatch_dfs)

    _create_combined_data_directory()
    _create_combined_activity_directory(activity_type)

    _write_combined_dataframe_to_csv(activity_type, combined_smartphone_dfs, source='sp')
    _write_combined_dataframe_to_csv(activity_type, combined_smartwatch_dfs, source='sw')


def _merge_smartphone_and_smartwatch_data(activity_type):
    features_smartphone_data = feature_data_reader.read_smartphone_features_data(activity_type)
    features_smartwatch_data = feature_data_reader.read_smartwatch_features_data(activity_type)

    merged_df = pd.concat([features_smartphone_data, features_smartwatch_data], axis=1)
    return merged_df


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
        dfs = []
        for sensor_name, values in windowed_data.items():
            df = values[i].dataframe
            dfs.append(df)

        combined_df_result.append(pd.concat(dfs, axis=1))

    return combined_df_result


def _combine_data_into_one(merged_dfs):
    combined_df = merged_dfs[0]
    for i in range(1, len(merged_dfs)):
        combined_df = combined_df.append(merged_dfs[i])

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


def _write_combined_dataframe_to_csv(activity_type, dataframe, source='sp'):
    file_path = os.path.join(CONFIG.COMBINED_DATA_DIR, activity_type, CONFIG.COMBINED_DATA_RESULT[source])
    dataframe.to_csv(file_path)


def _write_full_dataset_dataframe_to_csv(df):
    file_path = os.path.join(CONFIG.COMBINED_DATA_DIR, CONFIG.COMBINED_DATA_RESULT['full'])
    df.to_csv(file_path)


if __name__ == '__main__':
    combine_data_by_source('reading')
    # combine_data_sources_into_one('brushing')
    # combine_all_data_into_one_complete_dataset()