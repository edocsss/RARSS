import os
import config as CONFIG
import pandas as pd
import math
from util import combined_data_reader


def generate_feature(activity_type):
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
        'mean_ax',
        'mean_ay',
        'mean_az',
        'mean_acc_magnitude',
        'var_ax',
        'var_ay',
        'var_az',
        'var_acc_magnitude'
    ])

    for i in range(0, smartphone_df.shape[0], CONFIG.N_ROWS_PER_WINDOW):
        one_window_df = smartphone_df[i : i + CONFIG.N_ROWS_PER_WINDOW]
        accelerometer_features = _generate_accelerometer_feature_per_window(one_window_df)

        one_window_features = pd.concat([
            accelerometer_features
        ])

        result_df = result_df.append(one_window_features, ignore_index=True)

    return result_df


def _generate_smartwatch_features(smartwatch_df):
    print('Generating smartwatch features..')
    result_df = pd.DataFrame(data=None, columns=[
        'mean_ax',
        'mean_ay',
        'mean_az',
        'mean_acc_magnitude',
        'var_ax',
        'var_ay',
        'var_az',
        'var_acc_magnitude'
    ])

    for i in range(0, smartwatch_df.shape[0], CONFIG.N_ROWS_PER_WINDOW):
        one_window_df = smartwatch_df[i : i + CONFIG.N_ROWS_PER_WINDOW]
        accelerometer_features = _generate_accelerometer_feature_per_window(one_window_df)

        one_window_features = pd.concat([
            accelerometer_features
        ])

        result_df = result_df.append(one_window_features, ignore_index=True)

    return result_df


def _generate_accelerometer_feature_per_window(df):
    accelerometer_related_data = df[['ax', 'ay', 'az', 'acc_magnitude']]
    result = []
    result_cols = [
        'mean_ax',
        'mean_ay',
        'mean_az',
        'mean_acc_magnitude',
        'var_ax',
        'var_ay',
        'var_az',
        'var_acc_magnitude',
        'cov_a_xy',
        'cov_a_yz',
        'cov_a_xz',
        'cov_a_xmag',
        'cov_a_ymag',
        'cov_a_zmag'
    ]

    result += accelerometer_related_data.mean().tolist()
    result += accelerometer_related_data.var().tolist()

    result.append(_calculate_covariance(accelerometer_related_data, 'ax', 'ay'))
    result.append(_calculate_covariance(accelerometer_related_data, 'ax', 'az'))
    result.append(_calculate_covariance(accelerometer_related_data, 'ay', 'az'))
    result.append(_calculate_covariance(accelerometer_related_data, 'ax', 'acc_magnitude'))
    result.append(_calculate_covariance(accelerometer_related_data, 'ay', 'acc_magnitude'))
    result.append(_calculate_covariance(accelerometer_related_data, 'az', 'acc_magnitude'))

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
    file_path = os.path.join(CONFIG.FEATURES_DATA_DIR, activity_type, CONFIG.FEATURES_SMARTPHONE_DATA)
    smartphone_features.to_csv(file_path)


def _write_smartwatch_features_to_file(smartwatch_features, activity_type):
    print('Writing smartwatch features to file..')
    file_path = os.path.join(CONFIG.FEATURES_DATA_DIR, activity_type, CONFIG.FEATURES_SMARTWATCH_DATA)
    smartwatch_features.to_csv(file_path)


if __name__ == '__main__':
    generate_feature('standing')