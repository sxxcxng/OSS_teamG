import pygame

def drawObject(gamePad, obj, x, y):
    gamePad.blit(obj, (x, y))

def writeScore(gamePad, count):
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('파괴한 운석 수:' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))

def writePassed(gamePad, count):
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('놓친 운석 :' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (360, 0))
