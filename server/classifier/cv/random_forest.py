import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
import time

import config as CONFIG
from classifier.util import activity_encoding
from classifier.util import data_util, plot_util
import matplotlib.pyplot as plt


def run_cv(n_estimators=50, data_source='', activities=None, permutate_xyz=False):
    kfold_data = data_util.load_kfolds_training_and_testing_data(
        scaler_name=data_source + '_kfold_rf_' + CONFIG.MODEL_NAMES['minmax_scaler'],
        k=5,
        source=data_source,
        activities=activities,
        permutate_xyz=permutate_xyz
    )

    accuracy_results = []
    fscore_results = []
    c_matrix = []

    print('Data Source: {}'.format(data_source))
    print('Number of Estimators: {}'.format(n_estimators))
    print('Sampling Frequency: {}'.format(CONFIG.SAMPLING_FREQUENCY))
    print('Window Size: {}'.format(CONFIG.WINDOW_SIZE))
    print('Training Source: {}'.format(CONFIG.KFOLD_DATA_SOURCE_SUBJECT))
    print('Activities: {}'.format(activities))
    print('Permutate XYZ: {}'.format(permutate_xyz))
    print()

    for i, data in enumerate(kfold_data):
        X_train = data[0]
        X_test = data[1]
        Y_train = data[2]
        Y_test = data[3]

        model = RandomForestClassifier(n_estimators=n_estimators, n_jobs=-1, random_state=int(time.time()))
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
    # plt.figure(figsize=(7, 7), dpi=100)
    # plot_util.plot_confusion_matrix(
    #     cmr,
    #     [activity_encoding.INT_TO_ACTIVITY_MAPPING[i] for i in
    #      sorted([activity_encoding.ACTIVITY_TO_INT_MAPPING[a] for a in activities])]
    # )
    #
    # fig_name = os.path.join(CONFIG.CLASSIFIER_DIR, 'cv', 'results', 'cm_kfold_stairs_accbaro_rf_{}_{}.png'.format(
    #     n_estimators,
    #     data_source
    # ))
    #
    # plt.savefig(fig_name)
    # plt.clf()

    print('Accuracy: {}'.format(accuracy_results))
    print('Accuracy Mean: {}, Accuracy Standard deviation: {}'.format(accuracy_mean, accuracy_std_dev))
    print('F1 Score: {}'.format(fscore_results))
    print('F1 Mean: {}, F1 Standard deviation: {}'.format(fscore_mean, fscore_std_dev))
    print()
    print()
    print()

    return accuracy_mean, accuracy_std_dev, fscore_mean, fscore_std_dev


if __name__ == '__main__':
    n_estimators = [100, 300, 500, 1000]
    for n in n_estimators:
        run_cv(
            n_estimators=n,
            data_source='', # 'sw' (smartwatch only), 'sp' (smartphone only), '<empty_string>' (both SP + SW)
            permutate_xyz=False,
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
