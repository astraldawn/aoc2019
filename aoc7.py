from itertools import permutations

program_a = "3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0"
program_b = "3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0"
program_c = "3, 26, 1001,26,-4,26,3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5"
program_d = "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54, -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"
program_main = "3,8,1001,8,10,8,105,1,0,0,21,34,47,72,81,94,175,256,337,418,99999,3,9,102,3,9,9,1001,9,3,9,4,9,99,3,9,101,4,9,9,1002,9,5,9,4,9,99,3,9,1001,9,5,9,1002,9,5,9,1001,9,2,9,1002,9,5,9,101,5,9,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,1001,9,4,9,102,4,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99"

opcode_to_increment = {
    1: 4,
    2: 4,
    3: 2,
    4: 2,
    5: 3,
    6: 3,
    7: 4,
    8: 4,
}


class IntCodeComputer(object):
    def __init__(self,
                 computer_id,
                 input_program,
                 phase,
                 input_computer=None,
                 output_computer=None,
                 is_initial=False,
                 initial_input=0):
        # Inputs
        self.computer_id = computer_id
        self.phase = phase
        self.input_computer = input_computer
        self.output_computer = None
        self.is_initial = is_initial
        self.initial_input = initial_input

        # Program
        self.program = [int(p) for p in input_program.split(",")][:]

        # State
        self.ins_pointer = 0
        self.input_pointer = 0
        self.output = None
        self.is_running = False
        self.has_halt = False
        self.has_taken_input = False

    def __repr__(self):
        return f"{self.computer_id} {self.output} {self.has_halt}"

    def map_args(self, args_list):
        res = []
        for arg, mode in args_list:
            if mode == 0:
                res.append(self.program[arg])
            if mode == 1:
                res.append(arg)

        if len(res) == 1:
            return res[0]

        return res

    def handle_opcode(self, opcode, arg_mode=None):
        if opcode == 1:
            p1, p2, p3 = self.program[self.ins_pointer + 1:self.ins_pointer +
                                      4]

            if arg_mode == None:
                arg_mode = {'p1': 0, 'p2': 0, 'p3': 1}

            p1, p2, p3 = self.map_args([(p1, arg_mode['p1']),
                                        (p2, arg_mode['p2']),
                                        (p3, arg_mode['p3'])])
            self.program[p3] = p1 + p2
        if opcode == 2:
            p1, p2, p3 = self.program[self.ins_pointer + 1:self.ins_pointer +
                                      4]

            if arg_mode == None:
                arg_mode = {'p1': 0, 'p2': 0, 'p3': 1}

            p1, p2, p3 = self.map_args([(p1, arg_mode['p1']),
                                        (p2, arg_mode['p2']),
                                        (p3, arg_mode['p3'])])
            self.program[p3] = p1 * p2
        if opcode == 3:
            p1 = self.program[self.ins_pointer + 1]

            if arg_mode == None:
                arg_mode = {'p1': 1}

            p1 = self.map_args([(p1, arg_mode['p1'])])

            inp = 0
            if self.input_pointer == 0:
                inp = self.phase
                self.input_pointer += 1
            else:
                self.has_taken_input = True
                if self.is_initial:
                    inp = self.initial_input
                    self.is_initial = False
                else:
                    inp = self.input_computer.output

            self.program[p1] = inp
        if opcode == 4:
            # Halt after throwing output
            p1 = self.program[self.ins_pointer + 1]

            if arg_mode == None:
                arg_mode = {'p1': 0}

            p1 = self.map_args([(p1, arg_mode['p1'])])
            self.output = p1
        if opcode == 5:  # JUMP IF NOT ZERO
            p1, p2 = self.program[self.ins_pointer + 1:self.ins_pointer + 3]

            if arg_mode == None:
                arg_mode = {'p1': 0, 'p2': 0}

            p1, p2 = self.map_args([(p1, arg_mode['p1']),
                                    (p2, arg_mode['p2'])])
            if p1 != 0:
                return p2
        if opcode == 6:  # JUMP IF 0
            p1, p2 = self.program[self.ins_pointer + 1:self.ins_pointer + 3]

            if arg_mode == None:
                arg_mode = {'p1': 0, 'p2': 0}

            p1, p2 = self.map_args([(p1, arg_mode['p1']),
                                    (p2, arg_mode['p2'])])
            if p1 == 0:
                return p2
        if opcode == 7:  # LESS THAN
            p1, p2, p3 = self.program[self.ins_pointer + 1:self.ins_pointer +
                                      4]

            if arg_mode == None:
                arg_mode = {'p1': 0, 'p2': 0, 'p3': 1}

            p1, p2, p3 = self.map_args([(p1, arg_mode['p1']),
                                        (p2, arg_mode['p2']),
                                        (p3, arg_mode['p3'])])
            self.program[p3] = 1 if p1 < p2 else 0
        if opcode == 8:  # EQUAL
            p1, p2, p3 = self.program[self.ins_pointer + 1:self.ins_pointer +
                                      4]

            if arg_mode == None:
                arg_mode = {'p1': 0, 'p2': 0, 'p3': 1}

            p1, p2, p3 = self.map_args([(p1, arg_mode['p1']),
                                        (p2, arg_mode['p2']),
                                        (p3, arg_mode['p3'])])
            self.program[p3] = 1 if p1 == p2 else 0

        return self.ins_pointer + opcode_to_increment[opcode]

    def handle_complex_opcode(self, cur_opcode):
        cur_opcode = str(cur_opcode)
        while len(cur_opcode) < 5:
            cur_opcode = '0' + cur_opcode
        p3, p2, p1 = cur_opcode[0:3]
        actual_opcode = int(cur_opcode[3:])
        arg_mode = {
            'p1': int(p1),
            'p2': int(p2),
            'p3': 1,  # This always seems to be 1
        }
        return self.handle_opcode(actual_opcode, arg_mode=arg_mode)

    def run_program(self):
        while self.is_running:
            # print(f"{self.computer_id} {self.ins_pointer}")
            cur_opcode = self.program[self.ins_pointer]
            if cur_opcode == 99:
                self.is_running = False
                self.has_halt = True
                continue

            if len(str(cur_opcode)) == 1:
                if cur_opcode == 3 and self.has_taken_input:
                    self.is_running = False
                    self.has_taken_input = False
                    continue

                self.ins_pointer = self.handle_opcode(cur_opcode)
            else:
                if int(str(cur_opcode)[-2:]) == 3 and self.has_taken_input:
                    self.is_running = False
                    self.has_taken_input = False
                    continue

                self.ins_pointer = self.handle_complex_opcode(cur_opcode)


