import pandas as pd


file_names = ['subject10{}.csv'.format(i) for i in range(1, 10)]
activity_names = {
    1: 'lying',
    2: 'sitting',
    3: 'standing',
    4: 'walking',
    5: 'running',
    6: 'cycling',
    7: 'nordic_walking',
    12: 'going_upstairs',
    13: 'going_downstairs',
    16: 'vacuum_cleaning',
    17: 'ironing',
    24: 'rope_jumping'
}


for file_name in file_names:
    df = pd.read_csv(file_name)
    df = df[df.activity != 0]
    df['activity'] = df['activity'].apply(lambda id: activity_names[id])
    df.to_csv(file_name)