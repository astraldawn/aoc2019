from collections import defaultdict, deque
from functools import reduce
from itertools import permutations, product
import math
import copy
from intcode import IntCodeComputer

NORTH, SOUTH, WEST, EAST = 'NORTH', 'SOUTH', 'WEST', 'EAST'

dir_map = {
    NORTH: 1,
    SOUTH: 2,
    WEST: 3,
    EAST: 4,
}

backtrack = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    WEST: EAST,
    EAST: WEST,
}

move = {
    NORTH: (0, 1),
    SOUTH: (0, -1),
    EAST: (1, 0),
    WEST: (-1, 0),
}

computer = None


def dfs(c_x, c_y, grid, dist):
    global computer
    for dir in [NORTH, SOUTH, WEST, EAST]:
        n_x, n_y = c_x + move[dir][0], c_y + move[dir][1]

        # Don't try to explore further
        if (n_x, n_y) in grid.keys():
            continue

        # Save current computer state
        prev_computer = copy.deepcopy(computer)

        computer.add_input(dir_map[dir])
        computer.run()
        response = computer.output_queue.popleft()
        grid[(n_x, n_y)] = response + 1

        if response == 2:
            print("DONE", dist + 1)
            return dist
        if response == 1:
            dfs(n_x, n_y, grid, dist + 1)
            computer = prev_computer


def aoc_day15(input_file):
    global computer
    with open(input_file, "r") as f:
        input_program = [line.strip() for line in f][0]

    computer = IntCodeComputer(
        computer_id=1,
        input_program=input_program,
    )

    grid = defaultdict(int)
    grid[(0, 0)] = 2  # EMPTY

    # GENERATE THE GRID
    s_x, s_y = 0, 0
    print(dfs(0, 0, grid, 0))

    grid_size = 25
    for i in range(grid_size, -grid_size, -1):
        for j in range(-grid_size, grid_size, 1):
            if grid[(j, i)] == 1:  # HEX
                print("#", end="")
            elif grid[(j, i)] == 2:  # EMPTY
                print(".", end="")
            elif grid[(j, i)] == 3:  # DESTINATION
                print("%", end="")
                s_x, s_y = j, i
            else:
                print(" ", end="")
        print()

    queue = deque()
    vis = defaultdict(int)
    dist = defaultdict(int)
    queue.append((s_x, s_y))
    vis[(s_x, s_y)] = 1
    dist[(s_x, s_y)] = 0

    while queue:
        c_x, c_y = queue.popleft()
        vis[(c_x, c_y)] = 1
        for dir in [NORTH, SOUTH, WEST, EAST]:
            next_pos = (c_x + move[dir][0], c_y + move[dir][1])
            if grid[next_pos] == 2 and not vis[next_pos]:  # EMPTY
                dist[next_pos] = dist[(c_x, c_y)] + 1
                queue.append(next_pos)

    return max(dist.values())


def test_program():
    DAY = 15
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
        actual = aoc_day15(*inp)

        if actual == expected:
            print("OK")
        else:
            print(f"ERROR: actual: {actual} expected: {expected}")


test_program()
