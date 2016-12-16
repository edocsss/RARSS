from sklearn.svm import SVC
from classifier.util import data_util
import config as CONFIG
import os
import pickle


def run_training(c=100, gamma=0.5, kernel='rbf', data_source=''):
    print('Training SVM model for Real Time Monitoring..')
    print('Cost: {}'.format(c))
    print('Gamma: {}'.format(gamma))
    print('Kernel: {}'.format(kernel))
    print('Data Source: {}'.format(data_source))
    print()
    print()
    print()

    X_train, Y_train = data_util.load_training_data(
        CONFIG.REAL_TIME_MONITORING_TRAINING_DATA_SOURCE_SUBJECT,
        CONFIG.MODEL_NAMES['real_time_monitoring_minmax_scaler'],
        source=data_source
    )

    model = SVC(C=c, kernel=kernel, gamma=gamma)
    model.fit(X_train, Y_train)
    return model


def store_model(model):
    file_path = os.path.join(CONFIG.MODEL_DIR, CONFIG.MODEL_NAMES['real_time_monitoring_svm_model'])
    f = open(file_path, 'wb')
    pickle.dump(model, f)
    f.close()


if __name__ == '__main__':
    model = run_training(c=100, kernel='rbf', gamma=0.5)
    store_model(model)