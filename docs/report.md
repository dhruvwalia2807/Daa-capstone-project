# Report - Phases 2 to 5

All numbers below come from the files saved in `output/`.

## Phase 2 - sorting and packing

**Sorting.** The 12 sample parcels come out ordered by deadline (P05 at 10:00
first, P08 and P12 at 18:00 last). P07 and P11 share a 12:00 deadline and the same
priority, so the sort is stable and they stay in the order they had in the file
(P07 before P11). P03 and P10 (both 13:00) show the tie-break working: P03 has
priority 4 and P10 has 3, so P03 comes first. See `output/sample_run.txt`.

**Packing, 40 kg van.** The DP table gives a best value of 271. Parcels
loaded: P05, P01, P07, P11, P03, P02, P09, total weight exactly 40 kg. Left for
the next trip: P10, P06, P04, P08, P12.

I also compared against a greedy pick (best value per kg first). Greedy gets
258 for the same van, so the DP result is better by 13. That is the reason
for using DP here.

**Packing, 25 kg van.** Best value 206 with P05, P01, P07, P11, P02. Greedy
happens to reach the same value here, so DP is not always better, only never
worse.

## Phase 3 - route

For the 40 kg load the stops are MG Road, Cyber Hub, DLF Phase 3, Sector 56,
Golf Course Road and Udyog Vihar.

- Delivery order: Depot -> MG Road -> Cyber Hub -> DLF Phase 3 -> Udyog Vihar -> Golf Course Road -> Sector 56 -> Depot
- Roads actually driven (some legs pass through other places): Depot -> MG Road -> Cyber Hub -> DLF Phase 3 -> Udyog Vihar -> Cyber Hub -> Golf Course Road -> Sector 56 -> MG Road -> Depot
- Total length: 33.0 km

For the 25 kg van the route is 28.9 km (`output/small_van_run.txt`).

## Phase 4 - testing and timing

**Correctness** (`output/test_results.txt`, 6 tests, all pass)
- merge sort and insertion sort give the same result as Python's `sorted`
- knapsack matches a brute force search on 20 random small cases
- Dijkstra matches hand-worked distances on a 4-node graph
- the route starts and ends at the depot, visits every stop, and its length matches the hand calculation
- the sample map is fully connected

**Runtime** (`output/benchmark_table.txt`, chart in `output/runtime_chart.png`)

| Step | Smallest input | Largest input |
|---|---|---|
| Merge sort | 0.19 ms (100 parcels) | 6.6 ms (2000 parcels) |
| Insertion sort | 0.34 ms (100 parcels) | 184.8 ms (2000 parcels) |
| Knapsack, 200 kg | 0.50 ms (25 parcels) | 3.4 ms (200 parcels) |
| Dijkstra, one source | 0.16 ms (100 places) | 6.3 ms (3200 places) |
| Nearest neighbour | 0.05 ms (20 stops) | 1.1 ms (160 stops) |

What the numbers show:
- Insertion sort looks fine at 100 parcels but is about 28 times slower than merge sort at 2000. Doubling the input roughly quadruples its time, which is the O(n^2) behaviour.
- Knapsack time grows roughly in step with the number of parcels, because capacity was fixed at 200. It would also grow with capacity.
- Dijkstra grows a little faster than linearly, as expected from the log factor.
- Nearest neighbour grows faster than linearly, matching O(k^2).
- Times change a bit between runs and machines. Only the growth pattern matters.

**Ideas for future improvement**
- Deadlines are only used for sorting. A better planner would check arrival times along the route, and swap stops or leave a parcel for the next trip if a deadline would be missed.
- Nearest neighbour can be improved with 2-opt, which swaps pairs of legs when that makes the route shorter.
- Dijkstra is run once per stop. For many stops, Floyd-Warshall on the places that matter may be easier, or the results could be cached between trips.
- The knapsack table could be cut to a single row if only the best value is needed (the table is only kept so the chosen parcels can be traced back).
- Real road data would need to handle one-way streets, so the map would become a directed graph.

## Phase 5 - result summary

The planner takes a list of parcels and a city map and produces a sorted
parcel list, a loading plan, a delivery order and a distance. On the sample
data a 40 kg van carries 7 of the 12 parcels worth 271 and drives 33.0 km.

Limits: one van, one trip, nearest neighbour is only an approximation (the
best possible route could be shorter), and deadlines are not checked against
arrival times.

To demonstrate: run `python run.py`, then `python run.py --capacity 25`, then
`python run.py --bench`, and show the files in `output/`.
