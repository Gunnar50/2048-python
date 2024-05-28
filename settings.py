# COLORS (r, g, b)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTBROWN = (87, 74, 62)
DARKBROWN = (77, 63, 49)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (57, 42, 26)
BGCOLOUR = LIGHTBROWN
TILE_COLOURS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    "super": (60, 58, 50)
}

# game settings
FPS = 60
title = "2048"
ROWS = 4
COLS = 4
TILESIZE = 150
GAPSIZE = 15
WIDTH = (TILESIZE*COLS) + (GAPSIZE*(COLS+1)) + 200
HEIGHT = (TILESIZE*ROWS) + (GAPSIZE*(ROWS+1))

MARGIN_X = int((WIDTH - (4 * (TILESIZE + GAPSIZE))) / 2)
MARGIN_Y = int((HEIGHT - (4 * (TILESIZE + GAPSIZE))) / 2)


import pygame
pygame.init()
font = pygame.font.Font(None, 25)

def get_info(info_list):
    display_surface = pygame.display.get_surface()
    for i, key in enumerate(info_list):
        text = font.render(str(key) + " : " + str(info_list[key]), True, (255, 255, 255), (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.x = 700
        text_rect.y = 20 * i
        display_surface.blit(text, text_rect)
