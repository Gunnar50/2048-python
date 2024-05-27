import random

import pygame
from settings import *
from sprites import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.moved = False

        self.debug = {}
        self.debugging = False

    def debug_info(self):
        for i, row in enumerate(self.grid.cells):
            self.debug[i+1] = row
        for i, row in enumerate(self.previous_board):
            self.debug[i+5] = row

    def new(self):
        self.grid = Grid(4)
        self.score = 0
        self.game_over = False
        self.won = False

        self.previous_board = [[tile for tile in cell] for cell in self.grid.cells]

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.grid.update()
        if not self.grid.available_moves():
            print("game over")
            self.game_over = True
            self.playing = False
            self.end_screen()

        self.debug_info()

    def draw(self):
        self.screen.fill(BGCOLOUR)

        self.grid.draw(self.screen)
        get_info(self.debug)

        pygame.display.flip()

    def events(self):
        if self.moved and not self.grid.is_moving():
            self.grid.generate_tile()
            self.moved = False
        if self.debugging:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit(0)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.grid.prepare_tiles()
                            self.moved = self.grid.move_left(self.moved)

                        elif event.key == pygame.K_RIGHT:
                            self.grid.prepare_tiles()
                            self.moved = self.grid.move_right(self.moved)

                        elif event.key == pygame.K_UP:
                            self.grid.prepare_tiles()
                            self.moved = self.grid.move_up(self.moved)

                        elif event.key == pygame.K_DOWN:
                            self.grid.prepare_tiles()
                            self.moved = self.grid.move_down(self.moved)

                        if event.key == pygame.K_SPACE:
                            return
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
                if event.type == pygame.KEYDOWN:
                    self.previous_board = [[tile for tile in cell]for cell in self.grid.cells]
                    self.grid.prepare_tiles()
                    score = 0
                    if event.key == pygame.K_LEFT:
                        self.moved, score = self.grid.move_left(self.moved)

                    elif event.key == pygame.K_RIGHT:
                        self.moved = self.grid.move_right(self.moved)

                    elif event.key == pygame.K_UP:
                        self.moved = self.grid.move_up(self.moved)

                    elif event.key == pygame.K_DOWN:
                        self.moved = self.grid.move_down(self.moved)

                    if event.key == pygame.K_SPACE:
                        return

                    self.score += score
                    print(self.score)

    def end_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return


game = Game()
while True:
    game.new()
    game.run()
