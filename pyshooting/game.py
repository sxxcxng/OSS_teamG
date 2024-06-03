import pygame
import sys
import random
from pyshooting.resources import padWidth, padHeight, rock_images, explosion_sound
from pyshooting.graphics import draw_object, write_score, write_passed, write_level
from pyshooting.messages import write_message
from pyshooting.audio import load_sounds, play_music, stop_music
import os
import time

class Rock:
    def __init__(self, image, x, y, speed, hits_needed, x_speed=0):
        self.image = pygame.image.load(image)
        self.width, self.height = self.image.get_rect().size
        self.x = x
        self.y = y
        self.speed = speed
        self.hits_needed = hits_needed
        self.hits_taken = 0
        self.x_speed = x_speed

    def draw(self, screen):
        draw_object(screen, self.image, self.x, self.y)
        font = pygame.font.SysFont(None, 25)
        text = font.render(str(self.hits_needed - self.hits_taken), True, (255, 0, 0))
        screen.blit(text, (self.x + self.width, self.y))

    def move(self):
        self.y += self.speed
        self.x += self.x_speed
        if self.x < 0 or self.x > padWidth - self.width:
            self.x_speed = -self.x_speed

    def reset(self):
        self.image = pygame.image.load(random.choice(rock_images))
        self.width, self.height = self.image.get_rect().size
        self.x = random.randrange(0, padWidth - self.width)
        self.y = -self.height
        self.speed += 0.02
        self.hits_needed = random.randint(1, 3)
        self.hits_taken = 0

def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting')
    image_dir = 'assets/images'
    background = pygame.image.load(os.path.join(image_dir, 'background.png'))
    fighter = pygame.image.load(os.path.join(image_dir, 'fighter.png'))
    missile = pygame.image.load(os.path.join(image_dir, 'missile.png'))
    explosion = pygame.image.load(os.path.join(image_dir, 'explosion.png'))
    full_heart = pygame.image.load(os.path.join(image_dir, 'full_heart.png'))
    empty_heart = pygame.image.load(os.path.join(image_dir, 'empty_heart.png'))
    heart_item = pygame.image.load(os.path.join(image_dir, 'full_heart.png'))
    clear_item = pygame.image.load(os.path.join(image_dir, 'clear_item.png'))
    missile_item = pygame.image.load(os.path.join(image_dir, 'missile_item.png'))
    clock = pygame.time.Clock()
    missile_sound, game_over_sound, destroy_sound = load_sounds()
    play_music(os.path.join('assets/sounds', 'music.wav'))
    return screen, background, fighter, missile, explosion, missile_sound, game_over_sound, clock, destroy_sound, full_heart, empty_heart, heart_item, clear_item, missile_item

def display_level_page(screen, level):
    font = pygame.font.Font('NanumGothic.ttf', 80)
    text = font.render(f'레벨 {level}', True, (255, 255, 255))
    textpos = text.get_rect(center=(padWidth / 2, padHeight / 2))
    screen.fill((0, 0, 0))
    screen.blit(text, textpos)
    pygame.display.update()
    pygame.time.delay(2000)

def draw_hearts(screen, hearts, full_heart, empty_heart):
    heart_width, heart_height = full_heart.get_rect().size
    for i in range(3):
        heart_img = full_heart if i < hearts else empty_heart
        draw_object(screen, heart_img, 10 + i * (heart_width + 10), padHeight - heart_height - 10)

def game_over(screen, game_over_sound):
    write_message(screen, '게임 오버!', game_over_sound)
    stop_music()
    pygame.quit()
    sys.exit()

def check_pixel_collision(obj1, obj2, obj1_x, obj1_y, obj2_x, obj2_y):
    rect1 = obj1.get_rect(left=obj1_x, top=obj1_y)
    rect2 = obj2.get_rect(left=obj2_x, top=obj2_y)
    intersection = rect1.clip(rect2)
    return intersection.width > 0 and intersection.height > 0

