import random

def generate_dag(n, edge_prob=0.3, min_weight=1, max_weight=10, due_date_factor=1.5):
    """
    Генерирует случайный ациклический орграф (i->j только если i<j).
    n: число вершин
    edge_prob: вероятность ребра между i и j (i<j)
    min_weight, max_weight: диапазон длительностей задач
    due_date_factor: дедлайн = random.uniform(0.5, due_date_factor) * total_processing_time
    """
    adj = [[] for _ in range(n)]
    weights = [random.randint(min_weight, max_weight) for _ in range(n)]
    
    # генерируем рёбра (i<j)
    for i in range(n-1):
        for j in range(i+1, n):
            if random.random() < edge_prob: # добавляем ребро с вероятностью edge_prob
                adj[i].append(j)   # i -> j, список потомков вершины i
    
    total_time = sum(weights)
    # дедлайны: случайное число от 0.5*total_time до due_date_factor*total_time
    due_dates = [random.uniform(0.5*total_time, due_date_factor*total_time) for _ in range(n)]
    due_dates = [int(d) for d in due_dates]
    
    return adj, weights, due_dates
    """
    Функция возвращает три объекта:
        adj — список смежности (структура графа).
        weights — список длительностей.
        due_dates — список дедлайнов.
        """