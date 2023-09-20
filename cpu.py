from mem import Memory
from screen import Screen
from pc import ProgramCounter
from register import GeneralPurposeRegisters, IndexRegister
from keypad import Keypad
import random
import pygame

from timer import Timer, SoundTimer


class CPU:
    def __init__(self, memory: Memory, screen: Screen, keypad: Keypad):
        self.index_register = IndexRegister()
        self._stack = []  # stack holds up to 16bit numbers which are addresses for functions
        self.gp_registers = GeneralPurposeRegisters()
        self.pc = ProgramCounter()
        self.memory = memory
        self.screen = screen
        self.keypad = keypad
        self.timer = Timer(0)
        self.sound_timer = SoundTimer(0)

    def cycle(self):
        # Fetch
        instruction = self.pc.fetch_instruction(self.memory)
        # Decode and Execute
        self.timer.decrement()
        self.sound_timer.decrement()
        self.decode_and_execute(instruction)

    def decode_and_execute(self, instruction):
        # Extract the different parts of the instruction
        first_nibble = (instruction & 0xF000) >> 12
        X = (instruction & 0x0F00) >> 8
        Y = (instruction & 0x00F0) >> 4
        N = instruction & 0x000F
        NN = instruction & 0x00FF
        NNN = instruction & 0x0FFF

        # Decode based on the first nibble
        if first_nibble == 0x1:

            self.pc.set_value(NNN)
        elif first_nibble == 0xA:

            self.index_register.set_value(NNN)
        elif first_nibble == 0x6:

            self.gp_registers.set_value(X, NN)
        elif instruction == 0x00E0:
            self.screen.clear_screen()
        elif (instruction & 0xF000) == 0x7000:
            new_value = (self.gp_registers.get_value(X) + NN) % 256
            self.gp_registers.set_value(X, new_value)
        elif (instruction & 0xF000) == 0xD000:
            x = self.gp_registers.get_value((instruction & 0x0F00) >> 8)
            y = self.gp_registers.get_value((instruction & 0x00F0) >> 4)
            n = instruction & 0x000F
            sprite = [self.memory.get_value(self.index_register.get_value() + i)
                      for i in range(n)]
            collision = self.screen.draw_sprite(x, y, sprite)
            self.gp_registers.set_value(0xF, 1 if collision else 0)

        elif (instruction & 0xF000) == 0x3000:
            if self.gp_registers.get_value(X) == NN:
                self.pc.increment()
        elif (instruction & 0xF000) == 0x4000:
            if self.gp_registers.get_value(X) != NN:
                self.pc.increment()
        elif (instruction & 0xF00F) == 0x5000:
            if self.gp_registers.get_value(X) == self.gp_registers.get_value(Y):
                self.pc.increment()
        elif (instruction & 0xF000) == 0x6000:
            self.gp_registers.set_value(X, NN)
        elif (instruction & 0xF00F) == 0x8000:
            self.gp_registers.set_value(X, self.gp_registers.get_value(Y))
        elif (instruction & 0xF00F) == 0x8001:
            self.gp_registers.set_value(X, self.gp_registers.get_value(
                Y) | self.gp_registers.get_value(X))
        elif (instruction & 0xF00F) == 0x8002:
            self.gp_registers.set_value(X, self.gp_registers.get_value(
                Y) & self.gp_registers.get_value(X))
        elif (instruction & 0xF00F) == 0x8003:
            self.gp_registers.set_value(X, self.gp_registers.get_value(
                Y) ^ self.gp_registers.get_value(X))
        elif (instruction & 0xF00F) == 0x8004:
            sum_value = self.gp_registers.get_value(
                X) + self.gp_registers.get_value(Y)

            # check the carry. If the sum is greater than 255, then there is a carry (8bit register)
            if sum_value > 255:
                self.gp_registers.set_flag(1)
                sum_value &= 0xFF
            else:
                self.gp_registers.set_flag(0)
            self.gp_registers.set_value(X, sum_value)
        elif (instruction & 0xF00F) == 0x8005:
            vx_value = self.gp_registers.get_value(X)
            vy_value = self.gp_registers.get_value(Y)
            diff_value = vx_value - vy_value

            if diff_value < 0:
                self.gp_registers.set_flag(0)
                diff_value += 256
            else:
                self.gp_registers.set_flag(1)

            self.gp_registers.set_value(X, diff_value)

        elif (instruction & 0xF00F) == 0x8006:
            self.gp_registers.set_flag(self.gp_registers.get_value(X) & 1)
            self.gp_registers.set_value(X, self.gp_registers.get_value(X) >> 1)
        elif (instruction & 0xF00F) == 0x8007:
            vx_value = self.gp_registers.get_value(X)
            vy_value = self.gp_registers.get_value(Y)
            diff_value = vy_value - vx_value

            if diff_value < 0:
                self.gp_registers.set_flag(0)
                diff_value &= 0xFF
            else:
                self.gp_registers.set_flag(1)

            self.gp_registers.set_value(X, diff_value)
        elif (instruction & 0xF00F) == 0x800E:
            vx_value = self.gp_registers.get_value(X)

            self.gp_registers.set_flag((vx_value & 0x80) >> 7)

            new_value = (vx_value << 1) & 0xFF

            self.gp_registers.set_value(X, new_value)

        elif (instruction & 0xF00F) == 0x9000:
            if self.gp_registers.get_value(X) != self.gp_registers.get_value(Y):
                self.pc.increment()
        elif (instruction & 0xF000) == 0xA000:
            self.index_register.set_value(NNN)
        elif (instruction & 0xF000) == 0xB000:
            self.pc._pc = NNN + self.gp_registers.get_value(0)
        elif (instruction & 0xF000) == 0xC000:
            self.gp_registers.set_value(X, random.randint(0, 255) & NN)
        elif (instruction & 0xF0FF) == 0xE09E:
            key_value = self.gp_registers.get_value(X)
            qwerty_key = [
                k for k, v in self.keypad._qwerty_to_chip8.items() if v == key_value][0]
            keys = pygame.key.get_pressed()
            qwerty_key_index = pygame.key.key_code(qwerty_key.upper())

            if keys[qwerty_key_index]:
                self.pc.increment()

        elif (instruction & 0xF0FF) == 0xE0A1:
            key_value = self.gp_registers.get_value(X)
            qwerty_key = [
                k for k, v in self.keypad._qwerty_to_chip8.items() if v == key_value][0]
            keys = pygame.key.get_pressed()
            qwerty_key_index = pygame.key.key_code(qwerty_key.upper())

            if not keys[qwerty_key_index]:
                self.pc.increment()

        elif (instruction & 0xF0FF) == 0xF007:
            self.gp_registers.set_value(X, self.timer.value)

        elif (instruction & 0xF0FF) == 0xF00A:
            pressed_key = self.keypad.wait_for_key_press()
            self.gp_registers.set_value(X, pressed_key)
        elif (instruction & 0xF0FF) == 0xF015:
            self.timer.value = self.gp_registers.get_value(X)
        elif (instruction & 0xF0FF) == 0xF018:
            self.sound_timer.value = self.gp_registers.get_value(X)
        elif (instruction & 0xF0FF) == 0xF01E:
            self.index_register.set_value(
                self.index_register.get_value() + self.gp_registers.get_value(X))
        elif (instruction & 0xF0FF) == 0xF029:
            digit = self.gp_registers.get_value(X)
            sprite_location = 0x50 + (5 * digit)
            self.index_register.set_value(sprite_location)

        elif (instruction & 0xF0FF) == 0xF033:
            val = self.gp_registers.get_value(X)
            self.memory.set_value(self.index_register.get_value(), val // 100)
            self.memory.set_value(
                self.index_register.get_value() + 1, (val % 100) // 10)
            self.memory.set_value(
                self.index_register.get_value() + 2, val % 10)
        elif (instruction & 0xF0FF) == 0xF055:
            for i in range(X + 1):  # X + 1 because it's inclusive
                value_to_store = self.gp_registers.get_value(i)
                self.memory.set_value(
                    self.index_register.get_value() + i, value_to_store)
        elif (instruction & 0xF0FF) == 0xF065:
            I = self.index_register.get_value()
            for i in range(X + 1):
                value = self.memory.get_value(I + i)
                self.gp_registers.set_value(i, value)
        elif (instruction & 0xF000) == 0x2000:
            self._stack.append(self.pc.pc)
            self.pc.set_value(NNN)
        elif instruction == 0x00EE:
            if (len(self._stack) == 0):
                raise RuntimeError("stack underflow")
            return_addr = self._stack.pop()
            self.pc.set_value(return_addr)

        # ... (other cases)

        else:
            print(f"Unknown instruction: {hex(instruction)}")
