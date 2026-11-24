# routing.py - Phase 3: the map and the route
#
# The map is an undirected weighted graph stored as a dict:
#   graph["Cyber Hub"] = {"MG Road": 3.1, "Udyog Vihar": 2.4, ...}
# Dijkstra gives shortest distances from one point, and nearest neighbour
# uses those distances to build one tour that starts and ends at the depot.
import heapq
import json


def load_map(path):
    with open(path) as f:
        data = json.load(f)
    graph = {}
    for a, b, km in data["roads"]:
        graph.setdefault(a, {})[b] = km
        graph.setdefault(b, {})[a] = km
    return data["depot"], graph


def dijkstra(graph, start):
    dist = {node: float("inf") for node in graph}
    came_from = {}
    dist[start] = 0
    heap = [(0, start)]

    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue                      # old entry, a shorter way was already found
        for nxt, km in graph[node].items():
            new_d = d + km
            if new_d < dist[nxt]:
                dist[nxt] = new_d
                came_from[nxt] = node
                heapq.heappush(heap, (new_d, nxt))

    return dist, came_from


def path_to(came_from, start, end):
    path = [end]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    path.reverse()
    return path


def nearest_neighbour(dist_table, depot, stops):
    # dist_table[a][b] = shortest distance from a to b
    order = [depot]
    left = set(stops)
    total = 0
    here = depot
    while left:
        nxt = min(left, key=lambda s: dist_table[here][s])
        total += dist_table[here][nxt]
        order.append(nxt)
        left.remove(nxt)
        here = nxt
    total += dist_table[here][depot]
    order.append(depot)
    return order, total


def plan_route(graph, depot, stops):
    # run Dijkstra from the depot and from every stop
    points = [depot] + [s for s in stops if s != depot]
    dist_table = {}
    parents = {}
    for p in points:
        dist_table[p], parents[p] = dijkstra(graph, p)

    order, total = nearest_neighbour(dist_table, depot, [s for s in stops if s != depot])

    # expand each leg into the real roads driven
    full_path = [depot]
    for a, b in zip(order, order[1:]):
        leg = path_to(parents[a], a, b)
        full_path.extend(leg[1:])
    return order, full_path, total, dist_table
