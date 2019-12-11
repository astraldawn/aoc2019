from collections import defaultdict, deque
from itertools import permutations, product
from intcode import IntCodeComputer


"""
All panels start as black

Provide 0 if black, 1 if white

Turn and then move
"""

UP, DOWN, LEFT, RIGHT = "UP", "DOWN", "LEFT", "RIGHT"

# 0 --> turn left, 1 --> turn right
direction_change = {
    UP: [LEFT, RIGHT],
    DOWN: [RIGHT, LEFT],
    LEFT: [DOWN, UP],
    RIGHT: [UP, DOWN]
}

position_change = {UP: [0, 1], DOWN: [0, -1], LEFT: [-1, 0], RIGHT: [1, 0]}


# Paint cur, turn and then move
def aoc_day11(input_file):
    with open(input_file, "r") as f:
        input_program = [line.strip() for line in f][0]

    computer = IntCodeComputer(
        computer_id=1,
        input_program=input_program,
    )

    grid = defaultdict(int)
    painted = set()
    c_x, c_y, c_dir = 0, 0, UP

    # PART 2
    grid[(c_x, c_y)] = 1

    # PAINT
    computer.add_input(grid[(c_x, c_y)])
    computer.run()

    while True:
        if computer.has_halt:
            print("HALTED")
            break

        if not computer.output_queue:
            print("Something went wrong")
            break

        # PAINT
        paint_color = computer.output_queue.popleft()
        grid[(c_x, c_y)] = paint_color
        painted.add((c_x, c_y))

        # TURN
        turn_dir = computer.output_queue.popleft()

        # MOVE
        c_dir = direction_change[c_dir][turn_dir]
        c_x, c_y = (
            c_x + position_change[c_dir][0],
            c_y + position_change[c_dir][1],
        )

        # Supply input
        computer.add_input(grid[(c_x, c_y)])
        computer.run()

    min_x, max_x, min_y, max_y = 1000000, 0, 1000000, 0
    for x, y in painted:
        min_x = min(x, min_x)
        min_y = min(y, min_y)
        max_x = max(x, max_x)
        max_y = max(y, max_y)

    # Dumping the output
    for y in range(max_y, min_y - 1, -1):
        line_output = []
        for x in range(min_x, max_x + 1):
            c_pos = grid[(x, y)]
            if c_pos == 1:
                line_output.append("#")
            else:
                line_output.append(" ")
        print("".join(line_output))

    return 0


def test_program():
    DAY = 11
    test_arr = [
        (
            (f"{DAY}/aoc{DAY}.in1", ),
            8,
        ),
    ]

    for inp, expected in test_arr:
        actual = aoc_day11(*inp)

        if actual == expected:
            print("OK")
        else:
            print(f"ERROR: actual: {actual} expected: {expected}")


test_program()
