import pygame

from game.map_generator import MapConfig
from game.map import Map
from renderer import Renderer, RendererType
from asset_manager import get_asset_manager
from custom_types.int_vector2 import IntVector2
from constants import Constants
from game.tile import Tile

class TileManager:
    def __init__(self, map_config: MapConfig):
        self.asset_manager = get_asset_manager()
        self.floor_layer = map_config.floor_layer
        self.collision_layer = map_config.collision_layer
        self.tile_sprites = self.asset_manager.tile_sprites
        self.tiles = [[self.create_tile(col, row)
            for col in range(Constants.COLUMN_COUNT)]
                for row in range(Constants.ROW_COUNT)]


    def create_tile(self, col, row) -> Tile:
        index = IntVector2(col, row)
        values: dict[str, int] = {}
        values[Constants.NAME_FLOOR_LAYER] = self.floor_layer[row][col]
        values[Constants.NAME_COLLISION_LAYER] = self.collision_layer[row][col]
        values[Constants.NAME_PLACED_LAYER] = Map.PLACED_LAYER[row][col]
        return Tile(index, values)


    def draw_floor_layer(self, renderer: Renderer):
        for row in range(Constants.ROW_COUNT):
            for col in range(Constants.COLUMN_COUNT):
                tile = self.tiles[row][col]
                image = Constants.LAYER_FLOOR_SPRITES[tile.values[Constants.NAME_FLOOR_LAYER]]
                if image:
                    renderer.request_on_map_image_draw(
                        RendererType.FLOOR_TILE,
                        self.tile_sprites[image],
                        tile.position,
                        col,
                        row)


    def draw_selector(self, renderer: Renderer, row: int, col: int):
        tile = self.tiles[row][col]
        renderer.request_polygon_draw(
            RendererType.SELECTOR,
            Constants.COLOR_SELECTOR,
            tile.tile_points,
            Constants.SELECTOR_WIDTH,
            col,
            row)



    def draw_collision_layer(self, renderer: Renderer):
        for row in range(Constants.ROW_COUNT):
            for col in range(Constants.COLUMN_COUNT):
                tile = self.tiles[row][col]
                image = Constants.LAYER_COLLISION_SPRITES[tile.values[Constants.NAME_COLLISION_LAYER]]
                if image:
                    renderer.request_on_map_image_draw(
                        RendererType.COLLISION_TILE,
                        self.tile_sprites[image],
                        tile.two_high_render_offset_pos,
                        col,
                        row)


    def draw_fence(self, renderer: Renderer):
        # LEFT
        for row in range(Constants.ROW_COUNT):
            tile = self.tiles[row][0]
            renderer.request_off_map_image_draw(
                RendererType.FENCE_LEFT,
                self.asset_manager.tile_sprites[Constants.SPRITE_FENCE_LEFT],
                pygame.Vector2(
                    tile.position.x - Constants.TILE_RENDER_WIDTH + Constants.TILE_RENDER_WIDTH / 2, # 1 and a half width
                    tile.position.y - Constants.TILE_RENDER_HEIGHT * 2 + Constants.TILE_RENDER_HEIGHT / 2)) # 2 and a half height

        # TOP
        for col in range(Constants.COLUMN_COUNT):
            tile = self.tiles[0][col]
            renderer.request_off_map_image_draw(
                RendererType.FENCE_TOP,
                self.asset_manager.tile_sprites[Constants.SPRITE_FENCE_TOP],
                pygame.Vector2(
                    tile.position.x + Constants.TILE_RENDER_WIDTH / 2, # half width
                    tile.position.y - Constants.TILE_RENDER_HEIGHT * 2 + Constants.TILE_RENDER_HEIGHT / 2)) # 2 and a half height
