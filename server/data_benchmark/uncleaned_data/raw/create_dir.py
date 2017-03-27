import os


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


for k, v in activity_names.items():
    os.mkdir(v)