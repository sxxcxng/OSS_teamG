import pygame
import os

pygame.font.init()
pygame.mixer.init()

padWidth = 480
padHeight = 640

# 이미지와 사운드가 있는 디렉토리 경로 설정
rock_imagesDir = 'assets/images'
explosion_soundDir = 'assets/sounds'

# 운석 이미지 파일 이름을 담을 리스트
rock_images = []

# 'rock'으로 시작하는 파일 이름을 찾아 리스트에 추가
for filename in os.listdir(rock_imagesDir):
    if filename.startswith('rock') and filename.endswith('.png'):
        rock_images.append(os.path.join(rock_imagesDir, filename))

# 폭발 사운드 파일 이름을 담을 리스트
explosion_sound = []

# 'explosion'으로 시작하는 파일 이름을 찾아 리스트에 추가
for filename in os.listdir(explosion_soundDir):
    if filename.startswith('explosion') and filename.endswith('.wav'):
        explosion_sound.append(os.path.join(explosion_soundDir, filename))
        
clear_itemImage = 'clear_item.png'

# 이미지 로드 함수
def load_image(file_path):
    try:
        return pygame.image.load(file_path)
    except FileNotFoundError:
        print(f"Error: Image file {file_path} not found.")
        return None

# 사운드 로드 함수
def load_sound(file_path):
    try:
        return pygame.mixer.Sound(file_path)
    except FileNotFoundError:
        print(f"Error: Sound file {file_path} not found.")
        return None