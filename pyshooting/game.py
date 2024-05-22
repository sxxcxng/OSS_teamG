import pygame
import sys
import random
from pyshooting.resources import padWidth, padHeight, rockImage, explosionSound
from pyshooting.graphics import drawObject, writeScore, writePassed
from pyshooting.messages import writeMessage
from pyshooting.audio import loadSounds, playMusic, stopMusic

def initGame():
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting')
    background = pygame.image.load('background.png')
    fighter = pygame.image.load('fighter.png')
    missile = pygame.image.load('missile.png')
    explosion = pygame.image.load('explosion.png')
    fullHeart = pygame.image.load('full_heart.png')
    emptyHeart = pygame.image.load('empty_heart.png')
    heartItem = pygame.image.load('full_heart.png')
    clock = pygame.time.Clock()
    missileSound, gameOverSound, destroySound = loadSounds()
    playMusic('music.wav')
    return gamePad, background, fighter, missile, explosion, missileSound, gameOverSound, clock, destroySound, fullHeart, emptyHeart, heartItem

def drawHearts(gamePad, hearts, fullHeart, emptyHeart):
    heart_width = fullHeart.get_rect().width
    heart_height = fullHeart.get_rect().height
    for i in range(3):
        if i < hearts:
            drawObject(gamePad, fullHeart, 10 + i * (heart_width + 10), padHeight - heart_height - 10)
        else:
            drawObject(gamePad, emptyHeart, 10 + i * (heart_width + 10), padHeight - heart_height - 10)

def gameOver(gamePad, gameOverSound):
    writeMessage(gamePad, '게임 오버!', gameOverSound)
    stopMusic()
    pygame.quit()
    sys.exit()

def runGame(gamePad, background, fighter, missile, explosion, missileSound, gameOverSound, clock, destroySound, fullHeart, emptyHeart, heartItem):
    fighterSize = fighter.get_rect().size
    fighterWidth, fighterHeight = fighterSize
    x, y = padWidth * 0.45, padHeight * 0.9
    fighterX = 0
    missileXY = []

    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth, rockHeight = rockSize
    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    heartItemX = random.randrange(0, padWidth)
    heartItemY = 0
    heartItemSpeed = 2
    heartItemAppear = False

    hearts = 3

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

        gamePad.blit(background, (0, 0))
        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        fighterRect = pygame.Rect(x, y, fighterWidth, fighterHeight)
        rockRect = pygame.Rect(rockX, rockY, rockWidth, rockHeight)

        if fighterRect.colliderect(rockRect):
            hearts -= 1
            if hearts == 0:
                gameOver(gamePad, gameOverSound)
            else:
                rock = pygame.image.load(random.choice(rockImage))
                rockSize = rock.get_rect().size
                rockWidth = rockSize[0]
                rockHeight = rockSize[1]
                rockX = random.randrange(0, padWidth - rockWidth)
                rockY = 0

        drawObject(gamePad, fighter, x, y)

        if rockPassed == 3 or hearts == 0:
            gameOver(gamePad, gameOverSound)

        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10
                if bxy[1] < rockY and rockX < bxy[0] < rockX + rockWidth:
                    missileXY.remove(bxy)
                    isShot = True
                    shotCount += 1
                    destroySound.play()
                    rock = pygame.image.load(random.choice(rockImage))
                    rockSize = rock.get_rect().size
                    rockWidth, rockHeight = rockSize
                    rockX = random.randrange(0, padWidth - rockWidth)
                    rockY = -rockHeight
                    rockSpeed += 0.02
                if bxy[1] <= 0:
                    missileXY.remove(bxy)
            for bx, by in missileXY:
                drawObject(gamePad, missile, bx, by)

        writeScore(gamePad, shotCount)
        rockY += rockSpeed
        if rockY > padHeight:
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth, rockHeight = rockSize
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1

        if not heartItemAppear:
            if random.random() < 0.007:
                heartItemX = random.randrange(0, padWidth - heartItem.get_rect().width)
                heartItemY = 0
                heartItemAppear = True

        if heartItemAppear:
            heartItemY += heartItemSpeed
            drawObject(gamePad, heartItem, heartItemX, heartItemY)
            if heartItemY > padHeight:
                heartItemAppear = False
            if (y < heartItemY + heartItem.get_rect().height and
                ((heartItemX > x and heartItemX < x + fighterWidth) or
                 (heartItemX + heartItem.get_rect().width > x and heartItemX + heartItem.get_rect().width < x + fighterWidth))):
                if hearts < 3:
                    hearts += 1
                heartItemAppear = False

        writePassed(gamePad, rockPassed)
        drawObject(gamePad, rock, rockX, rockY)
        drawHearts(gamePad, hearts, fullHeart, emptyHeart)

        if rockPassed > 2:
            writeMessage(gamePad, '게임 오버!', gameOverSound)
            onGame = False

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()
