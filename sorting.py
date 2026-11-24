# sorting.py - Phase 2 (part 1): put parcels in delivery order
#
# Parcels are ordered by deadline (earliest first). If two parcels have the
# same deadline, the one with the higher priority goes first.
# I use merge sort because it is stable and always O(n log n).
# insertion_sort is only here so benchmark.py has something to compare against.


def parcel_key(parcel):
    return (parcel["deadline"], -parcel["priority"])


def merge_sort(items, key=parcel_key):
    if len(items) <= 1:
        return list(items)

    mid = len(items) // 2
    left = merge_sort(items[:mid], key)
    right = merge_sort(items[mid:], key)

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def insertion_sort(items, key=parcel_key):
    arr = list(items)
    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        while j >= 0 and key(arr[j]) > key(current):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
    return arr
