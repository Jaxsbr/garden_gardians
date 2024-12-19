import pygame

from renderer import Renderer

class State:
    def selected(self, state_values: dict[str, str | int | bool | pygame.Color] | None):
        pass
    def update(self, dt: int):
        pass
    def draw(self, screen: pygame.Surface, renderer: Renderer):
        pass
