import os
import pickle

import config as CONFIG
from classifier.util import activity_encoding
from classifier.util import data_util
from util.logger import classifier_logger as LOGGER


def predict_activity(X):
    if isinstance(X[0], list):
        LOGGER.error('Please pass in a 1-D array!')
        return ''

    model = _load_model()
    X_norm = data_util._normalize_X(X, CONFIG.MODEL_NAMES['real_time_monitoring_minmax_scaler'])

    predicted_activity = model.predict(X_norm)
    labelled_predicted_activity = activity_encoding.INT_TO_ACTIVITY_MAPPING[predicted_activity[0]]

    return labelled_predicted_activity


def _load_model():
    file_path = os.path.join(CONFIG.MODEL_DIR, CONFIG.MODEL_NAMES['real_time_monitoring_model'])
    f = open(file_path, 'rb')
    model = pickle.load(f)
    f.close()

    return model


if __name__ == '__main__':
    X = [ -7.46435907e+00,  -9.59585157e-01,   5.99840025e+00,
         9.62395919e+00,   8.66570342e-04,   1.68783332e-03,
         3.57285838e-04,   3.54296919e-04,  -2.14363172e-04,
         2.99197712e-04,   2.80559118e-05,  -4.66946305e-04,
         2.04514608e-05,  -1.20632162e-05,   3.06530259e-01,
         3.60976766e-01,   2.39507715e-01,   2.40528061e-01,
         2.26107938e+00,   2.25833535e+00,   2.20425388e+00,
         2.21579995e+00,  -1.39368627e+00,   5.05895869e+00,
        -8.22572666e+00,   9.75747076e+00,   4.08108328e-03,
         9.07475464e-03,   8.33065144e-04,   2.47767040e-03,
        -2.31394064e-03,  -2.35216908e-04,   1.09954487e-03,
        -1.57654269e-03,   4.14421482e-03,  -1.00387000e-04,
         4.36303318e-01,   5.25948902e-01,   2.77876461e-01,
         3.82370809e-01,   2.07263836e+00,   2.04545330e+00,
         1.96196116e+00,   2.05750631e+00]

    print(predict_activity(X))