from collections import deque, defaultdict
from itertools import permutations

program_day5_1 = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
program_a = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
program_b = "1102,34915192,34915192,7,4,7,99,0"
program_c = "104,1125899906842624,99"
program_main = "1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1101,3,0,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1102,1,37,1000,1101,856,0,1029,1101,286,0,1025,1101,39,0,1004,1101,861,0,1028,1101,845,0,1026,1102,28,1,1002,1102,1,0,1020,1101,0,892,1023,1101,0,291,1024,1101,35,0,1018,1101,0,27,1006,1102,1,26,1011,1101,33,0,1019,1102,31,1,1014,1102,1,36,1010,1102,23,1,1007,1101,0,32,1016,1101,29,0,1008,1101,20,0,1001,1102,1,25,1015,1101,38,0,1017,1101,0,24,1012,1102,1,22,1005,1101,1,0,1021,1101,0,21,1003,1102,1,838,1027,1102,1,30,1013,1101,895,0,1022,1101,0,34,1009,109,7,1208,0,22,63,1005,63,201,1001,64,1,64,1105,1,203,4,187,1002,64,2,64,109,-6,2102,1,5,63,1008,63,24,63,1005,63,223,1105,1,229,4,209,1001,64,1,64,1002,64,2,64,109,17,21102,40,1,-6,1008,1012,40,63,1005,63,255,4,235,1001,64,1,64,1106,0,255,1002,64,2,64,109,-15,21108,41,41,9,1005,1012,277,4,261,1001,64,1,64,1106,0,277,1002,64,2,64,109,11,2105,1,10,4,283,1105,1,295,1001,64,1,64,1002,64,2,64,109,-9,21101,42,0,8,1008,1013,44,63,1005,63,315,1105,1,321,4,301,1001,64,1,64,1002,64,2,64,109,13,1206,3,337,1001,64,1,64,1106,0,339,4,327,1002,64,2,64,109,-10,1208,0,29,63,1005,63,361,4,345,1001,64,1,64,1106,0,361,1002,64,2,64,109,2,2108,27,-4,63,1005,63,383,4,367,1001,64,1,64,1105,1,383,1002,64,2,64,109,-4,1207,2,30,63,1005,63,405,4,389,1001,64,1,64,1105,1,405,1002,64,2,64,109,22,1205,-8,417,1106,0,423,4,411,1001,64,1,64,1002,64,2,64,109,-27,2108,19,0,63,1005,63,443,1001,64,1,64,1106,0,445,4,429,1002,64,2,64,109,13,21108,43,45,-1,1005,1013,461,1106,0,467,4,451,1001,64,1,64,1002,64,2,64,109,1,21107,44,45,4,1005,1019,485,4,473,1105,1,489,1001,64,1,64,1002,64,2,64,109,-8,2102,1,-7,63,1008,63,37,63,1005,63,515,4,495,1001,64,1,64,1106,0,515,1002,64,2,64,109,1,2107,38,-4,63,1005,63,533,4,521,1105,1,537,1001,64,1,64,1002,64,2,64,109,4,21107,45,44,1,1005,1013,553,1106,0,559,4,543,1001,64,1,64,1002,64,2,64,109,-7,2107,21,-4,63,1005,63,575,1106,0,581,4,565,1001,64,1,64,1002,64,2,64,109,9,1205,7,599,4,587,1001,64,1,64,1105,1,599,1002,64,2,64,109,-11,2101,0,-3,63,1008,63,40,63,1005,63,619,1105,1,625,4,605,1001,64,1,64,1002,64,2,64,109,1,2101,0,-2,63,1008,63,28,63,1005,63,651,4,631,1001,64,1,64,1106,0,651,1002,64,2,64,109,1,21102,46,1,7,1008,1012,44,63,1005,63,671,1106,0,677,4,657,1001,64,1,64,1002,64,2,64,109,4,1201,-7,0,63,1008,63,28,63,1005,63,699,4,683,1105,1,703,1001,64,1,64,1002,64,2,64,109,-6,1207,-3,36,63,1005,63,719,1105,1,725,4,709,1001,64,1,64,1002,64,2,64,109,-4,1201,6,0,63,1008,63,23,63,1005,63,745,1106,0,751,4,731,1001,64,1,64,1002,64,2,64,109,8,1202,-6,1,63,1008,63,20,63,1005,63,777,4,757,1001,64,1,64,1105,1,777,1002,64,2,64,109,5,1202,-5,1,63,1008,63,25,63,1005,63,801,1001,64,1,64,1105,1,803,4,783,1002,64,2,64,109,8,21101,47,0,-6,1008,1014,47,63,1005,63,829,4,809,1001,64,1,64,1106,0,829,1002,64,2,64,109,1,2106,0,6,1001,64,1,64,1106,0,847,4,835,1002,64,2,64,109,11,2106,0,-4,4,853,1105,1,865,1001,64,1,64,1002,64,2,64,109,-15,1206,3,883,4,871,1001,64,1,64,1106,0,883,1002,64,2,64,109,14,2105,1,-8,1105,1,901,4,889,1001,64,1,64,4,64,99,21102,1,27,1,21102,1,915,0,1106,0,922,21201,1,57564,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21102,1,942,0,1105,1,922,22101,0,1,-1,21201,-2,-3,1,21101,957,0,0,1105,1,922,22201,1,-1,-2,1106,0,968,21202,-2,1,-2,109,-3,2106,0,0"

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

READ, WRITE = 'READ', 'WRITE'
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
        for op, arg, mode in zip(opcode_arg_op[opcode], opcode_args_list, args_mode_list):
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

        if opcode == 1: # ADD (READ READ WRITE)
            p1, p2, p3 = retrieved_args
            self.program[p3] = p1 + p2
        if opcode == 2: # MUL (READ READ WRITE)
            p1, p2, p3 = retrieved_args
            self.program[p3] = p1 * p2
        if opcode == 3: # INPUT (WRITE)
            p1 = retrieved_args
            inp = self.input_queue.popleft()
            self.program[p1] = inp
        if opcode == 4: # OUTPUT (READ)
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
        if opcode == 9: # RELATIVE (READ)
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


def aoc_day9(input_program, initial_input=0):
    computer = IntCodeComputer(
        computer_id=1,
        input_program=input_program,
    )

    computer.add_input(initial_input)
    computer.run()

    print(computer.output_queue)

    return 0


def test_program():
    test_arr = [
        (
            (program_a, 0),
            139629729,
        ),
        (
            (program_b, 0),
            5,
        ),
        (
            (program_c, 0),
            5,
        ),
        (
            (program_day5_1, 5),
            1,
        ),
        (
            (program_main, 1),
            5,
        ),
        (
            (program_main, 2),
            5,
        )
    ]

    for inp, expected in test_arr:
        actual = aoc_day9(*inp)

        if actual == expected:
            print("OK")
        else:
            print(f"ERROR: actual: {actual} expected: {expected}")


test_program()
