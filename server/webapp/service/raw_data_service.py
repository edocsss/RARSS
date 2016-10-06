from util import raw_data_reader


class RawDataService():
    def get_raw_data_by_activity_and_source(self, activity_type, source):
        if source == 'smartphone':
            data = raw_data_reader.read_smartphone_raw_data(activity_type)
        else:
            data = raw_data_reader.read_smartwatch_raw_data(activity_type)

        for k, v in data.items():
            data[k] = v.values.tolist()

        return data