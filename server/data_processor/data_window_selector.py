import os
import config as CONFIG
import pandas as pd


def divide_and_store_sampled_data_to_windows(activity_type):
    windowed_smartphone_df = divide_smartphone_data_to_windows(activity_type)
    windowed_smartwatch_df = divide_smartwatch_data_to_windows(activity_type)

    create_windowed_data_directory()
    create_windowed_activity_directory(activity_type)

    store_windowed_smartphone_df_to_file(windowed_smartphone_df, activity_type)
    store_windowed_smartwatch_df_to_file(windowed_smartwatch_df, activity_type)


def divide_smartphone_data_to_windows(activity_type):
    print('Dividing combined smartphone data into windows..')
    combined_smartphone_df = read_combined_smartphone_data(activity_type)
    print('Combined smartphone data divided into windows!')

    return divide_dataframe_to_windows(combined_smartphone_df)


def divide_smartwatch_data_to_windows(activity_type):
    print('Dividing combined smartwatch data into windows..')
    combined_smartwatch_df = read_combined_smartwatch_data(activity_type)
    print('Combined smartwatch data divided into windows!')

    return divide_dataframe_to_windows(combined_smartwatch_df)


def divide_dataframe_to_windows(df):
    result_df = pd.DataFrame(data=None, columns=df.columns)
    n_rows_per_window = int(CONFIG.WINDOW_SIZE / CONFIG.SAMPLING_INTERVAL)
    row_step = int(n_rows_per_window * CONFIG.WINDOW_OVERLAP)
    total_rows = df.shape[0]

    for i in range(0, total_rows, row_step):
        # Ignore the last window if the last window is NOT FULL!
        if i + n_rows_per_window > total_rows:
            break

        window_df = df[i:i + n_rows_per_window]
        result_df = result_df.append(window_df, ignore_index=True)

    return result_df


def read_combined_smartphone_data(activity_type):
    file_path = os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, CONFIG.COMBINED_SAMPLED_SMARTPHONE_DATA)
    return pd.read_csv(file_path)


def read_combined_smartwatch_data(activity_type):
    file_path = os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, CONFIG.COMBINED_SAMPLED_SMARTWATCH_DATA)
    return pd.read_csv(file_path)


def create_windowed_data_directory():
    dir_path = os.path.join(CONFIG.WINDOWED_DATA_DIR)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def create_windowed_activity_directory(activity_type):
    dir_path = os.path.join(CONFIG.WINDOWED_DATA_DIR, activity_type)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def store_windowed_smartphone_df_to_file(windowed_smartphone_df, activity_type):
    print('Storing windowed smartphone dataframe to file..')
    file_path = os.path.join(CONFIG.WINDOWED_DATA_DIR, activity_type, CONFIG.WINDOWED_SMARTPHONE_DATA)
    windowed_smartphone_df.to_csv(file_path)
    print('Windowed smartphone dataframe stored!')


def store_windowed_smartwatch_df_to_file(windowed_smartwatch_df, activity_type):
    print('Storing windowed smartwatch dataframe to file..')
    file_path = os.path.join(CONFIG.WINDOWED_DATA_DIR, activity_type, CONFIG.WINDOWED_SMARTWATCH_DATA)
    windowed_smartwatch_df.to_csv(file_path)
    print('Windowed smartwatch dataframe stored!')
