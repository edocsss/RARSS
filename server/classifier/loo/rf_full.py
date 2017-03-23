import time

import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.metrics import confusion_matrix

import config as CONFIG
from classifier.util import activity_encoding, plot_util
from classifier.util import data_util
import os


c_matrix = []


def run_test(training_subjects, test_subjects, n_estimators=50, data_source='', activities=None, permutate_xyz=False, show_confusion=False):
    X_train, Y_train = data_util.load_training_data(
        training_subjects,
        data_source + '_' + ''.join(training_subjects) + '_rfloo1_' + CONFIG.MODEL_NAMES['minmax_scaler'],
        source=data_source,
        activities=activities,
        permutate_xyz=permutate_xyz
    )

    X_test, Y_test = data_util.load_testing_data(
        test_subjects,
        data_source + '_' + ''.join(training_subjects) + '_rfloo1_' + CONFIG.MODEL_NAMES['minmax_scaler'],
        source=data_source,
        activities=activities
    )

    print('X_train size: {}'.format(len(X_train)))
    print('X_test size: {}'.format(len(X_test)))
    print()

    accuracy_results = []
    fscore_results = []

    model = RandomForestClassifier(n_estimators=n_estimators, n_jobs=-1, random_state=int(time.time()))
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
    n_estimators = [500]
    n_experiments = 3
    show_confusion = False

    for n in n_estimators:
        for test_subject in CONFIG.FULL_SUBJECT_LIST:
            training_subjects = [name for name in CONFIG.FULL_SUBJECT_LIST if name != test_subject]
            test_subject = [test_subject]

            f1 = []
            accuracy = []

            print('Number of Estimators: {}'.format(n))
            print('Activities: {}'.format(activities))
            print('Data Source: {}'.format(data_source))
            print('Training Subjects: {}'.format(training_subjects))
            print('Testing Subjects: {}'.format(test_subject))
            print('Permutate XYZ: {}'.format(permutate_xyz))

            for i in range(0, n_experiments):
                a, f = run_test(
                    training_subjects=training_subjects,
                    test_subjects=test_subject,
                    n_estimators=n,
                    data_source=data_source,
                    activities=activities,
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

        fig_name = os.path.join(CONFIG.CLASSIFIER_DIR, 'loo', 'cm_lopo_all_rf_accbarogyro_ori_zero_mean_{}_{}.png'.format(
            n_estimators,
            data_source
        ))

        plt.savefig(fig_name)
        plt.clf()