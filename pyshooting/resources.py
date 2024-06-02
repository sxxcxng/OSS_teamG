import pygame
import os

pygame.font.init()
pygame.mixer.init()

padWidth = 480
padHeight = 640

# 이미지와 사운드가 있는 디렉토리 경로 설정
rockImageDir = 'assets/images'
explosionSoundDir = 'assets/sounds'

# 운석 이미지 파일 이름을 담을 리스트
rockImage = []

# 'rock'으로 시작하는 파일 이름을 찾아 리스트에 추가
for filename in os.listdir(rockImageDir):
    if filename.startswith('rock') and filename.endswith('.png'):
        rockImage.append(os.path.join(rockImageDir, filename))

# 폭발 사운드 파일 이름을 담을 리스트
explosionSound = []

# 'explosion'으로 시작하는 파일 이름을 찾아 리스트에 추가
for filename in os.listdir(explosionSoundDir):
    if filename.startswith('explosion') and filename.endswith('.wav'):
        explosionSound.append(os.path.join(explosionSoundDir, filename))
        
clearItemImage = 'clear_item.png'

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