ACTIVITY_TO_INT_MAPPING = {
        'lying': 0,
        'sitting': 1,
        'standing': 2,
        'walking': 3,
        'running': 4,
        'cycling': 5,
        'nordic_walking': 6,
        'going_upstairs': 7,
        'going_downstairs': 8,
        'vacuum_cleaning': 9,
        'ironing': 10,
        'rope_jumping': 11
}

INT_TO_ACTIVITY_MAPPING = {v: k for k, v in ACTIVITY_TO_INT_MAPPING.items()}

INT_TO_BINARY_MAPPING = {
    '0': '100000000000000',
    '1': '010000000000000',
    '2': '001000000000000',
    '3': '000100000000000',
    '4': '000010000000000',
    '5': '000001000000000',
    '6': '000000100000000',
    '7': '000000010000000',
    '8': '000000001000000',
    '9': '000000000100000',
    '10': '000000000010000',
    '11': '000000000001000',
    '12': '000000000000100',
    '13': '000000000000010',
    '14': '000000000000001'
}

BINARY_TO_INT_MAPPING = {v: k for k, v in INT_TO_BINARY_MAPPING.items()}