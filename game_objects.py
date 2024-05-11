import pygame
import random
from resources import padWidth, padHeight, rockImage, explosionSound

# 게임에 등장하는 객체를 드로잉
def drawObject(gamePad, obj, x, y):
    gamePad.blit(obj, (x, y))

# 점수 표시
def writeScore(gamePad, count):
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('파괴한 운석 수:' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))

# 놓친 운석 수 표시
def writePassed(gamePad, count):
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('놓친 운석 :' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (360, 0))

# 게임 메시지 출력
def writeMessage(gamePad, text, gameOverSound):
    font = pygame.font.Font('NanumGothic.ttf', 80)
    text = font.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth / 2, padHeight / 2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()
    gameOverSound.play()
    pygame.time.delay(2000)
    pygame.mixer.music.play(-1)