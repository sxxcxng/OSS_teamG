import pygame
import sys
import random
from pyshooting.resources import padWidth, padHeight, rock_images, explosion_sound
from pyshooting.graphics import drawObject, writeScore, writePassed, writeLevel
from pyshooting.messages import writeMessage
from pyshooting.audio import loadSounds, playMusic, stopMusic
import os
import time

class Rock:
    def __init__(self, image, width, height, x, y, speed, hits_needed, x_speed=0):
        self.image = pygame.image.load(image)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.speed = speed
        self.hits_needed = hits_needed
        self.hits_taken = 0
        self.x_speed = x_speed

    def draw(self, gamePad):
        drawObject(gamePad, self.image, self.x, self.y)
        font = pygame.font.SysFont(None, 25)
        text = font.render(str(self.hits_needed - self.hits_taken), True, (255, 0, 0))
        gamePad.blit(text, (self.x + self.width, self.y))

    def move(self):
        self.y += self.speed
        self.x += self.x_speed
        if self.x < 0 or self.x > padWidth - self.width:
            self.x_speed = -self.x_speed

    def reset(self):
        self.image = pygame.image.load(random.choice(rock_images))
        rockSize = self.image.get_rect().size
        self.width = rockSize[0]
        self.height = rockSize[1]
        self.x = random.randrange(0, padWidth - self.width)
        self.y = -self.height
        self.speed += 0.02
        self.hits_needed = random.randint(1, 3)
        self.hits_taken = 0

def initialize_game():
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
    heart_item = pygame.image.load(os.path.join(imageDir, 'full_heart.png'))
    clear_item = pygame.image.load(os.path.join(imageDir, 'clear_item.png'))
    missile_item = pygame.image.load(os.path.join(imageDir, 'missile_item.png'))
    clock = pygame.time.Clock()
    missileSound, game_overSound, destroy_sound = loadSounds()
    playMusic(os.path.join('assets/sounds', 'music.wav'))
    return gamePad, background, fighter, missile, explosion, missileSound, game_overSound, clock, destroy_sound, fullHeart, emptyHeart, heart_item, clear_item, missile_item

def display_level_page(gamePad, level):
    font = pygame.font.Font('NanumGothic.ttf', 80)
    text = font.render(f'레벨 {level}', True, (255, 255, 255))
    textpos = text.get_rect(center=(padWidth / 2, padHeight / 2))
    gamePad.fill((0, 0, 0))
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.time.delay(2000)

def draw_hearts(gamePad, hearts, fullHeart, emptyHeart):
    heart_width = fullHeart.get_rect().width
    heart_height = fullHeart.get_rect().height
    for i in range(3):
        heart_img = fullHeart if i < hearts else emptyHeart
        drawObject(gamePad, heart_img, 10 + i * (heart_width + 10), padHeight - heart_height - 10)

def game_over(gamePad, game_overSound):
    writeMessage(gamePad, '게임 오버!', game_overSound)
    stopMusic()
    pygame.quit()
    sys.exit()

def check_pixel_collision(obj1, obj2, obj1_x, obj1_y, obj2_x, obj2_y):
    rect1 = obj1.get_rect(left=obj1_x, top=obj1_y)
    rect2 = obj2.get_rect(left=obj2_x, top=obj2_y)
    intersection = rect1.clip(rect2)
    return intersection.width > 0 and intersection.height > 0

