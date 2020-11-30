from collections import defaultdict, deque
from functools import reduce
from itertools import permutations, product
import math
import copy
from intcode import IntCodeComputer

DEAL_NEW, DEAL_INC, CUT = 'DEAL_NEW', 'DEAL_INC', 'CUT'


def aoc_program(input_file):
    instructions = []
    reverse = False
    deck_size = 119315717514047

    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            line = line.split(' ')
            if line[0] == 'cut':
                if not reverse:
                    instructions.append((CUT, int(line[1])))
                else:
                    instructions.append((CUT, -int(line[1])))
                continue

            if line[2] == 'new':
                instructions.append((DEAL_NEW, 0))
                continue

            if line[2] == 'increment':
                if not reverse:
                    instructions.append((DEAL_INC, int(line[3])))
                else:
                    instructions.append((DEAL_INC, -int(line[3]) % deck_size))
                continue

    if reverse:
        instructions = instructions[::-1]

    position = 2020
    n = 101741582076661

    # huhu's code
    d_multiplier = 1
    sd_multiplier = 0
    for ins_type, num in instructions:
        if ins_type == DEAL_NEW:
            sd_multiplier += -1 * d_multiplier
            d_multiplier *= -1
        if ins_type == CUT:
            sd_multiplier += num * d_multiplier
        if ins_type == DEAL_INC:
            d_multiplier *= pow(num, deck_size - 2, deck_size)
        d_multiplier %= deck_size
        sd_multiplier %= deck_size

    print("sd multiplier", sd_multiplier)
    print("d multiplier", d_multiplier)
    print((sd_multiplier * 1) % deck_size)

    a = d_multiplier
    b = sd_multiplier
    dn = pow(a, n, deck_size)
    sn = b * (1 - pow(a, n, deck_size)) * pow(1 - a, deck_size - 2, deck_size)
    sn %= deck_size
    print(sn, dn)
    print((sn + dn * position) % deck_size)

    return 0


def test_program():
    DAY = 22
    test_arr = [
        # (
        #     (f"{DAY}/aoc{DAY}.in1", ),
        #     -1,
        # ),
        # (
        #     (f"{DAY}/aoc{DAY}.in2", ),
        #     165,
        # ),
        # (
        #     (f"{DAY}/aoc{DAY}.in3", ),
        #     13312,
        # ),
        # (
        #     (f"{DAY}/aoc{DAY}.in4", ),
        #     180697,
        # ),
        # (
        #     (f"{DAY}/aoc{DAY}.in5", ),
        #     2210736,
        # ),
        (
            (f"{DAY}/aoc{DAY}.in6", ),
            0,
        ),
    ]

    for inp, expected in test_arr:
        # grid, max_x, max_y = aoc_program(*inp)
        # actual = aoc_part2(f"{DAY}/aoc{DAY}.in1", grid, max_x, max_y)
        actual = aoc_program(*inp)

        if actual == expected:
            print("OK")
        else:
            print(f"ERROR: actual: {actual} expected: {expected}")


test_program()
