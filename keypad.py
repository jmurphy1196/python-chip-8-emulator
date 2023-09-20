import pygame


class Keypad:
    def __init__(self) -> None:
        self._keys = (
            '1', '2', '3', 'C',
            '4', '5', '6', 'D',
            '7', '8', '9', 'E',
            'A', '0', 'B', 'F'
        )
        self._keys_map = {
            '1': 0x1, '2': 0x2, '3': 0x3, 'C': 0xC,
            '4': 0x4, '5': 0x5, '6': 0x6, 'D': 0xD,
            '7': 0x7, '8': 0x8, '9': 0x9, 'E': 0xE,
            'A': 0xA, '0': 0x0, 'B': 0xB, 'F': 0xF,

        }
        self._qwerty_to_chip8 = {
            '1': 0x1, '2': 0x2, '3': 0x3, '4': 0xC,
            'q': 0x4, 'w': 0x5, 'e': 0x6, 'r': 0xD,
            'a': 0x7, 's': 0x8, 'd': 0x9, 'f': 0xE,
            'z': 0xA, 'x': 0x0, 'c': 0xB, 'v': 0xF,
        }

    @property
    def get_querty_to_chip8(self):
        return self._qwerty_to_chip8

    def wait_for_key_press(self):
        while True:
            for event in pygame.event.get(pygame.KEYDOWN):
                if event.type == pygame.KEYDOWN:
                    chip8_key = self._qwerty_to_chip8.get(
                        pygame.key.name(event.key))
                    if chip8_key is not None:
                        return chip8_key
