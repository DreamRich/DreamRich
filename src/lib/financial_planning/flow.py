def generic_flow(array_change, duration, total):
    data = []

    for index in range(duration):
        total += array_change[index]
        data.append(total)

    return data


def create_array_change_annual(changes, duration, init_year):
    data = [0] * duration
    for unit_change in changes:
        index_change = unit_change.year - init_year
        data[index_change] += unit_change.annual_value

    return data
