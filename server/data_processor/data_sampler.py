import os
import pandas as pd
import config as CONFIG
from models.data_item import DataItem


def sample_data_by_frequency(raw_data, activity_type):
    raw_data_standardized_timestamp = standardize_timestamp(raw_data)
    latest_starting_timestamp = get_latest_starting_timestamp(raw_data_standardized_timestamp)
    earliest_ending_timestamp = get_earliest_ending_timestamp(raw_data_standardized_timestamp)

    starting_time = latest_starting_timestamp + CONFIG.OUTLIER_REMOVAL_SIZE
    ending_time = earliest_ending_timestamp - CONFIG.OUTLIER_REMOVAL_SIZE
    trimmed_data = trim_data(raw_data_standardized_timestamp, starting_time, ending_time)

    sampled_data = {}
    for k, v in trimmed_data.items():
        print('Sampling {}'.format(k))

        sampled_data_list = []
        for raw_data_item in v:
            dataframe = raw_data_item.dataframe
            lower_bound = 0
            upper_bound = starting_time

            prev_series = dataframe.iloc[0]
            sampled_df = pd.DataFrame(data=None, columns=dataframe.columns)

            while upper_bound <= ending_time:
                df_within_time_boundary = dataframe[(dataframe.timestamp >= lower_bound) & (dataframe.timestamp <= upper_bound)]
                timestamps_within_boundary = [int(series['timestamp']) for index, series in df_within_time_boundary.iterrows()]

                if len(timestamps_within_boundary) == 0:
                    sample_series = prev_series
                    prev_series.set_value('timestamp', upper_bound)
                else:
                    largest_timestamp_within_boundary = max(timestamps_within_boundary)
                    sample_series = dataframe[dataframe.timestamp == largest_timestamp_within_boundary].iloc[0]
                    sample_series.set_value('timestamp', upper_bound)
                    prev_series = sample_series

                sampled_df = sampled_df.append(sample_series, ignore_index=True)
                lower_bound = upper_bound
                upper_bound += CONFIG.SAMPLING_INTERVAL

            sampled_data_list.append(DataItem(raw_data_item.file_id, sampled_df))
            raw_data_item.dataframe = dataframe

        sampled_data[k] = sampled_data_list
        print('Done sampling {}'.format(k))
        print()

    write_sampled_data_to_files(sampled_data, activity_type)


def standardize_timestamp(raw_data):
    for k, v in raw_data.items():
        for raw_data_item in v:
            first_timestamp = raw_data_item.dataframe['timestamp'][0]
            raw_data_item.dataframe['timestamp'] = raw_data_item.dataframe['timestamp'] - first_timestamp

    return raw_data


def get_latest_starting_timestamp(raw_data):
    first_row_timestamps = [raw_data_item.dataframe['timestamp'][0] for k, v in raw_data.items() for raw_data_item in v]
    return max(first_row_timestamps)


def get_earliest_ending_timestamp(raw_data):
    last_row_timestamps = [raw_data_item.dataframe['timestamp'][raw_data_item.dataframe.shape[0] - 1] for k, v in raw_data.items() for raw_data_item in v]
    return min(last_row_timestamps)


def trim_data(raw_data, starting_timestamp, ending_timestamp):
    for k, v in raw_data.items():
        for raw_data_item in v:
            dataframe = raw_data_item.dataframe
            raw_data_item.dataframe = dataframe[(dataframe.timestamp >= starting_timestamp) & (dataframe.timestamp <= ending_timestamp)]

    return raw_data


def write_sampled_data_to_files(sampled_data, activity_type):
    print('Writing sampled data to files..')
    create_sampled_data_directory()
    create_sampled_activity_directory(activity_type)

    for k, v in sampled_data.items():
        for sampled_data_item in v:
            file_name = sampled_data_item.file_id + '_' + CONFIG.SAMPLED_DATA_RESULT[k]
            write_sampled_dataframe_to_csv(activity_type, file_name, sampled_data_item.dataframe)

    print('Sampled data stored!')


def create_sampled_data_directory():
    dir_path = os.path.join(CONFIG.SAMPLED_DATA_DIR)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def create_sampled_activity_directory(activity_type):
    dir_path = os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def write_sampled_dataframe_to_csv(activity_type, file_name, dataframe):
    file_path = os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, file_name)
    dataframe.to_csv(file_path)


# def combine_smartphone_sampled_dataframe(sampled_dataframe):
#     accelerometer_df = sampled_dataframe['sp_accelerometer']
#     barometer_df = sampled_dataframe['sp_barometer']
#     gravity_df = sampled_dataframe['sp_gravity']
#     gyroscope_df = sampled_dataframe['sp_gyroscope']
#     linear_accelerometer_df = sampled_dataframe['sp_linear_accelerometer']
#     magnetic_df = sampled_dataframe['sp_magnetic']
#
#     result_df = pd.DataFrame.merge(accelerometer_df, barometer_df, on='timestamp')
#     result_df = pd.DataFrame.merge(result_df, gravity_df, on='timestamp')
#     result_df = pd.DataFrame.merge(result_df, gyroscope_df, on='timestamp')
#     result_df = pd.DataFrame.merge(result_df, linear_accelerometer_df, on='timestamp')
#     result_df = pd.DataFrame.merge(result_df, magnetic_df, on='timestamp')
#
#     return result_df
#
#
# def combine_smartwatch_sampled_dataframe(sampled_dataframe):
#     accelerometer_df = sampled_dataframe['sw_accelerometer']
#     gyroscope_df = sampled_dataframe['sw_gyroscope']
#     light_df = sampled_dataframe['sw_light']
#     pressure_df = sampled_dataframe['sw_pressure']
#     magnetic_df = sampled_dataframe['sw_magnetic']
#     ultraviolet_df = sampled_dataframe['sw_ultraviolet']
#
#     result_df = pd.DataFrame.merge(accelerometer_df, gyroscope_df, on='timestamp')
#     result_df = pd.DataFrame.merge(result_df, light_df, on='timestamp')
#     result_df = pd.DataFrame.merge(result_df, pressure_df, on='timestamp')
#     result_df = pd.DataFrame.merge(result_df, magnetic_df, on='timestamp')
#     result_df = pd.DataFrame.merge(result_df, ultraviolet_df, on='timestamp')
#
#     return result_df
#
#
# def write_combined_data_to_files(smartphone_df, smartwatch_df, activity_type):
#     print('Writing combined sampled data frames to files..')
#     create_sampled_activity_directory(activity_type)
#
#     write_sampled_dataframe_to_csv(os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, CONFIG.COMBINED_SAMPLED_SMARTPHONE_DATA), smartphone_df)
#     write_sampled_dataframe_to_csv(os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, CONFIG.COMBINED_SAMPLED_SMARTWATCH_DATA), smartwatch_df)
#     print('Sampled data stored!')
