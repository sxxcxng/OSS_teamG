import pygame
import sys
import random
from pyshooting.resources import padWidth, padHeight, rockImage, load_image, load_sound
from pyshooting.graphics import drawObject, writeScore, writePassed, writeLevel
from pyshooting.messages import writeMessage
from pyshooting.audio import loadSounds, playMusic, stopMusic
import os

def initGame():
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting')

    # 모든 이미지 파일을 assets/images 폴더에서 로드
    imageDir = 'assets/images'
    background = load_image(os.path.join(imageDir, 'background.png'))
    fighter = load_image(os.path.join(imageDir, 'fighter.png'))
    missile = load_image(os.path.join(imageDir, 'missile.png'))
    explosion = load_image(os.path.join(imageDir, 'explosion.png'))
    fullHeart = load_image(os.path.join(imageDir, 'full_heart.png'))
    emptyHeart = load_image(os.path.join(imageDir, 'empty_heart.png'))
    heartItem = load_image(os.path.join(imageDir, 'full_heart.png'))
    clearItem = load_image(os.path.join(imageDir, 'clear_item.png'))
    missileItem = load_image(os.path.join(imageDir, 'missile_item.png'))

    clock = pygame.time.Clock()
    missileSound, gameOverSound, destroySound = loadSounds()
    playMusic(os.path.join('assets/sounds', 'music.wav'))
    
    return gamePad, background, fighter, missile, explosion, missileSound, gameOverSound, clock, destroySound, fullHeart, emptyHeart, heartItem, clearItem, missileItem

def showLevelPage(gamePad, level):
    font = pygame.font.Font('NanumGothic.ttf', 80)
    text = font.render(f'레벨 {level}', True, (255, 255, 255))
    textpos = text.get_rect(center=(padWidth / 2, padHeight / 2))
    gamePad.fill((0, 0, 0))
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.time.delay(2000)

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

def pixel_collision(obj1, obj2, obj1_x, obj1_y, obj2_x, obj2_y):
    rect1 = obj1.get_rect(left=obj1_x, top=obj1_y)
    rect2 = obj2.get_rect(left=obj2_x, top=obj2_y)
    intersection = rect1.clip(rect2)
    if intersection.width == 0 or intersection.height == 0:
        return False
    return True

