import copy
import math
from tqdm import tqdm
from collections import defaultdict, deque
from functools import reduce
from itertools import permutations, product
from queue import PriorityQueue

NULL = '?'
WALL = '#'

moves = [(1, 0), (-1, 0), (0, -1), (0, 1)]


def is_key(c):
    if len(c) > 1:
        return True
    return ord(c) >= ord('a') and ord(c) <= ord('z')


def is_block(c):
    if len(c) > 1:
        return False
    return ord(c) >= ord('A') and ord(c) <= ord('Z')


def compute_keys_distance(grid, keys, key_pos):
    distance_block = defaultdict(lambda: NULL)

    for start_key in keys:
        g_dist = defaultdict(int)
        start_pos = key_pos[start_key]

        queue = deque()
        # start at 1, subtract 1 later
        queue.append((1, start_pos, []))

        while queue:
            c_dist, c_pos, c_block = queue.popleft()

            # Seen
            if g_dist[c_pos] > 0:
                continue

            g_dist[c_pos] = c_dist
            c_x, c_y = c_pos
            for m_x, m_y in moves:
                n_pos = (c_x + m_x, c_y + m_y)
                if grid[(n_pos)] == NULL or grid[(
                        n_pos)] == '#' or g_dist[(n_pos)] > 0:
                    continue

                n_block = copy.deepcopy(c_block)
                if is_block(grid[n_pos]):
                    n_block.append(grid[n_pos])
                    queue.append((c_dist + 1, n_pos, n_block))
                    continue

                if is_key(grid[n_pos]):
                    queue.append((c_dist + 1, n_pos, n_block))
                    n_block = [n.lower() for n in n_block]

                    # No +1 here
                    distance_block[(start_key, grid[n_pos])] = (c_dist,
                                                                set(n_block))
                    distance_block[(grid[n_pos], start_key)] = (c_dist,
                                                                set(n_block))
                    continue

                queue.append((c_dist + 1, n_pos, n_block))

    return distance_block


def aoc_program(input_file):
    grid = defaultdict(lambda: NULL)
    keys = set()
    blocks = set()
    key_pos = {}
    start_count = 0
    start_keys = set()

    with open(input_file, "r") as f:
        y = 0
        for line in f:
            for x, c in enumerate(line.strip()):
                grid[(x, y)] = c

                if c == '@':
                    grid[(x, y)] = f'{c}{start_count}'
                    keys.add(grid[(x, y)])
                    start_keys.add(grid[(x, y)])
                    start_count += 1
                    key_pos[grid[(x, y)]] = (x, y)
                    continue

                if is_key(c):
                    keys.add(c)
                    key_pos[c] = (x, y)
                    continue

                if is_block(c):
                    blocks.add(c)
            y += 1

    keys = keys - start_keys
    distance_block = compute_keys_distance(grid, keys, key_pos)

    # (dist, ([positions], keys_left))
    start_state = (0, (list(start_keys), set()))
    queue = PriorityQueue()
    queue.put(start_state)
    visited = set()

    answer = 0
    steps = 0
    while True:
        if queue.empty():
            break

        c_dist, (c_positions, c_keys_available) = queue.get_nowait()
        steps += 1

        if c_keys_available == keys:
            answer = c_dist
            break

        c_keys_left = keys - c_keys_available
        for i, c_key in enumerate(c_positions):

            c_keys_tuple = tuple(sorted(c_keys_available))
            if (c_key, c_keys_tuple) in visited:
                continue

            visited.add((c_key, c_keys_tuple))

            for key in c_keys_left:
                if distance_block[(c_key, key)] == NULL:
                    continue

                distance_btwn_keys, blocks = distance_block[(c_key, key)]

                if blocks - c_keys_available:
                    continue

                n_positions = copy.deepcopy(c_positions)
                n_positions[i] = key
                n_keys_available = set(list(c_keys_available))
                n_keys_available.add(key)

                new_state = (c_dist + distance_btwn_keys, (n_positions,
                                                           n_keys_available))
                queue.put(new_state)

    return answer


def test_program():
    DAY = 18
    test_arr = [
        (
            (f"{DAY}/aoc{DAY}.in1", ),
            8,
        ),
        # (
        #     (f"{DAY}/aoc{DAY}.in2", ),
        #     86,
        # ),
        # (
        #     (f"{DAY}/aoc{DAY}.in3", ),
        #     132,
        # ),
        (
            (f"{DAY}/aoc{DAY}.in4", ),
            136,
        ),
        # (
        #     (f"{DAY}/aoc{DAY}.in5", ),
        #     81,
        # ),
        (
            (f"{DAY}/aoc{DAY}.in6", ),
            0,
        ),
    ]

    for inp, expected in test_arr:
        actual = aoc_program(*inp)

        if actual == expected:
            print("OK")
        else:
            print(f"ERROR: actual: {actual} expected: {expected}")


test_program()
