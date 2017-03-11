import os

import matplotlib.pyplot as plt
import pandas as pd

'''Typing vs Writing'''
'''Prove that SP Typing ~ SP Writing'''
'''Prove that SW Typing != SW Writing'''

def plot(data_source='phone', activity='', axis='ax', ylim=(10, 10)):
    file_paths = []
    for file_name in os.listdir(activity):
        file_path = os.path.join(activity, file_name)

        if os.path.isfile(file_path) and \
            'raw_barometer_' + data_source  in file_path and \
            'DS_Store' not in file_path and \
            'lauren' not in file_path and \
            'richsen' not in file_path and \
            'vina' not in file_path:

            file_paths.append(file_path)

    dfs = []
    for file_path in file_paths:
        dfs.append(pd.read_csv(file_path))

    for df in dfs:
        index = [i for i in range(len(df[axis]))]
        plt.plot(index, df[axis], linewidth=0.5)

    title = activity.capitalize() + ' - Raw Accelerometer - '
    title += 'SP' if data_source == 'phone' else 'SW'
    title += ' - Axis '
    title += 'X' if axis == 'ax' else 'Y' if axis == 'ay' else 'Z'

    plt.title(title)
    plt.ylim(ylim)
    plt.xlabel('Index')
    plt.ylabel('Accelerometer Readings')

    f_name = '{}_{}_{}.png'.format('sp' if data_source == 'phone' else 'sw', activity, axis)
    plt.savefig('plots/' + f_name, dpi=180)


if __name__ == '__main__':
    plot(data_source='phone', activity='going_upstairs', axis='pressure', ylim=None)
