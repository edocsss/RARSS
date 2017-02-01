import math
import os
import numpy as np
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
        'sp_var_ax',
        'sp_var_ay',
        'sp_var_az',
        'sp_var_acc_magnitude',
        'sp_cov_a_xy',
        'sp_cov_a_xz',
        'sp_cov_a_yz',
        'sp_cov_a_xmag',
        'sp_cov_a_ymag',
        'sp_cov_a_zmag',
        'sp_energy_ax',
        'sp_energy_ay',
        'sp_energy_az',
        'sp_energy_acc_magnitude',
        'sp_entropy_ax',
        'sp_entropy_ay',
        'sp_entropy_az',
        'sp_entropy_acc_magnitude',

        'sp_mean_ax_zero_mean',
        'sp_mean_ay_zero_mean',
        'sp_mean_az_zero_mean',
        'sp_mean_acc_magnitude_zero_mean',
        'sp_var_ax_zero_mean',
        'sp_var_ay_zero_mean',
        'sp_var_az_zero_mean',
        'sp_var_acc_magnitude_zero_mean',
        'sp_cov_a_xy_zero_mean',
        'sp_cov_a_xz_zero_mean',
        'sp_cov_a_yz_zero_mean',
        'sp_cov_a_xmag_zero_mean',
        'sp_cov_a_ymag_zero_mean',
        'sp_cov_a_zmag_zero_mean',
        'sp_energy_ax_zero_mean',
        'sp_energy_ay_zero_mean',
        'sp_energy_az_zero_mean',
        'sp_energy_acc_magnitude_zero_mean',
        'sp_entropy_ax_zero_mean',
        'sp_entropy_ay_zero_mean',
        'sp_entropy_az_zero_mean',
        'sp_entropy_acc_magnitude_zero_mean',

        'sp_mean_gx',
        'sp_mean_gy',
        'sp_mean_gz',
        'sp_mean_gyro_magnitude',
        'sp_var_gx',
        'sp_var_gy',
        'sp_var_gz',
        'sp_var_gyro_magnitude',
        'sp_cov_g_xy',
        'sp_cov_g_xz',
        'sp_cov_g_yz',
        'sp_cov_g_xmag',
        'sp_cov_g_ymag',
        'sp_cov_g_zmag',
        'sp_energy_gx',
        'sp_energy_gy',
        'sp_energy_gz',
        'sp_energy_gyro_magnitude',
        'sp_entropy_gx',
        'sp_entropy_gy',
        'sp_entropy_gz',
        'sp_entropy_gyro_magnitude',

        'sp_mean_gx_zero_mean',
        'sp_mean_gy_zero_mean',
        'sp_mean_gz_zero_mean',
        'sp_mean_gyro_magnitude_zero_mean',
        'sp_var_gx_zero_mean',
        'sp_var_gy_zero_mean',
        'sp_var_gz_zero_mean',
        'sp_var_gyro_magnitude_zero_mean',
        'sp_cov_g_xy_zero_mean',
        'sp_cov_g_xz_zero_mean',
        'sp_cov_g_yz_zero_mean',
        'sp_cov_g_xmag_zero_mean',
        'sp_cov_g_ymag_zero_mean',
        'sp_cov_g_zmag_zero_mean',
        'sp_energy_gx_zero_mean',
        'sp_energy_gy_zero_mean',
        'sp_energy_gz_zero_mean',
        'sp_energy_gyro_magnitude_zero_mean',
        'sp_entropy_gx_zero_mean',
        'sp_entropy_gy_zero_mean',
        'sp_entropy_gz_zero_mean',
        'sp_entropy_gyro_magnitude_zero_mean',

        'sp_mean_baro',
        'sp_var_baro',
        'sp_regression_baro',
        'sp_dir_baro',
        'sp_range_baro',

        'sp_mean_baro_zero_mean',
        'sp_var_baro_zero_mean',
        'sp_regression_baro_zero_mean',
        'sp_dir_baro_zero_mean',
        'sp_range_baro_zero_mean'
    ])

    for i in range(0, smartphone_df.shape[0], CONFIG.N_ROWS_PER_WINDOW):
        one_window_df = smartphone_df[i : i + CONFIG.N_ROWS_PER_WINDOW]

        accelerometer_features = _generate_accelerometer_feature_per_window(one_window_df, 'sp_', column_type='')
        zero_mean_accelerometer_features = _generate_accelerometer_feature_per_window(one_window_df, 'sp_', column_type='_zero_mean')

        gyroscope_features = _generate_gyroscope_feature_per_window(one_window_df, 'sp_', column_type='')
        zero_mean_gyroscope_features = _generate_gyroscope_feature_per_window(one_window_df, 'sp_', column_type='_zero_mean')

        barometer_features = _generate_barometer_feature_per_window(one_window_df, 'sp_', column_type='')
        zero_mean_barometer_features = _generate_barometer_feature_per_window(one_window_df, 'sp_', column_type='_zero_mean')

        one_window_features = pd.concat([
            accelerometer_features,
            zero_mean_accelerometer_features,
            gyroscope_features,
            zero_mean_gyroscope_features,
            barometer_features,
            zero_mean_barometer_features
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
        'sw_var_ax',
        'sw_var_ay',
        'sw_var_az',
        'sw_var_acc_magnitude',
        'sw_cov_a_xy',
        'sw_cov_a_xz',
        'sw_cov_a_yz',
        'sw_cov_a_xmag',
        'sw_cov_a_ymag',
        'sw_cov_a_zmag',
        'sw_energy_ax',
        'sw_energy_ay',
        'sw_energy_az',
        'sw_energy_acc_magnitude',
        'sw_entropy_ax',
        'sw_entropy_ay',
        'sw_entropy_az',
        'sw_entropy_acc_magnitude',

        'sw_mean_ax_zero_mean',
        'sw_mean_ay_zero_mean',
        'sw_mean_az_zero_mean',
        'sw_mean_acc_magnitude_zero_mean',
        'sw_var_ax_zero_mean',
        'sw_var_ay_zero_mean',
        'sw_var_az_zero_mean',
        'sw_var_acc_magnitude_zero_mean',
        'sw_cov_a_xy_zero_mean',
        'sw_cov_a_xz_zero_mean',
        'sw_cov_a_yz_zero_mean',
        'sw_cov_a_xmag_zero_mean',
        'sw_cov_a_ymag_zero_mean',
        'sw_cov_a_zmag_zero_mean',
        'sw_energy_ax_zero_mean',
        'sw_energy_ay_zero_mean',
        'sw_energy_az_zero_mean',
        'sw_energy_acc_magnitude_zero_mean',
        'sw_entropy_ax_zero_mean',
        'sw_entropy_ay_zero_mean',
        'sw_entropy_az_zero_mean',
        'sw_entropy_acc_magnitude_zero_mean',

        'sw_mean_gx',
        'sw_mean_gy',
        'sw_mean_gz',
        'sw_mean_gyro_magnitude',
        'sw_var_gx',
        'sw_var_gy',
        'sw_var_gz',
        'sw_var_gyro_magnitude',
        'sw_cov_g_xy',
        'sw_cov_g_xz',
        'sw_cov_g_yz',
        'sw_cov_g_xmag',
        'sw_cov_g_ymag',
        'sw_cov_g_zmag',
        'sw_energy_gx',
        'sw_energy_gy',
        'sw_energy_gz',
        'sw_energy_gyro_magnitude',
        'sw_entropy_gx',
        'sw_entropy_gy',
        'sw_entropy_gz',
        'sw_entropy_gyro_magnitude',

        'sw_mean_gx_zero_mean',
        'sw_mean_gy_zero_mean',
        'sw_mean_gz_zero_mean',
        'sw_mean_gyro_magnitude_zero_mean',
        'sw_var_gx_zero_mean',
        'sw_var_gy_zero_mean',
        'sw_var_gz_zero_mean',
        'sw_var_gyro_magnitude_zero_mean',
        'sw_cov_g_xy_zero_mean',
        'sw_cov_g_xz_zero_mean',
        'sw_cov_g_yz_zero_mean',
        'sw_cov_g_xmag_zero_mean',
        'sw_cov_g_ymag_zero_mean',
        'sw_cov_g_zmag_zero_mean',
        'sw_energy_gx_zero_mean',
        'sw_energy_gy_zero_mean',
        'sw_energy_gz_zero_mean',
        'sw_energy_gyro_magnitude_zero_mean',
        'sw_entropy_gx_zero_mean',
        'sw_entropy_gy_zero_mean',
        'sw_entropy_gz_zero_mean',
        'sw_entropy_gyro_magnitude_zero_mean',

        'sw_mean_baro',
        'sw_var_baro',
        'sw_regression_baro',
        'sw_dir_baro',
        'sw_range_baro',

        'sw_mean_baro_zero_mean',
        'sw_var_baro_zero_mean',
        'sw_regression_baro_zero_mean',
        'sw_dir_baro_zero_mean',
        'sw_range_baro_zero_mean'
    ])

    for i in range(0, smartwatch_df.shape[0], CONFIG.N_ROWS_PER_WINDOW):
        one_window_df = smartwatch_df[i : i + CONFIG.N_ROWS_PER_WINDOW]

        accelerometer_features = _generate_accelerometer_feature_per_window(one_window_df, 'sw_', column_type='')
        zero_mean_accelerometer_features = _generate_accelerometer_feature_per_window(one_window_df, 'sw_', column_type='_zero_mean')

        gyroscope_features = _generate_gyroscope_feature_per_window(one_window_df, 'sw_', column_type='')
        zero_mean_gyroscope_features = _generate_gyroscope_feature_per_window(one_window_df, 'sw_', column_type='_zero_mean')

        barometer_features = _generate_barometer_feature_per_window(one_window_df, 'sw_', column_type='')
        zero_mean_barometer_features = _generate_barometer_feature_per_window(one_window_df, 'sw_', column_type='_zero_mean')

        one_window_features = pd.concat([
            accelerometer_features,
            zero_mean_accelerometer_features,
            gyroscope_features,
            zero_mean_gyroscope_features,
            barometer_features,
            zero_mean_barometer_features
        ], axis=1)

        result_df = result_df.append(one_window_features, ignore_index=True)

    return result_df


