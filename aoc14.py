from collections import defaultdict, deque
from functools import reduce
from itertools import permutations, product
import math


def toposort2(data):
    for k, v in data.items():
        v.discard(k)  # Ignore self dependencies
    extra_items_in_deps = reduce(set.union, data.values()) - set(data.keys())
    data.update({item: set() for item in extra_items_in_deps})
    while True:
        ordered = set(item for item, dep in data.items() if not dep)
        if not ordered:
            break
        yield list(sorted(ordered))
        data = {
            item: (dep - ordered)
            for item, dep in data.items() if item not in ordered
        }
    assert not data, "A cyclic dependency exists amongst %r" % data


def calculate_ore_requirement(amt, ordering, reactions, reactions_amt):
    current_resources = defaultdict(int)
    current_resources['FUEL'] = amt
    for step_resources in ordering:
        for resource in step_resources:
            amt = current_resources[resource]
            if resource == 'ORE':
                continue

            n_react = math.ceil(amt / reactions_amt[resource])
            for req, req_resource in reactions[resource]:
                current_resources[req_resource] += req * n_react

    return current_resources['ORE']


def aoc_day14(input_file):
    reactions = defaultdict(list)
    reactions_amt = defaultdict(int)
    data = defaultdict(set)
    with open(input_file, "r") as f:
        for line in f:
            inputs, outputs = line.split('=>')
            inputs = [i.strip().split(' ') for i in inputs.strip().split(',')]
            inputs = [(int(i), nxt) for i, nxt in inputs]
            output = [
                i.strip().split(' ') for i in outputs.strip().split(',')
            ][0]
            reactions_amt[(output[1])] = int(output[0])
            for _, nxt in inputs:
                data[output[1]].add(nxt)
            reactions[(output[1])] = inputs

    ordering = list(toposort2(data))[::-1]
    print(ordering)

    ore_value = 1000000000000
    low = 0
    high = 10000000000

    while low <= high:
        mid = (low + high) // 2
        ore_amount = calculate_ore_requirement(mid, ordering, reactions,
                                               reactions_amt)

        if ore_amount > ore_value:
            high = mid - 1
        elif ore_amount < ore_value:
            low = mid + 1
            # print(ore_amount, mid)
        else:
            return mid

    return mid


def test_program():
    DAY = 14
    test_arr = [
        (
            (f"{DAY}/aoc{DAY}.in1", ),
            31,
        ),
        (
            (f"{DAY}/aoc{DAY}.in2", ),
            165,
        ),
        (
            (f"{DAY}/aoc{DAY}.in3", ),
            13312,
        ),
        (
            (f"{DAY}/aoc{DAY}.in4", ),
            180697,
        ),
        (
            (f"{DAY}/aoc{DAY}.in5", ),
            2210736,
        ),
        (
            (f"{DAY}/aoc{DAY}.in6", ),
            0,
        ),
    ]

    # test_arr = [
    #     (
    #         (f"{DAY}/aoc{DAY}.in3", ),
    #         82892753,
    #     ),
    #     (
    #         (f"{DAY}/aoc{DAY}.in4", ),
    #         5586022,
    #     ),
    #     (
    #         (f"{DAY}/aoc{DAY}.in5", ),
    #         460664,
    #     ),
    #     (
    #         (f"{DAY}/aoc{DAY}.in6", ),
    #         0,
    #     ),
    # ]

    for inp, expected in test_arr:
        actual = aoc_day14(*inp)

        if actual == expected:
            print("OK")
        else:
            print(f"ERROR: actual: {actual} expected: {expected}")


test_program()
