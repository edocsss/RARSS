import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

import config as CONFIG
from classifier.util import data_util
from classifier.util import activity_encoding


def run_test(n_estimators=50, data_source='', activities=None):
    X_train, Y_train = data_util.load_training_data(data_source, activities=activities)
    X_test, Y_test = data_util.load_testing_data(data_source, activities=activities)

    t = 100
    X_train = np.append(X_train, X_test[:t], axis=0)
    Y_train = np.append(Y_train, Y_test[:t], axis=0)
    X_test = X_test[t:]
    Y_test = Y_test[t:]

    accuracy_results = []
    fscore_results = []

    model = RandomForestClassifier(n_estimators=n_estimators, n_jobs=-1)
    model.fit(X_train, Y_train)
    predictions = model.predict(X_test)

    accuracy = accuracy_score(Y_test, predictions)
    accuracy_results.append(accuracy)

    fscore = f1_score(Y_test, predictions, average='weighted')
    fscore_results.append(fscore)

    int_labels = [i for i in range(len(activity_encoding.ACTIVITY_TO_INT_MAPPING.keys()))]
    cm = confusion_matrix(
        Y_test,
        predictions,
        labels=int_labels
    )

    print('n_estimators = {}'.format(n_estimators))
    print('accuracy = {}'.format(accuracy))
    print('fscore = {}'.format(fscore))
    print('Sampling Frequency: {}'.format(CONFIG.SAMPLING_FREQUENCY))
    print('Window Size: {}'.format(CONFIG.WINDOW_SIZE))
    print()
    print()


if __name__ == '__main__':
    n_estimators = [300, 500, 1000]
    for n in n_estimators:
        run_test(
            n_estimators=n,
            data_source=''
        )