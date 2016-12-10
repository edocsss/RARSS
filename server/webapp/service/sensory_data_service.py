import os
import config as CONFIG
from webapp.util import smartwatch_data_converter

class SensoryDataService:
    def handle_smartphone_sensory_data(self, activity_type, sensory_data, file_id):
        accelerometer_data = sensory_data['accelerometer']
        barometer_data = sensory_data['barometer']
        gravity_data = sensory_data['gravity']
        gyroscope_data = sensory_data['gyroscope']
        linear_accelerometer_data = sensory_data['linearAccelerometer']
        magnetic_data = sensory_data['magnetic']

        self._create_raw_data_directory()
        self._create_raw_activity_directory(activity_type)

        self._store_smartphone_file(activity_type, file_id + '_' + CONFIG.RAW_DATA_RESULT['sp_accelerometer'], accelerometer_data)
        self._store_smartphone_file(activity_type, file_id + '_' + CONFIG.RAW_DATA_RESULT['sp_barometer'], barometer_data)
        self._store_smartphone_file(activity_type, file_id + '_' + CONFIG.RAW_DATA_RESULT['sp_gravity'], gravity_data)
        self._store_smartphone_file(activity_type, file_id + '_' + CONFIG.RAW_DATA_RESULT['sp_gyroscope'], gyroscope_data)
        self._store_smartphone_file(activity_type, file_id + '_' + CONFIG.RAW_DATA_RESULT['sp_linear_accelerometer'], linear_accelerometer_data)
        self._store_smartphone_file(activity_type, file_id + '_' + CONFIG.RAW_DATA_RESULT['sp_magnetic'], magnetic_data)


    def handle_smartwatch_sensory_data(self, activity_type, sensory_data, file_id):
        accelerometer_data = smartwatch_data_converter.convert_smartwatch_accelerometer_data_to_csv(sensory_data['accelerometer']['data'])
        gyroscope_data = smartwatch_data_converter.convert_smartwatch_gyroscope_data_to_csv(sensory_data['gyroscope']['data'])
        light_data = smartwatch_data_converter.convert_smartwatch_light_data_to_csv(sensory_data['light']['data'])
        pressure_data = smartwatch_data_converter.convert_smartwatch_pressure_data_to_csv(sensory_data['pressure']['data'])
        magnetic_data = smartwatch_data_converter.convert_smartwatch_magnetic_data_to_csv(sensory_data['magnetic']['data'])
        uv_data = smartwatch_data_converter.convert_smartwatch_ultraviolet_data_to_csv(sensory_data['uv']['data'])

        self._create_raw_data_directory()
        self._create_raw_activity_directory(activity_type)

        self._store_smartwatch_file(activity_type, file_id + '_' + CONFIG.RAW_DATA_RESULT['sw_accelerometer'], accelerometer_data)
        self._store_smartwatch_file(activity_type, file_id + '_' + CONFIG.RAW_DATA_RESULT['sw_gyroscope'], gyroscope_data)
        self._store_smartwatch_file(activity_type, file_id + '_' + CONFIG.RAW_DATA_RESULT['sw_light'], light_data)
        self._store_smartwatch_file(activity_type, file_id + '_' + CONFIG.RAW_DATA_RESULT['sw_pressure'], pressure_data)
        self._store_smartwatch_file(activity_type, file_id + '_' + CONFIG.RAW_DATA_RESULT['sw_magnetic'], magnetic_data)
        self._store_smartwatch_file(activity_type, file_id + '_' + CONFIG.RAW_DATA_RESULT['sw_ultraviolet'], uv_data)


    def _store_smartphone_file(self, activity_type, file_name, file_content):
        f = open(os.path.join(CONFIG.RAW_DATA_DIR, activity_type, file_name), 'w')
        f.write(file_content)
        f.close()


    def _store_smartwatch_file(self, activity_type, file_name, file_content):
        f = open(os.path.join(CONFIG.RAW_DATA_DIR, activity_type, file_name), 'w')
        f.write(file_content)
        f.close()


    def _create_raw_data_directory(self):
        dir_path = os.path.join(CONFIG.RAW_DATA_DIR)
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)


    def _create_raw_activity_directory(self, activity_type):
        dir_path = os.path.join(CONFIG.RAW_DATA_DIR, activity_type)
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)