import pygame

# Pygame 초기화
pygame.font.init()
pygame.mixer.init()

# 게임 화면 크기 설정
padWidth = 480
padHeight = 640

# 운석 이미지 파일 목록
rockImage = [
    'rock01.png', 'rock02.png', 'rock03.png', 'rock04.png', 'rock05.png',
    'rock06.png', 'rock07.png', 'rock08.png', 'rock09.png', 'rock10.png',
    'rock11.png', 'rock12.png', 'rock13.png', 'rock14.png', 'rock15.png',
    'rock16.png', 'rock17.png', 'rock18.png', 'rock19.png', 'rock20.png',
    'rock21.png', 'rock22.png', 'rock23.png', 'rock24.png', 'rock25.png',
    'rock26.png', 'rock27.png', 'rock28.png', 'rock29.png', 'rock30.png'
]

# 폭발 사운드 파일 목록
explosionSound = ['explosion01.wav', 'explosion02.wav', 'explosion03.wav', 'explosion04.wav']
