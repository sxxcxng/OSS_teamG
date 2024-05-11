import random
import pygame
import sys
from resources import padWidth, padHeight, rockImage, explosionSound
from game_objects import drawObject, writeScore, writePassed, writeMessage

def initGame():
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting')
    background = pygame.image.load('background.png')
    fighter = pygame.image.load('fighter.png')
    missile = pygame.image.load('missile.png')
    explosion = pygame.image.load('explosion.png')
    pygame.mixer.music.load('music.wav')
    pygame.mixer.music.play(-1)
    missileSound = pygame.mixer.Sound('missile.wav')
    gameOverSound = pygame.mixer.Sound('gameover.wav')
    clock = pygame.time.Clock()
    return gamePad, background, fighter, missile, explosion, missileSound, gameOverSound, clock

def runGame(gamePad, background, fighter, missile, explosion, missileSound, gameOverSound, clock):
    # 전투기 크기 및 초기 위치
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0

    missileXY = []  # 미사일 위치 리스트

    # 운석 랜덤 생성
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))

    isShot = False
    shotCount = 0
    rockPassed = 0

    onGame = True
    while onGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    fighterX -= 5
                elif event.key == pygame.K_RIGHT:
                    fighterX += 5
                elif event.key == pygame.K_SPACE:
                    missileSound.play()
                    missileX = x + fighterWidth / 2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0

        gamePad.blit(background, (0, 0))  # 배경 화면 그리기

        # 전투기 위치 재조정
        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        # 전투기 충돌 체크
        if y < rockY + rockHeight:
            if (rockX > x and rockX < x + fighterWidth) or (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth):
                writeMessage(gamePad, '전투기 파괴!', gameOverSound)
                onGame = False

        drawObject(gamePad, fighter, x, y)  # 전투기 그리기

        # 미사일 발사 처리
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10  # 미사일 이동
                if bxy[1] < rockY and rockX < bxy[0] < rockX + rockWidth:
                    missileXY.remove(bxy)
                    isShot = True
                    shotCount += 1
                    destroySound.play()
                    rock = pygame.image.load(random.choice(rockImage))
                    rockSize = rock.get_rect().size
                    rockWidth = rockSize[0]
                    rockHeight = rockSize[1]
                    rockX = random.randrange(0, padWidth - rockWidth)
                    rockY = -rockHeight
                    rockSpeed += 0.02
                if bxy[1] <= 0:
                    missileXY.remove(bxy)
            for bx, by in missileXY:
                drawObject(gamePad, missile, bx, by)

        # 운석 맞춘 점수 표시
        writeScore(gamePad, shotCount)

        # 운석 위치 업데이트
        rockY += rockSpeed
        if rockY > padHeight:
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1

        # 놓친 운석 수 표시
        writePassed(gamePad, rockPassed)

        # 운석 그리기
        drawObject(gamePad, rock, rockX, rockY)

        # 게임 오버 조건 체크
        if rockPassed > 2:  # 운석 3개를 놓치면 게임 오버
            writeMessage(gamePad, '게임 오버!', gameOverSound)
            onGame = False

        pygame.display.update()  # 게임 화면 업데이트
        clock.tick(60)  # 게임의 프레임률을 60FPS로 설정

    # 게임 루프 종료 후 처리
    pygame.quit()  # Pygame 종료
    sys.exit()  # 시스템 종료

def main():
    gamePad, background, fighter, missile, explosion, missileSound, gameOverSound, clock = initGame()
    runGame(gamePad, background, fighter, missile, explosion, missileSound, gameOverSound, clock)

if __name__ == "__main__":
    main()