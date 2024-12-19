from dataclasses import dataclass, field

import pygame

from constants import Constants


@dataclass
class BaseButton:
    rect: pygame.Rect
    image: pygame.Surface
    image_disabled: pygame.Surface
    name: str
    values: dict[str, str | int]
    is_disabled: bool = field(default=False)
    is_selected: bool = field(default=False)
    is_over: bool = field(default=False)
    hover_rect: pygame.Rect = field(init=False)


    def __post_init__(self):
        self.hover_rect = self.rect.copy()
        self.hover_rect.inflate_ip(16, 16)
        self.hover_image = pygame.transform.scale(
            self.image, (self.hover_rect.width, self.hover_rect.height))


    def get_cost(self) -> int:
        return int(self.values[Constants.BUTTON_VALUES_NAME_ENERGY])


    def set_selection(self, selected: bool):
        self.is_selected = selected


    def update(self, mouse_pos, mouse_clicked):
        if self.is_disabled:
            return

        self.is_over = self.rect.collidepoint(mouse_pos)
        if self.is_over and mouse_clicked:
            self.is_selected = True


    def draw(self, screen):
        if self.is_disabled:
            screen.blit(self.image_disabled, self.rect)
        else:
            img = (self.hover_image if self.is_over or self.is_selected else self.image)
            rect = (self.hover_rect if self.is_over or self.is_selected else self.rect)
            screen.blit(img, rect)
