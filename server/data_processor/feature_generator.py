import os
import config as CONFIG
import pandas as pd


def read_windowed_smartphone_data(activity_type):
    print('Reading windowed smartphone data..')
    file_path = os.path.join(CONFIG.WINDOWED_DATA_DIR, activity_type, CONFIG.WINDOWED_SMARTPHONE_DATA)
    return pd.read_csv(file_path)


def read_windowed_smartwatch_data(activity_type):
    print('Reading windowed smartwatch data..')
    file_path = os.path.join(CONFIG.WINDOWED_DATA_DIR, activity_type, CONFIG.WINDOWED_SMARTWATCH_DATA)
    return pd.read_csv(file_path)


def generate_feature(activity_type):
    smartphone_df = read_windowed_smartphone_data(activity_type)
    smartwatch_df = read_windowed_smartwatch_data(activity_type)

    smartphone_features = generate_smartphone_features(smartphone_df)
    smartwatch_features = generate_smartwatch_features(smartwatch_df)

    create_features_directory()
    create_features_activity_directory(activity_type)

    write_smartphone_features_to_file(smartphone_features, activity_type)
    write_smartwatch_features_to_file(smartwatch_features, activity_type)


def generate_smartphone_features(smartphone_df):
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
        accelerometer_features = generate_accelerometer_feature_per_window(one_window_df)

        one_window_features = pd.concat([
            accelerometer_features
        ])

        result_df = result_df.append(one_window_features, ignore_index=True)

    return result_df


def generate_smartwatch_features(smartwatch_df):
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
        accelerometer_features = generate_accelerometer_feature_per_window(one_window_df)

        one_window_features = pd.concat([
            accelerometer_features
        ])

        result_df = result_df.append(one_window_features, ignore_index=True)

    return result_df


def generate_accelerometer_feature_per_window(df):
    print('Generating accelerometer feature for one window..')
    accelerometer_related_data = df[['ax', 'ay', 'az', 'acc_magnitude']]
    one_window_smartphone_data_mean = accelerometer_related_data.mean()
    one_window_smartphone_data_mean.rename({
        'ax': 'mean_ax',
        'ay': 'mean_ay',
        'az': 'mean_az',
        'acc_magnitude': 'mean_acc_magnitude'
    }, inplace=True)

    one_window_smartphone_data_variance = accelerometer_related_data.var()
    one_window_smartphone_data_variance.rename({
        'ax': 'var_ax',
        'ay': 'var_ay',
        'az': 'var_az',
        'acc_magnitude': 'var_acc_magnitude'
    }, inplace=True)

    one_window_smartphone_feature_series = pd.concat([
        one_window_smartphone_data_mean,
        one_window_smartphone_data_variance
    ])

    return one_window_smartphone_feature_series


def create_features_directory():
    dir_path = os.path.join(CONFIG.FEATURES_DATA_DIR)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def create_features_activity_directory(activity_type):
    dir_path = os.path.join(CONFIG.FEATURES_DATA_DIR, activity_type)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def write_smartphone_features_to_file(smartphone_features, activity_type):
    print('Writing smartphone features to file..')
    file_path = os.path.join(CONFIG.FEATURES_DATA_DIR, activity_type, CONFIG.FEATURES_SMARTPHONE_DATA)
    smartphone_features.to_csv(file_path)


def write_smartwatch_features_to_file(smartwatch_features, activity_type):
    print('Writing smartwatch features to file..')
    file_path = os.path.join(CONFIG.FEATURES_DATA_DIR, activity_type, CONFIG.FEATURES_SMARTWATCH_DATA)
    smartwatch_features.to_csv(file_path)


if __name__ == '__main__':
    generate_feature('standing')