import pygame
from settings import * 
from typing import Tuple, List, Union


class Tile:
    def __init__(self, x: int, y: int, value: int, colour: Tuple[int, int, int]):
        self.row, self.col = y, x
        self.x, self.y = (self.col * (TILESIZE + GAPSIZE)) + GAPSIZE, (self.row * (TILESIZE + GAPSIZE)) + GAPSIZE
        self.future_x, self.future_y = self.x, self.y
        self.value = value
        self.colour = colour
        self.tile_surface = pygame.Surface((TILESIZE, TILESIZE))
        self.update_font()
        self.moving: bool = False
        self.scale: float = 0.0  # Initial scale
        self.is_new: bool = True
        self.frame = 0  # Start frame as 0, indicating animation hasn't started
        self.merged_from: Union[None, List[Tile]] = None

    def update_position(self, x: int, y: int) -> None:
        self.row, self.col = x, y

    def update(self) -> None:
        self.future_x, self.future_y = (self.col * (TILESIZE + GAPSIZE)) + GAPSIZE, (self.row * (TILESIZE + GAPSIZE)) + GAPSIZE
        if self.future_x != self.x or self.future_y != self.y:
            self.move_animation()
        elif self.future_x == self.x and self.future_y == self.y:
            self.moving = False

        self.update_font()

        # If the tile is new, animate it
        if self.is_new:
            self.scale_animation()

    def update_colour(self) -> None:
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

    def update_font(self) -> None:
        font = pygame.font.SysFont("Consolas", 72)
        font_width, font_height = font.size(str(self.value))
        self.render = font.render(str(self.value), True, WHITE)
        self.font_x = (TILESIZE / 2) - (font_width / 2)
        self.font_y = (TILESIZE / 2) - (font_height / 2)
        self.font_width, self.font_height = font.size(str(self.value))

    def draw(self, screen: pygame.Surface) -> None:
        # Draw the tile scaled according to self.scale
        scaled_surface = pygame.transform.scale(self.tile_surface, (int(TILESIZE * self.scale), int(TILESIZE * self.scale)))
        pygame.draw.rect(scaled_surface, self.colour, (0, 0, int(TILESIZE * self.scale), int(TILESIZE * self.scale)), border_radius=2)
        
        # Scale the font surface and blit it onto the scaled tile surface
        font_surface = pygame.transform.scale(self.render, (int(self.font_width * self.scale), int(self.font_height * self.scale)))
        scaled_surface.blit(font_surface, (self.font_x * self.scale, self.font_y * self.scale))

        screen.blit(scaled_surface, ((self.x + TILESIZE / 2 - (TILESIZE * self.scale) / 2), (self.y + TILESIZE / 2 - (TILESIZE * self.scale) / 2)))

    def scale_animation(self) -> None:
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
            self.is_new = False

        self.frame += 1

    def move_animation(self) -> None:
        speed = 50
        distance_x = self.future_x - self.x
        distance_y = self.future_y - self.y

        # We calculate the step to move. If the step is larger than the distance,
        # we just move to the target position
        step_x = speed if abs(distance_x) > speed else abs(distance_x)
        step_y = speed if abs(distance_y) > speed else abs(distance_y)

        # Update position
        if distance_x != 0:
            self.x += step_x if distance_x > 0 else -step_x
            self.moving = True
        if distance_y != 0:
            self.y += step_y if distance_y > 0 else -step_y
            self.moving = True

    def move(self, direction: str, 
             tiles: List[List[Union["Tile", None]]], moved: bool) -> Tuple[bool, int]:
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
                next_tile: Union[None, Tile] = tiles[self.row][pos]
                if next_tile and next_tile.value == self.value and not next_tile.merged_from:
                    merged_tile = Tile(pos, self.row, self.value*2, BROWN)
                    merged_tile.update_colour()
                    tiles[self.row][pos] = merged_tile
                    tiles[self.row][self.col] = None
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
                    tiles[self.row][self.col] = None
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

    def __repr__(self) -> str:
        return f"Tile({self.x}, {self.y}, {self.value})"
    
    def __str__(self) -> str:
        return str(self.value)


