from sklearn.ensemble import RandomForestClassifier
from classifier.util import data_util
import config as CONFIG
import os
import pickle


def run_training(n_estimators=50, data_source=''):
    print('Training RF model for Real Time Monitoring..')
    print('Number of Estimators: {}'.format(n_estimators))
    print('Data Source: {}'.format(data_source))
    print('Training Subjects: {}'.format(CONFIG.REAL_TIME_MONITORING_TRAINING_DATA_SOURCE_SUBJECT))
    print()
    print()
    print()

    X_train, Y_train = data_util.load_training_data(
        CONFIG.REAL_TIME_MONITORING_TRAINING_DATA_SOURCE_SUBJECT,
        CONFIG.MODEL_NAMES['real_time_monitoring_minmax_scaler'],
        source=data_source
    )

    model = RandomForestClassifier(n_estimators=n_estimators, n_jobs=-1)
    model.fit(X_train, Y_train)
    return model


def store_model(model):
    file_path = os.path.join(CONFIG.MODEL_DIR, CONFIG.MODEL_NAMES['real_time_monitoring_rf_model'])
    f = open(file_path, 'wb')
    pickle.dump(model, f)
    f.close()


if __name__ == '__main__':
    model = run_training(n_estimators=2000)
    store_model(model)