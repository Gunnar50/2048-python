import pygame
import random
from settings import *
from tile import Tile
from typing import Optional, Union

CellsType = list[list[Union[None, Tile]]]


class Grid:

  def __init__(self, size: int):
    self.size = size
    self.cells: CellsType = [[None] * COLS for _ in range(ROWS)]

    self.initialise_grid()
    # self.test_tiles()

  def test_tiles(self):
    values = [
        [4, 4, 64, 16],
        [32, 64, 2, 4],
        [128, 4, 16, 8],
        [2, 256, 8, 64],
    ]
    # values: list[list[Union[None, int]]] = [
    #     [0, 2, 0, 0],
    #     [0, 0, 0, 0],
    #     [0, 0, 0, 0],
    #     [0, 2, 0, 0],
    # ]
    self.cells = []
    for y in range(len(values)):
      row: list[Optional[Tile]] = []
      for x in range(len(values[y])):
        value = values[x][y]
        if not value:
          row.append(None)
        else:
          tile = Tile(x, y, value, BROWN)
          tile.update_colour()
          row.append(tile)
      self.cells.append(row)

  def initialise_grid(self) -> None:
    for _ in range(2):
      self.generate_tile()

  def generate_tile(self) -> None:
    """Generate a tile in the cells list"""
    while True:
      row = random.randint(0, ROWS - 1)
      col = random.randint(0, COLS - 1)
      if self.cells[row][col] is None:
        tile_value = 2 if random.random() < 0.9 else 4
        tile = Tile(col, row, tile_value, TILE_COLOURS[tile_value])
        self.insert_tile(tile)
        break

  def insert_tile(self, tile: Tile) -> None:
    self.cells[tile.row][tile.col] = tile

  def update(self) -> None:
    for row in self.cells:
      for tile in row:
        if tile:
          if tile.merged_from:
            for merged_tile in tile.merged_from:
              merged_tile.update()
            if not self.is_moving():
              tile.update()
          else:
            tile.update()

  def draw_tiles(self, screen: pygame.Surface) -> None:
    for row in self.cells:
      for tile in row:
        if tile:
          if tile.merged_from:
            for merged_tile in tile.merged_from:
              merged_tile.draw(screen)
          tile.draw(screen)

  def draw(self, screen: pygame.Surface) -> None:
    for row in range(4):
      for col in range(4):
        pygame.draw.rect(
            screen,
            DARKBROWN,
            ((row * (TILESIZE + GAPSIZE)) + GAPSIZE,
             (col * (TILESIZE + GAPSIZE)) + GAPSIZE, TILESIZE, TILESIZE),
            border_radius=2,
        )

    self.draw_tiles(screen)

  def is_moving(self) -> bool:
    """
    Check if ANY tile in the grid is moving.
    This decides if the next move can be made or not.
    """
    for row in self.cells:
      for tile in row:
        if tile:
          if tile.moving:
            return True
          for merged_tile in tile.merged_from:
            if merged_tile.moving:
              return True
    return False

  def is_new(self) -> bool:
    for row in self.cells:
      for tile in row:
        if tile and tile.is_new:
          return True
    return False

  def move_left(self, moved: bool) -> tuple[bool, int]:
    score = 0
    for row in self.cells:
      for tile in row:
        if tile is not None:
          moved, points = tile.move(Directions.LEFT, self.cells, moved)
          score += points
    return moved, score

  def move_right(self, moved: bool) -> tuple[bool, int]:
    score = 0
    for row in self.cells:
      for i in range(len(row) - 1, -1, -1):
        tile = row[i]
        if tile is not None:
          moved, points = tile.move(Directions.RIGHT, self.cells, moved)
          score += points
    return moved, score

  def move_up(self, moved: bool) -> tuple[bool, int]:
    score = 0
    for row in self.cells:
      for tile in row:
        if tile is not None:
          moved, points = tile.move(Directions.UP, self.cells, moved)
          score += points
    return moved, score

  def move_down(self, moved: bool) -> tuple[bool, int]:
    score = 0
    for i in range(len(self.cells) - 1, -1, -1):
      for j in range(len(self.cells[i])):
        tile = self.cells[i][j]
        if tile is not None:
          moved, points = tile.move(Directions.DOWN, self.cells, moved)
          score += points
    return moved, score

  # save all tile positions and remove merger info
  def prepare_tiles(self) -> None:
    for row in self.cells:
      for tile in row:
        if tile is not None:
          tile.merged_from = []

  def available_moves(self) -> bool:
    return self.cells_available() or self.can_merge()

  def can_merge(self) -> bool:
    """Check if any cells can be merged"""
    # loop through all cells and check adjacent cells for merging
    for x in range(len(self.cells)):
      for y in range(len(self.cells[x])):
        tile = self.cells[x][y]
        if tile is not None:
          for offset_x, offset_y in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            adjacent_x = x + offset_x
            adjacent_y = y + offset_y
            if self.within_bounds(adjacent_x, adjacent_y):
              adjacent_tile = self.cells[adjacent_x][adjacent_y]
              if adjacent_tile is not None and adjacent_tile.value == tile.value:
                return True
    return False

  def cells_available(self) -> bool:
    return any(any(cell is None for cell in row) for row in self.cells)

  def within_bounds(self, x: int, y: int) -> bool:
    return 0 <= x < self.size and 0 <= y < self.size

  def print_board(self) -> None:
    for row in self.cells:
      print(row)
