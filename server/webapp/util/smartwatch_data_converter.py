def convert_smartwatch_accelerometer_data_to_csv(accelerometer_data):
    result_list = []
    result_list.append('{},{},{},{}'.format('timestamp', 'ax', 'ay', 'az'))
    print(accelerometer_data)

    for a in accelerometer_data:
        result_list.append('{},{},{},{}'.format(a['timestamp'], a['ax'], a['ay'], a['az']))

    return '\n'.join(result_list)


def convert_smartwatch_gyroscope_data_to_csv(gyroscope_data):
    result_list = []
    result_list.append('{},{},{},{}'.format('timestamp', 'gx', 'gy', 'gz'))

    for g in gyroscope_data:
        result_list.append('{},{},{},{}'.format(g['timestamp'], g['gx'], g['gy'], g['gz']))

    return '\n'.join(result_list)


def convert_smartwatch_light_data_to_csv(light_data):
    result_list = []
    result_list.append('{},{}'.format('timestamp', 'light'))

    for l in light_data:
        result_list.append('{},{}'.format(l['timestamp'], l['light']))

    return '\n'.join(result_list)


def convert_smartwatch_pressure_data_to_csv(pressure_data):
    result_list = []
    result_list.append('{},{}'.format('timestamp', 'pressure'))

    for p in pressure_data:
        result_list.append('{},{}'.format(p['timestamp'], p['pressure']))

    return '\n'.join(result_list)


def convert_smartwatch_magnetic_data_to_csv(magnetic_data):
    result_list = []
    result_list.append('{},{},{},{},{}'.format('timestamp', 'mx', 'my', 'mz', 'mAc'))

    for m in magnetic_data:
        result_list.append('{},{},{},{},{}'.format(
            m['timestamp'],
            m['mx'],
            m['my'],
            m['mz'],
            m['mAcc']
        ))

    return '\n'.join(result_list)


def convert_smartwatch_ultraviolet_data_to_csv(ultraviolet_data):
    result_list = []
    result_list.append('{},{}'.format('timestamp', 'uv'))

    for u in ultraviolet_data:
        result_list.append('{},{}'.format(u['timestamp'], u['uv']))

    return '\n'.join(result_list)