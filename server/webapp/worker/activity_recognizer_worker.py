import time
from datetime import datetime

import pandas as pd

from classifier.real_time_monitoring import activity_predictor
from data_processor import data_preprocessor
from models.data_item import DataItem
from util.logger import web_logger as LOGGER
from webapp.db.activity_history_db import ActivityHistoryDb
from webapp.db.raw_sensory_data_db import RawSensoryDataDb
from webapp.db.work_queue_db import WorkQueueDb
from webapp.handler.client_websocket_handler import ClientWebsocketHandler
import config as CONFIG


class ActivityRecognizerWorker():
    def __init__(self):
        self._work_queue_db = WorkQueueDb()
        self._raw_sensory_data_db = RawSensoryDataDb()
        self._activity_history_db = ActivityHistoryDb()
        self._working = True

    def start(self):
        LOGGER.info('Starting activity recognizer worker..')
        while self._working:
            try:
                self._process_next_uuid()
                time.sleep(1)

            except Exception as e:
                print(e)
                print('Exception during processing the next UUID!')

    def stop(self):
        LOGGER.info('Stopping activity recognizer worker..')
        self._working = False
        LOGGER.info('Activity recognizer worker stopped!')

    def _process_next_uuid(self):
        next_uuid = self._work_queue_db.get_next_uuid()
        if next_uuid is None:
            LOGGER.info('No UUID yet..')
            return

        LOGGER.info('Processing UUID: {}'.format(next_uuid))
        raw_accelerometer_data = self._get_raw_accelerometer_data_by_uuid(next_uuid)
        current_datetime = str(datetime.fromtimestamp(self._get_first_sp_timestamp(raw_accelerometer_data) / 1e3))
        predicted_activity = self._get_activity_prediction(raw_accelerometer_data)

        self._store_activity_history(current_datetime, next_uuid, predicted_activity)
        self._notify_web_client(current_datetime, next_uuid, predicted_activity)


    def _get_raw_accelerometer_data_by_uuid(self, uuid):
        sp_accelerometer_data = self._raw_sensory_data_db.get_sp_raw_accelerometer_data_by_uuid(uuid)
        sw_accelerometer_data = self._raw_sensory_data_db.get_sw_raw_accelerometer_data_by_uuid(uuid)

        return {
            'sp_accelerometer': self._convert_accelerometer_data_to_data_processor_format(uuid, sp_accelerometer_data),
            'sw_accelerometer': self._convert_accelerometer_data_to_data_processor_format(uuid, sw_accelerometer_data)
        }

    def _convert_accelerometer_data_to_data_processor_format(self, uuid, accelerometer_data):
        df = self._convert_accelerometer_data_to_df_and_clean(accelerometer_data)
        data_item = DataItem(uuid, df)
        return [data_item]

    def _convert_accelerometer_data_to_df_and_clean(self, accelerometer_data):
        df = pd.DataFrame(accelerometer_data)
        df['timestamp'] = df['timestamp'].apply(int)
        df.sort_values(by='timestamp', ascending=True, inplace=True)
        df.drop(['_id', 'uuid'], inplace=True, axis=1)
        return df

    def _get_activity_prediction(self, raw_data):
        processed_data = data_preprocessor.preprocess_data_for_real_time_monitoring(raw_data)
        processed_data_arrays = processed_data.values.astype('float64')
        predicted_activity = activity_predictor.predict_activity(processed_data_arrays, model_name=CONFIG.MODEL_NAMES['real_time_monitoring_rf_model'])
        return predicted_activity

    def _get_first_sp_timestamp(self, raw_accelerometer_data):
        sp_accelerometer_df = raw_accelerometer_data['sp_accelerometer'][0].dataframe
        first_timestamp = sp_accelerometer_df['timestamp'][0]
        return first_timestamp

    def _store_activity_history(self, current_datetime, next_uuid, predicted_activity):
        activity_history = {
            'uuid': next_uuid,
            'activity': predicted_activity,
            'datetime': current_datetime
        }

        self._activity_history_db.insert_activity_history(activity_history)

    def _notify_web_client(self, current_datetime, next_uuid, predicted_activity):
        message = {
            'uuid': next_uuid,
            'activity': predicted_activity,
            'datetime': current_datetime
        }

        ClientWebsocketHandler.broadcast(message)


if __name__ == '__main__':
    worker = ActivityRecognizerWorker()
    worker._process_next_uuid()
