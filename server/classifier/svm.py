from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

import config as CONFIG
from classifier.util import data_util
from classifier.util import activity_encoding


def run_test(C=10, kernel='sigmoid', data_source=''):
    X_train, Y_train = data_util.load_training_data(data_source)
    X_test, Y_test = data_util.load_testing_data(data_source)

    accuracy_results = []
    fscore_results = []

    model = SVC(C=C, kernel=kernel)
    model.fit(X_train, Y_train)
    predictions = model.predict(X_test)

    accuracy = accuracy_score(Y_test, predictions)
    accuracy_results.append(accuracy)

    fscore = f1_score(Y_test, predictions, average='weighted')
    fscore_results.append(fscore)

    print('accuracy = {}'.format(accuracy))
    print('fscore = {}'.format(fscore))
    print()
    print()

    print('Cost: {}'.format(C))
    print('Sampling Frequency: {}'.format(CONFIG.SAMPLING_FREQUENCY))
    print('Window Size: {}'.format(CONFIG.WINDOW_SIZE))
    print('Accuracy: {}'.format(accuracy_results))
    print('F1 Score: {}'.format(fscore_results))
    print()
    print()
    print()
    print()


if __name__ == '__main__':
    C = [100, 200, 300, 500, 1000]
    for c in C:
        run_test(
            C=c,
            data_source=''
        )