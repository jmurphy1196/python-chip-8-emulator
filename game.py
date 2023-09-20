from screen import Screen
from cpu import CPU
from mem import Memory
from keypad import Keypad
import pygame
import os


class Game:

    def __init__(self, rom) -> None:
        pygame.init()
        self._speed = 1  # speed of the game, instructions can be given 700 times a second speed = 1 = 700 instructions per second
        self._screen = Screen(scale=20)
        self._memory = Memory()
        self._keypad = Keypad()
        self._cpu = CPU(self._memory, self._screen, self._keypad)
        self.rom = rom

    def run(self):
        running = True
        clock = pygame.time.Clock()
        self._screen.create_window()
        self._memory.load_rom_data(
            f"{os.getcwd()}/roms/{self.rom}")

        print(str(self._memory))
        print("=====================================")
        print("=====================================")
        print("=====================================")

        while running:
            clock.tick(self._speed * 700)
            # run cpu cycle
            self._screen.draw_screen()
            self._cpu.cycle()
            self._cpu.cycle()
            self._cpu.cycle()
            self._cpu.cycle()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()
        pygame.quit()
