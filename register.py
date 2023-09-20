class IndexRegister:
    def __init__(self) -> None:
        self._register = bytearray(2)

    def set_value(self, value: int) -> None:
        if value < 0 or value > 0xFFFF:
            raise ValueError("Value must be between 0 and 65535")
        self._register[0] = value >> 8
        self._register[1] = value & 0xFF

    def get_value(self) -> int:
        return (self._register[0] << 8) | self._register[1]


class GeneralPurposeRegisters:
    def __init__(self) -> None:
        self._registers = bytearray(16)  # 16 8-bit registers

    def set_value(self, index: int, value: int) -> None:
        if index < 0 or index > 15:
            raise ValueError("Index must be between 0 and 15")
        if value < 0 or value > 0xFF:
            raise ValueError("Value must be between 0 and 255")
        self._registers[index] = value

    def get_value(self, index: int) -> int:
        if index < 0 or index > 15:
            raise ValueError("Index must be between 0 and 15")
        return self._registers[index]

    def set_flag(self, value: int) -> None:
        # 16th register is the typically the flag register
        self._registers[15] = value

    def get_flag(self, value: int) -> None:
        return self._registers[15]
