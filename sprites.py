import copy
import pygame
import random
from settings import *


class Tile:
    def __init__(self, x, y, value, colour):
        self.row, self.col = y, x
        self.x, self.y = (self.col * (TILESIZE + GAPSIZE)) + GAPSIZE, (self.row * (TILESIZE + GAPSIZE)) + GAPSIZE
        self.future_x, self.future_y = self.x, self.y
        self.value = value
        self.colour = colour
        self.tile_surface = pygame.Surface((TILESIZE, TILESIZE))
        self.update_font()
        self.moving = False
        self.scale = 0.0  # Initial scale
        self.is_new = True
        self.frame = 0  # Start frame as -1, indicating animation hasn't started
        self.merged_from = None

    def update_position(self, x, y):
        self.row, self.col = x, y

    def update(self):
        self.future_x, self.future_y = (self.col * (TILESIZE + GAPSIZE)) + GAPSIZE, (self.row * (TILESIZE + GAPSIZE)) + GAPSIZE
        if self.future_x != self.x or self.future_y != self.y:
            self.move_animation()
        elif self.future_x == self.x and self.future_y == self.y:
            self.moving = False

        self.update_font()

        # If the tile is new, animate it
        if self.is_new:
            self.scale_animation()

    def update_colour(self):
        r, g, b = self.colour
        r += self.value
        r = min(r, 255)
        if r == 255:
            g += self.value
            g = min(g, 255)
            if g == 255:
                b += self.value
                b = min(b, 255)
                if b == 255:
                    r, g, b = BROWN
        self.colour = r, g, b

    def update_font(self):
        font = pygame.font.SysFont("Consolas", 72)
        font_width, font_height = font.size(str(self.value))
        self.render = font.render(str(self.value), True, WHITE)
        self.font_x = (TILESIZE / 2) - (font_width / 2)
        self.font_y = (TILESIZE / 2) - (font_height / 2)
        self.font_width, self.font_height = font.size(str(self.value))

    def draw(self, screen):
        # Draw the tile scaled according to self.scale
        scaled_surface = pygame.transform.scale(self.tile_surface, (int(TILESIZE * self.scale), int(TILESIZE * self.scale)))
        pygame.draw.rect(scaled_surface, self.colour, (0, 0, int(TILESIZE * self.scale), int(TILESIZE * self.scale)), border_radius=2)
        # Scale the font surface and blit it onto the scaled tile surface
        font_surface = pygame.transform.scale(self.render, (int(self.font_width * self.scale), int(self.font_height * self.scale)))
        scaled_surface.blit(font_surface, (self.font_x * self.scale, self.font_y * self.scale))

        screen.blit(scaled_surface, ((self.x + TILESIZE / 2 - (TILESIZE * self.scale) / 2), (self.y + TILESIZE / 2 - (TILESIZE * self.scale) / 2)))

    def scale_animation(self):
        # Define the number of frames for each phase of the animation
        grow_frames = 3
        shrink_frames = 5

        # Grow phase
        if self.frame < grow_frames:
            self.scale = 0.8 * (self.frame + 1) / grow_frames  # Grows from 0 to 1.3

        # Shrink phase
        elif self.frame < grow_frames + shrink_frames and self.merged_from:
            self.scale = max(1.0, 1.2 - 0.3 * (self.frame - grow_frames + 1) / shrink_frames)  # Shrinks from 1.3 to 1.0
        # Animation finished
        else:
            self.scale = 1
            self.is_new = False  # Stop the animation by setting frame to -1

        self.frame += 1

    def move_animation(self):
        speed = 50
        distance_x = self.future_x - self.x
        distance_y = self.future_y - self.y

        # We calculate the step to move. If the step is larger than the distance, we just move to the target position
        step_x = speed if abs(distance_x) > speed else abs(distance_x)
        step_y = speed if abs(distance_y) > speed else abs(distance_y)

        # Update position
        if distance_x != 0:
            self.x += step_x if distance_x > 0 else -step_x
            self.moving = True
        if distance_y != 0:
            self.y += step_y if distance_y > 0 else -step_y
            self.moving = True

    def move(self, direction, tiles, moved):
        moved = moved
        score = 0
        if direction == "left":
            range_func = range(self.col - 1, -1, -1)
        elif direction == "right":
            range_func = range(self.col + 1, len(tiles))
        elif direction == "up":
            range_func = range(self.row - 1, -1, -1)
        else:
            range_func = range(self.row + 1, len(tiles))

        for pos in range_func:
            if direction == "left" or direction == "right":
                next_tile = tiles[self.row][pos]
                if next_tile and next_tile.value == self.value and not next_tile.merged_from:
                    merged_tile = Tile(pos, self.row, self.value*2, BROWN)
                    merged_tile.update_colour()
                    tiles[self.row][pos] = merged_tile
                    tiles[self.row][self.col] = 0
                    self.col = pos
                    merged_tile.merged_from = [self, next_tile]
                    score += merged_tile.value
                    moved = True
                elif not next_tile:
                    tiles[self.row][pos], tiles[self.row][self.col] = tiles[self.row][self.col], tiles[self.row][pos]
                    self.col = pos
                    moved = True
                else:
                    break

            elif direction == "up" or direction == "down":
                next_tile = tiles[pos][self.col]
                if next_tile and next_tile.value == self.value and not next_tile.merged_from:
                    merged_tile = Tile(self.col, pos, self.value * 2, BROWN)
                    merged_tile.update_colour()
                    tiles[pos][self.col] = merged_tile
                    tiles[self.row][self.col] = 0
                    self.row = pos
                    merged_tile.merged_from = [self, next_tile]
                    score += merged_tile.value
                    moved = True

                elif not next_tile:
                    tiles[pos][self.col], tiles[self.row][self.col] = tiles[self.row][self.col], tiles[pos][self.col]
                    self.row = pos
                    moved = True
                else:
                    break

        return moved, score

    def __repr__(self):
        return str(self.value)


