# Phase 1 - Design and Planning

## The problem

A courier van leaves a depot with a weight limit. There are more parcels
waiting than it can carry, each going to a different place, each with a
deadline. We need to decide (a) which parcels go first, (b) which ones fit on
this trip, and (c) in what order to visit the customers so the drive is short.

## Data design

**Parcel** (one dict per parcel, stored in `data/parcels.json`)

| field | meaning |
|---|---|
| id | P01, P02, ... |
| customer | the place it is going to, must exist on the map |
| weight | kg, whole number (needed for the DP table) |
| priority | 1 to 5, 5 = most urgent |
| deadline | hour of the day it must arrive by |
| value | worth of delivering it on this trip |

**Map** (`data/map.json`): places are nodes, roads are undirected edges with a
length in km. In the program it becomes an adjacency dict:
`graph[place] = {neighbour: km, ...}`. An adjacency dict was chosen over a
matrix because a city map has few roads compared to the number of possible
pairs.

## Which algorithm for which job

| Job | Algorithm | Why this one |
|---|---|---|
| Order parcels | Merge sort | Always O(n log n), stable so equal parcels keep their order. Insertion sort is used only as a comparison. |
| Choose parcels for the van | 0/1 knapsack (DP) | A parcel is either loaded or not, and a greedy pick can miss the best combination. DP always finds the best total value. |
| Distances between places | Dijkstra | Road lengths are never negative, so Dijkstra is correct and fast with a heap. |
| Order of customers | Nearest neighbour | The exact tour (TSP) takes factorial time. Nearest neighbour is quick and gives a reasonable route, not a perfect one. |

## How the parts connect

```
parcels.json ──> merge sort ──> knapsack ──> chosen parcels
                                                  │
                                    customers of chosen parcels (stops)
                                                  │
map.json ──> graph ──> Dijkstra from depot + each stop
                                                  │
                                     nearest neighbour tour
                                                  │
                          delivery order + roads driven + total km
```

## Complexity (n = parcels, C = capacity, V = places, E = roads, k = stops)

| Step | Time | Space |
|---|---|---|
| Merge sort | O(n log n) | O(n) |
| Knapsack | O(n * C) | O(n * C) |
| Dijkstra (one source, heap) | O((V + E) log V) | O(V) |
| Dijkstra for depot + k stops | O(k (V + E) log V) | O(k V) |
| Nearest neighbour | O(k^2) | O(k) |

## Assumptions

- One van, one trip, one depot.
- The van returns to the depot at the end.
- Deadlines decide the sorting order only. The route is chosen by distance, so a deadline could still be missed on a long route (see report).
