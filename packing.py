# packing.py - Phase 2 (part 2): decide what goes on the van
#
# 0/1 knapsack with dynamic programming.
#   weight   = parcel weight in kg (whole numbers)
#   value    = how much it is worth delivering this trip
#   capacity = how many kg the van can carry
# Time O(n * capacity), space O(n * capacity) because we keep the whole table
# (we need it to work out which parcels were picked).


def knapsack(parcels, capacity):
    n = len(parcels)
    table = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w = parcels[i - 1]["weight"]
        v = parcels[i - 1]["value"]
        for c in range(capacity + 1):
            table[i][c] = table[i - 1][c]          # skip this parcel
            if w <= c:
                take = table[i - 1][c - w] + v     # or take it
                if take > table[i][c]:
                    table[i][c] = take

    # walk back through the table to see which parcels were taken
    chosen = []
    c = capacity
    for i in range(n, 0, -1):
        if table[i][c] != table[i - 1][c]:
            chosen.append(parcels[i - 1])
            c -= parcels[i - 1]["weight"]
    chosen.reverse()

    return table[n][capacity], chosen, table


def show_table(table, parcels, max_cols=None):
    # prints the DP table so it can go in screenshots / the report
    cols = len(table[0]) if max_cols is None else min(max_cols, len(table[0]))
    header = "parcel".ljust(8) + "".join(str(c).rjust(5) for c in range(cols))
    lines = [header, "-" * len(header)]
    for i, row in enumerate(table):
        name = "none" if i == 0 else parcels[i - 1]["id"]
        lines.append(name.ljust(8) + "".join(str(x).rjust(5) for x in row[:cols]))
    return "\n".join(lines)