def _generate_accelerometer_feature_per_window(df, column_prefix, column_type=''):
    accelerometer_related_data = df[['ax' + column_type, 'ay' + column_type, 'az' + column_type, 'acc_magnitude' + column_type]]
    result = []
    result_cols = [
        column_prefix + 'mean_ax' + column_type,
        column_prefix + 'mean_ay' + column_type,
        column_prefix + 'mean_az' + column_type,
        column_prefix + 'mean_acc_magnitude' + column_type,
        column_prefix + 'var_ax' + column_type,
        column_prefix + 'var_ay' + column_type,
        column_prefix + 'var_az' + column_type,
        column_prefix + 'var_acc_magnitude' + column_type,
        column_prefix + 'cov_a_xy' + column_type,
        column_prefix + 'cov_a_xz' + column_type,
        column_prefix + 'cov_a_yz' + column_type,
        column_prefix + 'cov_a_xmag' + column_type,
        column_prefix + 'cov_a_ymag' + column_type,
        column_prefix + 'cov_a_zmag' + column_type,
        column_prefix + 'energy_ax' + column_type,
        column_prefix + 'energy_ay' + column_type,
        column_prefix + 'energy_az' + column_type,
        column_prefix + 'energy_acc_magnitude' + column_type,
        column_prefix + 'entropy_ax' + column_type,
        column_prefix + 'entropy_ay' + column_type,
        column_prefix + 'entropy_az' + column_type,
        column_prefix + 'entropy_acc_magnitude' + column_type
    ]

    result += accelerometer_related_data.mean().tolist()
    result += accelerometer_related_data.var().tolist()

    try:
        result.append(_calculate_covariance(accelerometer_related_data, 'ax' + column_type, 'ay' + column_type))
        result.append(_calculate_covariance(accelerometer_related_data, 'ax' + column_type, 'az' + column_type))
        result.append(_calculate_covariance(accelerometer_related_data, 'ay' + column_type, 'az' + column_type))
        result.append(_calculate_covariance(accelerometer_related_data, 'ax' + column_type, 'acc_magnitude' + column_type))
        result.append(_calculate_covariance(accelerometer_related_data, 'ay' + column_type, 'acc_magnitude' + column_type))
        result.append(_calculate_covariance(accelerometer_related_data, 'az' + column_type, 'acc_magnitude' + column_type))

        result.append(_calculate_energy(accelerometer_related_data['ax' + column_type]))
        result.append(_calculate_energy(accelerometer_related_data['ay' + column_type]))
        result.append(_calculate_energy(accelerometer_related_data['az' + column_type]))
        result.append(_calculate_energy(accelerometer_related_data['acc_magnitude' + column_type]))

        result.append(_calculate_entropy(accelerometer_related_data['ax' + column_type]))
        result.append(_calculate_entropy(accelerometer_related_data['ay' + column_type]))
        result.append(_calculate_entropy(accelerometer_related_data['az' + column_type]))
        result.append(_calculate_entropy(accelerometer_related_data['acc_magnitude' + column_type]))

    except:
        print('Feature generation exception!')

    result_df = pd.DataFrame(data=[result], columns=result_cols)
    return result_df


