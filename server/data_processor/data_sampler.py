import os

import math
import pandas as pd

import config as CONFIG
from models.data_item import DataItem


def sample_data(raw_data, real_time_mode=False):
    sampled_data = _sample_data_by_frequency(raw_data, real_time_mode)
    return sampled_data


def _sample_data_by_frequency(raw_data, real_time_mode=False):
    raw_data_standardized_timestamp = _standardize_timestamp(raw_data)
    trimmed_data = _trim_data(raw_data_standardized_timestamp, real_time_mode=real_time_mode)

    sampled_data = {}
    for k, v in trimmed_data.items():
        sampled_data_list = []

        for item in v:
            raw_data_item = item['data_item']
            starting_timestamp = item['starting_timestamp']
            ending_timestamp = item['ending_timestamp']

            dataframe = raw_data_item.dataframe
            dataframe = dataframe[(dataframe.timestamp >= starting_timestamp) & (dataframe.timestamp <= ending_timestamp)]

            dataframe = _include_additional_data(k, dataframe)
            dataframe = _zero_mean_cols(dataframe)

            lower_bound = 0
            upper_bound = starting_timestamp

            prev_series = dataframe.iloc[0]
            sampled_df = pd.DataFrame(data=None, columns=dataframe.columns)

            while upper_bound <= ending_timestamp:
                df_within_time_boundary = dataframe[(dataframe.timestamp >= lower_bound - 0.1) & (dataframe.timestamp <= upper_bound + 0.1)]
                timestamps_within_boundary = [series['timestamp'] for index, series in df_within_time_boundary.iterrows()]

                # When there is no row for the given timestamp boundary, then use the last value
                if len(timestamps_within_boundary) == 0:
                    sample_series = prev_series
                    prev_series.set_value('timestamp', upper_bound)

                # If there is at least 1 row, then take the latest data as the sampled data
                else:
                    largest_timestamp_within_boundary = max(timestamps_within_boundary)
                    sample_series = dataframe[(dataframe.timestamp >= largest_timestamp_within_boundary - 0.1) & (dataframe.timestamp <= largest_timestamp_within_boundary + 0.1)].iloc[0]
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

    return sampled_data


# Standardize the timestamp so that it always starts at time '0'
# This is mainly to synchronize the Smartphone and Smartwatch timestamp
# In addition, as the timestamp is standardized for each recording session data, for different sensors, and for different devices,
# it is much easier to combine the raw data in later stages
#
# Although the timestamp is standardized, it is possible that the Smartwatch starts later due to the WebSocket latency
# This problem cannot really be solved since we cannot ask the Smartwatch to tell Smartphone when it starts recording (again, due to latency)
# So, although there is latency, the outliers have been removed and hence the difference should not be huge and not going to affect the data
def _standardize_timestamp(raw_data):
    for k, v in raw_data.items():
        for raw_data_item in v:
            first_timestamp = raw_data_item.dataframe['timestamp'][0]
            raw_data_item.dataframe['timestamp'] = raw_data_item.dataframe['timestamp'] - first_timestamp

    return raw_data


def _get_latest_starting_timestamp(data_items):
    first_row_timestamps = [data_item.dataframe['timestamp'][0] for data_item in data_items]
    return max(first_row_timestamps)


def _get_earliest_ending_timestamp(data_items):
    last_row_timestamps = [data_item.dataframe['timestamp'][data_item.dataframe.shape[0] - 1] for data_item in data_items]
    return min(last_row_timestamps)


# Trim the starting and ending of the dataframe for each recording session
# This is mainly to remove the outliers (which are usually at the beginning and the end of the data)
def _trim_data(raw_data_standardized_timestamp, real_time_mode=False):
    data = raw_data_standardized_timestamp
    first_key = list(data.keys())[0]
    n_experiment = len(data[first_key])

    for i in range(0, n_experiment):
        data_items = [v[i] for k, v in data.items()]

        starting_timestamp = _get_latest_starting_timestamp(data_items)
        starting_timestamp = starting_timestamp + CONFIG.STARTING_OUTLIER_REMOVAL_SIZE if not real_time_mode else starting_timestamp

        ending_timestamp = _get_earliest_ending_timestamp(data_items)
        ending_timestamp = ending_timestamp - CONFIG.ENDING_OUTLIER_REMOVAL_SIZE if not real_time_mode else ending_timestamp

        # Include the starting and ending timestamp information for sampling later
        for k, v in data.items():
            dataframe = v[i].dataframe
            v[i].dataframe = dataframe[(dataframe.timestamp >= starting_timestamp) & (dataframe.timestamp <= ending_timestamp)]

            v[i] = {
                'data_item': v[i],
                'starting_timestamp': starting_timestamp,
                'ending_timestamp': ending_timestamp
            }

    return data


def write_sampled_data_to_files(sampled_data, activity_type):
    print('Writing sampled data to files..')
    _create_sampled_data_directory()
    _create_sampled_activity_directory(activity_type)

    for k, v in sampled_data.items():
        for sampled_data_item in v:
            file_name = CONFIG.FILE_NAME_SUFFIX + sampled_data_item.file_id + '_' + CONFIG.SAMPLED_DATA_RESULT[k]
            _write_sampled_dataframe_to_csv(activity_type, file_name, sampled_data_item.dataframe)

    print('Sampled data stored!')


def _create_sampled_data_directory():
    dir_path = os.path.join(CONFIG.SAMPLED_DATA_DIR)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def _create_sampled_activity_directory(activity_type):
    dir_path = os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def _write_sampled_dataframe_to_csv(activity_type, file_name, dataframe):
    file_path = os.path.join(CONFIG.SAMPLED_DATA_DIR, activity_type, file_name)
    dataframe.to_csv(file_path)


###############################################

def _include_additional_data(type, df):
    if 'accelerometer' in type:
        df['acc_magnitude'] = df.apply(
            _calculate_magnitude,
            axis=1,
            args=(['ax', 'ay', 'az'],)
        )

    elif 'gyroscope' in type:
        df['gyro_magnitude'] = df.apply(
            _calculate_magnitude,
            axis=1,
            args=(['gx', 'gy', 'gz'],)
        )

    return df


def _calculate_magnitude(row, fields):
    return math.sqrt(sum([math.pow(row[f], 2) for f in fields]))


def _zero_mean_cols(df):
    zero_mean_df = df - df.mean()
    zero_mean_df = zero_mean_df.rename(columns=lambda c: c + '_zero_mean')
    zero_mean_df.drop('timestamp_zero_mean', axis=1, inplace=True)
    return pd.concat([df, zero_mean_df], axis=1)
