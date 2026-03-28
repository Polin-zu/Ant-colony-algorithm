import random
import numpy as np
from scheduler import compute_lmax

class AntColony:
    def __init__(self, adj, weights, due_dates, n_ants=10, alpha=1.0, beta=1.0, rho=0.1, tau0=0.1, iterations=50):
        self.adj = adj
        self.n = len(adj)
        self.weights = weights
        self.due_dates = due_dates
        self.n_ants = n_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.tau0 = tau0
        self.iterations = iterations
        
        # феромонная матрица: tau[i][j] — выгодность i раньше j
        self.tau = np.full((self.n, self.n), tau0)
        self.best_schedule = None
        self.best_lmax = float('inf')
        self.history = []   # для графика сходимости

    def _get_available_tasks(self, scheduled):
        """Возвращает список задач, все предки которых уже в расписании."""
        in_degree = [0] * self.n
        for i in range(self.n):
            for j in self.adj[i]:
                in_degree[j] += 1
        # вычитаем уже запланированные
        for task in scheduled:
            for succ in self.adj[task]:
                in_degree[succ] -= 1
        available = [i for i in range(self.n) if i not in scheduled and in_degree[i] == 0]
        return available

    def _build_schedule(self):
        """Строит расписание одним муравьём."""
        schedule = []
        while len(schedule) < self.n:
            available = self._get_available_tasks(schedule)
            # вычисляем вероятности выбора
            probs = []
            for v in available:
                # произведение феромонов от всех уже запланированных задач к v
                c = 1.0
                for u in schedule:
                    c *= self.tau[u][v]
                # эвристика: обратная величина дедлайна (чем меньше дедлайн, тем лучше)
                eta = 1.0 / (self.due_dates[v] + 1e-6)
                probs.append((c ** self.alpha) * (eta ** self.beta))
            # нормализация
            total = sum(probs)
            if total == 0:
                # если все нули, выбираем случайно
                v = random.choice(available)
            else:
                #создаем список нормализованных вероятностей
                probs = [p / total for p in probs]
                #номер задачи, выбранный в соответствии с вычисленными вероятностями
                v = random.choices(available, weights=probs)[0]
            schedule.append(v)
        return schedule

    def _global_update(self, best_schedule, best_lmax):
        """Глобальное обновление феромона на основе лучшего расписания."""
        # испарение
        self.tau *= (1 - self.rho)
        # добавление феромона
        delta = 1.0 / (best_lmax + 1)   # +1 для защиты от деления на 0
        for i in range(self.n):
            for j in range(self.n):
                if i == j:
                    continue
                # если в лучшем расписании i идёт раньше j
                if best_schedule.index(i) < best_schedule.index(j):
                    self.tau[i][j] += delta

    def run(self):
        """Запуск муравьиного алгоритма."""
        self.history = []
        for it in range(self.iterations):
            schedules = []
            lmax_values = []
            # Каждый муравей строит своё расписание
            for _ in range(self.n_ants):
                sched = self._build_schedule()
                lmax = compute_lmax(sched, self.weights, self.due_dates)
                schedules.append(sched)
                lmax_values.append(lmax)
            
            # лучшее решение в итерации
            best_lmax_iter = min(lmax_values)
            best_idx = lmax_values.index(best_lmax_iter)
            best_sched_iter = schedules[best_idx]
            
            # глобальное обновление
            if best_lmax_iter < self.best_lmax:
                self.best_lmax = best_lmax_iter
                self.best_schedule = best_sched_iter[:] #копия
            
            self._global_update(self.best_schedule, self.best_lmax)
            self.history.append(self.best_lmax)
        
        return self.best_schedule, self.best_lmax, self.history