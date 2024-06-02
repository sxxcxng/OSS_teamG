import pygame
import sys
import random
from pyshooting.resources import padWidth, padHeight, rockImage, explosionSound
from pyshooting.graphics import drawObject, writeScore, writePassed, writeLevel
from pyshooting.messages import writeMessage
from pyshooting.audio import loadSounds, playMusic, stopMusic
import os
import time

class Rock:
    def __init__(self, image, width, height, x, y, speed, x_speed=0):
        self.image = pygame.image.load(image)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.speed = speed
        self.x_speed = x_speed

    def draw(self, gamePad):
        drawObject(gamePad, self.image, self.x, self.y)

    def move(self):
        self.y += self.speed
        self.x += self.x_speed
        if self.x < 0 or self.x > padWidth - self.width:
            self.x_speed = -self.x_speed

    def reset(self):
        self.image = pygame.image.load(random.choice(rockImage))
        rockSize = self.image.get_rect().size
        self.width = rockSize[0]
        self.height = rockSize[1]
        self.x = random.randrange(0, padWidth - self.width)
        self.y = -self.height
        self.speed += 0.02

def initGame():
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting')
    imageDir = 'assets/images'
    background = pygame.image.load(os.path.join(imageDir, 'background.png'))
    fighter = pygame.image.load(os.path.join(imageDir, 'fighter.png'))
    missile = pygame.image.load(os.path.join(imageDir, 'missile.png'))
    explosion = pygame.image.load(os.path.join(imageDir, 'explosion.png'))
    fullHeart = pygame.image.load(os.path.join(imageDir, 'full_heart.png'))
    emptyHeart = pygame.image.load(os.path.join(imageDir, 'empty_heart.png'))
    heartItem = pygame.image.load(os.path.join(imageDir, 'full_heart.png'))
    clearItem = pygame.image.load(os.path.join(imageDir, 'clear_item.png'))
    missileItem = pygame.image.load(os.path.join(imageDir, 'missile_item.png'))
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
    current_rock_speed_index = random.randint(0, len(rockSpeeds) - 1)
    rockSpeed = rockSpeeds[current_rock_speed_index]

    rock = Rock(random.choice(rockImage), 0, 0, random.randrange(0, padWidth), 0, rockSpeed)
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

    last_pause_time = time.time()
    is_paused = False

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
                elif event.key == pygame.K_p:
                    if time.time() - last_pause_time > 0.5:  # Debounce for 0.5 seconds
                        is_paused = not is_paused
                        if is_paused:
                            stopMusic()
                        else:
                            playMusic(os.path.join('assets/sounds', 'music.wav'))
                        last_pause_time = time.time()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0

        if is_paused:
            continue

        gamePad.blit(background, (0, 0))
        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        fighterRect = pygame.Rect(x, y, fighterWidth, fighterHeight)
        rockRect = pygame.Rect(rock.x, rock.y, rock.width, rock.height)

        if fighterRect.colliderect(rockRect):
            hearts -= 1
            if hearts == 0:
                gameOver(gamePad, gameOverSound)
            else:
                rock.reset()

        if rock2:
            rock2Rect = pygame.Rect(rock2.x, rock2.y, rock2.width, rock2.height)
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
                if pixel_collision(rock.image, missile, rock.x, rock.y, bxy[0], bxy[1]):
                    try:
                        missileXY.remove(bxy)
                    except ValueError:
                        pass
                    isShot = True
                    shotCount += 1
                    rocks_destroyed += 1
                    destroySound.play()
                    rock.reset()
                    if shotCount >= 3 and not rock2:
                        rock2 = Rock(random.choice(rockImage), rock.width, rock.height, random.randrange(0, padWidth - rock.width), -rock.height, rock.speed, random.choice([-2, 2]))
                if rock2 and pixel_collision(rock2.image, missile, rock2.x, rock2.y, bxy[0], bxy[1]):
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
                 (clearItemX + clearItem.get_rect().width > x and clearItem.get_rect().width < x + fighterWidth))):
                clearItemAppear = False
                rock.reset()
                rock2 = None
                rockPassed = 0

        if rocks_destroyed >= 4 * level:
            level += 1
            showLevelPage(gamePad, level)
            rocks_destroyed = 0
            rock.speed += 0.5

        writeScore(gamePad, shotCount)
        writeLevel(gamePad, level, padWidth, padHeight)
        rock.move()
        if rock.y > padHeight:
            rock.reset()
            rockPassed += 1

        if rock2:
            rock2.move()
            if rock2.y > padHeight:
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
                 (heartItemX + heartItem.get_rect().width > x and heartItem.get_rect().width < x + fighterWidth))):
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
                 (missileItemX + missileItem.get_rect().width > x and missileItem.get_rect().width < x + fighterWidth))):
                missileItemAppear = False
                missileEnhanced = True
                missileEnhanceEndTime = pygame.time.get_ticks() + 5000

        if missileEnhanced and pygame.time.get_ticks() > missileEnhanceEndTime:
            missileEnhanced = False

        writePassed(gamePad, rockPassed)
        rock.draw(gamePad)
        if rock2:
            rock2.draw(gamePad)
        drawHearts(gamePad, hearts, fullHeart, emptyHeart)

        if rockPassed > 2:
            writeMessage(gamePad, '게임 오버!', gameOverSound)
            onGame = False

        if pixel_collision(fighter, rock.image, x, y, rock.x, rock.y):
            hearts -= 1
            if hearts == 0:
                gameOver(gamePad, gameOverSound)
            else:
                rock.reset()

        if rock2:
            if pixel_collision(fighter, rock2.image, x, y, rock2.x, rock2.y):
                hearts -= 1
                if hearts == 0:
                    gameOver(gamePad, gameOverSound)
                else:
                    rock2 = None

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()