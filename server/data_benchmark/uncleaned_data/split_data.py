import pandas as pd


file_names = ['subject10{}.csv'.format(i) for i in range(6, 7)]
subject_id = 31234


for file_name in file_names:
    print(file_name)
    df = pd.read_csv(file_name)
    df.drop('Unnamed: 0', inplace=True, axis=1)
    activities = df['activity'].unique()

    subject_id += 1
    subject_name = file_name.split('.')[0]

    for a in activities:
        print(a)
        related_data = df[df.activity == a]
        data = []

        prev_row = None
        first = True

        for j, row in related_data.iterrows():
            row['timestamp'] *= 1000
            if first:
                prev_row = row
                first = False
                continue

            for c in related_data.columns:
                if c != 'timestamp' and c != 'activity' and pd.isnull(row[c]):
                    if prev_row[c] is not None:
                        row[c] = prev_row[c]
                    else:
                        print(prev_row)

            prev_row = row
            data.append(row.values)

        related_data = pd.DataFrame(columns=related_data.columns, data=data)
        sp_df = related_data[['timestamp', 'c5', 'c6', 'c7']].rename(columns={
            'c5': 'ax',
            'c6': 'ay',
            'c7': 'az'
        })

        sw_df = related_data[['timestamp', 'h5', 'h6', 'h7']].rename(columns={
            'h5': 'ax',
            'h6': 'ay',
            'h7': 'az'
        })

        sp_df = sp_df.astype(float)
        sw_df = sw_df.astype(float)

        sp_df.to_csv('raw/{}/{}{}_raw_accelerometer_phone.csv'.format(a, subject_id, subject_name), index=False)
        sw_df.to_csv('raw/{}/{}{}_raw_accelerometer_watch.csv'.format(a, subject_id, subject_name), index=False)