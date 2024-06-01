import pygame
import sys
from pyshooting.resources import padWidth, padHeight
from pyshooting.game import runGame, initGame
import pyshooting.settingTab as settingTab
import os

def draw_start_screen(gamePad, background):
    gamePad.blit(background, (0, 0))
    font = pygame.font.Font('NanumGothic.ttf', 30)
    start_text = font.render('게임 시작', True, (255, 255, 255))
    start_text_rect = start_text.get_rect(center=(padWidth / 2, padHeight / 2 - 50))
    gamePad.blit(start_text, start_text_rect)

    setting_text = font.render('설정', True, (255, 255, 255))
    setting_text_rect = setting_text.get_rect(center=(padWidth / 2, padHeight / 2 + 50))
    gamePad.blit(setting_text, setting_text_rect)
    
    pygame.display.update()

def wait_for_start(gamePad, background):
    global start_button, setting_button
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if start_button.collidepoint(mouse_x, mouse_y):
                    waiting = False
                elif setting_button.collidepoint(mouse_x, mouse_y):
                    settingTab.run_settings(gamePad)
                    draw_start_screen(gamePad, background)

def main():
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting')
    
    imageDir = 'assets/images'
    background = pygame.image.load(os.path.join(imageDir, 'background.png'))
    
    # initGame 함수를 통해 필요한 리소스들을 로드합니다.
    (gamePad, background, fighter, missile, explosion, missileSound, 
     gameOverSound, clock, destroySound, fullHeart, emptyHeart, heartItem, clearItem, missileItem) = initGame()
    
    # 시작 페이지 표시
    draw_start_screen(gamePad, background)
    
    # 시작 버튼 위치 정의
    global start_button, setting_button
    start_button = pygame.Rect(padWidth / 2 - 100, padHeight / 2 - 100, 200, 100)
    setting_button = pygame.Rect(padWidth / 2 - 100, padHeight / 2, 200, 100)
    
    # 시작 버튼 클릭 대기
    wait_for_start(gamePad, background)
    
    # 게임 시작
    runGame(gamePad, background, fighter, missile, explosion, missileSound, gameOverSound, clock, destroySound, fullHeart, emptyHeart, heartItem, clearItem, missileItem)

if __name__ == "__main__":
    main()
