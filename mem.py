class Memory:
    def __init__(self) -> None:
        self._memory = bytearray(4 * 1024)  # 4KB of memory
        self._fonts = (
            (0xF0, 0x90, 0x90, 0x90, 0xF0),  # 0
            (0x20, 0x60, 0x20, 0x20, 0x70),  # 1
            (0xF0, 0x10, 0xF0, 0x80, 0xF0),  # 2
            (0xF0, 0x10, 0xF0, 0x10, 0xF0),  # 3
            (0x90, 0x90, 0xF0, 0x10, 0x10),  # 4
            (0xF0, 0x80, 0xF0, 0x10, 0xF0),  # 5
            (0xF0, 0x80, 0xF0, 0x90, 0xF0),  # 6
            (0xF0, 0x10, 0x20, 0x40, 0x40),  # 7
            (0xF0, 0x90, 0xF0, 0x90, 0xF0),  # 8
            (0xF0, 0x90, 0xF0, 0x10, 0xF0),  # 9
            (0xF0, 0x90, 0xF0, 0x90, 0x90),  # A
            (0xE0, 0x90, 0xE0, 0x90, 0xE0),  # B
            (0xF0, 0x80, 0x80, 0x80, 0xF0),  # C
            (0xE0, 0x90, 0x90, 0x90, 0xE0),  # D
            (0xF0, 0x80, 0xF0, 0x80, 0xF0),  # E
            (0xF0, 0x80, 0xF0, 0x80, 0x80)   # F
        )
        self.load_fonts()

    @property
    def memory(self):
        return self._memory

    # loads the fonts into memory starting at location ox50. Seems to be the convention to start there

    def set_value(self, address, value) -> None:
        if address < 0 or address >= len(self._memory):
            raise ValueError("Address must be between 0 and 4095")
        if value < 0 or value > 0xFF:
            raise ValueError("Value must be between 0 and 255")
        self._memory[address] = value

    def get_value(self, address) -> int:
        if address < 0 or address >= len(self._memory):
            raise ValueError("Address must be between 0 and 4095")
        return self._memory[address]

    def load_fonts(self) -> None:
        index = 0x50
        for font in self._fonts:
            for byte in font:
                self._memory[index] = byte
                index += 1

    def load_program(self, rom_data):
        print("THIS IS THE ROM DATA BEING LOADED", rom_data)
        self._memory[0x200:0x200 + len(rom_data)] = rom_data

    def load_rom_data(self, rom_path):
        with open(rom_path, 'rb') as f:
            rom_data = bytearray(f.read())
        self.load_program(rom_data)

    def __str__(self) -> str:
        hex_memory = [f"{byte:02x}" for byte in self._memory]

        # Break the list into chunks of 10 elements
        chunks = [hex_memory[i:i + 50] for i in range(0, len(hex_memory), 50)]

        # Join each chunk into a string
        rows = [" ".join(chunk) for chunk in chunks]

        # Join the rows with newlines
        formatted_memory = "\n".join(rows)

        return f"MEMORY:\n{formatted_memory}"
