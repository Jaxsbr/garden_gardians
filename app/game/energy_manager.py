from dataclasses import dataclass, field

import pygame

from renderer import Renderer
from game.combat_text import CombatTextType
from game.combat_text_configs import get_combat_text
from constants import Constants
from events import GlobalEventDispatcher, Event


@dataclass
class EnergyManager:
    elapsed_regen_rate = 0
    energy_rect = pygame.Rect(
        Constants.BUTTON_OFFSET,
        Constants.BUTTON_OFFSET + Constants.HEALTH_HEIGHT,
        Constants.BUTTON_WIDTH,
        Constants.BUTTON_HEIGHT
    )
    energy = Constants.ENERGY_STARTING_VALUE


    def __post_init__(self):
        self.font = pygame.font.Font(pygame.font.get_default_font(), 36)
        GlobalEventDispatcher.register_listener(self, "EnergyManager")


    def on_event(self, event: Event) -> bool:
        if event.event_name == Constants.EVENT_ENEMY_DIED:
            enemy = event.args["enemy"]
            print(f"reward: +{enemy.reward} pos: {enemy.position.copy()}")
            GlobalEventDispatcher.dispatch(Event(
                Constants.EVENT_ADD_COMBAT_TEXT,
                { "combat_text": get_combat_text(CombatTextType.ENERGY_ADD, f"+{enemy.reward}", enemy.position.copy()) }))
            self.energy += enemy.reward
            return True
        return False


    def reduce_energy(self, energy_value):
        self.energy -= energy_value
        if self.energy < 0: # Avoid negatives
            self.energy = 0
            print("unexpected negative")


    def add_energy(self, energy_value, position: pygame.Vector2):
        self.energy += energy_value


    def update(self, dt):
        self.elapsed_regen_rate += 1 * dt
        if self.elapsed_regen_rate >= Constants.ENERGY_REGEN_RATE:
            self.elapsed_regen_rate = 0
            self.energy += Constants.ENERGY_REGEN_VALUE


    def draw_cost_text(self, screen, color, text, text_position):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=(text_position[0], text_position[1]))
        screen.blit(text_surface, text_rect)


    def draw_energy(self, screen, renderer: Renderer):
        pygame.draw.circle(
            screen,
            "yellow",
            (self.energy_rect.center[0], self.energy_rect.center[1]),
            Constants.BUTTON_HEIGHT / 3 + 5
        )

        pygame.draw.circle(
            screen,
            Constants.COLOR_TEXT_ONE,
            (self.energy_rect.center[0], self.energy_rect.center[1]),
            Constants.BUTTON_HEIGHT / 3
        )

        renderer.draw_text(
            screen,
            self.font,
            "black",
            f"x {self.energy}",
            (self.energy_rect.right + Constants.BUTTON_OFFSET + 1,
             self.energy_rect.y + Constants.BUTTON_OFFSET + 1))

        renderer.draw_text(
            screen,
            self.font,
            Constants.COLOR_TEXT_ONE,
            f"x {self.energy}",
            (self.energy_rect.right + Constants.BUTTON_OFFSET,
             self.energy_rect.y + Constants.BUTTON_OFFSET))
