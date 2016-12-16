from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import SGD
from sklearn.metrics import accuracy_score, f1_score

import config as CONFIG
from classifier.util import activity_encoding
from classifier.util import data_util


def run_cv(X_train, X_test, Y_train, Y_test, max_epoch=1000, alpha=0.1, n_hidden_layer=1, n_neuron_hidden_layer=10):
    print('Configuration:')
    print('max_epoch = {}, alpha = {}, n_hidden_layer = {}, n_neuron_hidden_layer = {}'.format(
        max_epoch,
        alpha,
        n_hidden_layer,
        n_neuron_hidden_layer
    ))

    batch_size = 32
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
    fscore = f1_score(Y_test, predictions, average='weighted')

    print()
    print()
    print('Sampling Frequency: {}'.format(CONFIG.SAMPLING_FREQUENCY))
    print('Window Size: {}'.format(CONFIG.WINDOW_SIZE))
    print('Accuracy: {}'.format(accuracy))
    print('F1 Score: {}'.format(fscore))
    print()
    print('==================================================================')


if __name__ == '__main__':
    X_train, Y_train = data_util.load_training_data(
        CONFIG.TRAINING_DATA_SOURCE_SUBJECT,
        CONFIG.MODEL_NAMES['minmax_scaler'],
        onehot=True
    )

    X_test, Y_test = data_util.load_testing_data(
        CONFIG.TESTING_DATA_SOURCE_SUBJECT,
        CONFIG.MODEL_NAMES['minmax_scaler'],
        onehot=False
    )

    alpha = [0.01]
    max_epoch = [2000]
    n_hidden_layer = [1]
    n_neuron_hidden_layer = [100]

    for a in alpha:
        for epoch in max_epoch:
            for layer in n_hidden_layer:
                for neuron in n_neuron_hidden_layer:
                    run_cv(
                        X_train,
                        X_test,
                        Y_train,
                        Y_test,
                        max_epoch=epoch,
                        alpha=a,
                        n_hidden_layer=layer,
                        n_neuron_hidden_layer=neuron,
                    )