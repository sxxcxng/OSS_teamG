import pygame
import random
from pyshooting.resources import explosionSound

def loadSounds():
    missileSound = pygame.mixer.Sound('missile.wav')
    gameOverSound = pygame.mixer.Sound('gameover.wav')
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))
    return missileSound, gameOverSound, destroySound

def playMusic(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)

def stopMusic():
    pygame.mixer.music.stop()

def isMusicPlaying():
    return pygame.mixer.music.get_busy()