def runGame(gamePad, background, fighter, missile, explosion, missileSound, gameOverSound, clock, destroySound, fullHeart, emptyHeart, heartItem, clearItem, missileItem):
    fighterSize = fighter.get_rect().size
    fighterWidth, fighterHeight = fighterSize
    x, y = padWidth * 0.45, padHeight * 0.9
    fighterX = 0
    missileXY = []

    rockSpeeds = [2, 3, 4]
    current_rock_speed_index = 0

    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth, rockHeight = rockSize
    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    current_rock_speed_index = random.randint(0, len(rockSpeeds) - 1)
    rockSpeed = rockSpeeds[current_rock_speed_index]
    rock2 = None

    heartItemX = random.randrange(0, padWidth)
    heartItemY = 0
    heartItemSpeed = 2
    heartItemAppear = False

    missileItemX = random.randrange(0, padWidth)
    missileItemY = 0
    missileItemSpeed = 3
    missileItemAppear = False
    missileEnhanced = False
    missileEnhanceEndTime = 0

    hearts = 3

    clearItemX = random.randrange(0, padWidth)
    clearItemY = 0
    clearItemSpeed = 3
    clearItemAppear = False

    isShot = False
    shotCount = 0
    rockPassed = 0
    onGame = True
    level = 1
    rocks_destroyed = 0

    showLevelPage(gamePad, level)

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
                    if missileEnhanced:
                        missileXY.append([missileX - 20, missileY])
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

        if rock2:
            rock2Rect = pygame.Rect(rock2['x'], rock2['y'], rock2['width'], rock2['height'])
            if fighterRect.colliderect(rock2Rect):
                hearts -= 1
                if hearts == 0:
                    gameOver(gamePad, gameOverSound)
                else:
                    rock2 = None

        drawObject(gamePad, fighter, x, y)

        if rockPassed == 3 or hearts == 0:
            gameOver(gamePad, gameOverSound)

        if len(missileXY) != 0:
            for bxy in missileXY[:]:
                bxy[1] -= 10
                if bxy[1] < rockY and rockX < bxy[0] < rockX + rockWidth:
                    try:
                        missileXY.remove(bxy)
                    except ValueError:
                        pass
                    isShot = True
                    shotCount += 1
                    rocks_destroyed += 1
                    destroySound.play()
                    rock = pygame.image.load(random.choice(rockImage))
                    rockSize = rock.get_rect().size
                    rockWidth, rockHeight = rockSize
                    rockX = random.randrange(0, padWidth - rockWidth)
                    rockY = -rockHeight
                    current_rock_speed_index = random.randint(0, len(rockSpeeds) - 1)
                    rockSpeed = rockSpeeds[current_rock_speed_index]
                    rockSpeed += 0.02
                    if shotCount >= 3 and not rock2:
                        rock2 = {
                            'image': pygame.image.load(random.choice(rockImage)),
                            'width': rockWidth,
                            'height': rockHeight,
                            'x': random.randrange(0, padWidth - rockWidth),
                            'y': -rockHeight,
                            'speed': rockSpeed,
                            'xSpeed': random.choice([-2, 2])
                        }
                if rock2 and bxy[1] < rock2['y'] + rock2['height'] and rock2['x'] < bxy[0] < rock2['x'] + rock2['width']:
                    try:
                        missileXY.remove(bxy)
                    except ValueError:
                        pass
                    isShot = True
                    shotCount += 1
                    rocks_destroyed += 1
                    destroySound.play()
                    rock2 = None
                if bxy[1] <= 0:
                    try:
                        missileXY.remove(bxy)
                    except ValueError:
                        pass
            for bx, by in missileXY:
                drawObject(gamePad, missile, bx, by)

        if not clearItemAppear:
            if random.random() < 0.007:
                clearItemX = random.randrange(0, padWidth - clearItem.get_rect().width)
                clearItemY = 0
                clearItemAppear = True

        if clearItemAppear:
            clearItemY += clearItemSpeed
            drawObject(gamePad, clearItem, clearItemX, clearItemY)
            if clearItemY > padHeight:
                clearItemAppear = False
            if (y < clearItemY + clearItem.get_rect().height and
                ((clearItemX > x and clearItemX < x + fighterWidth) or
                 (clearItemX + clearItem.get_rect().width > x and clearItemX + clearItem.get_rect().width < x + fighterWidth))):
                clearItemAppear = False
                rock = pygame.image.load(random.choice(rockImage))
                rockSize = rock.get_rect().size
                rockWidth = rockSize[0]
                rockHeight = rockSize[1]
                rockX = random.randrange(0, padWidth - rockWidth)
                rockY = -rockHeight
                rockSpeed += 0.02
                rock2 = None
                rockPassed = 0

        if rocks_destroyed >= 4 * level:
            level += 1
            showLevelPage(gamePad, level)
            rocks_destroyed = 0
            rockSpeed += 0.5

        writeScore(gamePad, shotCount)
        writeLevel(gamePad, level, padWidth, padHeight)
        rockY += rockSpeed
        if rockY > padHeight:
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth, rockHeight = rockSize
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1
            current_rock_speed_index = random.randint(0, len(rockSpeeds) - 1)
            rockSpeed = rockSpeeds[current_rock_speed_index]

        if rock2:
            rock2['y'] += rock2['speed']
            rock2['x'] += rock2['xSpeed']
            if rock2['x'] < 0 or rock2['x'] > padWidth - rock2['width']:
                rock2['xSpeed'] = -rock2['xSpeed']
            if rock2['y'] > padHeight:
                rock2 = None
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

        if not missileItemAppear:
            if random.random() < 0.002:
                missileItemX = random.randrange(0, padWidth - missileItem.get_rect().width)
                missileItemY = 0
                missileItemAppear = True

        if missileItemAppear:
            missileItemY += missileItemSpeed
            drawObject(gamePad, missileItem, missileItemX, missileItemY)
            if missileItemY > padHeight:
                missileItemAppear = False
            if (y < missileItemY + missileItem.get_rect().height and
                ((missileItemX > x and missileItemX < x + fighterWidth) or
                 (missileItemX + missileItem.get_rect().width > x and missileItemX + missileItem.get_rect().width < x + fighterWidth))):
                missileItemAppear = False
                missileEnhanced = True
                missileEnhanceEndTime = pygame.time.get_ticks() + 5000  # 5초 동안 미사일 발사 개수 증가

        if missileEnhanced and pygame.time.get_ticks() > missileEnhanceEndTime:
            missileEnhanced = False

        writePassed(gamePad, rockPassed)
        drawObject(gamePad, rock, rockX, rockY)
        if rock2:
            drawObject(gamePad, rock2['image'], rock2['x'], rock2['y'])
        drawHearts(gamePad, hearts, fullHeart, emptyHeart)

        if rockPassed > 2:
            writeMessage(gamePad, '게임 오버!', gameOverSound)
            onGame = False

        if pixel_collision(fighter, rock, x, y, rockX, rockY):
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

        if rock2:
            if pixel_collision(fighter, rock2['image'], x, y, rock2['x'], rock2['y']):
                hearts -= 1
                if hearts == 0:
                    gameOver(gamePad, gameOverSound)
                else:
                    rock2 = None


        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()