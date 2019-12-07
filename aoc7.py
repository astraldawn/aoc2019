from collections import deque
from itertools import permutations

program_a = "3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0"
program_b = "3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0"
program_c = "3, 26, 1001,26,-4,26,3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5"
program_d = "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54, -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"
program_main = "3,8,1001,8,10,8,105,1,0,0,21,34,47,72,81,94,175,256,337,418,99999,3,9,102,3,9,9,1001,9,3,9,4,9,99,3,9,101,4,9,9,1002,9,5,9,4,9,99,3,9,1001,9,5,9,1002,9,5,9,1001,9,2,9,1002,9,5,9,101,5,9,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,1001,9,4,9,102,4,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99"

opcode_args_map = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
}
opcode_argmode_map = {
    1: [0, 0, 1],
    2: [0, 0, 1],
    3: [1],
    4: [0],
    5: [0, 0],
    6: [0, 0],
    7: [0, 0, 1],
    8: [0, 0, 1],
}

opcode_increment_map = {
    opcode: args + 1
    for opcode, args in opcode_args_map.items()
}


class IntCodeComputer(object):
    def __init__(self,
                 computer_id,
                 input_program,
                 input_computer=None,
                 output_computer=None,
                 is_initial=False,
                 initial_input=0):
        # Inputs
        self.computer_id = computer_id
        self.input_computer = input_computer
        self.output_computer = output_computer
        self.input_queue = deque()

        # Program
        self.program = [int(p) for p in input_program.split(",")][:]

        # State
        self.last_output = None
        self.ins_pointer = 0
        self.has_halt = False

    def __repr__(self):
        return f"{self.computer_id} {self.last_output} {self.has_halt}"

    def add_input(self, inp):
        self.input_queue.append(inp)

    def get_args_with_mode(self, opcode_args_list, args_mode_list):
        res = []
        for arg, mode in zip(opcode_args_list, args_mode_list):
            mode = int(mode)
            if mode == 0:
                res.append(self.program[arg])
            if mode == 1:
                res.append(arg)

        return res if len(res) > 1 else res[0]

    def handle_opcode(self, opcode, args_mode_list=None):
        opcode_args_list = self.program[self.ins_pointer + 1:self.ins_pointer +
                                        opcode_increment_map[opcode]]
        if args_mode_list is None:
            args_mode_list = opcode_argmode_map[opcode]

        retrieved_args = self.get_args_with_mode(
            opcode_args_list,
            args_mode_list,
        )

        if opcode == 1:
            p1, p2, p3 = retrieved_args
            self.program[p3] = p1 + p2
        if opcode == 2:
            p1, p2, p3 = retrieved_args
            self.program[p3] = p1 * p2
        if opcode == 3:
            p1 = retrieved_args
            inp = self.input_queue.popleft()
            self.program[p1] = inp
        if opcode == 4:
            p1 = retrieved_args
            self.last_output = p1
            self.output_computer.add_input(p1)  # Push to next computer
        if opcode == 5:  # JUMP IF NOT ZERO
            p1, p2 = retrieved_args
            if p1 != 0:
                return p2
        if opcode == 6:  # JUMP IF 0
            p1, p2 = retrieved_args
            if p1 == 0:
                return p2
        if opcode == 7:  # LESS THAN
            p1, p2, p3 = retrieved_args
            self.program[p3] = 1 if p1 < p2 else 0
        if opcode == 8:  # EQUAL
            p1, p2, p3 = retrieved_args
            self.program[p3] = 1 if p1 == p2 else 0

        return self.ins_pointer + opcode_increment_map[opcode]

    def handle_complex_opcode(self, cur_opcode):
        cur_opcode = str(cur_opcode)
        while len(cur_opcode) < 5:
            cur_opcode = '0' + cur_opcode
        p3, p2, p1 = cur_opcode[0:3]
        actual_opcode = int(cur_opcode[3:])
        args_mode_list = [p1, p2, 1]
        return actual_opcode, args_mode_list

    def run(self):
        while True:
            cur_opcode, args_mode_list = self.program[self.ins_pointer], None
            if cur_opcode == 99:
                self.has_halt = True
                break

            if len(str(cur_opcode)) > 1:
                cur_opcode, args_mode_list = self.handle_complex_opcode(
                    cur_opcode)

            if cur_opcode == 3 and not self.input_queue:
                break

            self.ins_pointer = self.handle_opcode(cur_opcode, args_mode_list)


def run_intcode_with_phases(phase_list, input_program, initial_input=0):
    max_output = 0

    for phase_perm in permutations(phase_list):
        computers = []
        for computer_id, phase in enumerate(phase_perm):
            cur_computer = IntCodeComputer(
                computer_id=computer_id,
                input_program=input_program,
            )
            cur_computer.add_input(phase)
            computers.append(cur_computer)

        for i in range(0, 5):
            computers[i].output_computer = computers[(i + 1) % len(phase_list)]
            computers[i].input_computer = computers[(i - 1) % len(phase_list)]

        computers[0].add_input(initial_input)
        while True:
            computer_has_run = False
            for computer in computers:
                if not computer.has_halt:
                    computer_has_run = True
                    computer.run()

            if not computer_has_run:
                break

        max_output = max(max_output, computers[-1].last_output)

    return max_output


def test_program():
    test_arr = [
        (
            ([5, 6, 7, 8, 9], program_c),
            139629729,
        ),
        (
            ([5, 6, 7, 8, 9], program_d),
            18216,
        ),
        (
            ([5, 6, 7, 8, 9], program_main),
            1047153,
        ),
    ]

    for inp, expected in test_arr:
        actual = run_intcode_with_phases(*inp)

        if actual == expected:
            print("OK")
        else:
            print(f"ERROR: actual: {actual} expected: {expected}")


test_program()
