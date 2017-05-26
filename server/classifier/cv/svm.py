import numpy as np
import os
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.svm import SVC

import config as CONFIG
from classifier.util import data_util, plot_util, activity_encoding
import matplotlib.pyplot as plt


def run_cv(C=10, kernel='rbf', gamma='auto', degree=3, data_source='', activities=None):
    print('SVM Configuration:')
    print('C: {}'.format(C))
    print('Kernel: {}'.format(kernel))
    print('Gamma: {}'.format(gamma))
    print('Degree: {}'.format(degree))
    print('Data source: {}'.format(data_source))
    print()

    kfold_data = data_util.load_kfolds_training_and_testing_data(
        scaler_name=data_source + '_kfold_svm_' + CONFIG.MODEL_NAMES['minmax_scaler'],
        k=5,
        source=data_source,
        activities=activities
    )

    accuracy_results = []
    fscore_results = []
    c_matrix = []

    for i, data in enumerate(kfold_data):
        X_train = data[0]
        X_test = data[1]
        Y_train = data[2]
        Y_test = data[3]

        model = SVC(C=C, kernel=kernel, gamma=gamma, degree=degree)
        model.fit(X_train, Y_train)

        predictions = model.predict(X_test)
        accuracy = accuracy_score(Y_test, predictions)
        accuracy_results.append(accuracy)

        fscore = f1_score(Y_test, predictions, average='weighted')
        fscore_results.append(fscore)

        cm = confusion_matrix(Y_test, predictions)
        c_matrix.append(cm)

    accuracy_mean = np.mean(accuracy_results)
    accuracy_std_dev = np.std(accuracy_results)

    fscore_mean = np.mean(fscore_results)
    fscore_std_dev = np.std(fscore_results)

    # cmr = c_matrix[0]
    # for i in range(1, len(c_matrix)):
    #     cmr += c_matrix[i]
    #
    # plt.figure(figsize=(5, 5))
    # plot_util.plot_confusion_matrix(
    #     cmr,
    #     [activity_encoding.INT_TO_ACTIVITY_MAPPING[i] for i in
    #      sorted([activity_encoding.ACTIVITY_TO_INT_MAPPING[a] for a in activities])]
    # )
    #
    # fig_name = os.path.join(CONFIG.CLASSIFIER_DIR, 'cv', 'results', 'cm_kfold_stairs_accbaro_svm_{}_{}_{}.png'.format(
    #     C,
    #     gamma,
    #     data_source
    # ))
    #
    # plt.savefig(fig_name)
    # plt.clf()

    print('Cost: {}'.format(C))
    print('Sampling Frequency: {}'.format(CONFIG.SAMPLING_FREQUENCY))
    print('Window Size: {}'.format(CONFIG.WINDOW_SIZE))
    print('Accuracy: {}'.format(accuracy_results))
    print('Accuracy Mean: {}, Accuracy Standard deviation: {}'.format(accuracy_mean, accuracy_std_dev))
    print('F1 Score: {}'.format(fscore_results))
    print('F1 Mean: {}, F1 Standard deviation: {}'.format(fscore_mean, fscore_std_dev))
    print('Training Source: {}'.format(CONFIG.KFOLD_DATA_SOURCE_SUBJECT))
    print('Activities: {}'.format(activities))
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()

    return accuracy_mean, accuracy_std_dev, fscore_mean, fscore_std_dev


if __name__ == '__main__':
    x = []
    y = []

    C = [1, 100, 500, 1000, 5000]
    C = [1000, 5000]
    kernel = ['rbf']
    gamma = ['auto', 0.1, 0.5, 1]
    gamma = [0.1, 0.5, 1]
    degree = [1]

    for c in C:
        for k in kernel:
            for g in gamma:
                for d in degree:
                    accuracy_mean, accuracy_std_dev, fscore_mean, fscore_std_dev = run_cv(
                        C=c,
                        kernel=k,
                        gamma=g,
                        degree=d,
                        data_source='',  # 'sw' (smartwatch only), 'sp' (smartphone only), '<empty_string>' (both SP + SW)
                        activities=[
                            'brushing',
                            'folding',
                            'going_downstairs',
                            'going_upstairs',
                            'lying',
                            'reading',
                            'running',
                            'sitting',
                            'standing',
                            'sweeping_the_floor',
                            'food_preparation',
                            'typing',
                            'walking',
                            'writing'
                        ]
                    )
