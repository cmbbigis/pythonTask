import sys

import pygame
import random
from pygame import *
import pygame_menu

pygame.init()


class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, image_width, image_height,
                 sprite_x, sprite_y, sprite_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(sprite_image),
                                     (image_width, image_height))

        self.rect = self.image.get_rect()

        self.rect.x = sprite_x
        self.rect.y = sprite_y
        self.sprite_speed = sprite_speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def special_reset(self, fucked_x, y):
        window.blit(self.image, (fucked_x, y))

    def food_reset(self):
        surf.blit(self.image, (self.rect.x, self.rect.y))


class Snake(GameSprite):
    def update(self, snake_size1):
        global snake_speed
        global x1_change
        global y1_change
        global direction
        keys = key.get_pressed()
        if keys[K_LEFT]:
            if direction == 'RIGHT' and snake_length > 1:
                pass
            else:
                direction = 'LEFT'
                x1_change = -snake_size1
                y1_change = 0
        if keys[K_RIGHT]:
            if direction == 'LEFT' and snake_length > 1:
                pass
            else:
                direction = 'RIGHT'
                x1_change = snake_size1
                y1_change = 0
        elif keys[K_UP]:
            if direction == 'DOWN' and snake_length > 1:
                pass
            else:
                direction = "UP"
                y1_change = -snake_size1
                x1_change = 0
        elif keys[K_DOWN]:
            if direction == 'UP' and snake_length > 1:
                pass
            else:
                direction = "DOWN"
                y1_change = snake_size1
                x1_change = 0
        snake.rect.x += x1_change
        snake.rect.y += y1_change


class Food(GameSprite):
    def is_collide_with_snake(self):
        if sprite.collide_rect(self, snake):
            return True
        else:
            return False


class SpeedUpFood(Food):
    pass


class SpeedDownFood(Food):
    pass


class BadFood(Food):
    pass


class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3,
                 wall_width, wall_height, wall_x, wall_y):
        sprite.Sprite.__init__(self)
        self.width = wall_width
        self.height = wall_height
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3

        self.image = Surface([self.width, self.height])
        self.image.fill((color_1, color_2, color_3))

        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_rect(self):
        draw.rect(window, (self.color_1, self.color_2, self.color_3),
                  (self.rect.x, self.rect.y, self.width, self.height))


def player_score(score):
    font_score = pygame.font.SysFont("Calibri", 24, True)
    value = font_score.render("Your Score: " + str(score), True, (97, 55, 0))
    window.blit(value, [0, 500])


def level(current_level):
    level_font = pygame.font.SysFont("Calibri", 24, True)
    value = level_font.render("Level " + str(current_level),
                              True, (102, 51, 0))
    window.blit(value, [215, 500])
    window.blit(value, [215, 500])


def draw_lives(window, x, y, lives_count, img):
    for i in range(lives_count):
        img_rect = img.get_rect()
        img_rect.x = x + 24 * i
        img_rect.y = y + 24
        window.blit(img, img_rect)
        window.blit(img, img_rect)


def our_snake(list_snake):
    for x1 in list_snake:
        snake.special_reset(x1[0], x1[1])


