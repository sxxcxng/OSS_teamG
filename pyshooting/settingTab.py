import pygame
import sys
from pyshooting.resources import padWidth, padHeight
from pyshooting.audio import playMusic, stopMusic, isMusicPlaying
import os

def draw_settings_screen(gamePad):
    gamePad.fill((0, 0, 0))
    font = pygame.font.Font('NanumGothic.ttf', 30)
    text = font.render('설정 화면', True, (255, 255, 255))
    text_rect = text.get_rect(center=(padWidth / 2, padHeight / 2 - 150))
    gamePad.blit(text, text_rect)

    back_text = font.render('저장', True, (255, 255, 255))
    back_text_rect = back_text.get_rect(center=(padWidth / 2, padHeight / 2 + 150))
    gamePad.blit(back_text, back_text_rect)

    music_text = "배경음 ON" if isMusicPlaying() else "배경음 OFF"
    music_button_text = font.render(music_text, True, (255, 255, 255))
    music_button_text_rect = music_button_text.get_rect(center=(padWidth / 2, padHeight / 2))
    gamePad.blit(music_button_text, music_button_text_rect)
    
    pygame.display.update()

def wait_for_back(gamePad):
    back_button = pygame.Rect(padWidth / 2 - 100, padHeight / 2 + 100, 200, 100)
    music_button = pygame.Rect(padWidth / 2 - 100, padHeight / 2 - 50, 200, 100)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if back_button.collidepoint(mouse_x, mouse_y):
                    waiting = False
                elif music_button.collidepoint(mouse_x, mouse_y):
                    if isMusicPlaying():
                        stopMusic()
                    else:
                        playMusic(os.path.join('assets/sounds', 'music.wav'))
                    draw_settings_screen(gamePad)
        pygame.display.update()

def run_settings(gamePad):
    draw_settings_screen(gamePad)
    wait_for_back(gamePad)
