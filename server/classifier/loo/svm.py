from sklearn.metrics import accuracy_score, f1_score
from sklearn.svm import SVC

import config as CONFIG
from classifier.util import data_util
import numpy as np


def run_test(C=10, kernel='poly', degree=3, gamma='auto', data_source='', permutate_xyz=False, activities=None):
    print('Data Source: {}'.format(data_source))
    print('Cost: {}'.format(C))
    print('Sampling Frequency: {}'.format(CONFIG.SAMPLING_FREQUENCY))
    print('Window Size: {}'.format(CONFIG.WINDOW_SIZE))
    print('Training Subjects: {}'.format(CONFIG.TRAINING_DATA_SOURCE_SUBJECT))
    print('Testing Subjects: {}'.format(CONFIG.TESTING_DATA_SOURCE_SUBJECT))

    X_train, Y_train = data_util.load_training_data(
        CONFIG.TRAINING_DATA_SOURCE_SUBJECT,
        CONFIG.MODEL_NAMES['minmax_scaler'],
        source=data_source,
        activities=activities,
        permutate_xyz=permutate_xyz
    )

    X_test, Y_test = data_util.load_testing_data(
        CONFIG.TESTING_DATA_SOURCE_SUBJECT,
        CONFIG.MODEL_NAMES['minmax_scaler'],
        source=data_source,
        activities=activities
    )

    print('X_train size: {}'.format(len(X_train)))
    print('X_test size: {}'.format(len(X_test)))
    print()

    accuracy_results = []
    fscore_results = []

    model = SVC(C=C, kernel=kernel, gamma=gamma, degree=degree)
    model.fit(X_train, Y_train)
    predictions = model.predict(X_test)

    accuracy = accuracy_score(Y_test, predictions)
    accuracy_results.append(accuracy)

    fscore = f1_score(Y_test, predictions, average='weighted')
    fscore_results.append(fscore)

    print('Permutate XYZ: {}'.format(permutate_xyz))
    print('Accuracy: {}'.format(accuracy_results))
    print('F1 Score: {}'.format(fscore_results))
    print()
    print()
    print()
    print()

    return accuracy, fscore


if __name__ == '__main__':
    accuracy = []
    f1 = []

    C = [1, 5, 10, 50, 100, 500, 1000, 5000, 10000]
    gamma = [0.1, 0.5, 1]
    permutate_xyz = True
    data_source = ''

    activities = [
        'standing',
        'sitting',
        'lying',
        'walking',
        'running',
        'brushing',
        # 'eating',
        'writing',
        'reading',
        'typing',
        'going_downstairs',
        'going_upstairs',
        'food_preparation',
        'folding',
        'sweeping_the_floor'
    ]

    for c in C:
        for g in gamma:
            for i in range(1):
                a, f = run_test(
                    C=c,
                    gamma=g,
                    data_source=data_source,
                    activities=activities,
                    kernel='rbf',
                    degree=1,
                    permutate_xyz=permutate_xyz
                )

                accuracy.append(a)
                f1.append(f)

            print()
            print()
            print()
            print()
            print('Accuracy: {}'.format(accuracy))
            print('Accuracy Mean: {}, Accuracy Standard deviation: {}'.format(np.mean(accuracy), np.std(accuracy)))
            print('F1 Score: {}'.format(f1))
            print('F1 Mean: {}, F1 Standard deviation: {}'.format(np.mean(f1), np.std(f1)))
