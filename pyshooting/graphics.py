import pygame

def draw_object(screen, obj, x, y):
    screen.blit(obj, (x, y))

def write_score(screen, count):
    font = pygame.font.Font('NanumGothic.ttf', 20)
    pygame.draw.rect(screen, (0, 0, 0), (10, 0, 200, 30))  # 기존 텍스트 영역 지우기
    text = font.render(f'파괴한 운석 수: {count}', True, (255, 255, 255))
    screen.blit(text, (10, 0))

def write_passed(screen, count):
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render(f'놓친 운석: {count}', True, (255, 0, 0))
    screen.blit(text, (360, 0))

def write_level(screen, level, pad_width, pad_height):
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render(f'레벨: {level}', True, (0, 255, 0))
    screen.blit(text, (pad_width - 100, pad_height - 30))
