# run.py - start here:  python run.py
#
#   python run.py                 plan a trip with the sample data
#   python run.py --capacity 25   same, but with a smaller van
#   python run.py --bench         run the timing tests and save a chart
import argparse
import os
import time

from sorting import merge_sort
from packing import knapsack, show_table
from routing import load_map, plan_route
from benchmark import run_benchmarks, print_table, save_chart
import json

HERE = os.path.dirname(os.path.abspath(__file__))


def line(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def plan_trip(parcels_file, map_file, capacity):
    with open(parcels_file) as f:
        parcels = json.load(f)
    depot, graph = load_map(map_file)
    times = {}

    line("STEP 1: parcels sorted by deadline, then priority")
    t = time.perf_counter()
    ordered = merge_sort(parcels)
    times["sorting"] = time.perf_counter() - t
    print("%-5s %-18s %6s %5s %9s %6s" % ("id", "customer", "kg", "prio", "deadline", "value"))
    for p in ordered:
        print("%-5s %-18s %6d %5d %7d:00 %6d" % (p["id"], p["customer"], p["weight"],
                                                 p["priority"], p["deadline"], p["value"]))

    line("STEP 2: what fits in a %d kg van (knapsack DP)" % capacity)
    t = time.perf_counter()
    best, chosen, table = knapsack(ordered, capacity)
    times["knapsack"] = time.perf_counter() - t
    print("DP table (first 15 columns):")
    print(show_table(table, ordered, max_cols=15))
    print("\nBest total value: %d" % best)
    print("Loaded: " + ", ".join(p["id"] for p in chosen))
    print("Total weight: %d / %d kg" % (sum(p["weight"] for p in chosen), capacity))
    chosen_ids = [p["id"] for p in chosen]
    left_behind = [p["id"] for p in ordered if p["id"] not in chosen_ids]
    print("Left for the next trip: " + (", ".join(left_behind) or "nothing"))

    line("STEP 3: route")
    stops = []
    for p in chosen:
        if p["customer"] not in stops:
            stops.append(p["customer"])
    t = time.perf_counter()
    order, full_path, total, dist_table = plan_route(graph, depot, stops)
    times["routing"] = time.perf_counter() - t

    print("Shortest distances from the depot (Dijkstra):")
    for s in stops:
        print("  %-18s %5.1f km" % (s, dist_table[depot][s]))
    print("\nDelivery order (nearest neighbour):")
    print("  " + " -> ".join(order))
    print("\nRoads actually driven:")
    print("  " + " -> ".join(full_path))
    print("\nTotal route length: %.1f km" % total)

    line("TIMING")
    for name, secs in times.items():
        print("  %-10s %.4f ms" % (name, secs * 1000))


def main():
    ap = argparse.ArgumentParser(description="Mini-Courier Planner")
    ap.add_argument("--parcels", default=os.path.join(HERE, "data", "parcels.json"))
    ap.add_argument("--map", default=os.path.join(HERE, "data", "map.json"))
    ap.add_argument("--capacity", type=int, default=40, help="van capacity in kg (default 40)")
    ap.add_argument("--bench", action="store_true", help="run timing tests and save a chart")
    args = ap.parse_args()

    if args.bench:
        results = run_benchmarks()
        print_table(results)
        out = os.path.join(HERE, "output", "runtime_chart.png")
        if save_chart(results, out):
            print("\nChart saved to", out)
    else:
        plan_trip(args.parcels, args.map, args.capacity)


if __name__ == "__main__":
    main()
