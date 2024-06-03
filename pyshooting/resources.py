import pygame
import os

pygame.font.init()
pygame.mixer.init()

padWidth, padHeight = 480, 640

rock_images_dir = 'assets/images'
explosion_sound_dir = 'assets/sounds'

rock_images = [
    os.path.join(rock_images_dir, filename)
    for filename in os.listdir(rock_images_dir)
    if filename.startswith('rock') and filename.endswith('.png')
]

explosion_sound = [
    os.path.join(explosion_sound_dir, filename)
    for filename in os.listdir(explosion_sound_dir)
    if filename.startswith('explosion') and filename.endswith('.wav')
]

clear_item_image = 'clear_item.png'

def load_image(file_path):
    try:
        return pygame.image.load(file_path)
    except FileNotFoundError:
        print(f"Error: Image file {file_path} not found.")
        return None

def load_sound(file_path):
    try:
        return pygame.mixer.Sound(file_path)
    except FileNotFoundError:
        print(f"Error: Sound file {file_path} not found.")
        return None