class Grid:
    def __init__(self, size):
        self.size = size
        self.cells = [[0] * COLS for _ in range(ROWS)]
        # self.cells[3] = [Tile(0, 3, 4, BROWN), Tile(1, 3, 4, BROWN), Tile(2, 3, 4, BROWN), 0]
        # self.cells[0] = [Tile(0, 0, 2, BROWN), 0, 0, Tile(3, 0, 4, BROWN)]
        # self.cells[1] = [0, Tile(1, 1, 4, BROWN), Tile(2, 1, 2, BROWN), Tile(3, 1, 32, BROWN)]
        # self.cells[2] = [0, Tile(1, 2, 64, BROWN), Tile(2, 2, 8, BROWN), Tile(3, 2, 2, BROWN)]
        # self.cells[3] = [Tile(0, 3, 8, BROWN), Tile(1, 3, 4, BROWN), Tile(2, 3, 32, BROWN), Tile(3, 3, 8, BROWN)]
        for _ in range(2):
            self.generate_tile()

    def generate_tile(self):
        while True:
            row = random.randint(0, ROWS - 1)
            col = random.randint(0, COLS - 1)
            if self.cells[row][col] == 0:
                tile = Tile(col, row, 2 if random.random() < 0.9 else 4, BROWN)
                self.insert_tile(tile)
                break

    def insert_tile(self, tile):
        self.cells[tile.row][tile.col] = tile

    def remove_tile(self, tile):
        self.cells[tile.row][tile.col] = 0

    def update(self):
        for row in self.cells:
            for col in range(len(row)):
                tile = row[col]
                if tile:
                    if tile.merged_from:
                        if not self.is_moving():
                            tile.update()
                        for merged_tile in tile.merged_from:
                            merged_tile.update()
                    else:
                        tile.update()

    def draw_tiles(self, screen):
        for row in self.cells:
            for tile in row:
                if tile:
                    if tile.merged_from:
                        for merged_tile in tile.merged_from:
                            merged_tile.draw(screen)
                    tile.draw(screen)

    def draw(self, screen):
        for row in range(4):
            for col in range(4):
                pygame.draw.rect(screen, DARKBROWN, ((row * (TILESIZE + GAPSIZE)) + GAPSIZE,
                                                     (col * (TILESIZE + GAPSIZE)) + GAPSIZE,
                                                     TILESIZE, TILESIZE), border_radius=2)

        self.draw_tiles(screen)

    def is_moving(self):
        for row in self.cells:
            for tile in row:
                if tile and tile.moving:
                    return True
        return False

    def move_left(self, moved):
        for row in self.cells:
            for tile in row:
                if tile != 0:
                    moved, score = tile.move("left", self.cells, moved)
        return moved, score

    def move_right(self, moved):
        for row in self.cells:
            for i in range(len(row) - 1, -1, -1):
                tile = row[i]
                if tile != 0:
                    moved = tile.move("right", self.cells, moved)
        return moved

    def move_up(self, moved):
        for row in self.cells:
            for tile in row:
                if tile != 0:
                    moved = tile.move("up", self.cells, moved)
        return moved

    def move_down(self, moved):
        for i in range(len(self.cells) - 1, -1, -1):
            for j in range(len(self.cells[i])):
                tile = self.cells[i][j]
                if tile != 0:
                    moved = tile.move("down", self.cells, moved)
        return moved

    # save all tile positions and remove merger info
    def prepare_tiles(self):
        for row in self.cells:
            for tile in row:
                if tile:
                    tile.merged_from = None

    def available_moves(self):
        return self.cells_available() or self.can_merge()

    def can_merge(self):
        # loop through all cells and check adjacent cells for merging
        for x in range(len(self.cells)):
            for y in range(len(self.cells[x])):
                tile = self.cells[x][y]
                if tile:
                    for offset_x in (-1, 0, 1):
                        for offset_y in (-1, 0, 1):
                            adjacent_x = x + offset_x
                            adjacent_y = y + offset_y
                            adjacent_tile = self.cells[adjacent_x][adjacent_y]
                            if adjacent_tile:
                                if self.within_bounds(adjacent_x, adjacent_y) and adjacent_tile.value == tile.value:
                                    return True
        return False

    def cells_available(self):
        return any(any(cell for cell in row) for row in self.cells)

    def within_bounds(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size





    def print_board(self):
        for row in self.cells:
            print(row)