def run_game(screen, background, fighter, missile, explosion, missile_sound, game_over_sound, clock, destroy_sound, full_heart, empty_heart, heart_item, clear_item, missile_item):
    fighter_width, fighter_height = fighter.get_rect().size
    x, y = padWidth * 0.45, padHeight * 0.9
    fighter_dx, fighter_dy = 0, 0
    missiles = []

    rock_speed = random.choice([2, 3, 4])
    rock = Rock(random.choice(rock_images), random.randrange(0, padWidth), 0, rock_speed, random.randint(1, 3))
    rock2 = None

    heart_item_x, heart_item_y, heart_item_speed, heart_item_visible = random.randrange(0, padWidth), 0, 2, False

    missile_item_x, missile_item_y, missile_item_speed, missile_item_visible, missile_enhanced, missile_enhance_end_time = random.randrange(0, padWidth), 0, 3, False, False, 0

    clear_item_x, clear_item_y, clear_item_speed, clear_item_visible = random.randrange(0, padWidth), 0, 3, False

    hearts, rocks_destroyed_count = 3, 0
    rocks_passed, game_running, level = 0, True, 1

    last_pause_time, is_paused = time.time(), False

    display_level_page(screen, level)

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    fighter_dx = -5
                elif event.key == pygame.K_RIGHT:
                    fighter_dx = 5
                elif event.key == pygame.K_UP:
                    fighter_dy = -5
                elif event.key == pygame.K_DOWN:
                    fighter_dy = 5
                elif event.key == pygame.K_SPACE:
                    missile_sound.play()
                    missiles.append([x + fighter_width / 2, y - fighter_height])
                    if missile_enhanced:
                        missiles.append([x + fighter_width / 2 - 20, y - fighter_height])
                elif event.key == pygame.K_p:
                    if time.time() - last_pause_time > 0.5:
                        is_paused = not is_paused
                        stop_music() if is_paused else play_music(os.path.join('assets/sounds', 'music.wav'))
                        last_pause_time = time.time()
            elif event.type == pygame.KEYUP:
                if event.key in {pygame.K_LEFT, pygame.K_RIGHT}:
                    fighter_dx = 0
                elif event.key in {pygame.K_UP, pygame.K_DOWN}:
                    fighter_dy = 0

        if is_paused:
            continue

        screen.blit(background, (0, 0))
        x = max(0, min(x + fighter_dx, padWidth - fighter_width))
        y = max(0, min(y + fighter_dy, padHeight - fighter_height))

        fighter_rect = pygame.Rect(x, y, fighter_width, fighter_height)
        rock_rect = pygame.Rect(rock.x, rock.y, rock.width, rock.height)

        if fighter_rect.colliderect(rock_rect):
            hearts -= 1
            game_over(screen, game_over_sound) if hearts == 0 else rock.reset()

        if rock2 and fighter_rect.colliderect(pygame.Rect(rock2.x, rock2.y, rock2.width, rock2.height)):
            hearts -= 1
            game_over(screen, game_over_sound) if hearts == 0 else rock2.reset()

        draw_object(screen, fighter, x, y)

        if rocks_passed == 3 or hearts == 0:
            game_over(screen, game_over_sound)

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
            draw_object(screen, missile, bx, by)

        if not clear_item_visible and random.random() < 0.007:
            clear_item_x, clear_item_y, clear_item_visible = random.randrange(0, padWidth - clear_item.get_rect().width), 0, True

        if clear_item_visible:
            clear_item_y += clear_item_speed
            draw_object(screen, clear_item, clear_item_x, clear_item_y)
            if clear_item_y > padHeight:
                clear_item_visible = False
            if y < clear_item_y + clear_item.get_rect().height and clear_item_x < x < clear_item_x + clear_item.get_rect().width:
                clear_item_visible = False
                rock.reset()
                rock2 = None
                rocks_passed = 0

        if rocks_destroyed_count >= 4 * level:
            level += 1
            display_level_page(screen, level)
            rocks_destroyed_count = 0
            rock.speed += 0.5

        write_score(screen, rocks_destroyed_count)
        write_level(screen, level, padWidth, padHeight)
        rock.move()
        if rock.y > padHeight:
            rock.reset()
            rocks_passed += 1

        if rock2:
            rock2.move()
            if rock2.y > padHeight:
                rock2 = None
                rocks_passed += 1

        if not heart_item_visible and random.random() < 0.007:
            heart_item_x, heart_item_y, heart_item_visible = random.randrange(0, padWidth - heart_item.get_rect().width), 0, True

        if heart_item_visible:
            heart_item_y += heart_item_speed
            draw_object(screen, heart_item, heart_item_x, heart_item_y)
            if heart_item_y > padHeight:
                heart_item_visible = False
            if y < heart_item_y + heart_item.get_rect().height and heart_item_x < x < heart_item_x + heart_item.get_rect().width:
                hearts = min(3, hearts + 1)
                heart_item_visible = False

        if not missile_item_visible and random.random() < 0.002:
            missile_item_x, missile_item_y, missile_item_visible = random.randrange(0, padWidth - missile_item.get_rect().width), 0, True

        if missile_item_visible:
            missile_item_y += missile_item_speed
            draw_object(screen, missile_item, missile_item_x, missile_item_y)
            if missile_item_y > padHeight:
                missile_item_visible = False
            if y < missile_item_y + missile_item.get_rect().height and missile_item_x < x < missile_item_x + missile_item.get_rect().width:
                missile_item_visible = False
                missile_enhanced = True
                missile_enhance_end_time = pygame.time.get_ticks() + 5000

        if missile_enhanced and pygame.time.get_ticks() > missile_enhance_end_time:
            missile_enhanced = False

        write_passed(screen, rocks_passed)
        rock.draw(screen)
        if rock2:
            rock2.draw(screen)
        draw_hearts(screen, hearts, full_heart, empty_heart)

        if rocks_passed > 2:
            write_message(screen, '게임 오버!', game_over_sound)
            game_running = False

        if check_pixel_collision(fighter, rock.image, x, y, rock.x, rock.y):
            hearts -= 1
            game_over(screen, game_over_sound) if hearts == 0 else rock.reset()

        if rock2 and check_pixel_collision(fighter, rock2.image, x, y, rock2.x, rock2.y):
            hearts -= 1
            game_over(screen, game_over_sound) if hearts == 0 else rock2.reset()

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()
