# benchmark.py - Phase 4: how fast is each step as the input grows?
#
# Random data uses a fixed seed so the numbers are repeatable.
import random
import time

from sorting import merge_sort, insertion_sort
from packing import knapsack
from routing import dijkstra, nearest_neighbour


def fake_parcels(n, rng):
    return [
        {"id": "X%d" % i, "customer": "N0", "weight": rng.randint(1, 15),
         "priority": rng.randint(1, 5), "deadline": rng.randint(9, 20),
         "value": rng.randint(5, 60)}
        for i in range(n)
    ]


def fake_graph(n, rng):
    # a chain keeps everything connected, then extra roads are thrown in
    graph = {"N%d" % i: {} for i in range(n)}
    nodes = list(graph)
    rng.shuffle(nodes)
    for a, b in zip(nodes, nodes[1:]):
        km = rng.randint(1, 20)
        graph[a][b] = km
        graph[b][a] = km
    for _ in range(n * 3):
        a, b = rng.sample(nodes, 2)
        km = rng.randint(1, 20)
        graph[a][b] = km
        graph[b][a] = km
    return graph


def timed(fn, *args):
    start = time.perf_counter()
    fn(*args)
    return (time.perf_counter() - start) * 1000      # milliseconds


def run_benchmarks():
    rng = random.Random(7)
    results = {}

    sizes = [100, 500, 1000, 2000]
    results["Sorting"] = {
        "sizes": sizes,
        "Merge sort": [timed(merge_sort, fake_parcels(n, rng)) for n in sizes],
        "Insertion sort": [timed(insertion_sort, fake_parcels(n, rng)) for n in sizes],
    }

    sizes = [25, 50, 100, 200]
    results["Knapsack (capacity 200 kg)"] = {
        "sizes": sizes,
        "Knapsack DP": [timed(knapsack, fake_parcels(n, rng), 200) for n in sizes],
    }

    sizes = [100, 400, 1600, 3200]
    results["Dijkstra (one source)"] = {
        "sizes": sizes,
        "Dijkstra": [timed(dijkstra, fake_graph(n, rng), "N0") for n in sizes],
    }

    sizes = [20, 40, 80, 160]
    nn_times = []
    for n in sizes:
        g = fake_graph(n, rng)
        table = {node: dijkstra(g, node)[0] for node in g}
        nn_times.append(timed(nearest_neighbour, table, "N0", [s for s in g if s != "N0"]))
    results["Nearest neighbour (stops)"] = {"sizes": sizes, "Nearest neighbour": nn_times}

    return results


def print_table(results):
    for step, data in results.items():
        names = [k for k in data if k != "sizes"]
        print("\n" + step)
        print("  size".ljust(10) + "".join(n.rjust(20) for n in names))
        for i, size in enumerate(data["sizes"]):
            print(("  %d" % size).ljust(10) + "".join(("%.3f ms" % data[n][i]).rjust(20) for n in names))


def save_chart(results, path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed, skipping the chart (pip install matplotlib)")
        return False

    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    for ax, (step, data) in zip(axes.flat, results.items()):
        for name, times in data.items():
            if name != "sizes":
                ax.plot(data["sizes"], times, marker="o", label=name)
        ax.set_title(step)
        ax.set_xlabel("input size")
        ax.set_ylabel("time (ms)")
        ax.grid(alpha=0.3)
        ax.legend()
    fig.suptitle("Mini-Courier Planner - runtime of each step")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    return True
