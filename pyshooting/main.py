import pygame
import sys
from pyshooting.resources import padWidth, padHeight
from pyshooting.game import runGame, initGame

def main():
    gamePad, background, fighter, missile, explosion, missileSound, gameOverSound, clock, destroySound = initGame()
    runGame(gamePad, background, fighter, missile, explosion, missileSound, gameOverSound, clock, destroySound)

if __name__ == "__main__":
    main()
