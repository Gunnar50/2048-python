import pygame
from settings import *


class Text:

  def __init__(self, text: str, x: int, y: int, font_size: int) -> None:
    self.text = text
    self.x, self.y = x, y
    self.font_size = font_size
    self.create_text()

  def update_text(self, new_text: str):
    self.text = new_text
    self.create_text()

  def create_text(self):
    font = pygame.font.SysFont("Helvetica", self.font_size)
    self.render = font.render(self.text, True, WHITE)

  def draw(self, screen: pygame.Surface):
    screen.blit(self.render, (self.x, self.y))
