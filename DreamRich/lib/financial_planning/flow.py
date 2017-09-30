def generic_flow(array_change, duration, total):
    data = []

    for index in range(duration):
        total += array_change[index]
        data.append(total)

    return data
