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
    X = [
        2.0841226458549498, -9.602454805374146, 0.8667907878756523, 9.886371287125039, 0.1600517524461029,
        0.16948868135346448, 0.2684512707214887, 0.1366175311254695, 0.038136856550616584, -0.08552191967849586,
        0.028359826706752463, -0.005442287706180884, -0.1479459071412573, -0.020496952057297787, 1.2800374086047,
        1.1087058035735526, 1.3230502842219831, 1.09300428902656, 2.8531677772621697, 2.4501408630787096,
        2.5973252428754092, 2.569924355430216, -7.883393239974977, 3.7733617871999736, -5.99198694229126,
        12.151013193993332, 0.9186225908259914, 37.974045582246774, 1.2210471334790536, 2.8957511267339355,
        3.4356592920129376, -0.7633563105553116, -0.5086648368752262, 1.2790042563819717, 5.196004977486645,
        -1.3882103469561162, 1.8350861730501968, 4.195448656655522, 1.91200911943928, 2.4405301635672454,
        2.658184681325861, 2.4406070195368232, 2.621004226408645, 2.6619656088502928
    ]

    X = [[1, 2, 3], [4, 5, 6]]
    print(predict_activity(X))