import numpy as np
import math
from tqdm import tqdm
from collections import deque, defaultdict
from itertools import permutations, product

def get_dist(p1, p2):
     dist = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
     return dist

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    return angle

# def aoc_day10(input_file):
#     asteroids = []
#     max_x, max_y = 0, 0
#     lines = []
#     with open(input_file, "r") as f:
#         lines = [line.strip() for line in f]

#     for y, line in enumerate(lines):
#         max_x = len(line.strip())
#         for x, p in enumerate(line.strip()):
#             if p == '#':
#                 asteroids.append((x, y))

#     max_y = len(lines)

#     max_visible = 0
#     visible_from = defaultdict(int)
#     for cur_point in tqdm(asteroids):
#         occupied_angles = set()

#         for asteroid in asteroids:
#             if asteroid == cur_point:
#                 continue

#             v1 = (0, 1)
#             v2 = (asteroid[0] - cur_point[0], asteroid[1] - cur_point[1])
#             angle = round(np.degrees(angle_between(v1, v2)), 8)

#             if asteroid[0] > cur_point[0]:
#                 angle = 360.0 - angle
#             occupied_angles.add(angle)

#         max_visible = max(max_visible, len(occupied_angles))

#         if len(occupied_angles) == max_visible:
#             print(max_visible, cur_point)
#         visible_from[cur_point] = len(occupied_angles)

#     return max_visible

def aoc_day10(input_file, station_loc):
    asteroids = []
    max_x, max_y = 0, 0
    lines = []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f]

    for y, line in enumerate(lines):
        max_x = len(line.strip())
        for x, p in enumerate(line.strip()):
            if p == '#':
                asteroids.append((x, y))

    max_y = len(lines)

    max_visible = 0
    visible_from = defaultdict(int)
    occupied_angles = defaultdict(list)
    for cur_point in tqdm([station_loc]):

        for asteroid in asteroids:
            if asteroid == cur_point:
                continue

            v1 = (0, 1)
            v2 = (asteroid[0] - cur_point[0], asteroid[1] - cur_point[1])
            angle = round(np.degrees(angle_between(v1, v2)), 8)

            if asteroid[0] > cur_point[0]:
                angle = 360.0 - angle
            occupied_angles[angle].append(asteroid)

    points = 0
    ptr = 0
    occupied_angles_list = sorted(occupied_angles.keys())
    for angle in occupied_angles_list:
        if angle < 180:
            ptr += 1

    while points < 200:
        cur_angle = occupied_angles_list[ptr]

        if len(occupied_angles[cur_angle]) == 0:
            continue

        min_dist = 100000
        min_point = None
        for p in occupied_angles[cur_angle]:
            dist = get_dist(p, station_loc)
            if dist < min_dist:
                min_point = p

        occupied_angles[cur_angle].remove(min_point)

        points += 1
        ptr = (ptr + 1) % len(occupied_angles_list)

    print(min_point)
    return min_point[0] * 100 + min_point[1]


def test_program():
    test_arr = [
        # (
        #     ("aoc10.in1", ),
        #     8,
        # ),
        # (
        #     ("aoc10.in2", ),
        #     33,
        # ),
        # (
        #     ("aoc10.in3", ),
        #     35,
        # ),
        # (
        #     ("aoc10.in4", ),
        #     41,
        # ),
        (
            ("aoc10.in5", (11, 13)),
            210,
        ),
        (
            ("aoc10.in6", (37, 25)),
            5,
        ),
    ]

    for inp, expected in test_arr:
        actual = aoc_day10(*inp)

        if actual == expected:
            print("OK")
        else:
            print(f"ERROR: actual: {actual} expected: {expected}")


test_program()
