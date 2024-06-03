import pygame
import sys
from pyshooting.resources import padWidth, padHeight
from pyshooting.audio import play_music, stop_music, is_music_playing
import os

def draw_settings_screen(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.Font('NanumGothic.ttf', 30)
    
    settings_text = font.render('설정 화면', True, (255, 255, 255))
    settings_rect = settings_text.get_rect(center=(padWidth / 2, padHeight / 2 - 150))
    screen.blit(settings_text, settings_rect)
    
    save_text = font.render('저장', True, (255, 255, 255))
    save_rect = save_text.get_rect(center=(padWidth / 2, padHeight / 2 + 150))
    screen.blit(save_text, save_rect)
    
    music_status = "배경음 ON" if is_music_playing() else "배경음 OFF"
    music_text = font.render(music_status, True, (255, 255, 255))
    music_rect = music_text.get_rect(center=(padWidth / 2, padHeight / 2))
    screen.blit(music_text, music_rect)
    
    pygame.display.update()

def handle_events(back_button, music_button, screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if back_button.collidepoint(mouse_x, mouse_y):
                return False
            elif music_button.collidepoint(mouse_x, mouse_y):
                play_music(os.path.join('assets/sounds', 'music.wav')) if not is_music_playing() else stop_music()
                draw_settings_screen(screen)
    return True

def wait_for_back(screen):
    back_button = pygame.Rect(padWidth / 2 - 100, padHeight / 2 + 100, 200, 100)
    music_button = pygame.Rect(padWidth / 2 - 100, padHeight / 2 - 50, 200, 100)
    waiting = True
    while waiting:
        waiting = handle_events(back_button, music_button, screen)
        pygame.display.update()

def run_settings(screen):
    draw_settings_screen(screen)
    wait_for_back(screen)
