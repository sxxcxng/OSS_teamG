import pygame
import random
from pyshooting.resources import explosionSound
import os

def loadSounds():
    soundDir = 'assets/sounds'
    missileSound = pygame.mixer.Sound(os.path.join(soundDir, 'missile.wav'))
    gameOverSound = pygame.mixer.Sound(os.path.join(soundDir, 'gameover.wav'))
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))
    return missileSound, gameOverSound, destroySound

def playMusic(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)

def stopMusic():
    pygame.mixer.music.stop()

def isMusicPlaying():
    return pygame.mixer.music.get_busy()
