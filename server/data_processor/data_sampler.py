import os
import pandas as pd
import config as CONFIG
from models.data_item import DataItem
from util import raw_data_reader


def sample_data(activity_type):
    raw_data = raw_data_reader.read_all_raw_data(activity_type, CONFIG.TRAINING_DATA_SOURCE_SUBJECT)
    sampled_data = _sample_data_by_frequency(raw_data, activity_type)
    # post_processed_sampled_data = _post_process_sampled_data_for_weird_sw_timestamp(sampled_data)
    # post_processed_sampled_data = _post_process_to_unify_timestamps(post_processed_sampled_data)
    # _write_sampled_data_to_files(post_processed_sampled_data, activity_type)
    _write_sampled_data_to_files(sampled_data, activity_type)


def _sample_data_by_frequency(raw_data, activity_type):
    raw_data_standardized_timestamp = _standardize_timestamp(raw_data)
    latest_starting_timestamp = _get_latest_starting_timestamp(raw_data_standardized_timestamp)
    earliest_ending_timestamp = _get_earliest_ending_timestamp(raw_data_standardized_timestamp)

    starting_time = latest_starting_timestamp + CONFIG.OUTLIER_REMOVAL_SIZE
    ending_time = earliest_ending_timestamp - CONFIG.OUTLIER_REMOVAL_SIZE
    trimmed_data = _trim_data(raw_data_standardized_timestamp, starting_time, ending_time)

    sampled_data = {}
    for k, v in trimmed_data.items():
        print('Sampling {} for {}'.format(k, activity_type))

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

    return sampled_data


def _standardize_timestamp(raw_data):
    for k, v in raw_data.items():
        for raw_data_item in v:
            first_timestamp = raw_data_item.dataframe['timestamp'][0]
            raw_data_item.dataframe['timestamp'] = raw_data_item.dataframe['timestamp'] - first_timestamp

    return raw_data


def _get_latest_starting_timestamp(raw_data):
    first_row_timestamps = [raw_data_item.dataframe['timestamp'][0] for k, v in raw_data.items() for raw_data_item in v]
    return max(first_row_timestamps)


def _get_earliest_ending_timestamp(raw_data):
    last_row_timestamps = [raw_data_item.dataframe['timestamp'][raw_data_item.dataframe.shape[0] - 1] for k, v in raw_data.items() for raw_data_item in v]
    return min(last_row_timestamps)


def _trim_data(raw_data, starting_timestamp, ending_timestamp):
    for k, v in raw_data.items():
        for raw_data_item in v:
            dataframe = raw_data_item.dataframe
            raw_data_item.dataframe = dataframe[(dataframe.timestamp >= starting_timestamp) & (dataframe.timestamp <= ending_timestamp)]

    return raw_data


def _post_process_sampled_data_for_weird_sw_timestamp(sampled_data):
    for k, v in sampled_data.items():
        if 'sw' in k:
            for raw_data_item in v:
                df = raw_data_item.dataframe
                same_counter = 0
                first_index = -1
                prev_value = df.iloc[0][1]

                i = 1
                while i < len(df):
                    current_value = df.iloc[i][1]
                    if current_value == prev_value:
                        same_counter += 1
                        first_index = (i - 1) if first_index == -1 else first_index
                    else:
                        if same_counter >= CONFIG.THRESHOLD_WEIRD_TIMESTAMP_DETECTION:
                            df.drop(df.index[[x for x in range(first_index + CONFIG.N_SAMPLE_WEIRD_TIMESTAMP_REPLACEMENT, i)]], inplace=True)
                            i -= (i - first_index) - CONFIG.N_SAMPLE_WEIRD_TIMESTAMP_REPLACEMENT

                        same_counter = 0
                        first_index = -1

                    prev_value = current_value
                    i += 1

                if same_counter >= CONFIG.THRESHOLD_WEIRD_TIMESTAMP_DETECTION:
                    df.drop(df.index[[x for x in range(first_index + CONFIG.N_SAMPLE_WEIRD_TIMESTAMP_REPLACEMENT, i)]], inplace=True)

    return sampled_data


def _post_process_to_unify_timestamps(sampled_data):
    first_key = list(sampled_data.keys())[0]
    for i in range(len(sampled_data[first_key])):
        indices = _get_intersect_index_from_sampled_data(sampled_data, i)

        for k, v in sampled_data.items():
            raw_data_item = v[i]
            df = raw_data_item.dataframe
            raw_data_item.dataframe = df.ix[indices]

    return sampled_data


def _get_intersect_index_from_sampled_data(sampled_data, index):
    timestamp_list = []
    for k, v in sampled_data.items():
        raw_data_item = v[index]
        df = raw_data_item.dataframe
        timestamp_list.append(set(df.index.values.tolist()))

    result = timestamp_list[0]
    for r in timestamp_list:
        result = result.intersection(r)

    print(sorted(list(result)))
    return sorted(list(result))


def _write_sampled_data_to_files(sampled_data, activity_type):
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
