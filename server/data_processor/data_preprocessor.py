import math

from data_processor import data_sampler
from data_processor import data_window_selector
from data_processor import feature_generator
from data_processor import data_combiner
from util import raw_data_reader
import threading


def sample_and_generate_feature(raw_data, activity_type):
    # data_sampler.sample_data_by_frequency(raw_data, activity_type)
    # data_window_selector.divide_and_store_sampled_data_to_windows(activity_type)
    data_combiner.combine_data(activity_type)
    # feature_generator.generate_feature(activity_type)


def preprocess_data(activity_type):
    raw_data = raw_data_reader.read_all_raw_data(activity_type)
    sample_and_generate_feature(raw_data, activity_type)


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

    threads = []
    for activity in activities:
        print('Full pre-processing: {}'.format(activity))
        t = threading.Thread(target=preprocess_data, args=(activity,))
        t.start()
        threads.append(t)
        print()
        print()

    for t in threads:
        t.join()