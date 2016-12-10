import numpy as np
from sklearn.metrics import accuracy_score, f1_score
from sklearn.svm import SVC

import config as CONFIG
from classifier.util import data_util


def run_cv(C=10, kernel='rbf', data_source='', activities=None):
    kfold_data = data_util.load_kfolds_training_and_testing_data(k=5, source=data_source, activities=activities)
    accuracy_results = []
    fscore_results = []

    for i, data in enumerate(kfold_data):
        X_train = data[0]
        X_test = data[1]
        Y_train = data[2]
        Y_test = data[3]

        model = SVC(C=C, kernel=kernel)
        model.fit(X_train, Y_train)

        predictions = model.predict(X_test)
        accuracy = accuracy_score(Y_test, predictions)
        accuracy_results.append(accuracy)

        fscore = f1_score(Y_test, predictions, average='weighted')
        fscore_results.append(fscore)
        # print('k = {}, accuracy = {}'.format(i + 1, accuracy))
        # print('k = {}, fscore = {}'.format(i + 1, fscore))
        # print()
        # print()

    accuracy_mean = np.mean(accuracy_results)
    accuracy_std_dev = np.std(accuracy_results)

    fscore_mean = np.mean(fscore_results)
    fscore_std_dev = np.std(fscore_results)

    print('Cost: {}'.format(C))
    print('Sampling Frequency: {}'.format(CONFIG.SAMPLING_FREQUENCY))
    print('Window Size: {}'.format(CONFIG.WINDOW_SIZE))
    print('Accuracy: {}'.format(accuracy_results))
    print('Accuracy Mean: {}, Accuracy Standard deviation: {}'.format(accuracy_mean, accuracy_std_dev))
    print('F1 Score: {}'.format(fscore_results))
    print('F1 Mean: {}, F1 Standard deviation: {}'.format(fscore_mean, fscore_std_dev))
    print()
    print()
    print()
    print()

    return accuracy_mean, accuracy_std_dev, fscore_mean, fscore_std_dev


if __name__ == '__main__':
    x = []
    y = []

    C = [12500, 13625]
    activities = None

    for c in C:
        accuracy_mean, accuracy_std_dev, fscore_mean, fscore_std_dev = run_cv(
            C=c,
            data_source='',
            activities=activities
        )