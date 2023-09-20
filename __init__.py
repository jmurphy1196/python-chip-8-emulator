import pygame
import numpy as np
from game import Game


def main():
    rom = input("Enter the name of the rom: ")
    new_game = Game(rom=rom)
    new_game.run()

    pass


if __name__ == '__main__':
    main()
