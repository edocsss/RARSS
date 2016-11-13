ACTIVITY_TO_INT_MAPPING = {
    'brushing': 0,
    'eating': 1,
    'folding': 2,
    'going_downstairs': 3,
    'going_upstairs': 4,
    'lying': 5,
    'reading': 6,
    'running': 7,
    'sitting': 8,
    'standing': 9,
    'sweeping_the_floor': 10,
    'typing': 11,
    'walking': 12,
    'writing': 13,
    'food_preparation': 14
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