def run_intcode_with_phases(phase_combination, input_program, initial_input=0):
    max_output = 0

    for p in permutations(phase_combination):
        computers = []
        for computer_id, phase in enumerate(p):
            if computer_id == 0:
                computers.append(
                    IntCodeComputer(computer_id=computer_id,
                                    input_program=input_program,
                                    phase=phase,
                                    is_initial=True,
                                    initial_input=initial_input))
            else:
                computers.append(
                    IntCodeComputer(
                        computer_id=computer_id,
                        input_program=input_program,
                        phase=phase,
                    ))

        for i in range(0, 5):
            computers[i].output_computer = computers[(i + 1) %
                                                     len(phase_combination)]

        for i in range(0, 5):
            computers[i].input_computer = computers[(i - 1) %
                                                    len(phase_combination)]

        while True:
            computer_has_run = False
            for computer in computers:
                if not computer.has_halt:
                    computer.is_running = True
                    computer_has_run = True
                    computer.run_program()

            if not computer_has_run:
                break

        max_output = max(max_output, computers[-1].output)

    return max_output


def test_program():
    test_arr = [(
        ([5, 6, 7, 8, 9], program_c),
        139629729,
    ), (
        ([5, 6, 7, 8, 9], program_d),
        18216,
    ), (
        ([5, 6, 7, 8, 9], program_main),
        1047153,
    )]

    for inp, expected in test_arr:
        actual = run_intcode_with_phases(*inp)

        if actual == expected:
            print("OK")
        else:
            print(f"ERROR: actual: {actual} expected: {expected}")


test_program()
