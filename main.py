import pygame
import random
from pygame import *

pygame.init()


class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, image_width, image_height, sprite_x, sprite_y, sprite_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(sprite_image), (image_width, image_height))

        self.rect = self.image.get_rect()

        self.rect.x = sprite_x
        self.rect.y = sprite_y
        self.sprite_speed = sprite_speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def special_reset(self, fucked_x, y):
        window.blit(self.image, (fucked_x, y))


class Snake(GameSprite):
    def update(self, snake_size1):
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
    pass


class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y):
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
    font_score = pygame.font.SysFont("Calibri", 16)
    value = font_score.render("Your Score: " + str(score), True, (0, 0, 139))
    window.blit(value, [0, 0])


def level(current_level):
    level_font = pygame.font.SysFont("Calibri", 26)
    value = level_font.render("Level " + str(current_level), True, (255, 0, 0))
    window.blit(value, [215, 0])


def draw_lives(window, x, y, lives_count, img):
    for i in range(lives_count):
        img_rect = img.get_rect()
        img_rect.x = x + 12 * i
        img_rect.y = y + 12
        window.blit(img, img_rect)
        window.blit(img, img_rect)


def our_snake(list_snake):
    for x1 in list_snake:
        snake.special_reset(x1[0], x1[1])


# Window
display_width = 500
display_height = 500
window = pygame.display.set_mode((display_width, display_height))
background = transform.scale(image.load("background.png"), (display_width, display_width))
load = transform.scale(image.load("loading.jpg"), (display_width, display_width))
# Snake
snake_image = 'snake.png'
snake_x = display_width // 2
snake_y = display_height // 2
snake_speed = 10
snake_size = 15
snake = Snake(snake_image, snake_size, snake_size, snake_x, snake_y, snake_speed)
# Food
food_image = 'food.png'
food_x = round(random.randrange(0, display_width - snake_size) // 10.0) * 10.0
food_y = round(random.randrange(0, display_height - snake_size) // 10.0) * 10.0
food_size = 12
food = Food(food_image, food_size, food_size, food_x, food_y, 0)
# WALLS
color_1 = 0
color_2 = 0
color_3 = 0

display.update()
display.set_caption('Snake')
game_over = transform.scale(image.load("game_over.png"), (display_width, display_height))

clock = pygame.time.Clock()

direction = ''
x1_change = 0
y1_change = 0

lives_count = 3
lives_img = transform.scale(image.load("heart.png"), (12, 12))

end = False
run = True

snake_list = []
snake_length = 1

current_level = 5

while run:
    keys = key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT:
            run = False

    if not end:
        window.blit(background, (0, 0))
        snake.update(snake_size)
        snake.reset()
        food.reset()
        player_score(snake_length - 1)
        level(current_level)
        draw_lives(window, 0, 0, lives_count, lives_img)
        snake_head = [snake.rect.x, snake.rect.y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        our_snake(snake_list)

        for x in snake_list[:-1]:
            if x == snake_head:
                lives_count -= 1

        if snake.rect.x > display_width or snake.rect.x < 0 or snake.rect.y > display_height or snake.rect.y < 0:
            lives_count -= 1

        if lives_count == 0:
            end = True
            window.blit(game_over, (0, 0))

        if sprite.collide_rect(snake, food):
            food.rect.x = round(random.randrange(0, display_width - snake_size) // 10.0) * 10.0
            food.rect.y = round(random.randrange(0, display_height - snake_size) // 10.0) * 10.0
            food.reset()
            snake_length += 1

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
            direction = ''
            x1_change = 0
            y1_change = 0
            window.blit(load, (0, 0))
            display.update()
            time.wait(1000)

        if current_level == 2:
            wall_width = 10
            wall_height = 100
            wall_x = 240
            wall_y = 400
            vertical_wall_1 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 10
            wall_height = 100
            wall_x = 240
            wall_y = 0
            vertical_wall_2 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 100
            wall_height = 10
            wall_x = 0
            wall_y = 240
            horizontal_wall_1 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 100
            wall_height = 10
            wall_x = 400
            wall_y = 240
            horizontal_wall_2 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            vertical_wall_1.draw_rect()
            vertical_wall_2.draw_rect()
            horizontal_wall_1.draw_rect()
            horizontal_wall_2.draw_rect()
            if sprite.collide_rect(horizontal_wall_1, food) or sprite.collide_rect(horizontal_wall_2, food) or \
                    sprite.collide_rect(vertical_wall_1, food) or sprite.collide_rect(vertical_wall_2, food):
                food.rect.x = round(random.randrange(0, display_width - snake_size) // 10.0) * 10.0
                food.rect.y = round(random.randrange(0, display_height - snake_size) // 10.0) * 10.0
                food.reset()
            if sprite.collide_rect(horizontal_wall_1, snake) or sprite.collide_rect(horizontal_wall_2, snake) or \
                    sprite.collide_rect(vertical_wall_1, snake) or sprite.collide_rect(vertical_wall_2, snake):
                lives_count -= 1

        if current_level == 3:
            wall_width = 10
            wall_height = 100
            wall_x = 240
            wall_y = 400
            vertical_wall_1 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 10
            wall_height = 100
            wall_x = 240
            wall_y = 0
            vertical_wall_2 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 5
            wall_height = 60
            wall_x = 110
            wall_y = 70
            vertical_wall_3 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 5
            wall_height = 60
            wall_x = 390
            wall_y = 70
            vertical_wall_4 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 5
            wall_height = 60
            wall_x = 390
            wall_y = 370
            vertical_wall_5 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 5
            wall_height = 60
            wall_x = 110
            wall_y = 370
            vertical_wall_6 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 100
            wall_height = 10
            wall_x = 0
            wall_y = 240
            horizontal_wall_1 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 100
            wall_height = 10
            wall_x = 400
            wall_y = 240
            horizontal_wall_2 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            vertical_wall_1.draw_rect()
            vertical_wall_2.draw_rect()
            vertical_wall_3.draw_rect()
            vertical_wall_4.draw_rect()
            vertical_wall_5.draw_rect()
            vertical_wall_6.draw_rect()
            horizontal_wall_1.draw_rect()
            horizontal_wall_2.draw_rect()
            if sprite.collide_rect(horizontal_wall_1, food) or sprite.collide_rect(horizontal_wall_2, food) or \
                    sprite.collide_rect(vertical_wall_1, food) or sprite.collide_rect(vertical_wall_2, food) or \
                    sprite.collide_rect(vertical_wall_3, food) or sprite.collide_rect(vertical_wall_4, food) or \
                    sprite.collide_rect(vertical_wall_5, food) or sprite.collide_rect(vertical_wall_6, food):
                food.rect.x = round(random.randrange(0, display_width - snake_size) // 10.0) * 10.0
                food.rect.y = round(random.randrange(0, display_height - snake_size) // 10.0) * 10.0
                food.reset()
            if sprite.collide_rect(horizontal_wall_1, snake) or sprite.collide_rect(horizontal_wall_2, snake) or \
                    sprite.collide_rect(vertical_wall_1, snake) or sprite.collide_rect(vertical_wall_2, snake)or \
                    sprite.collide_rect(vertical_wall_3, snake) or sprite.collide_rect(vertical_wall_4, snake) or \
                    sprite.collide_rect(vertical_wall_5, snake) or sprite.collide_rect(vertical_wall_6, snake):
                lives_count -= 1

        if current_level == 4:
            wall_width = 10
            wall_height = 100
            wall_x = 240
            wall_y = 400
            vertical_wall_1 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 10
            wall_height = 100
            wall_x = 240
            wall_y = 0
            vertical_wall_2 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 5
            wall_height = 60
            wall_x = 110
            wall_y = 70
            vertical_wall_3 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 5
            wall_height = 60
            wall_x = 390
            wall_y = 70
            vertical_wall_4 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 5
            wall_height = 60
            wall_x = 390
            wall_y = 370
            vertical_wall_5 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 5
            wall_height = 60
            wall_x = 110
            wall_y = 370
            vertical_wall_6 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 100
            wall_height = 10
            wall_x = 0
            wall_y = 240
            horizontal_wall_1 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 100
            wall_height = 10
            wall_x = 400
            wall_y = 240
            horizontal_wall_2 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 50
            wall_height = 50
            wall_x = 220
            wall_y = 220
            central_square = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            vertical_wall_1.draw_rect()
            vertical_wall_2.draw_rect()
            vertical_wall_3.draw_rect()
            vertical_wall_4.draw_rect()
            vertical_wall_5.draw_rect()
            vertical_wall_6.draw_rect()
            horizontal_wall_1.draw_rect()
            horizontal_wall_2.draw_rect()
            central_square.draw_rect()
            if sprite.collide_rect(horizontal_wall_1, food) or sprite.collide_rect(horizontal_wall_2, food) or \
                    sprite.collide_rect(vertical_wall_1, food) or sprite.collide_rect(vertical_wall_2, food) or \
                    sprite.collide_rect(vertical_wall_3, food) or sprite.collide_rect(vertical_wall_4, food) or \
                    sprite.collide_rect(vertical_wall_5, food) or sprite.collide_rect(vertical_wall_6, food) or \
                    sprite.collide_rect(central_square, food):
                food.rect.x = round(random.randrange(0, display_width - snake_size) // 10.0) * 10.0
                food.rect.y = round(random.randrange(0, display_height - snake_size) // 10.0) * 10.0
                food.reset()
            if sprite.collide_rect(horizontal_wall_1, snake) or sprite.collide_rect(horizontal_wall_2, snake) or \
                    sprite.collide_rect(vertical_wall_1, snake) or sprite.collide_rect(vertical_wall_2, snake) or \
                    sprite.collide_rect(vertical_wall_3, snake) or sprite.collide_rect(vertical_wall_4, snake) or \
                    sprite.collide_rect(vertical_wall_5, snake) or sprite.collide_rect(vertical_wall_6, snake) or \
                    sprite.collide_rect(central_square, snake):
                lives_count -= 1

        if current_level == 5:
            wall_width = 10
            wall_height = 100
            wall_x = 240
            wall_y = 400
            vertical_wall_1 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 10
            wall_height = 100
            wall_x = 240
            wall_y = 0
            vertical_wall_2 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 40
            wall_height = 40
            wall_x = 90
            wall_y = 70
            vertical_wall_3 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 40
            wall_height = 40
            wall_x = 380
            wall_y = 70
            vertical_wall_4 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 40
            wall_height = 40
            wall_x = 380
            wall_y = 370
            vertical_wall_5 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 40
            wall_height = 40
            wall_x = 90
            wall_y = 370
            vertical_wall_6 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 100
            wall_height = 10
            wall_x = 0
            wall_y = 240
            horizontal_wall_1 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 100
            wall_height = 10
            wall_x = 400
            wall_y = 240
            horizontal_wall_2 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            wall_width = 50
            wall_height = 50
            wall_x = 220
            wall_y = 220
            central_square = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
            vertical_wall_1.draw_rect()
            vertical_wall_2.draw_rect()
            vertical_wall_3.draw_rect()
            vertical_wall_4.draw_rect()
            vertical_wall_5.draw_rect()
            vertical_wall_6.draw_rect()
            horizontal_wall_1.draw_rect()
            horizontal_wall_2.draw_rect()
            central_square.draw_rect()
            if sprite.collide_rect(horizontal_wall_1, food) or sprite.collide_rect(horizontal_wall_2, food) or \
                    sprite.collide_rect(vertical_wall_1, food) or sprite.collide_rect(vertical_wall_2, food) or \
                    sprite.collide_rect(vertical_wall_3, food) or sprite.collide_rect(vertical_wall_4, food) or \
                    sprite.collide_rect(vertical_wall_5, food) or sprite.collide_rect(vertical_wall_6, food) or \
                    sprite.collide_rect(central_square, food):
                food.rect.x = round(random.randrange(0, display_width - snake_size) // 10.0) * 10.0
                food.rect.y = round(random.randrange(0, display_height - snake_size) // 10.0) * 10.0
                food.reset()
            if sprite.collide_rect(horizontal_wall_1, snake) or sprite.collide_rect(horizontal_wall_2, snake) or \
                    sprite.collide_rect(vertical_wall_1, snake) or sprite.collide_rect(vertical_wall_2, snake) or \
                    sprite.collide_rect(vertical_wall_3, snake) or sprite.collide_rect(vertical_wall_4, snake) or \
                    sprite.collide_rect(vertical_wall_5, snake) or sprite.collide_rect(vertical_wall_6, snake) or \
                    sprite.collide_rect(central_square, snake):
                lives_count -= 1
        display.update()

    clock.tick(snake_speed)
