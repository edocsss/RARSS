from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

import config as CONFIG
from classifier.util import data_util


def run_test(n_estimators=50, data_source='', activities=None):
    X_train, Y_train = data_util.load_training_data(
        CONFIG.TRAINING_DATA_SOURCE_SUBJECT,
        CONFIG.MODEL_NAMES['minmax_scaler'],
        source=data_source
    )

    X_test, Y_test = data_util.load_testing_data(
        CONFIG.TESTING_DATA_SOURCE_SUBJECT,
        CONFIG.MODEL_NAMES['minmax_scaler'],
        source=data_source
    )

    accuracy_results = []
    fscore_results = []

    model = RandomForestClassifier(n_estimators=n_estimators, n_jobs=-1)
    model.fit(X_train, Y_train)
    predictions = model.predict(X_test)

    accuracy = accuracy_score(Y_test, predictions)
    accuracy_results.append(accuracy)

    fscore = f1_score(Y_test, predictions, average='weighted')
    fscore_results.append(fscore)

    print('n_estimators = {}'.format(n_estimators))
    print('accuracy = {}'.format(accuracy))
    print('fscore = {}'.format(fscore))
    print('Sampling Frequency: {}'.format(CONFIG.SAMPLING_FREQUENCY))
    print('Window Size: {}'.format(CONFIG.WINDOW_SIZE))
    print()
    print()


if __name__ == '__main__':
    n_estimators = [50, 100, 1000, 1500, 2000, 3000, 5000]
    for n in n_estimators:
        run_test(
            n_estimators=n,
            data_source=''
        )