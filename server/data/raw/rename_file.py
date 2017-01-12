import os


if __name__ == '__main__':
    PERSON_NAME = 'albert'
    ID_LIST = [
        150016
    ]

    for dir_name in os.listdir('.'):
        if os.path.isdir(dir_name):
            for file_name in os.listdir(dir_name):
                id = file_name.split('_')[0]
                try:
                    if int(id) in ID_LIST:
                        new_id = '{}{}'.format(id, PERSON_NAME)
                        new_file_name = '_'.join([new_id] + file_name.split('_')[1:])
                        os.rename(os.path.join(dir_name, file_name), os.path.join(dir_name, new_file_name))

                except:
                    continue