import os

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def plot(data_source='phone', activity='', axis='ax', ylim=(10, 10), zero_mean=False):
    file_paths = []
    for file_name in os.listdir(activity):
        file_path = os.path.join(activity, file_name)

        if os.path.isfile(file_path) and \
            'raw_accelerometer_' + data_source  in file_path and \
            'DS_Store' not in file_path and \
            'lauren' not in file_path and \
            'richsen' not in file_path and \
            'vina' not in file_path:

            file_paths.append(file_path)

    dfs = []
    for file_path in file_paths:
        dfs.append(pd.read_csv(file_path))

    c = ['#000000', '#888888']
    for i, df in enumerate(dfs[2:4]):
        if zero_mean:
            index = [i for i in range(20, len(df[axis]) - 1)]
            y = df[axis].values.tolist()[20:len(df[axis].values) - 1]
            mean_y = np.mean(y)
            y = [item - mean_y for item in y]
        else:
            index = [i for i in range(len(df[axis]))]
            y = df[axis]
            pass

        plt.plot(index, y, c=c[i], linewidth=1.5, label='Subject {}'.format(i))

    title = activity.capitalize() + ' - Raw Accelerometer - '
    title += 'SP' if data_source == 'phone' else 'SW'
    title += ' - Axis '
    title += 'X' if axis == 'ax' else 'Y' if axis == 'ay' else 'Z'
    title += ' - Zero Mean' if zero_mean else ''

    plt.title(title)
    plt.legend()
    plt.ylim(ylim)
    plt.xlabel('Index')
    plt.ylabel('Accelerometer Readings')

    f_name = '{}_{}_{}_{}.png'.format('sp' if data_source == 'phone' else 'sw', activity, axis, 'zero_mean' if zero_mean else '')
    plt.savefig('plots/' + f_name, dpi=180)


if __name__ == '__main__':
    plot(data_source='phone', activity='sitting', axis='ax', ylim=(-5, 5), zero_mean=True)