def run_game(gamePad, background, fighter, missile, explosion, missileSound, game_overSound, clock, destroy_sound, fullHeart, emptyHeart, heart_item, clear_item, missile_item):
    fighterWidth, fighterHeight = fighter.get_rect().size
    x, y = padWidth * 0.45, padHeight * 0.9
    fighter_dx, fighter_dy = 0, 0
    missiles = []

    rockSpeed = random.choice([2, 3, 4])
    rock = Rock(random.choice(rock_images), 0, 0, random.randrange(0, padWidth), 0, rockSpeed, random.randint(1, 3))
    rock2 = None

    heart_itemX, heart_itemY, heart_itemSpeed, heart_itemAppear = random.randrange(0, padWidth), 0, 2, False

    missile_itemX, missile_itemY, missile_itemSpeed, missile_itemAppear, missileEnhanced, missileEnhanceEndTime = random.randrange(0, padWidth), 0, 3, False, False, 0

    clear_itemX, clear_itemY, clear_itemSpeed, clear_itemAppear = random.randrange(0, padWidth), 0, 3, False

    hearts, rocks_destroyed_count = 3, 0

    is_shot, shot_count, rocks_passed, game_running, level = False, 0, 0, True, 1

    last_pause_time, is_paused = time.time(), False

    display_level_page(gamePad, level)

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    fighter_dx = -5
                elif event.key == pygame.K_RIGHT:
                    fighter_dx = 5
                elif event.key == pygame.K_UP:
                    fighter_dy = -5
                elif event.key == pygame.K_DOWN:
                    fighter_dy = 5
                elif event.key == pygame.K_SPACE:
                    missileSound.play()
                    missiles.append([x + fighterWidth / 2, y - fighterHeight])
                    if missileEnhanced:
                        missiles.append([x + fighterWidth / 2 - 20, y - fighterHeight])
                elif event.key == pygame.K_p:
                    if time.time() - last_pause_time > 0.5:  # Debounce for 0.5 seconds
                        is_paused = not is_paused
                        if is_paused:
                            stopMusic()
                        else:
                            playMusic(os.path.join('assets/sounds', 'music.wav'))
                        last_pause_time = time.time()
            if event.type == pygame.KEYUP:
                if event.key in {pygame.K_LEFT, pygame.K_RIGHT}:
                    fighter_dx = 0
                elif event.key in {pygame.K_UP, pygame.K_DOWN}:
                    fighter_dy = 0

        if is_paused:
            continue

        gamePad.blit(background, (0, 0))
        x = max(0, min(x + fighter_dx, padWidth - fighterWidth))
        y = max(0, min(y + fighter_dy, padHeight - fighterHeight))

        fighterRect = pygame.Rect(x, y, fighterWidth, fighterHeight)
        rockRect = pygame.Rect(rock.x, rock.y, rock.width, rock.height)

        if fighterRect.colliderect(rockRect):
            hearts -= 1
            if hearts == 0:
                game_over(gamePad, game_overSound)
            else:
                rock.reset()

        if rock2:
            rock2Rect = pygame.Rect(rock2.x, rock2.y, rock2.width, rock2.height)
            if fighterRect.colliderect(rock2Rect):
                hearts -= 1
                if hearts == 0:
                    game_over(gamePad, game_overSound)
                else:
                    rock2 = None

        drawObject(gamePad, fighter, x, y)

        if rocks_passed == 3 or hearts == 0:
            game_over(gamePad, game_overSound)

        new_missiles = []
        for bx, by in missiles:
            by -= 10
            if by > 0:
                if check_pixel_collision(rock.image, missile, rock.x, rock.y, bx, by):
                    rock.hits_taken += 1
                    if rock.hits_taken >= rock.hits_needed:
                        rock.reset()
                        rocks_destroyed_count += 1
                    destroy_sound.play()
                elif rock2 and check_pixel_collision(rock2.image, missile, rock2.x, rock2.y, bx, by):
                    rock2.hits_taken += 1
                    if rock2.hits_taken >= rock2.hits_needed:
                        rock2.reset()
                        rocks_destroyed_count += 1
                    destroy_sound.play()
                else:
                    new_missiles.append([bx, by])

        missiles = new_missiles


        for bx, by in missiles:
            drawObject(gamePad, missile, bx, by)

        if not clear_itemAppear and random.random() < 0.007:
            clear_itemX, clear_itemY, clear_itemAppear = random.randrange(0, padWidth - clear_item.get_rect().width), 0, True

        if clear_itemAppear:
            clear_itemY += clear_itemSpeed
            drawObject(gamePad, clear_item, clear_itemX, clear_itemY)
            if clear_itemY > padHeight:
                clear_itemAppear = False
            if y < clear_itemY + clear_item.get_rect().height and clear_itemX < x < clear_itemX + clear_item.get_rect().width:
                clear_itemAppear = False
                rock.reset()
                rock2 = None
                rocks_passed = 0

        if rocks_destroyed_count >= 4 * level:
            level += 1
            display_level_page(gamePad, level)
            rocks_destroyed_count = 0
            rock.speed += 0.5

        writeScore(gamePad, shot_count)
        writeLevel(gamePad, level, padWidth, padHeight)
        rock.move()
        if rock.y > padHeight:
            rock.reset()
            rocks_passed += 1

        if rock2:
            rock2.move()
            if rock2.y > padHeight:
                rock2 = None
                rocks_passed += 1

        if not heart_itemAppear and random.random() < 0.007:
            heart_itemX, heart_itemY, heart_itemAppear = random.randrange(0, padWidth - heart_item.get_rect().width), 0, True

        if heart_itemAppear:
            heart_itemY += heart_itemSpeed
            drawObject(gamePad, heart_item, heart_itemX, heart_itemY)
            if heart_itemY > padHeight:
                heart_itemAppear = False
            if y < heart_itemY + heart_item.get_rect().height and heart_itemX < x < heart_itemX + heart_item.get_rect().width:
                hearts = min(3, hearts + 1)
                heart_itemAppear = False

        if not missile_itemAppear and random.random() < 0.002:
            missile_itemX, missile_itemY, missile_itemAppear = random.randrange(0, padWidth - missile_item.get_rect().width), 0, True

        if missile_itemAppear:
            missile_itemY += missile_itemSpeed
            drawObject(gamePad, missile_item, missile_itemX, missile_itemY)
            if missile_itemY > padHeight:
                missile_itemAppear = False
            if y < missile_itemY + missile_item.get_rect().height and missile_itemX < x < missile_itemX + missile_item.get_rect().width:
                missile_itemAppear = False
                missileEnhanced, missileEnhanceEndTime = True, pygame.time.get_ticks() + 5000

        if missileEnhanced and pygame.time.get_ticks() > missileEnhanceEndTime:
            missileEnhanced = False

        writePassed(gamePad, rocks_passed)
        writeScore(gamePad, rocks_destroyed_count)  # Update the display of destroyed rocks
        rock.draw(gamePad)
        if rock2:
            rock2.draw(gamePad)
        draw_hearts(gamePad, hearts, fullHeart, emptyHeart)

        if rocks_passed > 2:
            writeMessage(gamePad, '게임 오버!', game_overSound)
            game_running = False

        if check_pixel_collision(fighter, rock.image, x, y, rock.x, rock.y):
            hearts -= 1
            if hearts == 0:
                game_over(gamePad, game_overSound)
            else:
                rock.reset()

        if rock2:
            if check_pixel_collision(fighter, rock2.image, x, y, rock2.x, rock2.y):
                hearts -= 1
                if hearts == 0:
                    game_over(gamePad, game_overSound)
                else:
                    rock2 = None

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()