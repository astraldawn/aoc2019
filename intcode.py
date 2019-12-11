from collections import defaultdict, deque
from itertools import permutations, product

opcode_args_map = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    9: 1,
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
    9: [0],
}

READ, WRITE = "READ", "WRITE"
opcode_arg_op = {
    1: [READ, READ, WRITE],
    2: [READ, READ, WRITE],
    3: [WRITE],
    4: [READ],
    5: [READ, READ],
    6: [READ, READ],
    7: [READ, READ, WRITE],
    8: [READ, READ, WRITE],
    9: [READ],
}

opcode_increment_map = {
    opcode: args + 1
    for opcode, args in opcode_args_map.items()
}


class IntCodeComputer(object):
    def __init__(
        self,
        computer_id,
        input_program,
        input_computer=None,
        output_computer=None,
    ):
        # Inputs
        self.computer_id = computer_id
        self.input_computer = input_computer
        self.output_computer = output_computer
        self.input_queue = deque()
        self.output_queue = deque()

        # Program
        self.program = defaultdict(int)
        tmp_program = [int(p) for p in input_program.split(",")][:]
        for p, v in enumerate(tmp_program):
            self.program[p] = v

        # State
        self.last_output = None
        self.ins_pointer = 0
        self.has_halt = False
        self.relative_base = 0

    def __repr__(self):
        return f"{self.computer_id} {self.last_output} {self.has_halt}"

    def add_input(self, inp):
        self.input_queue.append(inp)

    def get_args_with_mode(self, opcode, opcode_args_list, args_mode_list):
        res = []
        for op, arg, mode in zip(opcode_arg_op[opcode], opcode_args_list,
                                 args_mode_list):
            mode = int(mode)
            if mode == 0:
                res.append(self.program[arg])
            if mode == 1:
                res.append(arg)
            if mode == 2:
                if op == WRITE:
                    res.append(arg + self.relative_base)
                else:
                    res.append(self.program[arg + self.relative_base])

        return res if len(res) > 1 else res[0]

    def handle_opcode(self, opcode, args_mode_list=None):
        opcode_args_list = [
            self.program[self.ins_pointer + i]
            for i in range(1, opcode_increment_map[opcode])
        ]

        if args_mode_list is None:
            args_mode_list = opcode_argmode_map[opcode]

        retrieved_args = self.get_args_with_mode(
            opcode,
            opcode_args_list,
            args_mode_list,
        )

        if opcode == 1:  # ADD (READ READ WRITE)
            p1, p2, p3 = retrieved_args
            self.program[p3] = p1 + p2
        if opcode == 2:  # MUL (READ READ WRITE)
            p1, p2, p3 = retrieved_args
            self.program[p3] = p1 * p2
        if opcode == 3:  # INPUT (WRITE)
            p1 = retrieved_args
            inp = self.input_queue.popleft()
            self.program[p1] = inp
        if opcode == 4:  # OUTPUT (READ)
            p1 = retrieved_args
            self.last_output = p1
            # self.output_computer.add_input(p1)  # Push to next computer
            self.output_queue.append(p1)
        if opcode == 5:  # JUMP IF NOT ZERO (READ READ)
            p1, p2 = retrieved_args
            if p1 != 0:
                return p2
        if opcode == 6:  # JUMP IF 0 (READ READ)
            p1, p2 = retrieved_args
            if p1 == 0:
                return p2
        if opcode == 7:  # LESS THAN (READ READ WRITE)
            p1, p2, p3 = retrieved_args
            self.program[p3] = 1 if p1 < p2 else 0
        if opcode == 8:  # EQUAL (READ READ WRITE)
            p1, p2, p3 = retrieved_args
            self.program[p3] = 1 if p1 == p2 else 0
        if opcode == 9:  # RELATIVE (READ)
            p1 = retrieved_args
            self.relative_base += p1

        return self.ins_pointer + opcode_increment_map[opcode]

    def handle_complex_opcode(self, cur_opcode):
        cur_opcode = str(cur_opcode)
        actual_opcode = int(cur_opcode[-2:])
        remaining_code = [int(x) for x in cur_opcode[:-2]][::-1]

        default_args = opcode_argmode_map[actual_opcode]
        if len(remaining_code) < len(default_args):
            for i in range(len(remaining_code), len(default_args)):
                remaining_code.append(default_args[i])

        args_mode_list = remaining_code
        return actual_opcode, args_mode_list

    def run(self):
        while True:
            cur_opcode, args_mode_list = self.program[self.ins_pointer], None
            if cur_opcode == 99:
                self.has_halt = True
                break

            if len(str(cur_opcode)) > 2:
                cur_opcode, args_mode_list = self.handle_complex_opcode(
                    cur_opcode)

            if cur_opcode == 3 and not self.input_queue:
                break

            self.ins_pointer = self.handle_opcode(cur_opcode, args_mode_list)
