import pygame
import numpy as np


class Timer:
    def __init__(self, value) -> None:
        self.value = value
        self._clock = pygame.time.Clock()

    def decrement(self):
        if self.value > 0:
            self.value -= 1
            return True
        return False

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if type(value) != int:
            raise TypeError("Value must be an integer")
        if value < 0 or value > 0xFF:
            raise ValueError("Value must be between 0 and 255")
        self._value = value


class SoundTimer(Timer):
    def __init__(self, value) -> None:
        super().__init__(value)
        # Initialize the beep sound
        sound_array_mono = np.array(
            [4096 * np.sin(2.0 * np.pi * 440.0 * x / 44100)
             for x in range(0, 44100)]
        ).astype(np.int16)
        sound_array_stereo = np.column_stack(
            [sound_array_mono, sound_array_mono])
        self._beep_sound = pygame.sndarray.make_sound(sound_array_stereo)

    def decrement(self):
        if self.value > 0:
            self.value -= 1
            self._beep_sound.play(maxtime=16)  # Play a short beep
            return True
        return False
