import time

import numpy as np
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import os

import config as CONFIG
from classifier.util import activity_encoding, plot_util
from classifier.util import data_util


c_matrix = []


def run_test(training_subjects, test_subjects, C=1, kernel='rbf', degree=1, gamma='auto', data_source='', permutate_xyz=False, activities=None, show_confusion=False):
    X_train, Y_train = data_util.load_training_data(
        training_subjects,
        data_source + '_' + ''.join(training_subjects) + '_svmloo_' + CONFIG.MODEL_NAMES['minmax_scaler'],
        source=data_source,
        activities=activities,
        permutate_xyz=permutate_xyz
    )

    X_test, Y_test = data_util.load_testing_data(
        test_subjects,
        data_source + '_' + ''.join(training_subjects) + '_svmloo_' + CONFIG.MODEL_NAMES['minmax_scaler'],
        source=data_source,
        activities=activities
    )

    print('X_train size: {}'.format(len(X_train)))
    print('X_test size: {}'.format(len(X_test)))
    print()

    accuracy_results = []
    fscore_results = []

    model = SVC(C=C, kernel=kernel, gamma=gamma, degree=degree, random_state=int(time.time()))
    model.fit(X_train, Y_train)
    predictions = model.predict(X_test)

    accuracy = accuracy_score(Y_test, predictions)
    accuracy_results.append(accuracy)

    fscore = f1_score(Y_test, predictions, average='weighted')
    fscore_results.append(fscore)

    if show_confusion:
        cm = confusion_matrix(Y_test, predictions)
        c_matrix.append(cm)

    return accuracy, fscore


if __name__ == '__main__':
    accuracy = []
    f1 = []

    C = 1
    gamma = 'auto'
    permutate_xyz = False
    data_source = ''
    show_confusion = True

    activities = [
        # 'standing',
        # 'sitting',
        # 'lying',
        'walking',
        # 'running',
        # 'brushing',
        # 'writing',
        # 'reading',
        # 'typing',
        'going_downstairs',
        'going_upstairs',
        # 'food_preparation',
        # 'folding',
        # 'sweeping_the_floor'
    ]

    for test_subject in CONFIG.FULL_SUBJECT_LIST:
        training_subjects = [name for name in CONFIG.FULL_SUBJECT_LIST if name != test_subject]
        test_subject = [test_subject]

        accuracy = []
        f1 = []

        print('Data Source: {}'.format(data_source))
        print('Activities: {}'.format(activities))
        print('Cost: {}'.format(C))
        print('Gamma: {}'.format(gamma))
        print('Sampling Frequency: {}'.format(CONFIG.SAMPLING_FREQUENCY))
        print('Window Size: {}'.format(CONFIG.WINDOW_SIZE))
        print('Training Subjects: {}'.format(training_subjects))
        print('Testing Subjects: {}'.format(test_subject))

        for i in range(3):
            a, f = run_test(
                training_subjects=training_subjects,
                test_subjects=test_subject,
                C=C,
                gamma=gamma,
                data_source=data_source,
                activities=activities,
                kernel='rbf',
                degree=1,
                permutate_xyz=permutate_xyz,
                show_confusion=show_confusion
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

    if show_confusion:
        cmr = c_matrix[0]
        for i in range(1, len(c_matrix)):
            cmr += c_matrix[i]

        plt.figure(figsize=(7, 7), dpi=100)
        plot_util.plot_confusion_matrix(
            cmr,
            [activity_encoding.INT_TO_ACTIVITY_MAPPING[i] for i in
             sorted([activity_encoding.ACTIVITY_TO_INT_MAPPING[a] for a in activities])]
        )

        fig_name = os.path.join(CONFIG.CLASSIFIER_DIR, 'loo', 'loo_cm', 'cm_lopo_walk_stairs_svm_accbaro_{}_{}_{}.png'.format(
            C,
            gamma,
            data_source
        ))

        plt.savefig(fig_name)
        plt.clf()
