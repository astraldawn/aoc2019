from tqdm import tqdm
from collections import defaultdict, deque
from itertools import permutations, product

class Moon(object):
    def __init__(self, moon_id, pos_dict):
        self.id = moon_id
        self.pos = pos_dict
        self.vel = {k: 0 for k in pos_dict.keys()}

    def __repr__(self):
        return f"pos: {self.pos}   # vel: {self.vel}"

    def update_gravity(self, other_moon):
        for k in self.pos.keys():
            if self.pos[k] < other_moon.pos[k]:
                self.vel[k] += 1
                other_moon.vel[k] -= 1
            elif self.pos[k] > other_moon.pos[k]:
                self.vel[k] -= 1
                other_moon.vel[k] += 1

    def update_position(self):
        for k in self.pos.keys():
            self.pos[k] += self.vel[k]

    def get_energy(self):
        pos_v = sum([abs(x) for x in self.pos.values()])
        vel_v = sum([abs(x) for x in self.vel.values()])
        return pos_v * vel_v

    def get_vel(self):
        return (self.vel['x'], self.vel['y'], self.vel['z'])

    def get_pos(self):
        return (self.pos['x'], self.pos['y'], self.pos['z'])

    def get_state(self):
        return self.get_pos() + self.get_vel()


def aoc_day12(input_moons, n_steps):
    moons = []
    for i, (x, y, z) in enumerate(input_moons):
        moons.append(Moon(
            moon_id=i,
            pos_dict={
                'x': x,
                'y': y,
                'z': z
            }
        ))

    steps = 0
    zero_vel = []

    for step in tqdm(range(n_steps)):
        # GRAVITY
        for i in range(len(moons)):
            for j in range(i + 1, len(moons)):
                cur_moon, cmp_moon = moons[i], moons[j]
                cur_moon.update_gravity(cmp_moon)

        # VELOCITY
        all_zeros = True
        for moon in moons:
            moon.update_position()
            if moon.vel['y'] != 0:
                all_zeros = False

        if all_zeros:
            zero_vel.append(step)

    """
    How to do it
    1. Find the periods when velocity is zero for each component, let them be (p_x, p_y, p_z)
    2. LCM(p_x, p_y, p_z)
    3. Multiply by 2
    """

    print(zero_vel)

    for i in range(len(zero_vel) - 1):
        print(f"{zero_vel[i + 1] - zero_vel[i]} ", end="")
    print()

    for moon in moons:
        print(moon)

    energy = sum([moon.get_energy() for moon in moons])

    # 233517045776756

    return energy


def test_program():
    DAY = 12
    """
    Test case 1 has repeat velocity after 228 steps
    Test case 2 has repeat velocity after 578533 steps

    Moon state repeat
        - Moon 0 repeat state after 79 638 moves (test 2)
    """
    test_arr = [
        (
            ([(-1, 0, 2), (2, -10, -7), (4, -8, 8), (3, 5, -1)], 1386, ),
            0,
        ),
        # (
        #     ([(-8, -10, 0), (5, 5, 10), (2, -7, 3), (9, -8, -3)], 100000, ),
        #     1940,
        # ),
        # (
        #     ([(4, 12, 13), (-9, 14, -3), (-7, -1, 2), (-11, 17, -1)], 500000, ),
        #     5350,
        # ),
    ]

    for inp, expected in test_arr:
        actual = aoc_day12(*inp)

        if actual == expected:
            print("OK")
        else:
            print(f"ERROR: actual: {actual} expected: {expected}")


test_program()
