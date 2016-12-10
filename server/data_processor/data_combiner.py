import os

import pandas as pd

import config as CONFIG


def combine_all_data_into_one_complete_dataset():
    activities = [activity_name for activity_name in os.listdir(CONFIG.COMBINED_DATA_DIR) if os.path.isdir(os.path.join(CONFIG.COMBINED_DATA_DIR, activity_name))]
    combined_dfs = []

    for activity in activities:
        file_path = os.path.join(
            CONFIG.COMBINED_DATA_DIR,
            activity,
            CONFIG.FILE_NAME_SUFFIX + CONFIG.PREPROCESS_DATA_SOURCE_SUBJECT + '_' + CONFIG.COMBINED_DATA_RESULT['sp_sw']
        )

        df = pd.read_csv(file_path)
        activity_df = pd.DataFrame(data=[[activity]] * len(df), columns=['activity'])
        df = df.join(activity_df)
        combined_dfs.append(df)

    result_df = pd.DataFrame(data=None, columns=combined_dfs[0].columns)
    result_df = result_df.append(combined_dfs, ignore_index=True)
    result_df = drop_irrelevant_columns_from_combined_dfs(result_df)
    _write_full_dataset_dataframe_to_csv(result_df)


def drop_irrelevant_columns_from_combined_dfs(df):
    try:
        df.drop(['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.2'], axis=1, inplace=True)
    except:
        print('Columns Unnamed: 0, Unnamed: 0.1, Unnamed: 0.2 not found!')

    return df


def combine_sp_sw_into_one(smartphone_features, smartwatch_features):
    combined_features_df = pd.concat([smartphone_features, smartwatch_features], axis=1)
    return combined_features_df


def combine_data_by_device_source(windowed_data):
    windowed_smartphone_data = { k: v for k, v in windowed_data.items() if 'sp' in k }
    windowed_smartwatch_data = { k: v for k, v in windowed_data.items() if 'sw' in k }

    merged_smartphone_dfs = _merge_smartphone_multiple_sensors_into_one(windowed_smartphone_data)
    merged_smartwatch_dfs = _merge_smartwatch_multiple_sensors_into_one(windowed_smartwatch_data)

    combined_smartphone_dfs = _combine_multiple_data_collections_into_one(merged_smartphone_dfs)
    combined_smartwatch_dfs = _combine_multiple_data_collections_into_one(merged_smartwatch_dfs)

    combined_smartphone_dfs = drop_irrelevant_columns_from_combined_dfs(combined_smartphone_dfs)
    combined_smartwatch_dfs = drop_irrelevant_columns_from_combined_dfs(combined_smartwatch_dfs)

    return combined_smartphone_dfs, combined_smartwatch_dfs


def _merge_smartphone_multiple_sensors_into_one(windowed_smartphone_data):
    combined_smartphone_data = _merge_multiple_sensor_sources_into_one(windowed_smartphone_data)
    return combined_smartphone_data


def _merge_smartwatch_multiple_sensors_into_one(windowed_smartwatch_data):
    combined_smartwatch_data = _merge_multiple_sensor_sources_into_one(windowed_smartwatch_data)
    return combined_smartwatch_data


def _merge_multiple_sensor_sources_into_one(windowed_data):
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


def _combine_multiple_data_collections_into_one(merged_dfs):
    combined_df = merged_dfs[0]
    for i in range(1, len(merged_dfs)):
        combined_df = combined_df.append(merged_dfs[i])

    return combined_df


def store_combined_data_by_device_source(combined_smartphone_dfs, combined_smartwatch_dfs, activity_type):
    _create_combined_data_directory()
    _create_combined_activity_directory(activity_type)

    _write_combined_dataframe_to_csv(activity_type, combined_smartphone_dfs, source='sp')
    _write_combined_dataframe_to_csv(activity_type, combined_smartwatch_dfs, source='sw')


def store_combined_features(combined_features_df, activity_type):
    _create_combined_data_directory()
    _create_combined_activity_directory(activity_type)
    _write_combined_dataframe_to_csv(activity_type, combined_features_df, source='sp_sw')


def _create_combined_data_directory():
    dir_path = os.path.join(CONFIG.COMBINED_DATA_DIR)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def _create_combined_activity_directory(activity_type):
    dir_path = os.path.join(CONFIG.COMBINED_DATA_DIR, activity_type)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def _write_combined_dataframe_to_csv(activity_type, dataframe, source='sp'):
    file_path = os.path.join(
        CONFIG.COMBINED_DATA_DIR,
        activity_type,
        CONFIG.FILE_NAME_SUFFIX + CONFIG.PREPROCESS_DATA_SOURCE_SUBJECT + '_' + CONFIG.COMBINED_DATA_RESULT[source]
    )

    dataframe.to_csv(file_path)


def _write_full_dataset_dataframe_to_csv(df):
    file_path = os.path.join(
        CONFIG.COMBINED_DATA_DIR,
        CONFIG.FILE_NAME_SUFFIX + CONFIG.PREPROCESS_DATA_SOURCE_SUBJECT + '_' + CONFIG.COMBINED_DATA_RESULT['full']
    )

    df.to_csv(file_path)