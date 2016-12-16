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

    model = _load_model(model_name)
    X_norm = data_util._normalize_X(X, CONFIG.MODEL_NAMES['real_time_monitoring_minmax_scaler'])

    predicted_activity = model.predict(X_norm)
    labelled_predicted_activity = activity_encoding.INT_TO_ACTIVITY_MAPPING[predicted_activity[0]]

    return labelled_predicted_activity


def _load_model(model_name):
    file_path = os.path.join(CONFIG.MODEL_DIR, model_name)
    f = open(file_path, 'rb')
    model = pickle.load(f)
    f.close()

    return model


if __name__ == '__main__':
    X = [-9.309105014801023,-0.9018658518791198,2.4462456703186035,9.667372635825334,0.0004832354773546166,0.0005655222066881491,0.000557399125233659,0.0003665684169066895,-0.00019060043545993723,0.00018194418746469152,-2.1396716179896627e-05,-0.0004013489783279439,0.00012511224868300318,-3.2103611045411624e-05,0.28502961615053524,0.3080688202789592,0.2918861779499962,0.2719254953859121,2.680833498625826,2.8223930529805075,2.706479693473711,2.748755134278733,0.053599228220991786,2.7594030857086183,-9.28570704460144,9.687567098651122,0.00251830001416912,0.005103374223934159,0.0010373920711452534,0.000845691548430581,-0.002226233754980001,0.00033906601294808353,0.0009431036882712432,-0.0009498570603256217,0.0005528458833122994,-0.0007212865282784398,0.4395928776291853,0.501609467800896,0.3475494105458659,0.33575777612021507,2.7663695393161603,2.6883098707784847,2.7299274734573786,2.7640931810189886]
    print(predict_activity(X))