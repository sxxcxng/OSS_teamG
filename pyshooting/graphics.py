import pygame

def drawObject(gamePad, obj, x, y):
    gamePad.blit(obj, (x, y))

def writeScore(gamePad, count):
    font = pygame.font.Font('NanumGothic.ttf', 20)
    pygame.draw.rect(gamePad, (0, 0, 0), (10, 0, 200, 30))  # 기존 텍스트 영역 지우기
    text = font.render('파괴한 운석 수:' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))

def writePassed(gamePad, count):
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('놓친 운석 :' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (360, 0))

def writeLevel(gamePad, level, padWidth, padHeight):
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('레벨 :' + str(level), True, (0, 255, 0))
    gamePad.blit(text, (padWidth - 100, padHeight - 30))

