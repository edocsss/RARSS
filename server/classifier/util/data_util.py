import copy
import os
import pickle

import pandas as pd
import numpy as np
from sklearn.cross_validation import KFold
from sklearn.preprocessing import MinMaxScaler

import classifier.util.activity_encoding as ENCODING
import config as CONFIG


def _load_data(subject):
    file_path = os.path.join(
        CONFIG.COMBINED_DATA_DIR,
        CONFIG.FILE_NAME_SUFFIX +
        subject +
        '_' +
        CONFIG.COMBINED_DATA_RESULT['full']
    )

    df = pd.read_csv(file_path)
    df = df[df.activity != 'testing']
    df = _drop_irrelevant_columns(df)
    return df


def _drop_irrelevant_columns(df):
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df.drop('Unnamed: 0.1', axis=1, inplace=True)
    return df


def _load_data_by_multiple_subjects(subjects):
    dfs = []
    for subject in subjects:
        df = _load_data(subject)
        dfs.append(df)

    result_df = pd.concat(dfs)
    result_df = result_df.iloc[np.random.permutation(len(result_df))]
    return result_df


def load_training_data(subjects, scaler_name, source='', onehot=False, permutate_xyz=False, activities=None):
    full_data = _load_data_by_multiple_subjects(subjects)
    full_data = _filter_features_by_source(full_data, source)
    full_data = _filter_data_by_activity(full_data, activities)

    if permutate_xyz:
        full_data = _permutate_xyz_data(full_data)

    X = full_data.drop('activity', axis=1).values.astype('float64')
    Y = full_data['activity']

    Y_encoded = _map_activity_to_int_encoding(Y)
    Y_encoded = pd.DataFrame(data=Y_encoded.values, columns=['label'])

    if onehot:
        Y_encoded = Y_encoded.apply(_binarize_label, axis=1)
        Y_encoded = Y_encoded.drop('label', axis=1)

    _train_minmax_scaler(X, scaler_name, force=True)
    X_norm = _normalize_X(X, scaler_name)

    Y_encoded = Y_encoded.values.astype('float64')
    return X_norm, Y_encoded


def load_testing_data(subjects, scaler_name, source='', onehot=False, permutate_xyz=False, activities=None):
    full_data = _load_data_by_multiple_subjects(subjects)
    full_data = _filter_features_by_source(full_data, source)
    full_data = _filter_data_by_activity(full_data, activities)

    if permutate_xyz:
        full_data = _permutate_xyz_data(full_data)

    X = full_data.drop('activity', axis=1).values.astype('float64')
    Y = full_data['activity']

    Y_encoded = _map_activity_to_int_encoding(Y)
    Y_encoded = pd.DataFrame(data=Y_encoded.values, columns=['label'])

    if onehot:
        Y_encoded = Y_encoded.apply(_binarize_label, axis=1)
        Y_encoded = Y_encoded.drop('label', axis=1)

    X_norm = _normalize_X(X, scaler_name)
    Y_encoded = Y_encoded.values.astype('float64')
    return X_norm, Y_encoded


def load_kfolds_training_and_testing_data(scaler_name, k=5, source='', activities=None, permutate_xyz=False, onehot=False):
    full_data = _load_data_by_multiple_subjects(CONFIG.KFOLD_DATA_SOURCE_SUBJECT)
    full_data = _filter_features_by_source(full_data, source)
    full_data = _filter_data_by_activity(full_data, activities)

    if permutate_xyz:
        full_data = _permutate_xyz_data(full_data)

    X = full_data.drop('activity', axis=1).values.astype('float64')
    Y = full_data['activity']

    Y_encoded = _map_activity_to_int_encoding(Y)
    Y_encoded = pd.DataFrame(data=Y_encoded.values, columns=['label'])

    if onehot:
        Y_encoded = Y_encoded.apply(_binarize_label, axis=1)
        Y_encoded = Y_encoded.drop('label', axis=1)

    Y_encoded = Y_encoded.values.astype('float64')

    kfold_indices = KFold(len(X), n_folds=k)
    kfolds_data = []

    for train_indices, test_indices in kfold_indices:
        X_train = X[train_indices]
        X_test = X[test_indices]
        Y_train = Y_encoded[train_indices]
        Y_test = Y_encoded[test_indices]

        if onehot:
            Y_test = unbinarize_label(Y_test)

        _train_minmax_scaler(X_train, scaler_name, force=True)
        X_train_norm = _normalize_X(X_train, scaler_name)
        X_test_norm = _normalize_X(X_test, scaler_name)

        kfolds_data.append((
            X_train_norm,
            X_test_norm,
            Y_train,
            Y_test
        ))

    return kfolds_data


