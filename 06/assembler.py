import math
import re
import sys

pre_defined_symbols_table = {
    "R0": 0, 
    "R1": 1, 
    "R2": 2, 
    "R3": 3, 
    "R4": 4, 
    "R5": 5, 
    "R6": 6, 
    "R7": 7, 
    "R8": 8, 
    "R9": 9, 
    "R10": 10, 
    "R11": 11, 
    "R12": 12, 
    "R13": 13, 
    "R14": 14, 
    "R15": 15,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576
}

class CompData:
    def __init__(self, comp_bits, a_bit):
        self.comp_bits = comp_bits
        self.a_bit = a_bit

    def get_data(self):
        return self.comp_bits, self.a_bit
        
comp_table = {
    "0": CompData("101010", "0"),
    "1": CompData("111111", "0"),
    "-1": CompData("111010", "0"),
    "D": CompData("001100", "0"),
    "A": CompData("110000", "0"),
    "!D": CompData("001101", "0"),
    "!A": CompData("110001", "0"),
    "-D": CompData("001111", "0"),
    "-A": CompData("110011", "0"),
    "D+1": CompData("011111", "0"),
    "A+1": CompData("110111", "0"),
    "D-1": CompData("001110", "0"),
    "A-1": CompData("110010", "0"),
    "D+A": CompData("000010", "0"),
    "D-A": CompData("010011", "0"),
    "A-D": CompData("000111", "0"),
    "D&A": CompData("000000", "0"),
    "D|A": CompData("010101", "0"),
    "M": CompData("110000", "1"),
    "!M": CompData("110001", "1"),
    "-M": CompData("110011", "1"),
    "M+1": CompData("110111", "1"),
    "M-1": CompData("110010", "1"),
    "D+M": CompData("000010", "1"),
    "D-M": CompData("010011", "1"),
    "M-D": CompData("000111", "1"),
    "D&M": CompData("000000", "1"),
    "D|M": CompData("010101", "1")
}

dest_table = {
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

jump_table = {
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

def parse_valid_lines(lines):
    valid_lines = []
    
    for line in lines:
        pattern = re.compile(r'\s+')
        line_with_no_white_space_or_comments = re.sub(pattern, '', line)

        if line_with_no_white_space_or_comments.startswith("//") or line_with_no_white_space_or_comments == "":
            continue
        if "//" in line:
            i = line_with_no_white_space_or_comments.index("//")
            line_with_no_white_space_or_comments= line_with_no_white_space_or_comments[0:i]
        
        valid_lines.append(line_with_no_white_space_or_comments)

    return valid_lines

def decimal_to_binary(decimal):
    assert decimal <= math.pow(2, 15) and decimal >= 0

    bits = []

    while decimal > 0:
        bit = decimal % 2
        decimal = decimal // 2
        bits.append(str(bit))

    bits.reverse()

    return "".join(bits)

def pad_zeros(binary_number, n = 15):
    assert n >= len(binary_number)
    num_zeros_to_pad = n - len(binary_number)
    return "0" * num_zeros_to_pad + binary_number

class Assembler:
    def __init__(self, file_path, out_file_path):
        assert file_path
        assert out_file_path

        self.file_path = file_path
        self.source_code_lines = None
        self.symbols_table = {}
        self.symbols_table.update(pre_defined_symbols_table)
        self.machine_code = []
        self.symbol_allocation_pointer = 16
        self.out_file_path = out_file_path
            
    def load_source_code_lines(self):
        source_code = open(self.file_path, "r")
        self.source_code_lines = parse_valid_lines(source_code.readlines())

    def load_label_symbols_table(self):
        assert self.source_code_lines != None

        label_symbols_table = {}

        source_code_lines_without_labels = []

        decrement_count = 0

        for index, line in enumerate(self.source_code_lines):
            if line.startswith("(") and line.endswith(")"):
                label = line[1:-1]
                label_symbols_table[label] = index - decrement_count
                decrement_count += 1
            else:
                source_code_lines_without_labels.append(line)

        self.symbols_table.update(label_symbols_table)
        self.source_code_lines = source_code_lines_without_labels

    def assemble(self):
        assert not self.machine_code

        for line in self.source_code_lines:
            if line.startswith("@"):
                self.machine_code.append(self.convert_a_instruction(line[1:]))
            else:
                self.machine_code.append(self.convert_c_instruction(line))

    def write_assembled_machine_code(self):
        assert self.machine_code
        f = open(self.out_file_path, "w")
        f.write("\n".join(self.machine_code))

    def convert_c_instruction(self, line):
        assert ";" in line or "=" in line

        dest_bits = "000"
        jump_bits = "000"
        comp_bits = None
        a_bit = None

        if ";" in line:
            comp, jump = line.split(";")
            
            assert comp in comp_table
            assert jump in jump_table

            comp_data = comp_table[comp]
            comp_bits, a_bit = comp_data.get_data()
            jump_bits = jump_table[jump]
        elif "=" in line:
            dest, comp = line.split("=")

            assert dest in dest_table
            assert comp in comp_table

            comp_data = comp_table[comp]
            comp_bits, a_bit = comp_data.get_data()
            dest_bits = dest_table[dest]

        return "111" + a_bit + comp_bits + dest_bits + jump_bits        

    def convert_a_instruction(self, symbol):
        number_to_convert = None

        if symbol.isnumeric():
            number_to_convert = int(symbol)
            assert number_to_convert >= 0
        elif symbol in self.symbols_table:
            number_to_convert = int(self.symbols_table[symbol])
        else:
            self.symbols_table[symbol] = self.symbol_allocation_pointer
            number_to_convert = int(self.symbol_allocation_pointer)
            self.symbol_allocation_pointer += 1

        return "0" + pad_zeros(decimal_to_binary(number_to_convert))

    def run(self):
        self.load_source_code_lines()
        self.load_label_symbols_table()
        self.assemble()
        self.write_assembled_machine_code()

in_file_path = sys.argv[1]
out_file_path = sys.argv[2]

assembler = Assembler(in_file_path, out_file_path)
assembler.run()


