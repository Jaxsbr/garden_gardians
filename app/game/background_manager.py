from dataclasses import dataclass, field
import random

import pygame

from asset_manager import get_asset_manager
from constants import Constants


@dataclass
class BackgroundManager:
    background_1_pos: pygame.Vector2 = field(init=False)
    background_2_pos: pygame.Vector2 = field(init=False)


    def __post_init__(self):
        self.asset_manager = get_asset_manager()
        self.background_1_pos = pygame.Vector2(0, 0)
        self.background_2_pos = pygame.Vector2(
            random.randint(0, Constants.SCREEN_WIDTH * 2), 0)


    def update(self, dt):
        # [--screen--]
        # [-------][--bk1--][-------]
        # 2--][-------][-------][--bk
        x1_speed = Constants.BACKGROUND_1_MOVE_SPEED * dt
        x2_speed = Constants.BACKGROUND_2_MOVE_SPEED * dt

        self.background_1_pos.x += x1_speed
        self.background_2_pos.x += x2_speed

        if self.background_1_pos.x >= Constants.SCREEN_WIDTH * 1:
            self.background_1_pos.x = -Constants.SCREEN_WIDTH

        if self.background_2_pos.x >= Constants.SCREEN_WIDTH * 2:
            self.background_2_pos.x = -Constants.SCREEN_WIDTH


    def draw(self, screen):
        screen.blit(
            self.asset_manager.backgrounds_sprites[Constants.SPRITE_BACKGROUND_1],
            (self.background_1_pos.x, self.background_1_pos.y))
        screen.blit(
            self.asset_manager.backgrounds_sprites[Constants.SPRITE_BACKGROUND_2],
            (self.background_2_pos.x, self.background_2_pos.y))
