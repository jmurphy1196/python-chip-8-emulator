# !/

import numpy as np
from game import Game


def list_ch8_files():
    import os
    ch8_files = [file for file in os.listdir('roms') if file.endswith('.ch8')]
    return ch8_files


def main():
    ch8_files = list_ch8_files()
    if len(ch8_files) == 0:
        print("No roms found in roms folder")
        return
    print("Available roms:")
    for idx, file in enumerate(ch8_files):
        print(f"{idx + 1}: {file}")
    rom = input("Select rom: ")
    while not rom.isdigit() or int(rom) > len(ch8_files):
        print("Invalid input")
        rom = input("Select rom: ")

    print(ch8_files[int(rom) - 1])
    new_game = Game(rom=ch8_files[int(rom) - 1])
    new_game.run()

    pass


if __name__ == '__main__':
    main()