# Only select features related to the given source parameter
# Empty string means use all features (Smartphone and Smartwatch)
def _filter_features_by_source(df, source):
    if len(source) <= 0:
        return df

    return df[[col for col in df.columns if source in col] + ['activity']]


def _filter_data_by_activity(df, activities):
    if activities is None:
        return df

    return df[df['activity'].isin(activities)]


def _permutate_xyz_data(full_data):
    features = ['mean', 'var', 'energy', 'entropy']
    axes = ['x', 'y', 'z']
    dfs = []

    for axis1 in axes:
        for axis2 in [a for a in axes if a != axis1]:
            for axis3 in [a for a in axes if a != axis1 and a != axis2]:
                renamed_df = _rename_full_data_accelerometer_columns(full_data, features, [axis1, axis2, axis3])
                dfs.append(renamed_df)

    return pd.concat(dfs)


def _rename_full_data_accelerometer_columns(full_data, features, axes_order):
    full_data_copy = copy.deepcopy(full_data)

    for f in features:
        full_data_copy = full_data_copy.rename(columns={
            'sp_{}_ax'.format(f): 'sp_{}_a{}'.format(f, axes_order[0]),
            'sp_{}_ay'.format(f): 'sp_{}_a{}'.format(f, axes_order[1]),
            'sp_{}_az'.format(f): 'sp_{}_a{}'.format(f, axes_order[2]),

            'sw_{}_ax'.format(f): 'sw_{}_a{}'.format(f, axes_order[0]),
            'sw_{}_ay'.format(f): 'sw_{}_a{}'.format(f, axes_order[1]),
            'sw_{}_az'.format(f): 'sw_{}_a{}'.format(f, axes_order[2])
        })

    return full_data_copy


def _map_activity_to_int_encoding(Y):
    Y_encoded = Y.apply(lambda row: ENCODING.ACTIVITY_TO_INT_MAPPING[row])
    return Y_encoded


def _binarize_label(row):
    binary_label = ENCODING.INT_TO_BINARY_MAPPING[str(row['label'])]
    for i, c in enumerate(binary_label):
        row['label_{}'.format(i)] = c

    return row


def unbinarize_label(Y):
    Y = pd.DataFrame(data=Y, columns=['label_{}'.format(i) for i in range(len(ENCODING.INT_TO_BINARY_MAPPING))])
    return Y.apply(_convert_binary_label_to_int, axis=1)['label'].values


def _convert_binary_label_to_int(row):
    bin = ''
    for i in range (0, len(ENCODING.INT_TO_BINARY_MAPPING['0'])):
        bin += str(int(row['label_{}'.format(i)]))

    row['label'] = float(ENCODING.BINARY_TO_INT_MAPPING[bin])
    return row


# Normalizer model is stored based on the given name
# This is to differentiate the model used for Activity Recording and Real Time Monitoring
def _normalize_X(X, scaler_name):
    file_path = os.path.join(CONFIG.MODEL_DIR, scaler_name)
    f = open(file_path, 'rb')
    scaler = pickle.load(f)
    f.close()

    return scaler.transform(X)


def _train_minmax_scaler(X_train, scaler_name, force=False):
    if _check_if_scaler_exists(scaler_name) and not force:
        return

    minmax_scaler = MinMaxScaler()
    minmax_scaler.fit(X_train)
    _store_scaler(minmax_scaler, scaler_name)


def _check_if_scaler_exists(scaler_name):
    file_path = os.path.join(CONFIG.MODEL_DIR, scaler_name)
    return os.path.isfile(file_path)


def _store_scaler(scaler, scaler_name):
    file_path = os.path.join(CONFIG.MODEL_DIR, scaler_name)
    f = open(file_path, 'wb')
    pickle.dump(scaler, f)
    f.close()


def get_data_distribution(Y):
    df = pd.DataFrame(data=Y, columns=['activity'])
    counts = df['activity'].value_counts()
    return counts


if __name__ == '__main__':
    data = _load_data_by_multiple_subjects(['andri'])
    print(get_data_distribution(data['activity']))
