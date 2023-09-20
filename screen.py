import numpy as np
import pygame


class Screen:
    def __init__(self, scale=1) -> None:
        self.scale = scale
        self._width = 64 * self.scale
        self._height = 32 * self.scale
        self._cols = 64
        self._rows = 32
        self._pixels = np.zeros((self._rows, self._cols), dtype=np.uint8)
        self.on_color = (243, 240, 247)
        self.off_color = (156, 87, 247)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        if type(value) != int:
            raise TypeError("Scale must be an integer")
        if value < 1:
            raise ValueError("Scale cannot be less than 1")
        elif value > 30:
            raise ValueError("Scale cannot be greater than 30")
        self._scale = value

    def draw_sprite(self, x: int, y: int, sprite: [int]) -> bool:
        collision = False
        for i in range(len(sprite)):
            row = sprite[i]
            for j in range(8):
                if (row & (0x80 >> j)) != 0:
                    pixel_x = (x + j) % self._cols
                    pixel_y = (y + i) % self._rows

                    # Check for collision
                    if self._pixels[pixel_y, pixel_x] == 1:
                        collision = True

                    # XOR the pixel value
                    self._pixels[pixel_y, pixel_x] ^= 1
        return collision

    def clear_screen(self) -> None:
        self._pixels = np.zeros((self._rows, self._cols), dtype=np.uint8)

    def draw_screen(self) -> None:
        for y in range(self._rows):
            for x in range(self._cols):
                pixel = self._pixels[y, x]
                if pixel == 1:
                    color = self.on_color
                else:
                    color = self.off_color
                pygame.draw.rect(
                    self._window, color, (x * self._scale, y * self._scale, self._scale, self._scale))

    def create_window(self):
        # create pygame window
        self._window = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption('CHIP-8 Emulator')
