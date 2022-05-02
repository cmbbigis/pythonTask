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

def Your_score(score):
    font_score = pygame.font.SysFont(None, 20)
    value = font_score.render("Your Score: " + str(score), True, (0, 0, 139))
    window.blit(value, [0, 20])

def draw_lives(window, x, y, lives_count, img):
    for i in range(lives_count):
        img_rect = img.get_rect()
        img_rect.x = x + 12 * i
        img_rect.y = y
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
        Your_score(snake_length - 1)
        draw_lives(window, 0, 0, lives_count, lives_img)
        snake_head = [snake.rect.x, snake.rect.y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        our_snake(snake_list)

        for x in snake_list[:-1]:
            if x == snake_head:
                if lives_count <= 1:
                    end = True
                    window.blit(game_over, (0, 0))
                else:
                    lives_count -= 1

        if snake.rect.x > display_width or snake.rect.x < 0 or snake.rect.y > display_height or snake.rect.y < 0:
            if lives_count <= 1:
                end = True
                window.blit(game_over, (0, 0))
            else:
                lives_count -= 1

        display.update()

        if sprite.collide_rect(snake, food):
            food.rect.x = round(random.randrange(0, display_width - snake_size) // 10.0) * 10.0
            food.rect.y = round(random.randrange(0, display_height - snake_size) // 10.0) * 10.0
            food.reset()
            snake_length += 1

    clock.tick(snake_speed)
