import os
import pandas as pd
import config as CONFIG


def sample_data_by_frequency(raw_data, activity_type):
    latest_starting_timestamp = get_latest_starting_timestamp(raw_data)
    earliest_ending_timestamp = get_earliest_ending_timestamp(raw_data)

    starting_time = latest_starting_timestamp + CONFIG.OUTLIER_REMOVAL_SIZE
    ending_time = earliest_ending_timestamp - CONFIG.OUTLIER_REMOVAL_SIZE
    trimmed_data = trim_data(raw_data, starting_time, ending_time)

    sampled_data = {}
    for k, v in trimmed_data.items():
        print('Sampling {}'.format(k))

        lower_bound = 0
        upper_bound = starting_time

        prev_series = v.iloc[0]
        sampled_df = pd.DataFrame(data=None, columns=v.columns)

        while upper_bound <= ending_time:
            df_within_time_boundary = v[(v.timestamp >= lower_bound) & (v.timestamp <= upper_bound)]
            timestamps_within_boundary = [int(series['timestamp']) for index, series in df_within_time_boundary.iterrows()]

            if len(timestamps_within_boundary) == 0:
                sample_series = prev_series
                prev_series.set_value('timestamp', upper_bound)
            else:
                largest_timestamp_within_boundary = max(timestamps_within_boundary)
                sample_series = v[v.timestamp == largest_timestamp_within_boundary].iloc[0]
                sample_series.set_value('timestamp', upper_bound)
                prev_series = sample_series

            sampled_df = sampled_df.append(sample_series, ignore_index=True)
            lower_bound = upper_bound
            upper_bound += CONFIG.SAMPLING_INTERVAL

        sampled_data[k] = sampled_df
        print('Done sampling {}'.format(k))

    combined_smartphone_df = combine_smartphone_sampled_dataframe(sampled_data)
    combined_smartwatch_df = combine_smartwatch_sampled_dataframe(sampled_data)

    write_sampled_data_to_files(sampled_data, activity_type)
    write_combined_data_to_files(combined_smartphone_df, combined_smartwatch_df, activity_type)


def get_latest_starting_timestamp(raw_data):
    first_row_timestamps = [v['timestamp'][0] for k, v in raw_data.items()]
    return max(first_row_timestamps)


def get_earliest_ending_timestamp(raw_data):
    last_row_timestamps = [v['timestamp'][v.shape[0] - 1] for k, v in raw_data.items()]
    return min(last_row_timestamps)


def trim_data(raw_data, starting_timestamp, ending_timestamp):
    for k, v in raw_data.items():
        raw_data[k] = v[(v.timestamp >= starting_timestamp) & (v.timestamp <= ending_timestamp)]

    return raw_data


def write_sampled_data_to_files(sampled_data, activity_type):
    print('Writing sampled data to files..')
    create_sampled_data_directory()
    create_sampled_activity_directory(activity_type)

    write_dataframe_to_csv(os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, CONFIG.SAMPLED_ACCELEROMETER_RESULT_SMARTPHONE), sampled_data['sp_accelerometer'])
    write_dataframe_to_csv(os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, CONFIG.SAMPLED_BAROMETER_RESULT_SMARTPHONE), sampled_data['sp_barometer'])
    write_dataframe_to_csv(os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, CONFIG.SAMPLED_GRAVITY_RESULT_SMARTPHONE), sampled_data['sp_gravity'])
    write_dataframe_to_csv(os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, CONFIG.SAMPLED_GYROSCOPE_RESULT_SMARTPHONE), sampled_data['sp_gyroscope'])
    write_dataframe_to_csv(os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, CONFIG.SAMPLED_LINEAR_ACCELEROMETER_RESULT_SMARTPHONE), sampled_data['sp_linear_accelerometer'])
    write_dataframe_to_csv(os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, CONFIG.SAMPLED_MAGNETIC_RESULT_SMARTPHONE), sampled_data['sp_magnetic'])

    write_dataframe_to_csv(os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, CONFIG.SAMPLED_ACCELEROMETER_RESULT_SMARTWATCH), sampled_data['sw_accelerometer'])
    write_dataframe_to_csv(os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, CONFIG.SAMPLED_GYROSCOPE_RESULT_SMARTWATCH), sampled_data['sw_gyroscope'])
    write_dataframe_to_csv(os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, CONFIG.SAMPLED_LIGHT_RESULT_SMARTWATCH), sampled_data['sw_light'])
    write_dataframe_to_csv(os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, CONFIG.SAMPLED_PRESSURE_RESULT_SMARTWATCH), sampled_data['sw_pressure'])
    write_dataframe_to_csv(os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, CONFIG.SAMPLED_MAGNETIC_RESULT_SMARTWATCH), sampled_data['sw_magnetic'])
    write_dataframe_to_csv(os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, CONFIG.SAMPLED_ULTRAVIOLET_RESULT_SMARTWATCH), sampled_data['sw_ultraviolet'])
    print('Sampled data stored!')


def create_sampled_data_directory():
    dir_path = os.path.join(CONFIG.SAMPLED_DATA_DIR)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def create_sampled_activity_directory(activity_type):
    dir_path = os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def write_dataframe_to_csv(file_path, dataframe):
    dataframe.to_csv(file_path)


def combine_smartphone_sampled_dataframe(sampled_dataframe):
    accelerometer_df = sampled_dataframe['sp_accelerometer']
    barometer_df = sampled_dataframe['sp_barometer']
    gravity_df = sampled_dataframe['sp_gravity']
    gyroscope_df = sampled_dataframe['sp_gyroscope']
    linear_accelerometer_df = sampled_dataframe['sp_linear_accelerometer']
    magnetic_df = sampled_dataframe['sp_magnetic']

    result_df = pd.DataFrame.merge(accelerometer_df, barometer_df, on='timestamp')
    result_df = pd.DataFrame.merge(result_df, gravity_df, on='timestamp')
    result_df = pd.DataFrame.merge(result_df, gyroscope_df, on='timestamp')
    result_df = pd.DataFrame.merge(result_df, linear_accelerometer_df, on='timestamp')
    result_df = pd.DataFrame.merge(result_df, magnetic_df, on='timestamp')

    return result_df


def combine_smartwatch_sampled_dataframe(sampled_dataframe):
    accelerometer_df = sampled_dataframe['sw_accelerometer']
    gyroscope_df = sampled_dataframe['sw_gyroscope']
    light_df = sampled_dataframe['sw_light']
    pressure_df = sampled_dataframe['sw_pressure']
    magnetic_df = sampled_dataframe['sw_magnetic']
    ultraviolet_df = sampled_dataframe['sw_ultraviolet']

    result_df = pd.DataFrame.merge(accelerometer_df, gyroscope_df, on='timestamp')
    result_df = pd.DataFrame.merge(result_df, light_df, on='timestamp')
    result_df = pd.DataFrame.merge(result_df, pressure_df, on='timestamp')
    result_df = pd.DataFrame.merge(result_df, magnetic_df, on='timestamp')
    result_df = pd.DataFrame.merge(result_df, ultraviolet_df, on='timestamp')

    return result_df


def write_combined_data_to_files(smartphone_df, smartwatch_df, activity_type):
    print('Writing combined sampled data frames to files..')
    create_sampled_activity_directory(activity_type)

    write_dataframe_to_csv(os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, CONFIG.COMBINED_SAMPLED_SMARTPHONE_DATA), smartphone_df)
    write_dataframe_to_csv(os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, CONFIG.COMBINED_SAMPLED_SMARTWATCH_DATA), smartwatch_df)
    print('Sampled data stored!')

