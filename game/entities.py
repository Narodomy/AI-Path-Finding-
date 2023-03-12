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

    def collision_win(self, area):
        if self.rect.colliderect(area.rect):
            self.win = True

    def target_information(self, win, area, switch):
        self.target = area

        pygame.draw.line(win, RED, (self.x, self.y), (self.target.x, self.target.y))

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

        self.surface = pygame.image.load('./game/resources/images/entities/ball.png').convert_alpha()
        self.rect = self.surface.get_rect(center=(self.x, self.y))

    def draw(self, win):
        self.rect = self.surface.get_rect(center=(self.x, self.y))
        win.blit(self.surface, self.rect)

    def move(self):
        self.count += self.speed

        if self.type % 2 == 1:
            self.x += self.speed
            if self.x + self.speed >= 665 or self.x + self.speed <= 235 and self.count != 0:
                self.count = 0
                self.speed *= -1
        else:
            self.x -= self.speed
            if self.x - self.speed >= 665 or self.x - self.speed <= 235 and self.count != 0:
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
