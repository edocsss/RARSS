import pandas as pd


file_names = ['subject10{}.csv'.format(i) for i in range(1, 10)]
col_names = [
    'timestamp', 'activity', 'hr'
] + ['h{}'.format(i) for i in range(1, 18)] + ['c{}'.format(i) for i in range(1, 18)] + ['a{}'.format(i) for i in range(1, 18)]

filter_col_names = ['timestamp', 'activity', 'h5', 'h6', 'h7', 'c5', 'c6', 'c7']
for file_name in file_names:
    print(file_name)
    df = pd.read_csv(file_name, names=col_names)
    df = df[filter_col_names]
    df.to_csv(file_name)