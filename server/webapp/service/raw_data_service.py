import config as CONFIG
from data_processor.util import raw_data_reader


"""
Provides services related to raw data as needed by the AngularJS web application.
"""


class RawDataService():
    def get_raw_data_by_activity_and_source(self, activity_type, data_source, data_subject):
        if data_source == 'smartphone':
            raw_data = raw_data_reader.read_smartphone_raw_data(activity_type, data_subject, CONFIG.SENSOR_SOURCES['sp_full'])
        else:
            raw_data = raw_data_reader.read_smartwatch_raw_data(activity_type, data_subject, CONFIG.SENSOR_SOURCES['sw_full'])

        result = self._convert_raw_data_format_to_dict_by_file_id(raw_data)
        return result

    # Convert the dictionary format organized by sensor type to dictionary format organized by the File ID
    def _convert_raw_data_format_to_dict_by_file_id(self, raw_data):
        result = {}
        for k, v in raw_data.items():
            for i in range(len(v)):
                file_id = v[i].file_id
                values = v[i].dataframe.values.tolist()

                if file_id in result:
                    result[file_id][k] = values
                else:
                    result[file_id] = {
                        k: values
                    }

        return result