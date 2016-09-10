import os

class SensoryDataService:
    def store_file(self, activity_type, file_name, file_content):
        file_date, file_content = self.get_file_creation_date(file_content)
        file_name = self.update_file_name_with_date_timestamp(file_name, file_date)

        f = open(os.path.join(os.getcwd(), 'data', activity_type, file_name), 'w')
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