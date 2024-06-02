import pygame
import random
from pyshooting.resources import explosionSound, load_sound
import os

def loadSounds():
    soundDir = 'assets/sounds'
    missileSound = load_sound(os.path.join(soundDir, 'missile.wav'))
    gameOverSound = load_sound(os.path.join(soundDir, 'gameover.wav'))
    destroySound = load_sound(random.choice(explosionSound))
    return missileSound, gameOverSound, destroySound

def playMusic(file):
    try:
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1)
    except FileNotFoundError:
        print(f"Error: Music file {file} not found.")

def stopMusic():
    pygame.mixer.music.stop()

def isMusicPlaying():
    return pygame.mixer.music.get_busy()
