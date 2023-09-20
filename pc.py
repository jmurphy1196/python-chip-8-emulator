class ProgramCounter:
    def __init__(self) -> None:
        self._pc = 0x200  # program counter starts at 0x200

    def fetch_instruction(self, memory) -> int:
        # fetch the instruction from memory
        high_byte = memory.memory[self._pc] << 8
        low_byte = memory.memory[self._pc + 1]
        instruction = high_byte | low_byte
        # increment the program counter
        self._pc += 2
        # return the instruction
        return instruction

    def increment(self, value=2) -> None:
        self._pc += value

    def set_value(self, value):
        self._pc = value

    @property
    def pc(self):
        return self._pc
