from collections import defaultdict, deque
from functools import reduce
from itertools import permutations, product
import math
import copy
from intcode import IntCodeComputer

computer = None

UP, DOWN, LEFT, RIGHT = 'UP', 'DOWN', 'LEFT', 'RIGHT'

move = {
    UP: (0, -1),
    DOWN: (0, 1),
    RIGHT: (1, 0),
    LEFT: (-1, 0),
}

# 0 = LEFT, 1 = RIGHT
turn = {
    UP: (LEFT, RIGHT),
    DOWN: (RIGHT, LEFT),
    RIGHT: (UP, DOWN),
    LEFT: (DOWN, UP),
}


def print_grid(grid, max_x, max_y):
    for i in range(max_y):
        for j in range(max_x):
            cur = grid[(j, i)]
            print(chr(cur), end="")
        print()


def aoc_program(input_file):
    with open(input_file, "r") as f:
        input_program = [line.strip() for line in f][0]

    computer = IntCodeComputer(
        computer_id=1,
        input_program=input_program,
    )

    grid = defaultdict(int)

    computer.run()

    x, y = 0, 0
    max_x, max_y = 0, 0
    for item in computer.output_queue:
        if item == 10:
            max_x, max_y = max(x, max_x), max(y, max_y)
            x, y = 0, y + 1
            continue

        grid[(x, y)] = item
        x += 1

    intersections_sum = 0
    for i in range(max_y):
        for j in range(max_x):
            cur = grid[(j, i)]
            if cur != 35:
                continue

            surrounded = True
            for mx, my in move.values():
                nx, ny = j + mx, i + my
                if grid[(nx, ny)] != 35:
                    surrounded = False
                    break

            if surrounded:
                intersections_sum += j * i

    return (grid, max_x, max_y)


def aoc_part2_grid(input_file, grid, max_x, max_y):
    cx, cy = 0, 0
    for i in range(max_y):
        for j in range(max_x):
            if grid[(j, i)] == 94:
                cx, cy = j, i

    cur_dist, cur_dir = 0, UP
    all_moves = []

    while True:
        mx, my = move[cur_dir]
        nx, ny = cx + mx, cy + my
        next_pos = (nx, ny)

        # Means no direction change
        if grid[next_pos] == 35:
            cx, cy = nx, ny
            cur_dist += 1
            continue

        has_move = False
        for chosen, new_dir in enumerate(turn[cur_dir]):
            mx, my = move[new_dir]
            nx, ny = cx + mx, cy + my
            next_pos = (nx, ny)

            if grid[next_pos] == 35:
                has_move = True
                break

        if not has_move:
            print("END")
            break

        all_moves.append((chosen, cur_dir, cur_dist))
        cur_dir = new_dir
        cur_dist = 0
        # break

    robot_moves = []
    for i in range(1, len(all_moves)):
        turn_dir = 'L' if all_moves[i - 1][0] == 0 else 'R'
        robot_moves.append(f"{turn_dir}{all_moves[i][2]}")

    print(robot_moves)


def aoc_part2(input_file):
    with open(input_file, "r") as f:
        input_program = [line.strip() for line in f][0]

    computer = IntCodeComputer(
        computer_id=1,
        input_program=input_program,
    )

    program = 'B,A,B,A,C,B,A,C,B,C'
    A = 'L,8,L,6,L,10,L,6'
    B = 'R,6,L,6,L,10'
    C = 'R,6,L,8,L,10,R,6'
    video = 'n'

    for prm in [program, A, B, C, video]:
        computer_input = [ord(p) for p in prm] + [10]
        for inp in computer_input:
            computer.add_input(inp)

        computer.run()

    print(computer.output_queue)


def test_program():
    DAY = 17
    test_arr = [
        (
            (f"{DAY}/aoc{DAY}.in1", ),
            1,
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
        actual = aoc_part2(*inp)

        if actual == expected:
            print("OK")
        else:
            print(f"ERROR: actual: {actual} expected: {expected}")


test_program()
