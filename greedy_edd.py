from scheduler import compute_lmax

def greedy_edd(adj, weights, due_dates):
    
    # Жадный алгоритм строит расписание, на каждом шаге выбирая доступную задачу с наименьшим дедлайном.

    n = len(adj)
    in_degree = [0] * n # in_degree[i] - число входящих ребер для задачи i
    for i in range(n):
        for j in adj[i]:
            in_degree[j] += 1
    
    schedule = []
    available = [i for i in range(n) if in_degree[i] == 0] #список задач, которые могут быть выполнены на текущем шаге
    # Это те задачи, у которых in_degree равен 0 (нет невыполненных предшественников)
    
    while available:
        # выбираем задачу с минимальным дедлайном
        task = min(available, key=lambda x: due_dates[x])
        schedule.append(task)
        available.remove(task)
        
        # обновляем доступные задачи
        for succ in adj[task]:
            in_degree[succ] -= 1
            if in_degree[succ] == 0:
                available.append(succ)
    
    lmax = compute_lmax(schedule, weights, due_dates)
    return schedule, lmax