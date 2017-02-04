import threading
import time

import config as CONFIG
from data_processor import data_combiner
from data_processor import data_sampler
from data_processor import data_window_selector
from data_processor import feature_generator
from data_processor.util import raw_data_reader


def preprocess_data_for_manual_testing(activity_type, data_subject=CONFIG.PREPROCESS_DATA_SOURCE_SUBJECT):
    raw_data = raw_data_reader.read_all_raw_data(activity_type)

    print('Data sampling started for {}!'.format(activity_type))
    sampled_data = data_sampler.sample_data(raw_data)
    data_sampler.write_sampled_data_to_files(sampled_data, activity_type)
    print('Data sampling done for {}!'.format(activity_type))
    print()

    print('Data windowing started for {}!'.format(activity_type))
    windowed_data = data_window_selector.divide_sampled_data_to_windows(sampled_data)
    data_window_selector.store_windowed_data_to_files(windowed_data, activity_type)
    print('Data windowing done for {}!'.format(activity_type))
    print()

    combined_smartphone_dfs, combined_smartwatch_dfs = data_combiner.combine_data_by_device_source(windowed_data)
    data_combiner.store_combined_data_by_device_source(combined_smartphone_dfs, combined_smartwatch_dfs, activity_type)

    print('Features generation started for {}!'.format(activity_type))
    smartphone_features, smartwatch_features = feature_generator.generate_feature(combined_smartphone_dfs, combined_smartwatch_dfs)
    feature_generator.store_features_df(smartphone_features, smartwatch_features, activity_type)
    print('Features generation done for {}!'.format(activity_type))
    print()
    print()

    combined_features_df = data_combiner.combine_sp_sw_into_one(smartphone_features, smartwatch_features)
    data_combiner.store_combined_features(combined_features_df, activity_type)


def preprocess_data_for_real_time_monitoring(raw_data):
    sampled_data = data_sampler.sample_data(raw_data, real_time_mode=True)
    combined_smartphone_dfs, combined_smartwatch_dfs = data_combiner.combine_data_by_device_source(sampled_data)
    smartphone_features, smartwatch_features = feature_generator.generate_feature(combined_smartphone_dfs, combined_smartwatch_dfs)
    combined_features_df = data_combiner.combine_sp_sw_into_one(smartphone_features, smartwatch_features)
    combined_features_df = data_combiner.drop_irrelevant_columns_from_combined_dfs(combined_features_df)
    return combined_features_df


if __name__ == '__main__':
    activities = [
        'brushing',
        'folding',
        'going_downstairs',
        'going_upstairs',
        'lying',
        'reading',
        'running',
        'sitting',
        'standing',
        'sweeping_the_floor',
        'food_preparation',
        'typing',
        'walking',
        'writing'
    ]

    for subject in CONFIG.FULL_SUBJECT_LIST:
        print('Data preprocessing configuration:')
        print('Subject: {}'.format(subject))
        print('Sampling Frequency: {}'.format(CONFIG.SAMPLING_FREQUENCY))
        print('Window Size: {}'.format(CONFIG.WINDOW_SIZE))
        print('Window Overlap Size: {}'.format(CONFIG.WINDOW_OVERLAP))
        print('Starting Outlier Removal Size: {}'.format(CONFIG.STARTING_OUTLIER_REMOVAL_SIZE))
        print('Ending Outlier Removal Size: {}'.format(CONFIG.ENDING_OUTLIER_REMOVAL_SIZE))
        print()
        print()
        print()

        start = time.time()
        threads = []

        for activity in activities:
            print('Full pre-processing: {}'.format(activity))
            t = threading.Thread(target=preprocess_data_for_manual_testing, args=(activity, subject,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        data_combiner.combine_all_data_into_one_complete_dataset()
        print('Timer: {}'.format(time.time() - start))