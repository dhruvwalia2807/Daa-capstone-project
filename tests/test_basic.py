# Run with:  python -m unittest discover tests
import itertools
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sorting import merge_sort, insertion_sort, parcel_key
from packing import knapsack
from routing import dijkstra, nearest_neighbour, plan_route, load_map


def random_parcels(n, rng):
    return [{"id": "T%d" % i, "weight": rng.randint(1, 10), "value": rng.randint(1, 40),
             "priority": rng.randint(1, 5), "deadline": rng.randint(8, 20)} for i in range(n)]


class SortingTests(unittest.TestCase):
    def test_matches_python_sorted(self):
        rng = random.Random(1)
        data = random_parcels(200, rng)
        self.assertEqual(merge_sort(data), sorted(data, key=parcel_key))
        self.assertEqual(insertion_sort(data), sorted(data, key=parcel_key))

    def test_empty_and_single(self):
        self.assertEqual(merge_sort([]), [])
        one = [{"deadline": 9, "priority": 1}]
        self.assertEqual(merge_sort(one), one)


class KnapsackTests(unittest.TestCase):
    def test_against_brute_force(self):
        rng = random.Random(2)
        for _ in range(20):
            items = random_parcels(8, rng)
            cap = rng.randint(5, 35)
            best, chosen, _ = knapsack(items, cap)

            brute = 0
            for r in range(len(items) + 1):
                for combo in itertools.combinations(items, r):
                    if sum(p["weight"] for p in combo) <= cap:
                        brute = max(brute, sum(p["value"] for p in combo))

            self.assertEqual(best, brute)
            self.assertLessEqual(sum(p["weight"] for p in chosen), cap)
            self.assertEqual(sum(p["value"] for p in chosen), best)


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.graph = {
            "A": {"B": 4, "C": 1},
            "B": {"A": 4, "C": 2, "D": 5},
            "C": {"A": 1, "B": 2, "D": 8},
            "D": {"B": 5, "C": 8},
        }

    def test_dijkstra(self):
        dist, _ = dijkstra(self.graph, "A")
        self.assertEqual(dist, {"A": 0, "B": 3, "C": 1, "D": 8})

    def test_route_visits_everything_and_returns(self):
        order, full_path, total, _ = plan_route(self.graph, "A", ["B", "D"])
        self.assertEqual(order[0], "A")
        self.assertEqual(order[-1], "A")
        self.assertEqual(set(order), {"A", "B", "D"})
        self.assertEqual(total, 3 + 5 + 8)       # A-B, B-D, D-A (via C)

    def test_sample_map_is_connected(self):
        here = os.path.dirname(__file__)
        depot, graph = load_map(os.path.join(here, "..", "data", "map.json"))
        dist, _ = dijkstra(graph, depot)
        self.assertTrue(all(d < float("inf") for d in dist.values()))


if __name__ == "__main__":
    unittest.main()
