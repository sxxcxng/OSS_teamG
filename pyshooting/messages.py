import pygame
from pyshooting.resources import padWidth, padHeight
from pyshooting.audio import stop_music, play_music

def write_message(screen, text, game_over_sound):
    font = pygame.font.Font('NanumGothic.ttf', 80)
    rendered_text = font.render(text, True, (255, 0, 0))
    text_rect = rendered_text.get_rect(center=(padWidth / 2, padHeight / 2))
    screen.blit(rendered_text, text_rect)
    
    pygame.display.update()
    stop_music()
    game_over_sound.play()
    pygame.time.delay(2000)
    play_music('music.wav')
