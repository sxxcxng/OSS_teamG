import pygame
import random
import os
from pyshooting.resources import explosion_sound, load_sound

def load_sounds():
    soundDir = 'assets/sounds'
    missileSound = load_sound(os.path.join(soundDir, 'missile.wav'))
    game_overSound = load_sound(os.path.join(soundDir, 'game_over.wav'))
    destroy_sound = load_sound(random.choice(explosion_sound))
    return missileSound, game_overSound, destroy_sound

def play_music(file):
    try:
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1)
    except FileNotFoundError:
        print(f"Error: Music file {file} not found.")

def stop_music():
    pygame.mixer.music.stop()

def is_music_playing():
    return pygame.mixer.music.get_busy()
