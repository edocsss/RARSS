class DataItem:
    def __init__(self, file_name, dataframe):
        self.file_id = file_name.split('_')[0]
        self.dataframe = dataframe


    def __str__(self):
        return '{} \n {}'.format(self.file_id, self.dataframe)


    def __repr__(self):
        return '{} \n {}'.format(self.file_id, self.dataframe)