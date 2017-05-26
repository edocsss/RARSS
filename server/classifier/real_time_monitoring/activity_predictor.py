import os
import pickle

import config as CONFIG
from classifier.util import activity_encoding
from classifier.util import data_util
from util.logger import classifier_logger as LOGGER


def predict_activity(X, model_name=CONFIG.MODEL_NAMES['real_time_monitoring_rf_model']):
    if isinstance(X[0], list):
        LOGGER.error('Please pass in a 1-D array!')
        return ''

    X_norm = data_util._normalize_X(X, CONFIG.MODEL_NAMES['real_time_monitoring_minmax_scaler'])

    model = _load_model(model_name)
    predicted_activity = model.predict(X_norm)
    labelled_predicted_activity = activity_encoding.INT_TO_ACTIVITY_MAPPING[predicted_activity[0]]

    return labelled_predicted_activity


def _load_model(model_name):
    file_path = os.path.join(CONFIG.MODEL_DIR, model_name)
    f = open(file_path, 'rb')
    model = pickle.load(f)
    f.close()

    return model