import math
import os
import numpy as np
import pandas as pd
import config as CONFIG


def generate_feature(smartphone_df, smartwatch_df):
    smartphone_df = _include_additional_data(smartphone_df)
    smartwatch_df = _include_additional_data(smartwatch_df)

    smartphone_features = _generate_smartphone_features(smartphone_df)
    smartwatch_features = _generate_smartwatch_features(smartwatch_df)

    return smartphone_features, smartwatch_features


def _include_additional_data(df):
    df['acc_magnitude'] = df.apply(
        _calculate_magnitude,
        axis=1,
        args=(['ax', 'ay', 'az'],)
    )

    df['gyro_magnitude'] = df.apply(
        _calculate_magnitude,
        axis=1,
        args=(['gx', 'gx', 'gz'],)
    )

    return df


def _calculate_magnitude(row, fields):
    return math.sqrt(sum([math.pow(row[f], 2) for f in fields]))


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
        'sp_std_acc_magnitude',
        'sp_min_ax',
        'sp_min_ay',
        'sp_min_az',
        'sp_min_acc_magnitude',
        'sp_max_ax',
        'sp_max_ay',
        'sp_max_az',
        'sp_max_acc_magnitude',
        'sp_semi_quartile_ax',
        'sp_semi_quartile_ay',
        'sp_semi_quartile_az',
        'sp_semi_quartile_acc_magnitude',
        'sp_median_ax',
        'sp_median_ay',
        'sp_median_az',
        'sp_median_acc_magnitude',
        'sp_sum_10_fft_ax',
        'sp_sum_10_fft_ay',
        'sp_sum_10_fft_az',
        'sp_sum_10_fft_acc_magnitude',

        'sp_mean_gx',
        'sp_mean_gy',
        'sp_mean_gz',
        'sp_mean_gyro_magnitude',
        'sp_std_gx',
        'sp_std_gy',
        'sp_std_gz',
        'sp_std_gyro_magnitude',
        'sp_min_gx',
        'sp_min_gy',
        'sp_min_gz',
        'sp_min_gyro_magnitude',
        'sp_max_gx',
        'sp_max_gy',
        'sp_max_gz',
        'sp_max_gyro_magnitude',
        'sp_semi_quartile_gx',
        'sp_semi_quartile_gy',
        'sp_semi_quartile_gz',
        'sp_semi_quartile_gyro_magnitude',
        'sp_median_gx',
        'sp_median_gy',
        'sp_median_gz',
        'sp_median_gyro_magnitude',
        'sp_sum_10_fft_gx',
        'sp_sum_10_fft_gy',
        'sp_sum_10_fft_gz',
        'sp_sum_10_fft_gyro_magnitude'
    ])

    for i in range(0, smartphone_df.shape[0], CONFIG.N_ROWS_PER_WINDOW):
        one_window_df = smartphone_df[i : i + CONFIG.N_ROWS_PER_WINDOW]
        accelerometer_features = _generate_accelerometer_feature_per_window(one_window_df, 'sp_')
        gyroscope_features = _generate_gyroscope_feature_per_window(one_window_df, 'sp_')

        one_window_features = pd.concat([
            accelerometer_features,
            gyroscope_features
        ], axis=1)

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
        'sw_std_acc_magnitude',
        'sw_min_ax',
        'sw_min_ay',
        'sw_min_az',
        'sw_min_acc_magnitude',
        'sw_max_ax',
        'sw_max_ay',
        'sw_max_az',
        'sw_max_acc_magnitude',
        'sw_median_ax',
        'sw_median_ay',
        'sw_median_az',
        'sw_median_acc_magnitude',
        'sw_semi_quartile_ax',
        'sw_semi_quartile_ay',
        'sw_semi_quartile_az',
        'sw_semi_quartile_acc_magnitude',
        'sw_sum_10_fft_ax',
        'sw_sum_10_fft_ay',
        'sw_sum_10_fft_az',
        'sw_sum_10_fft_acc_magnitude',

        'sw_mean_gx',
        'sw_mean_gy',
        'sw_mean_gz',
        'sw_mean_gyro_magnitude',
        'sw_std_gx',
        'sw_std_gy',
        'sw_std_gz',
        'sw_std_gyro_magnitude',
        'sw_min_gx',
        'sw_min_gy',
        'sw_min_gz',
        'sw_min_gyro_magnitude',
        'sw_max_gx',
        'sw_max_gy',
        'sw_max_gz',
        'sw_max_gyro_magnitude',
        'sw_median_gx',
        'sw_median_gy',
        'sw_median_gz',
        'sw_median_gyro_magnitude',
        'sw_semi_quartile_gx',
        'sw_semi_quartile_gy',
        'sw_semi_quartile_gz',
        'sw_semi_quartile_gyro_magnitude',
        'sw_sum_10_fft_gx',
        'sw_sum_10_fft_gy',
        'sw_sum_10_fft_gz',
        'sw_sum_10_fft_gyro_magnitude'
    ])

    for i in range(0, smartwatch_df.shape[0], CONFIG.N_ROWS_PER_WINDOW):
        one_window_df = smartwatch_df[i : i + CONFIG.N_ROWS_PER_WINDOW]
        accelerometer_features = _generate_accelerometer_feature_per_window(one_window_df, 'sw_')
        gyroscope_features = _generate_gyroscope_feature_per_window(one_window_df, 'sw_')

        one_window_features = pd.concat([
            accelerometer_features,
            gyroscope_features
        ], axis=1)

        result_df = result_df.append(one_window_features, ignore_index=True)

    return result_df


