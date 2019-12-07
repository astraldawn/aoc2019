import copy

with open('aoc2.in', 'r') as f:
    original_program = [line.split(',') for line in f][0]
    original_program = [int(p) for p in original_program]

    for noun in range(0, 100):
        for verb in range(0, 100):
            program = copy.copy(original_program)
            program[1], program[2] = noun, verb
            for i in range(0, len(program), 4):
                opcode, p1, p2, p_res = program[i:i+4]
                if opcode == 1:
                    program[p_res] = program[p1] + program[p2]
                if opcode == 2:
                    program[p_res] = program[p1] * program[p2]
                if opcode == 99:
                    break

            if program[0] == 19690720:
                print(noun, verb)
                print(100 * noun + verb)
