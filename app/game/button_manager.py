from dataclasses import dataclass

import pygame

from asset_manager import get_asset_manager
from constants import Constants
from custom_types.base_button import BaseButton
from renderer import Renderer


@dataclass
class ButtonManager():
    def __post_init__(self):
        self.asset_manager = get_asset_manager()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 36)
        self.buttons = [
            BaseButton( # Sun Flower Button
                rect = pygame.Rect(
                    Constants.SCREEN_WIDTH - Constants.BUTTON_WIDTH - Constants.BUTTON_OFFSET,
                    Constants.BUTTON_OFFSET,
                    Constants.BUTTON_WIDTH,
                    Constants.BUTTON_HEIGHT),
                image = self.asset_manager.button_sprites[Constants.SPRITE_BUTTON_SUN_FLOWER],
                image_disabled = self.asset_manager.button_sprites[Constants.SPRITE_BUTTON_SUN_FLOWER_NO_MONEY],
                name = Constants.SPRITE_SUN_FLOWER,
                values={
                    Constants.BUTTON_VALUES_NAME_ENERGY: Constants.BUTTON_SUN_FLOWER_ENERGY
                }
            ),
            BaseButton( # Freeze Flower Button
                rect = pygame.Rect(
                    Constants.SCREEN_WIDTH - (Constants.BUTTON_WIDTH + Constants.BUTTON_OFFSET) * 2,
                    Constants.BUTTON_OFFSET,
                    Constants.BUTTON_WIDTH,
                    Constants.BUTTON_HEIGHT),
                image = self.asset_manager.button_sprites[Constants.SPRITE_BUTTON_FREEZE_FLOWER],
                image_disabled = self.asset_manager.button_sprites[Constants.SPRITE_BUTTON_FREEZE_FLOWER_NO_MONEY],
                name = Constants.SPRITE_FREEZE_FLOWER,
                values={
                    Constants.BUTTON_VALUES_NAME_ENERGY: Constants.BUTTON_FREEZE_FLOWER_ENERGY
                }
            )
        ]


    def _update_button_enablement(self, mouse_x, mouse_y, energy_available: int):
        mouse_clicked = pygame.mouse.get_pressed()[0]
        for button in self.buttons:
            button.is_disabled = False
            if int(button.values[Constants.BUTTON_VALUES_NAME_ENERGY]) > energy_available:
                button.is_disabled = True
            button.update((mouse_x, mouse_y), mouse_clicked)


    def get_selected_button(self) -> BaseButton | None:
        for button in self.buttons:
            if button.is_selected:
                return button
        return None


    def update(self, dt, energy_available: int):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self._update_button_enablement(mouse_x, mouse_y, energy_available)


    def draw(self, screen: pygame.Surface, renderer: Renderer):
        for button in self.buttons:
            button.draw(screen)
            text_position = (
                button.rect.x + Constants.BUTTON_OFFSET,
                button.rect.bottom + Constants.BUTTON_OFFSET / 2)
            text = str(button.values[Constants.BUTTON_VALUES_NAME_ENERGY])
            color = ("red" if button.is_disabled else Constants.COLOR_TEXT_ONE)
            # text_surface = self.font.render(text, True, color)
            # text_rect = text_surface.get_rect(topleft=(text_position[0], text_position[1]))
            # screen.blit(text_surface, text_rect)

            renderer.draw_text(
                screen,
                self.font,
                "black",
                text,
                (text_position[0] + 1, text_position[1] + 1))

            renderer.draw_text(
                screen,
                self.font,
                color,
                text,
                (text_position[0], text_position[1]))
