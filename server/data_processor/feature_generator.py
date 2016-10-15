import os
import config as CONFIG
import pandas as pd
import math
import numpy as np
from util import combined_data_reader


def generate_feature(activity_type):
    print('Generating features for {}..'.format(activity_type))
    combined_data = combined_data_reader.read_all_combined_data(activity_type)
    smartphone_df = combined_data['sp']
    smartwatch_df = combined_data['sw']

    smartphone_df = _include_additional_data(smartphone_df)
    smartwatch_df = _include_additional_data(smartwatch_df)

    smartphone_features = _generate_smartphone_features(smartphone_df)
    smartwatch_features = _generate_smartwatch_features(smartwatch_df)

    _create_features_directory()
    _create_features_activity_directory(activity_type)

    _write_smartphone_features_to_file(smartphone_features, activity_type)
    _write_smartwatch_features_to_file(smartwatch_features, activity_type)
    print('Features generated for {}..'.format(activity_type))


def _include_additional_data(df):
    df['acc_magnitude'] = df.apply(
        _calculate_accelerometer_magnitude,
        axis=1,
        args=(['ax', 'ay', 'az'],)
    )

    return df


def _calculate_accelerometer_magnitude(row, fields):
    return math.sqrt(sum([math.pow(row[f], 2) for f in fields]))


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
        'sp_cov_a_yz',
        'sp_cov_a_xz',
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
        'sp_entropy_acc_magnitude'
    ])

    for i in range(0, smartphone_df.shape[0], CONFIG.N_ROWS_PER_WINDOW):
        one_window_df = smartphone_df[i : i + CONFIG.N_ROWS_PER_WINDOW]
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
        'sw_var_ax',
        'sw_var_ay',
        'sw_var_az',
        'sw_var_acc_magnitude',
        'sw_cov_a_xy',
        'sw_cov_a_yz',
        'sw_cov_a_xz',
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
        'sw_entropy_acc_magnitude'
    ])

    for i in range(0, smartwatch_df.shape[0], CONFIG.N_ROWS_PER_WINDOW):
        one_window_df = smartwatch_df[i : i + CONFIG.N_ROWS_PER_WINDOW]
        accelerometer_features = _generate_accelerometer_feature_per_window(one_window_df, 'sw_')

        one_window_features = pd.concat([
            accelerometer_features
        ])

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
        column_prefix + 'var_ax',
        column_prefix + 'var_ay',
        column_prefix + 'var_az',
        column_prefix + 'var_acc_magnitude',
        column_prefix + 'cov_a_xy',
        column_prefix + 'cov_a_yz',
        column_prefix + 'cov_a_xz',
        column_prefix + 'cov_a_xmag',
        column_prefix + 'cov_a_ymag',
        column_prefix + 'cov_a_zmag',
        column_prefix + 'energy_ax',
        column_prefix + 'energy_ay',
        column_prefix + 'energy_az',
        column_prefix + 'energy_acc_magnitude',
        column_prefix + 'entropy_ax',
        column_prefix + 'entropy_ay',
        column_prefix + 'entropy_az',
        column_prefix + 'entropy_acc_magnitude'
    ]

    result += accelerometer_related_data.mean().tolist()
    result += accelerometer_related_data.var().tolist()

    result.append(_calculate_covariance(accelerometer_related_data, 'ax', 'ay'))
    result.append(_calculate_covariance(accelerometer_related_data, 'ax', 'az'))
    result.append(_calculate_covariance(accelerometer_related_data, 'ay', 'az'))
    result.append(_calculate_covariance(accelerometer_related_data, 'ax', 'acc_magnitude'))
    result.append(_calculate_covariance(accelerometer_related_data, 'ay', 'acc_magnitude'))
    result.append(_calculate_covariance(accelerometer_related_data, 'az', 'acc_magnitude'))

    result.append(_calculate_energy(accelerometer_related_data['ax']))
    result.append(_calculate_energy(accelerometer_related_data['ay']))
    result.append(_calculate_energy(accelerometer_related_data['az']))
    result.append(_calculate_energy(accelerometer_related_data['acc_magnitude']))

    result.append(_calculate_entropy(accelerometer_related_data['ax']))
    result.append(_calculate_entropy(accelerometer_related_data['ay']))
    result.append(_calculate_entropy(accelerometer_related_data['az']))
    result.append(_calculate_entropy(accelerometer_related_data['acc_magnitude']))

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
    file_path = os.path.join(CONFIG.FEATURES_DATA_DIR, activity_type, CONFIG.FEATURES_DATA_RESULT['sp'])
    smartphone_features.to_csv(file_path)


def _write_smartwatch_features_to_file(smartwatch_features, activity_type):
    print('Writing smartwatch features to file..')
    file_path = os.path.join(CONFIG.FEATURES_DATA_DIR, activity_type, CONFIG.FEATURES_DATA_RESULT['sw'])
    smartwatch_features.to_csv(file_path)


if __name__ == '__main__':
    activities = [
        'brushing',
        'eating',
        'folding',
        'going_downstairs',
        'going_upstairs',
        'lying',
        'reading',
        'running',
        'sitting',
        'standing',
        'sweeping_the_floor',
        # 'testing',
        'typing',
        'walking',
        'writing'
    ]

    generate_feature('reading')