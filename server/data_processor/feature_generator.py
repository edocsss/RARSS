import math
import os
from scipy.stats._binned_statistic import binned_statistic
import pandas as pd
import config as CONFIG


def generate_feature(smartphone_df, smartwatch_df):
    smartphone_features = _generate_smartphone_features(smartphone_df)
    smartwatch_features = _generate_smartwatch_features(smartwatch_df)

    return smartphone_features, smartwatch_features


def _generate_smartphone_features(smartphone_df):
    print('Generating smartphone features..')
    result_df = pd.DataFrame(data=None, columns=[
        'sp_mean_ax',
        'sp_mean_ay',
        'sp_mean_az',
        'sp_mean_acc_magnitude',
        'sp_std_ax',
        'sp_std_ay',
        'sp_std_az',
        'sp_aad_ax',
        'sp_aad_ay',
        'sp_aad_az',
        'sp_bin_ax_0',
        'sp_bin_ax_1',
        'sp_bin_ax_2',
        'sp_bin_ax_3',
        'sp_bin_ax_4',
        'sp_bin_ax_5',
        'sp_bin_ax_6',
        'sp_bin_ax_7',
        'sp_bin_ax_8',
        'sp_bin_ax_9',
        'sp_bin_ay_0',
        'sp_bin_ay_1',
        'sp_bin_ay_2',
        'sp_bin_ay_3',
        'sp_bin_ay_4',
        'sp_bin_ay_5',
        'sp_bin_ay_6',
        'sp_bin_ay_7',
        'sp_bin_ay_8',
        'sp_bin_ay_9',
        'sp_bin_az_0',
        'sp_bin_az_1',
        'sp_bin_az_2',
        'sp_bin_az_3',
        'sp_bin_az_4',
        'sp_bin_az_5',
        'sp_bin_az_6',
        'sp_bin_az_7',
        'sp_bin_az_8',
        'sp_bin_az_9'
    ])

    for i in range(0, smartphone_df.shape[0], CONFIG.N_ROWS_PER_WINDOW):
        one_window_df = smartphone_df[i: i + CONFIG.N_ROWS_PER_WINDOW]
        accelerometer_features = _generate_accelerometer_feature_per_window(one_window_df, 'sp_')
        one_window_features = pd.concat([
            accelerometer_features
        ])

        result_df = result_df.append(one_window_features, ignore_index=True)

    return result_df


def _generate_smartwatch_features(smartwatch_df):
    print('Generating smartwatch features..')
    result_df = pd.DataFrame(data=None, columns=[
        'sw_mean_ax',
        'sw_mean_ay',
        'sw_mean_az',
        'sw_mean_acc_magnitude',
        'sw_std_ax',
        'sw_std_ay',
        'sw_std_az',
        'sw_aad_ax',
        'sw_aad_ay',
        'sw_aad_az',
        'sw_bin_ax_0',
        'sw_bin_ax_1',
        'sw_bin_ax_2',
        'sw_bin_ax_3',
        'sw_bin_ax_4',
        'sw_bin_ax_5',
        'sw_bin_ax_6',
        'sw_bin_ax_7',
        'sw_bin_ax_8',
        'sw_bin_ax_9',
        'sw_bin_ay_0',
        'sw_bin_ay_1',
        'sw_bin_ay_2',
        'sw_bin_ay_3',
        'sw_bin_ay_4',
        'sw_bin_ay_5',
        'sw_bin_ay_6',
        'sw_bin_ay_7',
        'sw_bin_ay_8',
        'sw_bin_ay_9',
        'sw_bin_az_0',
        'sw_bin_az_1',
        'sw_bin_az_2',
        'sw_bin_az_3',
        'sw_bin_az_4',
        'sw_bin_az_5',
        'sw_bin_az_6',
        'sw_bin_az_7',
        'sw_bin_az_8',
        'sw_bin_az_9'
    ])

    for i in range(0, smartwatch_df.shape[0], CONFIG.N_ROWS_PER_WINDOW):
        one_window_df = smartwatch_df[i : i + CONFIG.N_ROWS_PER_WINDOW]
        accelerometer_features = _generate_accelerometer_feature_per_window(one_window_df, 'sw_')
        one_window_features = pd.concat([
            accelerometer_features
        ])

        result_df = result_df.append(one_window_features, ignore_index=True)

    return result_df


