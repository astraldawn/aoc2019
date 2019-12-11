from collections import defaultdict, deque
from itertools import permutations, product


def aoc_day11(input_file):
    with open(input_file, "r") as f:
        pass

    return 0


def test_program():
    DAY = 11
    test_arr = [
        (
            (f"{DAY}/aoc{DAY}.in1", ),
            8,
        ),
    ]

    for inp, expected in test_arr:
        actual = aoc_day11(*inp)

        if actual == expected:
            print("OK")
        else:
            print(f"ERROR: actual: {actual} expected: {expected}")


test_program()
