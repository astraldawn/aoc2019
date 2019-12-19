from collections import defaultdict, deque
from functools import reduce
from itertools import permutations, product
from tqdm import tqdm
import math
import copy
from intcode import IntCodeComputer


def aoc_program(input_file):
    with open(input_file, "r") as f:
        input_program = [line.strip() for line in f][0]

    square_size = 100

    counter = 0
    prev_x = 0

    items = {
        0: 1,
        1: 0,
        2: 0,
        3: 0,
    }

    answer_found = False
    square_size = 99
    for s_x in range(416, 871, 1):
        print(f"Probing {s_x}")
        for s_y in range(577, 1101, 1):
            # print(f"Probing {s_x} {s_y}")
            counter = 0

            computer = IntCodeComputer(
                computer_id=1,
                input_program=input_program,
            )
            computer.add_input(s_x)
            computer.add_input(s_y + square_size)
            computer.run()
            counter += computer.output_queue.popleft()

            if counter != 1:
                continue

            computer = IntCodeComputer(
                computer_id=1,
                input_program=input_program,
            )
            computer.add_input(s_x + square_size)
            computer.add_input(s_y + square_size)
            computer.run()
            counter += computer.output_queue.popleft()

            if counter != 2:
                continue

            computer = IntCodeComputer(
                computer_id=1,
                input_program=input_program,
            )
            computer.add_input(s_x + square_size)
            computer.add_input(s_y)
            computer.run()
            counter += computer.output_queue.popleft()

            if counter != 3:
                continue

            computer = IntCodeComputer(
                computer_id=1,
                input_program=input_program,
            )
            computer.add_input(s_x)
            computer.add_input(s_y)
            computer.run()
            counter += computer.output_queue.popleft()

            if counter == 4:
                answer_found = True
                print(s_x, s_y, s_x * 10000 + s_y)
                break

        if answer_found:
            break

    return counter

def test_program():
    DAY = 19
    test_arr = [
        (
            (f"{DAY}/aoc{DAY}.in1", ),
            -1,
        ),
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
        # (
        #     (f"{DAY}/aoc{DAY}.in6", ),
        #     0,
        # ),
    ]

    for inp, expected in test_arr:
        actual = aoc_program(*inp)

        if actual == expected:
            print("OK")
        else:
            print(f"ERROR: actual: {actual} expected: {expected}")


test_program()
