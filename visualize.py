import matplotlib.pyplot as plt

def plot_convergence(history, title="Convergence of Ant Colony"):
    plt.figure()
    plt.plot(history, marker='o', linestyle='-', markersize=2)
    plt.xlabel("Iteration")
    plt.ylabel("Best L_max")
    plt.title(title)
    plt.grid(True)
    plt.show()

def compare_bar(greedy_lmax, ant_lmax):
    plt.figure()
    plt.bar(["Greedy EDD", "Ant Colony"], [greedy_lmax, ant_lmax], color=['blue', 'green'])
    plt.ylabel("L_max")
    plt.title("Comparison of Scheduling Algorithms")
    for i, v in enumerate([greedy_lmax, ant_lmax]):
        plt.text(i, v + 0.5, str(v), ha='center')
    plt.show()