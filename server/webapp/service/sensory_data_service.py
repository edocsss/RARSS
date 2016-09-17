import os
import webapp.constant.data_path as DATA_PATH

class SensoryDataService:
    def store_smartphone_file(self, activity_type, file_name, file_content):
        file_date, file_content = self.get_file_creation_date(file_content)
        file_name = self.update_file_name_with_date_timestamp(file_name, file_date)
        self.create_activity_directory(activity_type)

        f = open(os.path.join(DATA_PATH.DATA_FOLDER_PATH, activity_type, file_name), 'w')
        f.write(file_content)
        f.close()


    def store_smartwatch_file(self, activity_type, file_name, file_content, file_date):
        file_name = self.update_file_name_with_date_timestamp(file_name, file_date)
        self.create_activity_directory(activity_type)

        f = open(os.path.join(DATA_PATH.DATA_FOLDER_PATH, activity_type, file_name), 'w')
        f.write(file_content)
        f.close()


    def get_file_creation_date(self, file_content):
        first_newline_index = file_content.find('\n')
        return file_content[0:first_newline_index], file_content[first_newline_index + 1:]


    def update_file_name_with_date_timestamp(self, file_name, file_date):
        l = file_name.split('.')
        file_name = l[0]
        file_extension = l[1]

        file_name = file_name + '_' + file_date + '.' + file_extension
        return file_name.replace(' ', '_')


    def create_activity_directory(self, activity_type):
        dir_path = os.path.join(DATA_PATH.DATA_FOLDER_PATH, activity_type)
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)


    def convert_smartwatch_accelerometer_data_to_csv(self, accelerometer_data):
        result_list = []
        for a in accelerometer_data:
            result_list.append('{},{}'.format(a['timestamp'], a['ax'], a['ay'], ['az']))

        return '\n'.join(result_list)


    def convert_smartwatch_gyroscope_data_to_csv(self, gyroscope_data):
        result_list = []
        for g in gyroscope_data:
            result_list.append('{},{}'.format(g['timestamp'], g['gx'], g['gy'], g['gz']))

        return '\n'.join(result_list)


    def convert_smartwatch_light_data_to_csv(self, light_data):
        result_list = []
        for l in light_data:
            result_list.append('{},{}'.format(l['timestamp'], l['light']))

        return '\n'.join(result_list)


    def convert_smartwatch_pressure_data_to_csv(self, pressure_data):
        result_list = []
        for p in pressure_data:
            result_list.append('{},{}'.format(p['timestamp'], p['pressure']))

        return '\n'.join(result_list)


    def convert_smartwatch_magnetic_data_to_csv(self, magnetic_data):
        result_list = []
        for m in magnetic_data:
            result_list.append('{},{},{},{},{}'.format(
                m['timestamp'],
                m['mx'],
                m['my'],
                m['mz'],
                m['mAcc']
            ))

        return '\n'.join(result_list)


    def convert_smartwatch_ultraviolet_data_to_csv(self, ultraviolet_data):
        result_list = []
        for u in ultraviolet_data:
            result_list.append('{},{}'.format(u['timestamp'], u['uv']))

        return '\n'.join(result_list)