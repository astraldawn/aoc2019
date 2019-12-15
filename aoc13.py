from collections import defaultdict, deque
from itertools import permutations, product
from intcode import IntCodeComputer


def print_grid(grid):
    for i in range(0, 25):
        for j in range(0, 50):
            if grid[(j, i)] > 0:
                print(grid[(j, i)], end="")
            else:
                print(" ", end="")
        print()


# Paint cur, turn and then move
def aoc_day13(input_file):
    with open(input_file, "r") as f:
        input_program = [line.strip() for line in f][0]

    computer = IntCodeComputer(
        computer_id=1,
        input_program=input_program,
    )

    computer.run()

    tiles = defaultdict(list)
    grid = defaultdict(int)
    score = 0

    for i in range(0, len(computer.output_queue), 3):
        x = computer.output_queue.popleft()
        y = computer.output_queue.popleft()
        tile_id = computer.output_queue.popleft()
        tiles[tile_id].append((x, y))
        grid[(x, y)] = tile_id
        if x == -1:
            score = tile_id

    ball_x, ball_y = tiles[4][0][0], tiles[4][0][1]
    paddle_x, paddle_y = tiles[3][0][0], tiles[3][0][1]

    while True:
        if computer.output_queue:
            for i in range(0, len(computer.output_queue), 3):
                x = computer.output_queue.popleft()
                y = computer.output_queue.popleft()
                tile_id = computer.output_queue.popleft()

                if x == -1:
                    score = tile_id
                    print(f"SCORE IS: {score}")
                    continue

                grid[(x, y)] = tile_id
                if tile_id == 3:
                    paddle_x, paddle_y = x, y
                elif tile_id == 4:
                    ball_x, ball_y = x, y

        if computer.has_halt:
            break

        if paddle_x < ball_x:
            computer.add_input(1)
        elif paddle_x > ball_x:
            computer.add_input(-1)
        else:
            computer.add_input(0)

        computer.run()

    print_grid(grid)

    return len(tiles[2])


def test_program():
    DAY = 13
    test_arr = [
        (
            (f"{DAY}/aoc{DAY}.in1", ),
            8,
        ),
    ]

    for inp, expected in test_arr:
        actual = aoc_day13(*inp)

        if actual == expected:
            print("OK")
        else:
            print(f"ERROR: actual: {actual} expected: {expected}")


test_program()