def _generate_accelerometer_feature_per_window(df, column_prefix):
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
        column_prefix + 'std_acc_magnitude',
        column_prefix + 'min_ax',
        column_prefix + 'min_ay',
        column_prefix + 'min_az',
        column_prefix + 'min_acc_magnitude',
        column_prefix + 'max_ax',
        column_prefix + 'max_ay',
        column_prefix + 'max_az',
        column_prefix + 'max_acc_magnitude',
        column_prefix + 'median_ax',
        column_prefix + 'median_ay',
        column_prefix + 'median_az',
        column_prefix + 'median_acc_magnitude',
        column_prefix + 'semi_quartile_ax',
        column_prefix + 'semi_quartile_ay',
        column_prefix + 'semi_quartile_az',
        column_prefix + 'semi_quartile_acc_magnitude',
        column_prefix + 'sum_10_fft_ax',
        column_prefix + 'sum_10_fft_ay',
        column_prefix + 'sum_10_fft_az',
        column_prefix + 'sum_10_fft_acc_magnitude',
    ]

    result += accelerometer_related_data.mean().tolist()
    result += accelerometer_related_data.std().tolist()
    result += accelerometer_related_data.min().tolist()
    result += accelerometer_related_data.max().tolist()
    result += accelerometer_related_data.median().tolist()

    try:
        result.append(_calculate_semi_quartile(accelerometer_related_data['ax']))
        result.append(_calculate_semi_quartile(accelerometer_related_data['ay']))
        result.append(_calculate_semi_quartile(accelerometer_related_data['az']))
        result.append(_calculate_semi_quartile(accelerometer_related_data['acc_magnitude']))

        result.append(_calculate_sum_first_10_fft(accelerometer_related_data['ax']))
        result.append(_calculate_sum_first_10_fft(accelerometer_related_data['ay']))
        result.append(_calculate_sum_first_10_fft(accelerometer_related_data['az']))
        result.append(_calculate_sum_first_10_fft(accelerometer_related_data['acc_magnitude']))

    except Exception as e:
        print('Feature generation exception!')
        print(e)
        print()
        print()

    result_df = pd.DataFrame(data=[result], columns=result_cols)
    return result_df


def _generate_gyroscope_feature_per_window(df, column_prefix):
    gyroscope_related_data = df[['gx', 'gy', 'gz', 'gyro_magnitude']]
    result = []
    result_cols = [
        column_prefix + 'mean_gx',
        column_prefix + 'mean_gy',
        column_prefix + 'mean_gz',
        column_prefix + 'mean_gyro_magnitude',
        column_prefix + 'std_gx',
        column_prefix + 'std_gy',
        column_prefix + 'std_gz',
        column_prefix + 'std_gyro_magnitude',
        column_prefix + 'min_gx',
        column_prefix + 'min_gy',
        column_prefix + 'min_gz',
        column_prefix + 'min_gyro_magnitude',
        column_prefix + 'max_gx',
        column_prefix + 'max_gy',
        column_prefix + 'max_gz',
        column_prefix + 'max_gyro_magnitude',
        column_prefix + 'median_gx',
        column_prefix + 'median_gy',
        column_prefix + 'median_gz',
        column_prefix + 'median_gyro_magnitude',
        column_prefix + 'semi_quartile_gx',
        column_prefix + 'semi_quartile_gy',
        column_prefix + 'semi_quartile_gz',
        column_prefix + 'semi_quartile_gyro_magnitude',
        column_prefix + 'sum_10_fft_gx',
        column_prefix + 'sum_10_fft_gy',
        column_prefix + 'sum_10_fft_gz',
        column_prefix + 'sum_10_fft_gyro_magnitude'
    ]

    result += gyroscope_related_data.mean().tolist()
    result += gyroscope_related_data.std().tolist()
    result += gyroscope_related_data.min().tolist()
    result += gyroscope_related_data.max().tolist()
    result += gyroscope_related_data.median().tolist()


    try:
        result.append(_calculate_semi_quartile(gyroscope_related_data['gx']))
        result.append(_calculate_semi_quartile(gyroscope_related_data['gy']))
        result.append(_calculate_semi_quartile(gyroscope_related_data['gz']))
        result.append(_calculate_semi_quartile(gyroscope_related_data['gyro_magnitude']))

        result.append(_calculate_sum_first_10_fft(gyroscope_related_data['gx']))
        result.append(_calculate_sum_first_10_fft(gyroscope_related_data['gy']))
        result.append(_calculate_sum_first_10_fft(gyroscope_related_data['gz']))
        result.append(_calculate_sum_first_10_fft(gyroscope_related_data['gyro_magnitude']))

    except:
        print('Feature generation exception!')

    result_df = pd.DataFrame(data=[result], columns=result_cols)
    return result_df


def _calculate_semi_quartile(series):
    first_quartile = series.quantile(0.25)
    third_quartile = series.quantile(0.75)
    return (first_quartile + third_quartile) / 2


def _calculate_sum_first_10_fft(series):
    values = series.tolist()
    fft = _calculate_fft(values)
    return sum(fft[:10])


# For details about FFT, take a look at Prof. Tan's and Dr. Wang's paper
# Basically, the FFT in NumPy and the one in the paper is slightly different
# The one in NumPy has already iterated through the K value, we just need to sum them up
# That's why the NumPy still produces an array of size len(series) after calculating FFT
# WE NEED TO DISCARD THE FIRST ITEM, SEE EQUATION (6) --> k = 1 to N - 1
def _calculate_fft(vector):
    fft_vector = np.fft.fft(vector)
    return np.absolute(fft_vector)





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
