from data_processor import raw_data_reader
from data_processor import data_sampler
from data_processor import data_window_selector
import math

def sample_and_generate_feature(raw_data, activity_type):
    data_sampler.sample_data_by_frequency(raw_data, activity_type)
    data_window_selector.divide_and_store_sampled_data_to_windows(activity_type)
    # generate feature here


def preprocess_data(activity_type):
    raw_data = raw_data_reader.read_all_data(activity_type)
    raw_data = calculate_additional_fields(raw_data)

    sample_and_generate_feature(raw_data, activity_type)


def calculate_additional_fields(raw_data):
    print('Calculating additional dataframe fields..')
    raw_data['sp_accelerometer']['acc_magnitude'] = raw_data['sp_accelerometer'].apply(
        calculate_accelerometer_magnitude,
        axis=1,
        args=(['ax', 'ay', 'az'],)
    )

    raw_data['sw_accelerometer']['acc_magnitude'] = raw_data['sw_accelerometer'].apply(
        calculate_accelerometer_magnitude,
        axis=1,
        args=(['ax', 'ay', 'az'],)
    )

    print('Additional dataframe fields calculated and added to raw dataframe!')
    return raw_data


def calculate_accelerometer_magnitude(series, fields):
    return math.sqrt(sum([math.pow(series[f], 2) for f in fields]))


if __name__ == '__main__':
    preprocess_data('standing')