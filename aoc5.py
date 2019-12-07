import copy

program_a = "3,0,4,0,99"
program_b = "1002,4,3,4,33"
program_c = "1101,100,-1,4,0"
program_d = "3,9,8,9,10,9,4,9,99,-1,8"
program_e = "3,9,7,9,10,9,4,9,99,-1,8"
program_f = "3,3,1108,-1,8,3,4,3,99"
program_g = "3,3,1107,-1,8,3,4,3,99"
program_h = "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"
program_i = "3,3,1105,-1,9,1101,0,0,12,4,12,99,1"
program_j = "3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99"
program_input = "3,225,1,225,6,6,1100,1,238,225,104,0,1101,91,67,225,1102,67,36,225,1102,21,90,225,2,13,48,224,101,-819,224,224,4,224,1002,223,8,223,101,7,224,224,1,223,224,223,1101,62,9,225,1,139,22,224,101,-166,224,224,4,224,1002,223,8,223,101,3,224,224,1,223,224,223,102,41,195,224,101,-2870,224,224,4,224,1002,223,8,223,101,1,224,224,1,224,223,223,1101,46,60,224,101,-106,224,224,4,224,1002,223,8,223,1001,224,2,224,1,224,223,223,1001,191,32,224,101,-87,224,224,4,224,102,8,223,223,1001,224,1,224,1,223,224,223,1101,76,90,225,1101,15,58,225,1102,45,42,224,101,-1890,224,224,4,224,1002,223,8,223,1001,224,5,224,1,224,223,223,101,62,143,224,101,-77,224,224,4,224,1002,223,8,223,1001,224,4,224,1,224,223,223,1101,55,54,225,1102,70,58,225,1002,17,80,224,101,-5360,224,224,4,224,102,8,223,223,1001,224,3,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,677,677,224,102,2,223,223,1005,224,329,1001,223,1,223,1108,677,226,224,1002,223,2,223,1006,224,344,101,1,223,223,107,677,226,224,1002,223,2,223,1006,224,359,101,1,223,223,108,677,677,224,1002,223,2,223,1006,224,374,1001,223,1,223,108,226,677,224,1002,223,2,223,1006,224,389,101,1,223,223,7,226,677,224,102,2,223,223,1006,224,404,1001,223,1,223,1108,677,677,224,1002,223,2,223,1005,224,419,101,1,223,223,1008,226,677,224,102,2,223,223,1006,224,434,101,1,223,223,107,226,226,224,102,2,223,223,1005,224,449,1001,223,1,223,1007,677,677,224,1002,223,2,223,1006,224,464,1001,223,1,223,1007,226,226,224,1002,223,2,223,1005,224,479,101,1,223,223,1008,226,226,224,102,2,223,223,1006,224,494,1001,223,1,223,8,226,226,224,102,2,223,223,1006,224,509,101,1,223,223,1107,677,677,224,102,2,223,223,1005,224,524,1001,223,1,223,1108,226,677,224,1002,223,2,223,1006,224,539,101,1,223,223,1107,677,226,224,1002,223,2,223,1006,224,554,101,1,223,223,1007,677,226,224,1002,223,2,223,1005,224,569,101,1,223,223,7,677,226,224,1002,223,2,223,1006,224,584,101,1,223,223,107,677,677,224,1002,223,2,223,1005,224,599,1001,223,1,223,8,226,677,224,1002,223,2,223,1005,224,614,101,1,223,223,7,677,677,224,1002,223,2,223,1006,224,629,1001,223,1,223,1107,226,677,224,1002,223,2,223,1006,224,644,101,1,223,223,108,226,226,224,102,2,223,223,1005,224,659,1001,223,1,223,8,677,226,224,1002,223,2,223,1005,224,674,101,1,223,223,4,223,99,226"


def map_args(program, args_list):
    res = []
    for arg, mode in args_list:
        if mode == 0:
            res.append(program[arg])
        if mode == 1:
            res.append(arg)

    if len(res) == 1:
        return res[0]

    return res

