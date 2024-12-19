from dataclasses import dataclass, field

import pygame

from custom_types.int_vector2 import IntVector2
from constants import Constants


@dataclass
class Tile:
    index: IntVector2
    values: dict[str, int]
    cartesian_position: pygame.Vector2 = field(init=False)
    position: pygame.Vector2 = field(init=False)
    bounds: pygame.Rect = field(init=False)
    isometric_position: pygame.Vector2 = field(init=False)
    cartesian_bounds: pygame.Rect = field(init=False)
    two_high_render_offset_pos: pygame.Vector2 = field(init=False)


    def __post_init__(self):
        self.position = pygame.Vector2(
            (self.index.x - self.index.y) * Constants.TILE_RENDER_WIDTH / 2 + Constants.TILE_OFFSET_X,
            (self.index.x + self.index.y) * Constants.TILE_RENDER_HEIGHT / 2 + Constants.TILE_OFFSET_Y)

        self.two_high_render_offset_pos = pygame.Vector2(
            self.position.x,
            self.position.y - Constants.TILE_RENDER_HEIGHT
        )

        self.bounds = pygame.Rect(
            self.position.x,
            self.position.y,
            Constants.TILE_RENDER_WIDTH,
            Constants.TILE_RENDER_HEIGHT)

        self.tile_points = [
            (self.bounds.center[0], self.position.y), # top
            (self.position.x, self.bounds.center[1]), # left
            (self.bounds.center[0], self.position.y + Constants.TILE_RENDER_HEIGHT), # bottom
            (self.position.x + Constants.TILE_RENDER_WIDTH, self.bounds.center[1]) # right
        ]

        self.cartesian_position = pygame.Vector2(
            self.index.x * Constants.TILE_RENDER_HEIGHT,
            self.index.y * Constants.TILE_RENDER_WIDTH)

        self.cartesian_bounds = pygame.Rect(
            self.cartesian_position.x,
            self.cartesian_position.y,
            Constants.TILE_RENDER_WIDTH,
            Constants.TILE_RENDER_HEIGHT)


    def set_placed_layer_value(self, placeable_value: int):
        self.values[Constants.NAME_PLACED_LAYER] = placeable_value


    def can_place(self) -> bool:
        can_walk = self.can_walk()
        placed_obj_empty = self.values[Constants.NAME_PLACED_LAYER] == 0
        return can_walk and placed_obj_empty


    def can_walk(self) -> bool:
        collision_obj_empty = self.values[Constants.NAME_COLLISION_LAYER] == 0
        return collision_obj_empty


    def contains_point(self, px, py):
        """
        Check if the point (px, py) is inside the diamond-shaped isometric tile.
        """
        dx = abs(px - self.bounds.center[0])
        dy = abs(py - self.bounds.center[1])
        return (dx / (Constants.TILE_RENDER_WIDTH / 2)) + (dy / (Constants.TILE_RENDER_HEIGHT / 2)) <= 1

