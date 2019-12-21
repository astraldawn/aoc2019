from collections import defaultdict, deque
from functools import reduce
from itertools import permutations, product
import math
import copy
from intcode import IntCodeComputer

computer = None


def simulate(program, sequence, debug=False):
    A, B, C, D, E, F, G, H, I, J, T = tuple("ABCDEFGHIJT")
    reg = {}

    reg[J], reg[T] = False, False
    # reg[A], reg[B], reg[C], reg[D], reg[E], reg[F], reg[G], reg[H], reg[I] = tuple(bool(int(x)) for x in sequence[1:])
    reg[A], reg[B], reg[C], reg[D] = tuple(bool(int(x)) for x in sequence[1:])

    for line in program:
        if line == "WALK" or line == "RUN":
            continue

        ins, r1, r2 = line.strip().split(' ')
        if ins == 'NOT':
            reg[r2] = not reg[r1]

        if ins == 'AND':
            reg[r2] = (reg[r1] and reg[r2])

        if ins == 'OR':
            reg[r2] = (reg[r1] or reg[r2])

        if debug:
            print(sequence, ins, r1, r2, f"T: {reg[T]}", f"J: {reg[J]}")

    return reg[J]


def aoc_program(input_file):
    with open(input_file, "r") as f:
        input_program = [line.strip() for line in f][0]

    computer = IntCodeComputer(
        computer_id=1,
        input_program=input_program,
    )

    program_3 = [
        # (NOT A OR NOT B OR NOT C)
        "NOT A J",
        "NOT B T",
        "OR T J",
        "NOT C T",
        "OR T J",

        # (NOT A OR NOT B OR NOT C) and D
        "AND D J",

        # above AND (E OR H)
        "AND E T",
        "OR H T",
        "AND T J",

        # Exec
        "RUN",
    ]

    # Config
    program = program_3
    simulate_seq = False

    # Simulation
    if simulate_seq:
        sequences = []
        for i in range(0, 32):
            seq = str(bin(i))[2:]
            while len(seq) < 5:
                seq = '0' + seq
            if seq[0] == '0':
                continue

            invalid = False
            for i in range(4, 10):
                zeros = ''
                while len(zeros) < i:
                    zeros += '0'

                if zeros in seq:
                    invalid = True
                    break

            if invalid:
                continue

            if seq[:5] == "11111":
                sequences.append((seq, 0))
                continue

            sequences.append((seq, int(seq[-1])))

        for sequence, expected in sequences:
            s = copy.deepcopy(sequence)
            res = simulate(program, s, debug=False)

            if res == expected:
                print("OK", sequence)
                continue

            print("ERROR", sequence, res)
            simulate(program, s, debug=True)

    for prm in program:
        computer_input = [ord(p) for p in prm] + [10]
        for inp in computer_input:
            computer.add_input(inp)

    computer.run()

    for output in computer.output_queue:
        try:
            print(chr(output), end="")
        except Exception:
            return output


def test_program():
    DAY = 21
    test_arr = [
        (
            (f"{DAY}/aoc{DAY}.in1", ),
            19358870,
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
        # grid, max_x, max_y = aoc_program(*inp)
        # actual = aoc_part2(f"{DAY}/aoc{DAY}.in1", grid, max_x, max_y)
        actual = aoc_program(*inp)

        if actual == expected:
            print("OK")
        else:
            print(f"ERROR: actual: {actual} expected: {expected}")


test_program()