def _generate_gyroscope_feature_per_window(df, column_prefix, column_type=''):
    gyroscope_related_data = df[['gx' + column_type, 'gy' + column_type, 'gz' + column_type, 'gyro_magnitude' + column_type]]
    result = []
    result_cols = [
        column_prefix + 'mean_gx' + column_type,
        column_prefix + 'mean_gy' + column_type,
        column_prefix + 'mean_gz' + column_type,
        column_prefix + 'mean_gyro_magnitude' + column_type,
        column_prefix + 'var_gx' + column_type,
        column_prefix + 'var_gy' + column_type,
        column_prefix + 'var_gz' + column_type,
        column_prefix + 'var_gyro_magnitude' + column_type,
        column_prefix + 'cov_g_xy' + column_type,
        column_prefix + 'cov_g_xz' + column_type,
        column_prefix + 'cov_g_yz' + column_type,
        column_prefix + 'cov_g_xmag' + column_type,
        column_prefix + 'cov_g_ymag' + column_type,
        column_prefix + 'cov_g_zmag' + column_type,
        column_prefix + 'energy_gx' + column_type,
        column_prefix + 'energy_gy' + column_type,
        column_prefix + 'energy_gz' + column_type,
        column_prefix + 'energy_gyro_magnitude' + column_type,
        column_prefix + 'entropy_gx' + column_type,
        column_prefix + 'entropy_gy' + column_type,
        column_prefix + 'entropy_gz' + column_type,
        column_prefix + 'entropy_gyro_magnitude' + column_type
    ]

    result += gyroscope_related_data.mean().tolist()
    result += gyroscope_related_data.var().tolist()

    try:
        result.append(_calculate_covariance(gyroscope_related_data, 'gx' + column_type, 'gy' + column_type))
        result.append(_calculate_covariance(gyroscope_related_data, 'gx' + column_type, 'gz' + column_type))
        result.append(_calculate_covariance(gyroscope_related_data, 'gy' + column_type, 'gz' + column_type))
        result.append(_calculate_covariance(gyroscope_related_data, 'gx' + column_type, 'gyro_magnitude' + column_type))
        result.append(_calculate_covariance(gyroscope_related_data, 'gy' + column_type, 'gyro_magnitude' + column_type))
        result.append(_calculate_covariance(gyroscope_related_data, 'gz' + column_type, 'gyro_magnitude' + column_type))

        result.append(_calculate_energy(gyroscope_related_data['gx' + column_type]))
        result.append(_calculate_energy(gyroscope_related_data['gy' + column_type]))
        result.append(_calculate_energy(gyroscope_related_data['gz' + column_type]))
        result.append(_calculate_energy(gyroscope_related_data['gyro_magnitude' + column_type]))

        result.append(_calculate_entropy(gyroscope_related_data['gx' + column_type]))
        result.append(_calculate_entropy(gyroscope_related_data['gy' + column_type]))
        result.append(_calculate_entropy(gyroscope_related_data['gz' + column_type]))
        result.append(_calculate_entropy(gyroscope_related_data['gyro_magnitude' + column_type]))

    except:
        print('Feature generation exception!')

    result_df = pd.DataFrame(data=[result], columns=result_cols)
    return result_df


