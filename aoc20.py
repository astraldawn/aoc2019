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


def is_alpha(c):
    return ord(c) >= 65 and ord(c) <= 90


def is_portal(input_grid, c_x, c_y, max_x, max_y):
    c_tile = input_grid[(c_x, c_y)]
    neighbours = defaultdict(int)
    for (m_x, m_y) in moves:
        next_pos = (c_x + m_x, c_y + m_y)
        neighbours[input_grid[next_pos]] += 1

    # is_portal, portal_id, is_inner
    portal_id = c_tile
    is_inner = False

    if neighbours['.'] != 1:
        return (False, portal_id, is_inner)

    for k in neighbours.keys():
        if is_alpha(k):
            portal_id += k

    portal_id = ''.join(sorted(portal_id))

    # Distance to any edge
    dist_edge = 1000
    dist_edge = min(dist_edge, c_y - 0)
    dist_edge = min(dist_edge, max_y - c_y)
    dist_edge = min(dist_edge, c_x)
    dist_edge = min(dist_edge, max_x - c_x)
    return (True, portal_id, dist_edge > 2)


def aoc_program(input_file):
    input_grid = defaultdict(lambda: NULL)
    grid = defaultdict(lambda: NULL)
    portals = {}
    portal_coords = defaultdict(list)
    portal_traverse = defaultdict(int)
    max_x, max_y = 0, 0

    with open(input_file, "r") as f:
        y = 0
        for line in f:
            line = line.replace(' ', '?')
            for x, c in enumerate(line.strip()):
                input_grid[(x, y)] = c
                max_x = max(x, max_x)
            y += 1
            max_y = max(y, max_y)

    for y in range(max_y):
        for x in range(max_x):
            c_tile = input_grid[(x, y)]
            if c_tile == '?':
                continue

            if c_tile == '.' or c_tile == '#':
                grid[(x, y)] = c_tile
                continue

            # Alphabet
            if is_alpha(c_tile):
                portal, portal_id, is_inner = is_portal(
                    input_grid, x, y, max_x, max_y)
                if not portal:
                    continue

                grid[(x, y)] = 'P'
                portals[(x, y)] = (portal_id, is_inner)
                portal_coords[portal_id].append((x, y))

    # This is locked
    s_x, s_y = portal_coords['AA'][0]
    visited = defaultdict(lambda: NULL)
    queue = PriorityQueue()
    queue.put((0, (s_x, s_y, 0)))

    while queue:
        c_dist, (c_x, c_y, c_level) = queue.get_nowait()
        c_pos = (c_x, c_y)

        if c_pos == portal_coords['ZZ'][0] and c_level == 0:
            # Because we want the open tile
            return c_dist - 1
            break

        if visited[(c_x, c_y, c_level)] != NULL:
            continue
        visited[(c_x, c_y, c_level)] = c_dist

        n_dist = c_dist + 1 if grid[c_pos] != 'P' else c_dist

        for (m_x, m_y) in moves:
            n_x, n_y = c_x + m_x, c_y + m_y
            next_pos = (n_x, n_y)

            # Blocked
            if grid[next_pos] == '#':
                continue

            # Walkable
            if grid[next_pos] == '.':
                queue.put((n_dist, (n_x, n_y, c_level)))

            # Portal handling
            if grid[next_pos] == 'P':

                # AA and ZZ are walls if level is more than 0
                if c_level > 0:
                    portal_id, is_inner = portals[next_pos]
                    if portal_id == 'AA' or portal_id == 'ZZ':
                        continue

                queue.put((n_dist, (n_x, n_y, c_level)))

        if grid[c_pos] == 'P':
            portal_id, is_inner = portals[c_pos]
            portal_traverse[portals[c_pos]] += 1

            for (x, y) in portal_coords[portal_id]:
                if (x, y) == c_pos:
                    continue

                n_level = c_level + 1 if is_inner else c_level - 1

                # Don't go below level 0
                if n_level < 0:
                    continue

                queue.put((n_dist, (x, y, n_level)))

    return -1


def test_program():
    DAY = 20
    test_arr = [
        # (
        #     (f"{DAY}/aoc{DAY}.in1", ),
        #     23,
        # ),
        # (
        #     (f"{DAY}/aoc{DAY}.in2", ),
        #     58,
        # ),
        (
            (f"{DAY}/aoc{DAY}.in3", ),
            396,
        ),
        # (
        #     (f"{DAY}/aoc{DAY}.in4", ),
        #     136,
        # ),
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
