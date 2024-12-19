from dataclasses import dataclass, field

import pygame

from state import State
from renderer import Renderer
from enums import GameState


@dataclass
class StateManager:
    current_state: GameState
    state_objects: dict[GameState, State] = field(init=False)

    def __post_init__(self):
        self.current_state_values = {}


    def change(self, new_state: GameState, values: dict[str, str | int | bool | pygame.Color] | None = None):
        self.current_state = new_state
        self.state_objects[self.current_state].selected(values)


    def update(self, dt):
        self.state_objects[self.current_state].update(dt)


    def draw(self, screen: pygame.Surface, renderer: Renderer):
        self.state_objects[self.current_state].draw(screen, renderer)


    # TODO: Call State.selected
