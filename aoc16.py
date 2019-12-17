import copy
import math
from tqdm import tqdm
from collections import defaultdict, deque
from functools import reduce
from itertools import permutations, product
"""
12345678

1 + (-3) + 5 + (-7) = 4
2 + 3 + (-6) + (-7) = 8
3 + 4 + 5 = 2
4 + 5 + 6 + 7 = 2
5 + 6 + 7 + 8 = 5
6 + 7 + 8 = 1
7 + 8 = 5
8 = 8

4 + (-2) + 6 + (-5) = 3


"""

base_pattern = [0, 1, 0, -1]


def aoc_program(input_file, phases, has_offset=True):
    with open(input_file, "r") as f:
        inp = f.readline()

    offset = int(inp[:7])
    inp = [int(x) for x in inp]

    if has_offset:
        expanded_inp = inp * 10000

    to_compute = len(expanded_inp) - offset
    inp = expanded_inp[offset:][::-1]

    phase_arr = [inp[0]] * phases  # LAST DIGIT
    result = [inp[0]]

    for i in tqdm(range(1, to_compute)):
    # for i in range(1, 4):
        next_arr = []
        for k in range(phases):
            if k == 0:
                next_arr.append((phase_arr[k] + inp[i]) % 10)
            else:
                next_arr.append((phase_arr[k] + next_arr[-1]) % 10)

        phase_arr = copy.deepcopy(next_arr)
        result.append(phase_arr[-1])

    result = result[::-1]
    result = [str(x) for x in result[:8]]
    print(''.join(result))

    # for

    # memo = defaultdict(int)  # Digit, output_pos

    # for output_pos in tqdm(range(len(inp))):
    #     repeats = output_pos + 1
    #     pattern = []
    #     complete = False

    #     while not complete:
    #         for x in base_pattern:
    #             pattern.extend([x] * repeats)
    #             if len(pattern) >= len(inp) + 1:
    #                 complete = True
    #                 break

    #     memo[output_pos] = pattern[1:len(inp) + 1]
    #     print(output_pos, memo[output_pos])

    # output = []
    # for i in tqdm(range(phases)):
    #     new_inp = []
    #     for output_pos in range(len(inp)):
    #         pattern = memo[output_pos]
    #         result = sum(map(lambda x: x[0] * x[1], zip(inp, pattern)))
    #         result = abs(result) % 10
    #         new_inp.append(result)
    #     inp = copy.deepcopy(new_inp)
    #     output.extend(copy.deepcopy(new_inp))
    #     print(inp)

    # inp = [str(x) for x in inp]

    # if has_offset:
    #     print(offset)
    #     print(output[offset:offset + 8])
    #     return 0

    # return int(''.join(inp[:8]))


def test_program():
    DAY = 16
    test_arr = [
        # (
        #     (f"{DAY}/aoc{DAY}.in1", 4, False),
        #     1029498,
        # ),
        # (
        #     (f"{DAY}/aoc{DAY}.in2", 100, False),
        #     24176176,
        # ),
        (
            (f"{DAY}/aoc{DAY}.in3", 100),
            13312,
        ),
        (
            (f"{DAY}/aoc{DAY}.in4", 100),
            180697,
        ),
        (
            (f"{DAY}/aoc{DAY}.in5", 100),
            2210736,
        ),
        (
            (f"{DAY}/aoc{DAY}.in6", 100, True),
            82435530,
        ),
    ]

    for inp, expected in test_arr:
        actual = aoc_program(*inp)

        if actual == expected:
            print("OK")
        else:
            print(f"ERROR: actual: {actual} expected: {expected}")


test_program()
