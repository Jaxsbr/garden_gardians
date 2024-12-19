from dataclasses import dataclass, field

import pygame

from utils.random_helper import get_variable_float
from renderer import Renderer, RendererType
from asset_manager import get_asset_manager
from constants import Constants
from game.tile import Tile
from events import Event, GlobalEventDispatcher


@dataclass
class TowerConfig:
    name: str
    image: pygame.Surface
    shoot_rate: float
    range: float


@dataclass
class Tower:
    tile: Tile
    config: TowerConfig
    elapsed_shoot_time: float = field(default=0)
    shoot_rate: float = field(init=False)


    def __post_init__(self):
        self.asset_manager = get_asset_manager()
        variable = Constants.TOWER_SUN_FLOWER_SHOOT_RATE / 10
        self.shoot_rate = get_variable_float(self.config.shoot_rate, variable)
        self.center = pygame.Vector2(
            self.tile.bounds.center[0], self.tile.bounds.center[1])


    def _get_damage(self) -> int:
        if self.config.name == Constants.SPRITE_SUN_FLOWER:
            return Constants.TOWER_SUN_FLOWER_DAMAGE
        elif self.config.name == Constants.SPRITE_FREEZE_FLOWER:
            return Constants.TOWER_FREEZE_FLOWER_DAMAGE
        else:
            raise Exception(f"no such tower type {self.config.name}")


    def _get_bullet_color(self) -> str:
        if self.config.name == Constants.SPRITE_SUN_FLOWER:
            return Constants.TOWER_SUN_FLOWER_BULLET_COLOR
        elif self.config.name == Constants.SPRITE_FREEZE_FLOWER:
            return Constants.TOWER_FREEZE_FLOWER_BULLET_COLOR
        else:
            raise Exception(f"no such tower type {self.config.name}")

    def _get_bullet_speed(self) -> float:
        if self.config.name == Constants.SPRITE_SUN_FLOWER:
            return Constants.TOWER_SUN_FLOWER_BULLET_SPEED
        elif self.config.name == Constants.SPRITE_FREEZE_FLOWER:
            return Constants.TOWER_SUN_FLOWER_BULLET_SPEED
        else:
            raise Exception(f"no such tower type {self.config.name}")


    # TODO: Don't use this tuple, find alternative
    def set_shoot_target(self, target_center: pygame.Vector2):
        self.has_target = True
        self.target_center_pos = target_center


    def cancel_target(self):
        self.has_target = False
        self.target_center_pos = pygame.Vector2(0, 0)


    def shoot(self):
        if self.has_target:
            GlobalEventDispatcher.dispatch(Event(
                Constants.EVENT_SHOOT_BULLET,
                {"position": self.center.copy(),
                 "target_pos": self.target_center_pos,
                 "bullet_config": {
                     "damage": self._get_damage(),
                     "effect": self.config.name,
                     "color": self._get_bullet_color(),
                     "speed": self._get_bullet_speed()
                 }}))
        else:
            # NOTE:
            # Shoot is called without a valid target,
            # thus we set the elapse time to max to ensure
            # the tower can shoot instantly when target is received.
            self.elapsed_shoot_time = self.shoot_rate


    def update(self, dt):
        self.elapsed_shoot_time += 1 * dt
        if self.elapsed_shoot_time >= self.shoot_rate:
            self.elapsed_shoot_time = 0
            self.shoot()


    def draw(self, renderer: Renderer):
        renderer.request_on_map_image_draw(
            RendererType.PLACED,
            self.config.image,
            self.tile.position,
            self.tile.index.x,
            self.tile.index.y)


