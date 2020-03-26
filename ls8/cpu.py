"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        # self.pc = 0

    def load(self, file_name):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        file = open("examples/" + file_name)

        for instruction in [x[:8] for x in file.read().split("\n")]:
            if(instruction.strip() == "" or instruction[0] == "#"):
                continue

            self.ram[address] = int(instruction, 2)
            address += 1

        file.close()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif asm == "SUB":
            self.registers[reg_a] -= self.registers[reg_b]
        elif asm == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
        elif asm == "MOD":
            self.registers[reg_a] *= self.registers[reg_b]
        # elif asm == "CMP":
        #     self.reg[reg_a] *= self.reg[reg_b]
        
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(idx):
        return self.memory[idx]

    def ram_write(idx, val):
        self.memory[idx] = val

    def opcode_to_asm(self, opcode):
        return {
            0b10100000: "ADD",
            0b10100001: "SUB",
            0b10100010: "MUL",
            0b10100011: "DIV",
            0b10100100: "MOD",
            0b01100101: "INC",
            0b01100110: "DEC",
            0b10100111: "CMP",
            0b10101000: "AND",
            0b01101001: "NOT",
            0b10101010: "OR",
            0b10101011: "XOR",
            0b10101100: "SHL",
            0b10101101: "SHR",
            0b01010000: "CALL",
            0b00010001: "RET",
            0b01010010: "INT",
            0b00010011: "IRET",
            0b01010100: "JMP",
            0b01010101: "JEQ",
            0b01010110: "JNE",
            0b01010111: "JGT",
            0b01011000: "JLT",
            0b01011001: "JLE",
            0b01011010: "JGE",
            0b00000000: "NOP",
            0b00000001: "HLT",
            0b10000010: "LDI",
            0b10000011: "LD",
            0b10000100: "ST",
            0b01000101: "PUSH",
            0b01000110: "POP",
            0b01000111: "PRN",
            0b01001000: "PRA",
        }[opcode]

    def is_alu_instruction(self, asm):
        return asm in ["ADD", "SUB", "CMP", "MOD", "MUL", "DIV"]

    def run(self):
        """Run the CPU."""
        # ir = 0
        pc = 0
        asm = ""
        self.registers[6] = len(self.ram) - 1 #stack pointer

        i = 0
        
        while asm != "HLT" and i < 30:
            i += 1
            asm = self.opcode_to_asm(self.ram[pc])
            
            if self.is_alu_instruction(asm):
                self.alu(asm, self.ram[pc + 1], self.ram[pc + 2])
                pc += 3
            elif asm == "LDI":
                self.registers[self.ram[pc + 1]] = self.ram[pc + 2]
                pc += 3
            elif asm == "PRN":
                print(self.registers[self.ram[pc + 1]])
                pc += 2
            # elif asm == "ADD":
            #     self.registers[self.ram[pc + 1]] += self.registers[self.ram[pc + 2]]
            #     pc += 3
            # elif asm == "SUB":
            #     self.registers[self.ram[pc + 1]] -= self.registers[self.ram[pc + 2]]
            #     pc += 3
            # elif asm == "MUL":
            #     self.registers[self.ram[pc + 1]] *= self.registers[self.ram[pc + 2]]
            #     pc += 3
            elif asm == "PUSH":
                self.registers[6] -= 1
                self.ram[self.registers[6]] = self.registers[self.ram[pc + 1]]
                pc += 2
            elif asm == "POP":
                self.registers[self.ram[pc + 1]] = self.ram[self.registers[6]]
                self.registers[6] += 1
                pc += 2
            elif asm == "CALL":
                self.registers[6] -= 1
                self.ram[self.registers[6]] = pc + 2 #store the value of next instruction to return to
                pc = self.registers[self.ram[pc + 1]]
            elif asm == "RET":
                pc = self.ram[self.registers[6]]
                self.registers[6] += 1
            elif asm == "JMP":
                pc = self.registers[self.ram[pc + 1]]

c = CPU()
c.load("call.ls8")
c.run()