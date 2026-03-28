from graph import generate_dag
from greedy_edd import greedy_edd
from ant_colony import AntColony
from visualize import plot_convergence, compare_bar
import random

def main():
    # параметры
    n = 15
    edge_prob = 0.3
    due_date_factor = 1.0   # можно регулировать срочность дедлайнов
    
    adj, weights, due_dates = generate_dag(n, edge_prob, min_weight=1, max_weight=8, due_date_factor=due_date_factor)
    
    # жадный алгоритм
    greedy_sched, greedy_lmax = greedy_edd(adj, weights, due_dates)
    print("Greedy L_max:", greedy_lmax)
    
    # муравьиный алгоритм
    ac = AntColony(adj, weights, due_dates, n_ants=20, alpha=0.5, beta=0.8, rho=0.3, tau0=1.0, iterations=50)
    ant_sched, ant_lmax, history = ac.run()
    print("Ant Colony L_max:", ant_lmax)

    if greedy_lmax == 0:
        improvement = 0.0
        print("Greedy algorithm already found optimal schedule (L_max = 0)")
    else:
        improvement = (greedy_lmax - ant_lmax) / greedy_lmax * 100
        print(f"Improvement: {improvement:.2f}%")
   
    
    # визуализация
    plot_convergence(history)
    compare_bar(greedy_lmax, ant_lmax)

if __name__ == "__main__":
    main()