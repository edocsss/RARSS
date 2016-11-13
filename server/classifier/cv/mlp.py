import time

import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import SGD
from sklearn.metrics import accuracy_score, f1_score

import config as CONFIG
from classifier.util import activity_encoding
from classifier.util import data_util


def run_cv(kfold_data, max_epoch=1000, alpha=0.1, n_hidden_layer=1, n_neuron_hidden_layer=10):
    print('Configuration:')
    print('max_epoch = {}, alpha = {}, n_hidden_layer = {}, n_neuron_hidden_layer = {}'.format(
        max_epoch,
        alpha,
        n_hidden_layer,
        n_neuron_hidden_layer
    ))

    accuracy_results = []
    fscore_results = []

    for i, data in enumerate(kfold_data):
        print(i)
        batch_size = 32

        X_train = data[0]
        X_test = data[1]
        Y_train = data[2]
        Y_test = data[3]

        model = Sequential()
        model.add(Dense(n_neuron_hidden_layer, input_dim=len(X_train[0]), activation='sigmoid', init='uniform'))

        for n in range(1, n_hidden_layer):
            model.add(Dense(n_neuron_hidden_layer, activation='sigmoid', init='uniform'))

        model.add(Dense(len(activity_encoding.ACTIVITY_TO_INT_MAPPING.keys()), activation='sigmoid', init='uniform'))
        sgd = SGD(lr=alpha)

        model.compile(
            optimizer=sgd,
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

        model.fit(
            X_train,
            Y_train,
            nb_epoch=max_epoch,
            batch_size=batch_size,
            verbose=0
        )

        predictions = model.predict_classes(X_test)
        accuracy = accuracy_score(Y_test, predictions)
        accuracy_results.append(accuracy)

        fscore = f1_score(Y_test, predictions, average='weighted')
        fscore_results.append(fscore)

    accuracy_mean = np.mean(accuracy_results)
    accuracy_std_dev = np.std(accuracy_results)

    fscore_mean = np.mean(fscore_results)
    fscore_std_dev = np.std(fscore_results)

    print()
    print()
    print('Sampling Frequency: {}'.format(CONFIG.SAMPLING_FREQUENCY))
    print('Window Size: {}'.format(CONFIG.WINDOW_SIZE))
    print('Accuracy: {}'.format(accuracy_results))
    print('Accuracy Mean: {}, Accuracy Standard deviation: {}'.format(accuracy_mean, accuracy_std_dev))
    print('F1 Score: {}'.format(fscore_results))
    print('F1 Mean: {}, F1 Standard deviation: {}'.format(fscore_mean, fscore_std_dev))
    print()
    print('==================================================================')

    return accuracy_mean, accuracy_std_dev, fscore_mean, fscore_std_dev


if __name__ == '__main__':
    kfold_data = data_util.load_kfolds_training_and_testing_data(k=5, source='sw', activities=None, onehot=True)
    alpha = [0.5]
    max_epoch = [3000]
    n_hidden_layer = [1]
    n_neuron_hidden_layer = [50]

    for a in alpha:
        for epoch in max_epoch:
            for layer in n_hidden_layer:
                for neuron in n_neuron_hidden_layer:
                    accuracy_mean, accuracy_std_dev, fscore_mean, fscore_std_dev = run_cv(
                        kfold_data,
                        max_epoch=epoch,
                        alpha=a,
                        n_hidden_layer=layer,
                        n_neuron_hidden_layer=neuron,
                    )