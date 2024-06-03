import pygame
import sys
import os
from pyshooting.resources import padWidth, padHeight
from pyshooting.game import run_game, initialize_game
import pyshooting.settingTab as settingTab

def draw_start_screen(gamePad, background, start_button_rect, setting_button_rect):
    gamePad.blit(background, (0, 0))
    font = pygame.font.Font('NanumGothic.ttf', 30)
    start_text = font.render('게임 시작', True, (255, 255, 255))
    start_text_rect = start_text.get_rect(center=start_button_rect.center)
    gamePad.blit(start_text, start_text_rect)

    setting_text = font.render('설정', True, (255, 255, 255))
    setting_text_rect = setting_text.get_rect(center=setting_button_rect.center)
    gamePad.blit(setting_text, setting_text_rect)
    
    pygame.display.update()

def wait_for_start(gamePad, background, start_button_rect, setting_button_rect):
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    waiting = False
                elif setting_button_rect.collidepoint(mouse_x, mouse_y):
                    settingTab.run_settings(gamePad)
                    draw_start_screen(gamePad, background, start_button_rect, setting_button_rect)

def main():
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting')
    
    imageDir = 'assets/images'
    background = pygame.image.load(os.path.join(imageDir, 'background.png'))
    
    (gamePad, background, fighter, missile, explosion, missileSound, 
     game_overSound, clock, destroy_sound, fullHeart, emptyHeart, heart_item, clear_item, missile_item) = initialize_game()
    
    start_button_rect = pygame.Rect(padWidth / 2 - 100, padHeight / 2 - 100, 200, 100)
    setting_button_rect = pygame.Rect(padWidth / 2 - 100, padHeight / 2, 200, 100)
    draw_start_screen(gamePad, background, start_button_rect, setting_button_rect)
    
    wait_for_start(gamePad, background, start_button_rect, setting_button_rect)
    
    run_game(gamePad, background, fighter, missile, explosion, missileSound, game_overSound, clock, destroy_sound, fullHeart, emptyHeart, heart_item, clear_item, missile_item)

if __name__ == "__main__":
    main()