def respawn_other_food(food_type):
    if food_type == "bad_food":
        for i in range(1):
            surf.fill((0, 255, 0))
            bad_food.rect.x = \
                round(random.randrange(0, display_width - snake_size)
                      // 10.0) * 10.0
            bad_food.rect.y = \
                round(random.randrange(0, display_width - snake_size)
                      // 10.0) * 10.0
            bad_food.food_reset()
    if food_type == "speed_up_food":
        for i in range(1):
            surf.fill((0, 255, 0))
            speed_up_food.rect.x = \
                round(random.randrange(0, display_width - snake_size)
                      // 10.0) * 10.0
            speed_up_food.rect.y = \
                round(random.randrange(0, display_width - snake_size)
                      // 10.0) * 10.0
            speed_up_food.food_reset()
    if food_type == "speed_down_food":
        for i in range(1):
            surf.fill((0, 255, 0))
            speed_down_food.rect.x = \
                round(random.randrange(0, display_width - snake_size)
                      // 10.0) * 10.0
            speed_down_food.rect.y = \
                round(random.randrange(0, display_width - snake_size)
                      // 10.0) * 10.0
            speed_down_food.food_reset()
    if food_type == "food":
        for i in range(1):
            surf.fill((0, 255, 0))
            food.rect.x = \
                round(random.randrange(0, display_width - snake_size)
                      // 10.0) * 10.0
            food.rect.y = \
                round(random.randrange(0, display_width - snake_size)
                      // 10.0) * 10.0
            food.food_reset()


# Window
display_width = 500
display_height = 500
actual_display_height = 600
window = pygame.display.set_mode(
    (display_width, actual_display_height))
background = transform.scale(
    image.load("pictures/background.png"),
    (display_width, display_height))
load = transform.scale(
    image.load("pictures/loading.jpg"),
    (display_width, display_height))
surf = pygame.Surface((display_width, display_height))
surf.fill((0, 255, 0))
surf.set_alpha(150)
# HUD Background
hud_background = transform.scale(
    image.load("pictures/hud_background.jpg"), (display_width, 150))
# Snake
snake_image = 'pictures/snake.png'
snake_x = display_width // 2
snake_y = display_height // 2
snake_speed = 10
snake_size = 15
snake = Snake(snake_image, snake_size,
              snake_size, snake_x, snake_y, snake_speed)
# Food
food_image = 'pictures/food.png'
food_x = \
    round(random.randrange(0, display_width - snake_size)
          // 10.0) * 10.0
food_y = \
    round(random.randrange(0, display_height - snake_size)
          // 10.0) * 10.0
food_size = 12
food = Food(food_image, food_size, food_size, food_x, food_y, 0)
# Speed up food
speed_up_food_x =\
    round(random.randrange(0, display_width - snake_size)
          // 10.0) * 10.0
speed_up_food_y = \
    round(random.randrange(0, display_height - snake_size)
          // 10.0) * 10.0
speed_up_food_image = "pictures/speed_up.png"
speed_up_food = SpeedUpFood(speed_up_food_image,
                            food_size, food_size,
                            speed_up_food_x, speed_up_food_y, 0)
# Speed down food
speed_down_food_x = round(random.randrange(0, display_width - snake_size) // 10.0) * 10.0
speed_down_food_y = round(random.randrange(0, display_height - snake_size) // 10.0) * 10.0
speed_down_food_image = "pictures/speed_down.png"
speed_down_food = SpeedDownFood(speed_down_food_image,
                                food_size, food_size,
                                speed_down_food_x, speed_down_food_y, 0)
# Points down food
bad_food_x = \
    round(random.randrange(0, display_width - snake_size)
          // 10.0) * 10.0
bad_food_y = \
    round(random.randrange(0, display_height - snake_size)
          // 10.0) * 10.0
bad_food_image = "pictures/bad_food.png"
bad_food = BadFood(bad_food_image, food_size,
                   food_size, bad_food_x, bad_food_y, 0)
# WALLS
color_1 = 0
color_2 = 0
color_3 = 0

display.update()
display.set_caption('Snake')
game_over = transform.scale(image.load("pictures/game_over.png"),
                            (display_width, display_height))

clock = pygame.time.Clock()

direction = ''
x1_change = 0
y1_change = 0

lives_count = 3
lives_img = transform.scale(image.load("pictures/heart.png"), (24, 24))

end = False
run = True

snake_list = []
snake_length = 1

all_food = ["bad_food", "speed_up_food", "speed_down_food"]
other_food_type = all_food[random.randint(0, 2)]

food_collide_snake = False
bad_food_collide_snake = False
speed_up_food_collide_snake = False
speed_down_food_collide_snake = False

def start_the_game(current_level=1):
    global run, x, end, snake, snake_speed, \
        other_food_type, snake_length, lives_count, snake_x, snake_y
    while run:
        food_collide_snake = False
        bad_food_collide_snake = False
        speed_up_food_collide_snake = False
        speed_down_food_collide_snake = False

        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()

        if not end:
            window.blit(hud_background, (0, 500))
            window.blit(background, (0, 0))
            window.blit(surf, (0, 0))
            snake.update(snake_speed)
            snake.reset()
            food.food_reset()
            if other_food_type == "bad_food":
                bad_food.food_reset()
            if other_food_type == "speed_up_food":
                speed_up_food.food_reset()
            if other_food_type == "speed_down_food":
                speed_down_food.food_reset()

            player_score(snake_length - 1)
            level(current_level)
            draw_lives(window, 0, 510, lives_count, lives_img)
            snake_head = [snake.rect.x, snake.rect.y]
            snake_list.append(snake_head)
            if len(snake_list) > snake_length:
                del snake_list[0]

            our_snake(snake_list)

            for x in snake_list[:-1]:
                if x == snake_head:
                    lives_count -= 1

            if snake.rect.x > display_width or \
                    snake.rect.x < 0 or \
                    snake.rect.y > display_height or \
                    snake.rect.y < 0:
                lives_count -= 1

            if lives_count == 0:
                end = True
                window.blit(game_over, (0, 0))

            if snake.rect.x > display_width:
                snake.rect.x = 0
            elif snake.rect.x < 0:
                snake.rect.x = display_width
            elif snake.rect.y >= display_height-10:
                snake.rect.y = 0
                lives_count -= 1
            elif snake.rect.y < 0:
                snake.rect.y = display_height - snake_size

            if sprite.collide_rect(snake, food):
                food_collide_snake = True
                respawn_other_food("food")
                snake_length += 1
                other_food_type = all_food[random.randint(0, 2)]
                respawn_other_food(other_food_type)

            if sprite.collide_rect(snake, bad_food):
                bad_food_collide_snake = True
                if snake_length >= 1:
                    snake_length -= 1
                    del snake_list[len(snake_list) - 1]
                else:
                    lives_count -= 1
                other_food_type = all_food[random.randint(0, 2)]
                respawn_other_food(other_food_type)
                respawn_other_food("food")

            if sprite.collide_rect(snake, speed_up_food):
                speed_up_food_collide_snake = True
                snake_speed *= 1.1
                other_food_type = all_food[random.randint(0, 2)]
                respawn_other_food(other_food_type)
                respawn_other_food("food")

            if sprite.collide_rect(snake, speed_down_food):
                speed_down_food_collide_snake = True
                snake_speed *= 0.9
                other_food_type = all_food[random.randint(0, 2)]
                respawn_other_food(other_food_type)
                respawn_other_food("food")

            if snake_length - 1 == 5:
                current_level += 1
                if current_level >= 4:
                    snake_x = 50
                    snake_y = 50
                snake.rect.x = snake_x
                snake.rect.y = snake_y
                snake_length = 1
                snake_head = [snake.rect.x, snake.rect.y]
                snake_list.clear()
                snake_list.append(snake_head)
                lives_count = 3
                window.blit(load, (0, 0))
                display.update()
                time.wait(1000)

            if current_level == 2:
                wall_width = 10
                wall_height = 100
                wall_x = 240
                wall_y = 400
                vertical_wall_1 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 10
                wall_height = 100
                wall_x = 240
                wall_y = 0
                vertical_wall_2 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 100
                wall_height = 10
                wall_x = 0
                wall_y = 240
                horizontal_wall_1 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 100
                wall_height = 10
                wall_x = 400
                wall_y = 240
                horizontal_wall_2 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                vertical_wall_1.draw_rect()
                vertical_wall_2.draw_rect()
                horizontal_wall_1.draw_rect()
                horizontal_wall_2.draw_rect()
                if sprite.collide_rect(horizontal_wall_1, food) or \
                        sprite.collide_rect(horizontal_wall_2, food) or \
                        sprite.collide_rect(vertical_wall_1, food) or \
                        sprite.collide_rect(vertical_wall_2, food):
                    food.rect.x = \
                        round(random.randrange(0, display_width - snake_size)
                              // 10.0) * 10.0
                    food.rect.y = \
                        round(random.randrange(0, display_height - snake_size)
                              // 10.0) * 10.0
                    food.reset()
                if sprite.collide_rect(horizontal_wall_1, snake) or \
                        sprite.collide_rect(horizontal_wall_2, snake) or \
                        sprite.collide_rect(vertical_wall_1, snake) or \
                        sprite.collide_rect(vertical_wall_2, snake):
                    lives_count -= 1

            if current_level == 3:
                wall_width = 10
                wall_height = 100
                wall_x = 240
                wall_y = 400
                vertical_wall_1 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 10
                wall_height = 100
                wall_x = 240
                wall_y = 0
                vertical_wall_2 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 5
                wall_height = 60
                wall_x = 110
                wall_y = 70
                vertical_wall_3 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 5
                wall_height = 60
                wall_x = 390
                wall_y = 70
                vertical_wall_4 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 5
                wall_height = 60
                wall_x = 390
                wall_y = 370
                vertical_wall_5 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 5
                wall_height = 60
                wall_x = 110
                wall_y = 370
                vertical_wall_6 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 100
                wall_height = 10
                wall_x = 0
                wall_y = 240
                horizontal_wall_1 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 100
                wall_height = 10
                wall_x = 400
                wall_y = 240
                horizontal_wall_2 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                vertical_wall_1.draw_rect()
                vertical_wall_2.draw_rect()
                vertical_wall_3.draw_rect()
                vertical_wall_4.draw_rect()
                vertical_wall_5.draw_rect()
                vertical_wall_6.draw_rect()
                horizontal_wall_1.draw_rect()
                horizontal_wall_2.draw_rect()
                if sprite.collide_rect(horizontal_wall_1, food) or \
                        sprite.collide_rect(horizontal_wall_2, food) or \
                        sprite.collide_rect(vertical_wall_1, food) or \
                        sprite.collide_rect(vertical_wall_2, food) or \
                        sprite.collide_rect(vertical_wall_3, food) or \
                        sprite.collide_rect(vertical_wall_4, food) or \
                        sprite.collide_rect(vertical_wall_5, food) or \
                        sprite.collide_rect(vertical_wall_6, food):
                    food.rect.x = \
                        round(random.randrange(0, display_width - snake_size)
                              // 10.0) * 10.0
                    food.rect.y = \
                        round(random.randrange(0, display_height - snake_size)
                              // 10.0) * 10.0
                    food.reset()
                if sprite.collide_rect(horizontal_wall_1, snake) or \
                        sprite.collide_rect(horizontal_wall_2, snake) or \
                        sprite.collide_rect(vertical_wall_1, snake) or \
                        sprite.collide_rect(vertical_wall_2, snake) or \
                        sprite.collide_rect(vertical_wall_3, snake) or \
                        sprite.collide_rect(vertical_wall_4, snake) or \
                        sprite.collide_rect(vertical_wall_5, snake) or \
                        sprite.collide_rect(vertical_wall_6, snake):
                    lives_count -= 1

            if current_level == 4:
                wall_width = 10
                wall_height = 100
                wall_x = 240
                wall_y = 400
                vertical_wall_1 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 10
                wall_height = 100
                wall_x = 240
                wall_y = 0
                vertical_wall_2 =\
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 5
                wall_height = 60
                wall_x = 110
                wall_y = 70
                vertical_wall_3 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 5
                wall_height = 60
                wall_x = 390
                wall_y = 70
                vertical_wall_4 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 5
                wall_height = 60
                wall_x = 390
                wall_y = 370
                vertical_wall_5 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 5
                wall_height = 60
                wall_x = 110
                wall_y = 370
                vertical_wall_6 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 100
                wall_height = 10
                wall_x = 0
                wall_y = 240
                horizontal_wall_1 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 100
                wall_height = 10
                wall_x = 400
                wall_y = 240
                horizontal_wall_2 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 50
                wall_height = 50
                wall_x = 220
                wall_y = 220
                central_square = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                vertical_wall_1.draw_rect()
                vertical_wall_2.draw_rect()
                vertical_wall_3.draw_rect()
                vertical_wall_4.draw_rect()
                vertical_wall_5.draw_rect()
                vertical_wall_6.draw_rect()
                horizontal_wall_1.draw_rect()
                horizontal_wall_2.draw_rect()
                central_square.draw_rect()
                if sprite.collide_rect(horizontal_wall_1, food) or \
                        sprite.collide_rect(horizontal_wall_2, food) or \
                        sprite.collide_rect(vertical_wall_1, food) or \
                        sprite.collide_rect(vertical_wall_2, food) or \
                        sprite.collide_rect(vertical_wall_3, food) or \
                        sprite.collide_rect(vertical_wall_4, food) or \
                        sprite.collide_rect(vertical_wall_5, food) or \
                        sprite.collide_rect(vertical_wall_6, food) or \
                        sprite.collide_rect(central_square, food):
                    food.rect.x = \
                        round(random.randrange(0, display_width - snake_size)
                              // 10.0) * 10.0
                    food.rect.y = \
                        round(random.randrange(0, display_height - snake_size)
                              // 10.0) * 10.0
                    food.reset()
                if sprite.collide_rect(horizontal_wall_1, snake) or \
                        sprite.collide_rect(horizontal_wall_2, snake) or \
                        sprite.collide_rect(vertical_wall_1, snake) or \
                        sprite.collide_rect(vertical_wall_2, snake) or \
                        sprite.collide_rect(vertical_wall_3, snake) or \
                        sprite.collide_rect(vertical_wall_4, snake) or \
                        sprite.collide_rect(vertical_wall_5, snake) or \
                        sprite.collide_rect(vertical_wall_6, snake) or \
                        sprite.collide_rect(central_square, snake):
                    lives_count -= 1

            if current_level == 5:
                wall_width = 10
                wall_height = 100
                wall_x = 240
                wall_y = 400
                vertical_wall_1 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 10
                wall_height = 100
                wall_x = 240
                wall_y = 0
                vertical_wall_2 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 40
                wall_height = 40
                wall_x = 90
                wall_y = 70
                vertical_wall_3 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 40
                wall_height = 40
                wall_x = 380
                wall_y = 70
                vertical_wall_4 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 40
                wall_height = 40
                wall_x = 380
                wall_y = 370
                vertical_wall_5 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 40
                wall_height = 40
                wall_x = 90
                wall_y = 370
                vertical_wall_6 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 100
                wall_height = 10
                wall_x = 0
                wall_y = 240
                horizontal_wall_1 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 100
                wall_height = 10
                wall_x = 400
                wall_y = 240
                horizontal_wall_2 = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                wall_width = 50
                wall_height = 50
                wall_x = 220
                wall_y = 220
                central_square = \
                    Wall(color_1, color_2, color_3,
                         wall_width, wall_height, wall_x, wall_y)
                vertical_wall_1.draw_rect()
                vertical_wall_2.draw_rect()
                vertical_wall_3.draw_rect()
                vertical_wall_4.draw_rect()
                vertical_wall_5.draw_rect()
                vertical_wall_6.draw_rect()
                horizontal_wall_1.draw_rect()
                horizontal_wall_2.draw_rect()
                central_square.draw_rect()
                if sprite.collide_rect(horizontal_wall_1, food) \
                        or sprite.collide_rect(horizontal_wall_2, food) or \
                        sprite.collide_rect(vertical_wall_1, food) \
                        or sprite.collide_rect(vertical_wall_2, food) or \
                        sprite.collide_rect(vertical_wall_3, food) \
                        or sprite.collide_rect(vertical_wall_4, food) or \
                        sprite.collide_rect(vertical_wall_5, food) \
                        or sprite.collide_rect(vertical_wall_6, food) or \
                        sprite.collide_rect(central_square, food):
                    food.rect.x = \
                        round(random.randrange(0, display_width - snake_size)
                              // 10.0) * 10.0
                    food.rect.y = \
                        round(random.randrange(0, display_height - snake_size)
                              // 10.0) * 10.0
                    food.reset()
                if sprite.collide_rect(horizontal_wall_1, snake) \
                        or sprite.collide_rect(horizontal_wall_2, snake) or \
                        sprite.collide_rect(vertical_wall_1, snake) \
                        or sprite.collide_rect(vertical_wall_2, snake) or \
                        sprite.collide_rect(vertical_wall_3, snake) \
                        or sprite.collide_rect(vertical_wall_4, snake) or \
                        sprite.collide_rect(vertical_wall_5, snake) \
                        or sprite.collide_rect(vertical_wall_6, snake) or \
                        sprite.collide_rect(central_square, snake):
                    lives_count -= 1
            display.update()

        clock.tick(snake_speed)


menu = pygame_menu.Menu('Welcome', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)
menu.add.text_input('Имя: ', default='Игрок 1')
menu.add.button('Играть', start_the_game)
menu.add.button('Выход', pygame_menu.events.EXIT)
menu.mainloop(window)
