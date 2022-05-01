from pygame import *


class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(sprite_image), (player_image_width, player_image_height))
        
        self.rect = self.image.get_rect()

        self.rect.x = sprite_x
        self.rect.y = sprite_y
        self.sprite_speed = sprite_speed

    def reset(self):
        first_window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):    
        keys = key.get_pressed()
        time.delay(5)   
        if keys[K_LEFT] and self.rect.x > self.sprite_speed:
            self.rect.x -= self.sprite_speed     
        elif keys[K_RIGHT] and self.rect.x < width_display - player_image_width:
            self.rect.x += self.sprite_speed
        elif keys[K_DOWN] and self.rect.y < height_display - player_image_height:
            self.rect.y += self.sprite_speed
        elif keys[K_UP] and self.rect.y > self.sprite_speed:
            self.rect.y -= self.sprite_speed


class Enemy(GameSprite):
    side = str()
    def update(self):
        if self.rect.y == 490:
            self.side = "up"
        elif self.rect.y == 690:
            self.side = "down"
        if self.side == "up":
            self.rect.y += self.sprite_speed
        elif self.side == "down":
            self.rect.y -= self.sprite_speed


class Finish(GameSprite):
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
        draw.rect(first_window, (self.color_1, self.color_2, self.color_3), (self.rect.x, self.rect.y, self.width, self.height))


# WINDOW SIZE
width_display = 1024
height_display = 768
# PLAYER SIZE
player_image_width = 80
player_image_height = 80
# WINDOW
first_window = display.set_mode((width_display, height_display))
display.set_caption("Лабиринт")
background = transform.scale(image.load("background.png"), (width_display, height_display))
# WALLS
color_1 = 0
color_2 = 0
color_3 = 0
wall_width = 10
wall_height = 600
wall_x = 230
wall_y = 0
# VERTICAL WALLS
vertical_wall = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
wall_height = 650
wall_x = 360
wall_y = 118
vertical_wall_1 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
wall_height = 370
wall_x = 890
wall_y = 118
vertical_wall_2 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
wall_height = 220
wall_x = 490
wall_y = 258
vertical_wall_3 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
# HORIZONTAL WALLS
wall_width = 100
wall_height = 10
wall_x = 0
wall_y = 100
horizontal_wall = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
wall_y = 400
horizontal_wall_1 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
wall_x = 130
wall_y = 250
horizontal_wall_2 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
wall_y = 550
horizontal_wall_3 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
wall_width = 530
wall_x = 360
wall_y = 118
horizontal_wall_4 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
wall_width = 400
wall_x = 490
wall_y = 478
horizontal_wall_5 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
wall_width = 280
wall_x = 490
wall_y = 258
horizontal_wall_6 = Wall(color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y)
# PLAYER
player_image = "2-2.png"
player_x = 3
player_y = 3 
player_speed = 3
player = Player(player_image, player_x, player_y, player_speed)
# ENEMY
enemy_image = "cyborg.png"
enemy_x = 490
enemy_y = 490
enemy_1_x = 655
enemy_1_y = 690 
enemy_2_x = 820
enemy_2_y = 490  
enemy_speed = 2
enemy = Enemy(enemy_image, enemy_x, enemy_y, enemy_speed)
enemy_1 = Enemy(enemy_image, enemy_1_x, enemy_1_y, enemy_speed)
enemy_2 = Enemy(enemy_image, enemy_2_x, enemy_2_y, enemy_speed)
# FINISH
finish_image = "trophy-1.png"
finish_x = 570
finish_y = 340
finish_speed = 0
finish = Finish(finish_image, finish_x, finish_y, finish_speed)
# GAME OVER / WIN
game_over = transform.scale(image.load("game-over_2.png"), (width_display, height_display))
win = transform.scale(image.load("winner_1-1.jpg"), (width_display, height_display)) 

end = False
# GAME
run = True
while run:  
    keys = key.get_pressed()
    for e in event.get():
        if e.type == QUIT:
            run = False
    if keys[K_SPACE]:
        end = False
        player.rect.x = player_x
        player.rect.y = player_y

    if not end:
        first_window.blit(background, (0, 0))

        vertical_wall.draw_rect()
        vertical_wall_1.draw_rect()
        vertical_wall_2.draw_rect()
        vertical_wall_3.draw_rect()

        horizontal_wall.draw_rect()
        horizontal_wall_1.draw_rect()
        horizontal_wall_2.draw_rect()
        horizontal_wall_3.draw_rect()
        horizontal_wall_4.draw_rect()
        horizontal_wall_5.draw_rect()
        horizontal_wall_6.draw_rect()

        player.update()
        player.reset()

        enemy.update()
        enemy.reset()

        enemy_1.update()
        enemy_1.reset()

        enemy_2.update()
        enemy_2.reset()

        finish.reset()
        
        if sprite.collide_rect(enemy, player) or sprite.collide_rect(enemy_1, player) or sprite.collide_rect(enemy_2, player) \
                or sprite.collide_rect(vertical_wall, player) or sprite.collide_rect(vertical_wall_1, player) \
                or sprite.collide_rect(vertical_wall_2, player) or sprite.collide_rect(vertical_wall_3, player) \
                or sprite.collide_rect(horizontal_wall, player) or sprite.collide_rect(horizontal_wall_1, player) \
                or sprite.collide_rect(horizontal_wall_2, player) or sprite.collide_rect(horizontal_wall_3, player) \
                or sprite.collide_rect(horizontal_wall_4, player) or sprite.collide_rect(horizontal_wall_5, player) \
                or sprite.collide_rect(horizontal_wall_6, player):
            end = True
            first_window.blit(game_over, (0, 0))
        elif sprite.collide_rect(finish, player):
            end = True
            first_window.blit(win, (0, 0))
    display.update()