def _generate_barometer_feature_per_window(df, column_prefix, column_type=''):
    barometer_related_data = df[['pressure' + column_type]]
    result = []
    result_cols = [
        column_prefix + 'mean_baro' + column_type,
        column_prefix + 'var_baro' + column_type,
        column_prefix + 'regression_baro' + column_type,
        column_prefix + 'dir_baro' + column_type,
        column_prefix + 'range_baro' + column_type
    ]

    result += barometer_related_data.mean().tolist()
    result += barometer_related_data.var().tolist()

    try:
        x = [i for i in range (0, len(barometer_related_data.values))]
        y = [data[0] for data in barometer_related_data.values.tolist()]

        result.append(np.polyfit(x, y, 1)[0])
        result.append(y[-1] - y[0])
        result.append(math.fabs(max(y) - min(y)))

    except Exception as e:
        print('Feature generation exception!')
        print(e)

    result_df = pd.DataFrame(data=[result], columns=result_cols)
    return result_df


def _calculate_covariance(df, col1, col2):
    relevant_df = df[[col1, col2]]
    mean_col1 = relevant_df[col1].mean()
    mean_col2 = relevant_df[col2].mean()

    total = 0
    for i, row in relevant_df.iterrows():
        total += (row[col1] - mean_col1) * (row[col2] - mean_col2)

    return total / (len(relevant_df) - 1)


def _calculate_energy(series):
    values = series.tolist()
    N = len(values)

    fft = _calculate_fft(values)
    total = sum(fft[1:])
    return math.sqrt(total / (N - 1))


def _calculate_entropy(series):
    values = series.tolist()
    N = len(values)
    fft = _calculate_fft(values)

    terms = [(-_calculate_O(fft, l) * math.log(_calculate_O(fft, l))) for l in range(1, N)]
    return sum(terms)


def _calculate_O(fft, l):
    nom = math.fabs(fft[l])
    if nom == 0:
        return 1

    denom = sum([math.fabs(fft_value) for fft_value in fft[1:]])
    return nom / denom


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
