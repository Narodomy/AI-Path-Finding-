import math

from game.constant import *
from game.map import *


class Player:
    def __init__(self):
        self.x = 75
        self.y = 146
        self.x_speed = 4
        self.y_speed = 4

        self.width = 30
        self.height = 30

        self.target = self
        self.distance = 99999
        self.fitness = 0

        self.coin = False
        self.collided = False
        self.win = False

        self.surface = pygame.image.load('./game/resources/images/entities/player.png').convert_alpha()
        self.surface = pygame.transform.scale(self.surface, (self.width, self.height))
        self.rect = self.surface.get_rect(center=(self.x, self.y))

    def draw(self, win):
        self.rect = self.surface.get_rect(center=(self.x, self.y))
        win.blit(self.surface, self.rect)

    def move_up(self):
        self.y -= self.y_speed

    def move_down(self):
        self.y += self.y_speed

    def move_left(self):
        self.x -= self.x_speed

    def move_right(self):
        self.x += self.x_speed

    def collision_walls(self, map):
        for wall in map.walls:
            if self.rect.colliderect(wall.rect):

                if wall.index == 's':
                    self.y += self.y_speed

                if wall.index == 'i':
                    self.y -= self.y_speed

                if wall.index == 'e':
                    self.x += self.x_speed

                if wall.index == 'd':
                    self.x -= self.x_speed

    def collision_balls(self, balls):
        for ball in balls:
            if self.rect.colliderect(ball.rect):
                self.collided = True

    def collision_coins(self, coin):
        if self.rect.colliderect(coin.rect):
            self.coin = True
            self.fitness = 30

    def collision_win(self, area):
        if self.rect.colliderect(area.rect):
            self.win = True

    def target_information(self, win, area, coin, switch):
        # Define o target
        if not self.coin:
            self.target = coin
            color = GREEN
        else:
            self.target = area
            color = BLUE

        # pygame.draw.line(win, RED, (self.x, self.y), (self.target.x, self.target.y))
        pygame.draw.line(win, color, (self.x, self.y), (self.target.x, self.target.y), 2)

        self.distance = math.dist([self.x, self.y], [self.target.x, self.target.y])

        if switch:
            Xm = ((self.x + self.target.x) / 2) - 15
            Ym = ((self.y + self.target.y) / 2) - 15

            distance_text = DIST_FONT.render("d: " + "{:.2f}".format(self.distance), 1, (0, 0, 0, 191))
            win.blit(distance_text, (Xm, Ym))


class Ball:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.speed = 4
        self.type = type
        self.count = 0
        self.limit = [665, 235]
        self.level = 1
        self.surface = pygame.image.load('./game/resources/images/entities/ball.png').convert_alpha()
        self.rect = self.surface.get_rect(center=(self.x, self.y))

    def lv2(self):
        self.level = 2
        self.x = 212 + (44 * (self.type - 1) + 4.5 * (self.type - 2))
        self.speed = 3.5

    def draw(self, win):
        self.rect = self.surface.get_rect(center=(self.x, self.y))
        win.blit(self.surface, self.rect)

    def move(self):
        self.count += self.speed
        # level 1
        if self.level == 1:
            if self.type % 2 == 1:
                self.x += self.speed
                if self.x + self.speed >= self.limit[0] or self.x + self.speed <= self.limit[1] and self.count != 0:
                    self.count = 0
                    self.speed *= -1
            else:
                self.x -= self.speed
                if self.x - self.speed >= self.limit[0] or self.x - self.speed <= self.limit[1] and self.count != 0:
                    self.count = 0
                    self.speed *= -1

        # level 2
        elif self.level == 2:
            if self.type % 2 == 1:
                self.y += self.speed
                if self.y + self.speed >= self.limit[0] or self.y + self.speed <= self.limit[1] and self.count != 0:
                    self.count = 0
                    self.speed *= -1
            else:
                self.y -= self.speed
                if self.y - self.speed >= self.limit[0] or self.y - self.speed <= self.limit[1] and self.count != 0:
                    self.count = 0
                    self.speed *= -1


# Coin
class Coin:
    def __init__(self):
        self.x = 474
        self.y = 186

        self.width = 24
        self.height = 24

        self.surface = pygame.image.load('./game/resources/images/entities/coin.png').convert_alpha()
        self.rect = self.surface.get_rect(center=(self.x, self.y))

    def draw(self, win):
        win.blit(self.surface, self.rect)
