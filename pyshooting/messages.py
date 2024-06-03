import pygame
from pyshooting.resources import padWidth, padHeight
from pyshooting.audio import stopMusic, playMusic

def writeMessage(gamePad, text, game_overSound):
    font = pygame.font.Font('NanumGothic.ttf', 80)
    text = font.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth / 2, padHeight / 2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    stopMusic()
    game_overSound.play()
    pygame.time.delay(2000)
    playMusic('music.wav')