def _generate_accelerometer_feature_per_window(df, column_prefix, column_type=''):
    accelerometer_related_data = df[['ax', 'ay', 'az', 'acc_magnitude']]
    result = []
    result_cols = [
        column_prefix + 'mean_ax',
        column_prefix + 'mean_ay',
        column_prefix + 'mean_az',
        column_prefix + 'mean_acc_magnitude',
        column_prefix + 'std_ax',
        column_prefix + 'std_ay',
        column_prefix + 'std_az',
        column_prefix + 'aad_ax',
        column_prefix + 'aad_ay',
        column_prefix + 'aad_az',
        column_prefix + 'bin_ax_0',
        column_prefix + 'bin_ax_1',
        column_prefix + 'bin_ax_2',
        column_prefix + 'bin_ax_3',
        column_prefix + 'bin_ax_4',
        column_prefix + 'bin_ax_5',
        column_prefix + 'bin_ax_6',
        column_prefix + 'bin_ax_7',
        column_prefix + 'bin_ax_8',
        column_prefix + 'bin_ax_9',
        column_prefix + 'bin_ay_0',
        column_prefix + 'bin_ay_1',
        column_prefix + 'bin_ay_2',
        column_prefix + 'bin_ay_3',
        column_prefix + 'bin_ay_4',
        column_prefix + 'bin_ay_5',
        column_prefix + 'bin_ay_6',
        column_prefix + 'bin_ay_7',
        column_prefix + 'bin_ay_8',
        column_prefix + 'bin_ay_9',
        column_prefix + 'bin_az_0',
        column_prefix + 'bin_az_1',
        column_prefix + 'bin_az_2',
        column_prefix + 'bin_az_3',
        column_prefix + 'bin_az_4',
        column_prefix + 'bin_az_5',
        column_prefix + 'bin_az_6',
        column_prefix + 'bin_az_7',
        column_prefix + 'bin_az_8',
        column_prefix + 'bin_az_9'
    ]

    result += accelerometer_related_data.mean().tolist()
    result += accelerometer_related_data.std().tolist()[0:3]  # ignore std acc magnitude

    try:
        result.append(_calculate_average_absolute_difference(accelerometer_related_data['ax']))
        result.append(_calculate_average_absolute_difference(accelerometer_related_data['ay']))
        result.append(_calculate_average_absolute_difference(accelerometer_related_data['az']))

        result += _calculate_bin_distribution(accelerometer_related_data['ax'])
        result += _calculate_bin_distribution(accelerometer_related_data['ay'])
        result += _calculate_bin_distribution(accelerometer_related_data['az'])

    except Exception as e:
        print(e)
        print('Feature generation exception!')
        print()
        print()

    result_df = pd.DataFrame(data=[result], columns=result_cols)
    return result_df


def _calculate_average_absolute_difference(series):
    data = series.tolist()
    mean = series.mean()
    absolute_difference = [math.fabs(d - mean) for d in data]
    return sum(absolute_difference) / len(absolute_difference)


def _calculate_bin_distribution(series):
    data = series.tolist()
    bin_count, _, _ = binned_statistic(data, data, statistic='count', bins=10)

    n = len(data)
    return [item / n for item in bin_count]


def store_features_df(smartphone_features, smartwatch_features, activity_type):
    _create_features_directory()
    _create_features_activity_directory(activity_type)

    _write_smartphone_features_to_file(smartphone_features, activity_type)
    _write_smartwatch_features_to_file(smartwatch_features, activity_type)


def _create_features_directory():
    dir_path = os.path.join(CONFIG.FEATURES_DATA_DIR)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def _create_features_activity_directory(activity_type):
    dir_path = os.path.join(CONFIG.FEATURES_DATA_DIR, activity_type)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def _write_smartphone_features_to_file(smartphone_features, activity_type):
    print('Writing smartphone features to file..')
    file_path = os.path.join(
        CONFIG.FEATURES_DATA_DIR,
        activity_type,
        CONFIG.FILE_NAME_SUFFIX + CONFIG.PREPROCESS_DATA_SOURCE_SUBJECT + '_' + CONFIG.FEATURES_DATA_RESULT['sp']
    )

    smartphone_features.to_csv(file_path)


def _write_smartwatch_features_to_file(smartwatch_features, activity_type):
    print('Writing smartwatch features to file..')
    file_path = os.path.join(
        CONFIG.FEATURES_DATA_DIR,
        activity_type,
        CONFIG.FILE_NAME_SUFFIX + CONFIG.PREPROCESS_DATA_SOURCE_SUBJECT + '_' + CONFIG.FEATURES_DATA_RESULT['sw']
    )

    smartwatch_features.to_csv(file_path)
