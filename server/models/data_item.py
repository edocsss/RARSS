"""
Wrapper around the sensory data.
This includes the sensory data File ID which is very helpful for handling data pre-processing of multiple CSV raw data
files for the same subject.
"""


class DataItem:
    def __init__(self, file_id, dataframe):
        self.file_id = file_id
        self.dataframe = dataframe

    def __str__(self):
        return '{} \n {}'.format(self.file_id, self.dataframe)

    def __repr__(self):
        return '{} \n {}'.format(self.file_id, self.dataframe)