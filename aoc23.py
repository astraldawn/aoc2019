from collections import defaultdict, deque
from functools import reduce
from itertools import permutations, product
import math
import copy
from intcode import IntCodeComputer


def aoc_program(input_file):
    with open(input_file, "r") as f:
        input_program = [line.strip() for line in f][0]

    computers = []
    for i in range(0, 50):
        computer = IntCodeComputer(
            computer_id=i,
            input_program=input_program,
        )
        computer.add_input(i)
        computer.run()
        computers.append(computer)

    cnt = 0
    instructions = defaultdict(deque)
    seen = set()
    keep_running = True
    while keep_running:

        cnt += 1
        if cnt > 500:
            break

        # read output
        for computer in computers:
            while computer.output_queue:
                dest = computer.output_queue.popleft()
                x = computer.output_queue.popleft()
                y = computer.output_queue.popleft()
                instructions[dest].append((x, y))
                if dest == 255:
                    instructions[dest] = deque([(x, y)])
                    # print(dest, x, y)

        all_listen = True
        for i in range(50):
            if instructions[i]:
                all_listen = False
                break

        if all_listen:
            for i in range(50):
                if i != 0:
                    computers[i].add_input(-1)
                    continue

                if instructions[255]:
                    nx, ny = instructions[255].popleft()
                    computers[i].add_input(nx)
                    computers[i].add_input(ny)
                    if ny in seen:
                        print("REPEAT", ny)
                        keep_running = False
                        break
                    # print(nx, ny)
                    seen.add(ny)
                else:
                    computers[i].add_input(-1)

            for computer in computers:
                computer.run()

        else:
            # When its not all listening
            # add more input
            for computer in computers:
                if len(instructions[computer.computer_id]) == 0:
                    computer.add_input(-1)
                    continue

                nx, ny = instructions[computer.computer_id].popleft()
                computer.add_input(nx)
                computer.add_input(ny)

            # run
            for computer in computers:
                computer.run()

    return -1



def test_program():
    DAY = 23
    test_arr = [
        (
            (f"{DAY}/aoc{DAY}.in1", ),
            0,
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
