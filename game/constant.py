import pygame

LEVEL = 1

WIDTH = 900
HEIGHT = 450

FPS = 60

GROUND = (180, 181, 254)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (66, 179, 245)
YELLOW = (141, 122, 23)

pygame.font.init()
STAT_FONT = pygame.font.Font(None, 32)
ALIVE_FONT = pygame.font.Font(None, 32)
WON_FONT = pygame.font.Font(None, 32)
TIME_FONT = pygame.font.Font(None, 32)
ATW_FONT = pygame.font.Font(None, 32)
DIST_FONT = pygame.font.Font(None, 18)