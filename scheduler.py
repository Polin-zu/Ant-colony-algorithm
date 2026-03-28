def compute_lmax(schedule, weights, due_dates):
    """
    Вычисляет максимальное опоздание lmax для расписания.
    schedule: список индексов задач в порядке выполнения.
    weights: список длительностей.
    due_dates: список дедлайнов.
    """
    time = 0
    max_lateness = 0
    for task in schedule:
        time += weights[task]
        lateness = max(0, time - due_dates[task])
        if lateness > max_lateness:
            max_lateness = lateness
    return max_lateness