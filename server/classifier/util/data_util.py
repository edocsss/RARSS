import os
import pickle

import numpy as np
import pandas as pd
from sklearn.cross_validation import KFold
from sklearn.preprocessing import MinMaxScaler

import classifier.util.activity_encoding as ENCODING
import config as CONFIG


def _load_data(subject):
    file_path = os.path.join(
        CONFIG.COMBINED_DATA_DIR,
        CONFIG.FILE_NAME_SUFFIX +
        '_'.join(subject) +
        '_' +
        CONFIG.COMBINED_DATA_RESULT['full']
    )

    df = pd.read_csv(file_path)
    df = df[df.activity != 'testing']
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df = df.iloc[np.random.permutation(len(df))]

    return df


def load_training_data(source='', onehot=False, activities=None):
    full_data = _load_data(CONFIG.TRAINING_DATA_SOURCE_SUBJECT)
    full_data = _filter_features_by_source(full_data, source)

    X = full_data.drop('activity', axis=1).values.astype('float64')
    Y = full_data['activity']

    Y_encoded = _map_activity_to_int_encoding(Y)
    Y_encoded = pd.DataFrame(data=Y_encoded.values, columns=['label'])

    if onehot:
        Y_encoded = Y_encoded.apply(_binarize_label, axis=1)
        Y_encoded = Y_encoded.drop('label', axis=1)

    _train_minmax_scaler(X, force=True)
    X_norm = _normalize_minmax_X(X)

    Y_encoded = Y_encoded.values.astype('float64')
    return X_norm, Y_encoded


def load_testing_data(source='', onehot=False, activities=None):
    full_data = _load_data(CONFIG.TESTING_DATA_SOURCE_SUBJECT)
    full_data = _filter_features_by_source(full_data, source)
    full_data = _filter_data_by_activity(full_data, activities)

    X = full_data.drop('activity', axis=1).values.astype('float64')
    Y = full_data['activity']

    Y_encoded = _map_activity_to_int_encoding(Y)
    Y_encoded = pd.DataFrame(data=Y_encoded.values, columns=['label'])

    if onehot:
        Y_encoded = Y_encoded.apply(_binarize_label, axis=1)
        Y_encoded = Y_encoded.drop('label', axis=1)

    # _train_minmax_scaler(X, force=True)
    X_norm = _normalize_minmax_X(X)

    Y_encoded = Y_encoded.values.astype('float64')
    return X_norm, Y_encoded


def load_kfolds_training_and_testing_data(k=5, source='', activities=None, onehot=False):
    full_data = _load_data(CONFIG.KFOLD_DATA_SOURCE_SUBJECT)
    full_data = _filter_features_by_source(full_data, source)
    full_data = _filter_data_by_activity(full_data, activities)

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

        _train_minmax_scaler(X_train, force=True)
        X_train_norm = _normalize_minmax_X(X_train)
        X_test_norm = _normalize_minmax_X(X_test)

        kfolds_data.append((
            X_train_norm,
            X_test_norm,
            Y_train,
            Y_test
        ))

    return kfolds_data


def _filter_features_by_source(df, source):
    if len(source) <= 0:
        return df

    return df[[col for col in df.columns if source in col] + ['activity']]


def _filter_data_by_activity(df, activities):
    if activities is None:
        return df

    return df[df['activity'].isin(activities)]


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


def _normalize_minmax_X(X):
    file_path = os.path.join(CONFIG.CLASSIFIER_MODEL_DIR, CONFIG.CLASSIFIER_MODEL_NAMES['minmax_scaler'])
    f = open(file_path, 'rb')
    minmax_scaler = pickle.load(f)
    f.close()

    return minmax_scaler.transform(X)


def _train_minmax_scaler(X_train, force=False):
    if _check_if_minmax_scaler_exists() and not force:
        return

    minmax_scaler = MinMaxScaler()
    minmax_scaler.fit(X_train)
    _store_minmax_scaler(minmax_scaler)


def _check_if_minmax_scaler_exists():
    file_path = os.path.join(CONFIG.CLASSIFIER_MODEL_DIR, CONFIG.CLASSIFIER_MODEL_NAMES['minmax_scaler'])
    return os.path.isfile(file_path)


def _store_minmax_scaler(minmax_scaler):
    file_path = os.path.join(CONFIG.CLASSIFIER_MODEL_DIR, CONFIG.CLASSIFIER_MODEL_NAMES['minmax_scaler'])
    f = open(file_path, 'wb')
    pickle.dump(minmax_scaler, f)
    f.close()


def get_data_distribution(Y):
    df = pd.DataFrame(data=Y, columns=['activity'])
    counts = df['activity'].value_counts()
    return counts


if __name__ == '__main__':
    data = _load_data(CONFIG.TRAINING_DATA_SOURCE_SUBJECT)
    print(len(data))
    print(get_data_distribution(data['activity']))