def handle_opcode(ins_pointer, opcode, program, arg_mode=None):
    if opcode == 1:
        p1, p2, p3 = program[ins_pointer + 1:ins_pointer + 4]

        if arg_mode == None:
            arg_mode = {'p1': 0, 'p2': 0, 'p3': 1}

        p1, p2, p3 = map_args(
            program,
            [(p1, arg_mode['p1']), (p2, arg_mode['p2']), (p3, arg_mode['p3'])]
        )
        program[p3] = p1 + p2
        return ins_pointer + 4
    if opcode == 2:
        p1, p2, p3 = program[ins_pointer + 1:ins_pointer + 4]

        if arg_mode == None:
            arg_mode = {'p1': 0, 'p2': 0, 'p3': 1}

        p1, p2, p3 = map_args(
            program,
            [(p1, arg_mode['p1']), (p2, arg_mode['p2']), (p3, arg_mode['p3'])]
        )
        program[p3] = p1 * p2
        return ins_pointer + 4
    if opcode == 3:
        p1 = program[ins_pointer + 1]

        if arg_mode == None:
            arg_mode = {'p1': 1}

        p1 = map_args(program, [(p1, arg_mode['p1'])])
        inp = input("Key in number: ")
        program[p1] = int(inp)
        return ins_pointer + 2
    if opcode == 4:
        p1 = program[ins_pointer + 1]

        if arg_mode == None:
            arg_mode = {'p1': 0}

        p1 = map_args(program, [(p1, arg_mode['p1'])])
        print(f"PROGRAM OUT: {p1}")
        return ins_pointer + 2
    if opcode == 5: # JUMP IF NOT ZERO
        p1, p2 = program[ins_pointer + 1: ins_pointer + 3]

        if arg_mode == None:
            arg_mode = {'p1': 0, 'p2': 0}

        p1, p2 = map_args(
            program,
            [(p1, arg_mode['p1']), (p2, arg_mode['p2'])]
        )
        if p1 != 0:
            return p2
        return ins_pointer + 3
    if opcode == 6:  # JUMP IF 0
        p1, p2 = program[ins_pointer + 1: ins_pointer + 3]

        if arg_mode == None:
            arg_mode = {'p1': 0, 'p2': 0}

        p1, p2 = map_args(
            program,
            [(p1, arg_mode['p1']), (p2, arg_mode['p2'])]
        )
        if p1 == 0:
            return p2
        return ins_pointer + 3
    if opcode == 7: # LESS THAN
        p1, p2, p3 = program[ins_pointer + 1:ins_pointer + 4]

        if arg_mode == None:
            arg_mode = {'p1': 0, 'p2': 0, 'p3': 1}

        p1, p2, p3 = map_args(
            program,
            [(p1, arg_mode['p1']), (p2, arg_mode['p2']), (p3, arg_mode['p3'])]
        )
        program[p3] = 1 if p1 < p2 else 0
        return ins_pointer + 4
    if opcode == 8: # EQUAL
        p1, p2, p3 = program[ins_pointer + 1:ins_pointer + 4]

        if arg_mode == None:
            arg_mode = {'p1': 0, 'p2': 0, 'p3': 1}

        p1, p2, p3 = map_args(
            program,
            [(p1, arg_mode['p1']), (p2, arg_mode['p2']), (p3, arg_mode['p3'])]
        )
        program[p3] = 1 if p1 == p2 else 0
        return ins_pointer + 4




def handle_complex_opcode(ins_pointer, cur_opcode, program):
    cur_opcode = str(cur_opcode)
    while len(cur_opcode) < 5:
        cur_opcode = '0' + cur_opcode
    p3, p2, p1 = cur_opcode[0:3]
    actual_opcode = int(cur_opcode[3:])
    arg_mode = {
        'p1': int(p1),
        'p2': int(p2),
        'p3': 1, # This always seems to be 1
    }
    return handle_opcode(ins_pointer, actual_opcode, program, arg_mode=arg_mode)


def run_program(program_input):
    original_program = program_input.split(",")
    original_program = [int(p) for p in original_program]

    ins_pointer = 0
    program = copy.deepcopy(original_program)

    while True:
        cur_opcode = program[ins_pointer]
        if cur_opcode == 99:
            break

        if len(str(cur_opcode)) == 1:
            ins_pointer = handle_opcode(ins_pointer, cur_opcode, program)
        else:
            ins_pointer = handle_complex_opcode(ins_pointer, cur_opcode, program)

run_program(program_input)
