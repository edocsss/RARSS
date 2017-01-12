import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.metrics import confusion_matrix

import config as CONFIG
from classifier.util import activity_encoding, plot_util
from classifier.util import data_util


def run_test(n_neighbors=50, data_source='', activities=None, permutate_xyz=False):
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

    model = KNeighborsClassifier(n_neighbors=n_neighbors, n_jobs=-1, weights='uniform')
    model.fit(X_train, Y_train)
    predictions = model.predict(X_test)

    accuracy = accuracy_score(Y_test, predictions)
    accuracy_results.append(accuracy)

    fscore = f1_score(Y_test, predictions, average='weighted')
    fscore_results.append(fscore)

    # cm = confusion_matrix(
    #     Y_test,
    #     predictions
    # )
    #
    # plt.figure()
    # plot_util.plot_confusion_matrix(
    #     cm,
    #     [activity_encoding.INT_TO_ACTIVITY_MAPPING[i] for i in sorted([activity_encoding.ACTIVITY_TO_INT_MAPPING[a] for a in activities])]
    # )
    # plt.show()

    return accuracy, fscore


if __name__ == '__main__':
    activities = [
        'standing',
        'sitting',
        'lying',
        'walking',
        'running',
        'brushing',
        'writing',
        'reading',
        'typing',
        'going_downstairs',
        'going_upstairs',
        'food_preparation',
        'folding',
        'sweeping_the_floor'
    ]

    data_source = ''
    permutate_xyz = False
    n_neighbors = [1, 5, 10, 15, 30, 50, 500]

    for n in n_neighbors:
        f1 = []
        accuracy = []

        print('Number of Neighbors: {}'.format(n))
        print('Activities: {}'.format(activities))
        print('Data Source: {}'.format(data_source))
        print('Training Subjects: {}'.format(CONFIG.TRAINING_DATA_SOURCE_SUBJECT))
        print('Testing Subjects: {}'.format(CONFIG.TESTING_DATA_SOURCE_SUBJECT))
        print('Permutate XYZ: {}'.format(permutate_xyz))

        for i in range(0, 1):
            a, f = run_test(
                n_neighbors=n,
                data_source=data_source,
                activities=activities,
                permutate_xyz=permutate_xyz
            )

            accuracy.append(a)
            f1.append(f)

        print()
        print('Accuracy: {}'.format(accuracy))
        print('Accuracy Mean: {}, Accuracy Standard deviation: {}'.format(np.mean(accuracy), np.std(accuracy)))
        print('F1 Score: {}'.format(f1))
        print('F1 Mean: {}, F1 Standard deviation: {}'.format(np.mean(f1), np.std(f1)))
        print()
        print()
        print()
        print()
        print()