from dataclasses import dataclass, field
from enum import Enum
import math
import random
import copy

from game.map import Map
from custom_types.int_vector2 import IntVector2
from constants import Constants


class MapQuadrantName(Enum):
    TOP_LEFT = (0, 0)
    TOP_RIGHT = (1, 0)
    BOTTOM_LEFT = (1, 0)
    BOTTOM_RIGHT = (1, 1)


@dataclass
class MapQuadrant:
    name: MapQuadrantName
    start_index: IntVector2
    col_count: int
    row_count: int
    main_index: IntVector2 = field(init=False)

    def __post_init__(self):
        if self.row_count != self.col_count:
            raise ValueError("row_count and col_count need to match")

        self.main_index = self.get_random_tile_index()


    def get_random_tile_index(self) -> IntVector2:
        return IntVector2(
            random.randint(self.start_index.x, self.start_index.x + self.col_count),
            random.randint(self.start_index.y, self.start_index.y + self.row_count))


@dataclass
class MapConfig:
    start_quadrant: MapQuadrant
    end_quadrant: MapQuadrant
    remaining_quadrant_1: MapQuadrant
    remaining_quadrant_2: MapQuadrant
    floor_layer: list[list[int]]
    collision_layer: list[list[int]]


@dataclass
class MapGenerator:
    map_config: MapConfig = field(init=False)

    def __post_init__(self):
        self.map_config = self._get_random_map_config()


    def _get_quadrants(self) -> list[MapQuadrant]:
        quadrants = []

        if Constants.ROW_COUNT != Constants.COLUMN_COUNT:
            raise ValueError("ROW_COUNT and COLUMN_COUNT need to match")

        col_count = int(Constants.COLUMN_COUNT / 2)
        row_count = int(Constants.ROW_COUNT / 2)

        quadrants.append(MapQuadrant(
            MapQuadrantName.TOP_LEFT,
            IntVector2(0, 0),
            col_count,
            row_count))

        quadrants.append(MapQuadrant(
            MapQuadrantName.TOP_RIGHT,
            IntVector2(col_count - 1, 0),
            col_count,
            row_count))

        quadrants.append(MapQuadrant(
            MapQuadrantName.BOTTOM_LEFT,
            IntVector2(0, row_count - 1),
            col_count,
            row_count))

        quadrants.append(MapQuadrant(
            MapQuadrantName.BOTTOM_RIGHT,
            IntVector2(col_count - 1, row_count - 1),
            col_count,
            row_count))

        return quadrants


    def _apply_random_collisions(self, collision_layer: list[list[int]], quadrant: MapQuadrant, tile_percentage: int = 10):
        # Calculate 10% of tiles
        layer = collision_layer.copy()
        tiles_in_quadrant = quadrant.col_count * quadrant.row_count
        collision_tile_count = math.ceil(tiles_in_quadrant / 100 * tile_percentage)

        # Get random tile_index
        tile_indexes = []
        found_count = 0
        while found_count < collision_tile_count:
            tile_index = quadrant.get_random_tile_index()
            if tile_index.x == quadrant.main_index.x and tile_index.y == quadrant.main_index.y:
                print("main tile skipped")
                continue
            if tile_index not in tile_indexes:
                tile_indexes.append(tile_index)
                found_count += 1
                continue
            print("something else")

        # Apply random collision directly
        for tile_index in tile_indexes:
            collision_value = random.choice([1, 2]) # 1 tall tree, 2 short tree
            layer[tile_index.y][tile_index.x] = collision_value

        return layer


    def _get_random_map_config(self):
        # Define indices and quadrants
        q_indexes = range(0, 4)  # 0, 1, 2, 3
        quadrants = self._get_quadrants()

        # Map of diagonally opposed indices
        diagonal_pairs = {0: 3, 1: 2, 2: 1, 3: 0}

        # Randomly select a start index
        start_index = random.choice(list(diagonal_pairs.keys()))

        # Get the corresponding end index (diagonal pair)
        end_index = diagonal_pairs[start_index]

        # Retrieve corresponding quadrants
        start_quadrant = quadrants[start_index]
        end_quadrant = quadrants[end_index]

        # Find remaining indices (diagonal pair of the other set)
        remaining_start_index = [i for i in q_indexes if i not in [start_index, end_index]][0]
        remaining_end_index = diagonal_pairs[remaining_start_index]

        # Retrieve remaining quadrants
        remaining_1 = quadrants[remaining_start_index]
        remaining_2 = quadrants[remaining_end_index]

        floor_layer = self._get_floor_layer(start_quadrant, end_quadrant)
        collision_layer = self._get_collision_layer(start_quadrant, end_quadrant, remaining_1, remaining_2)

        return MapConfig(
            start_quadrant,
            end_quadrant,
            remaining_1,
            remaining_2,
            floor_layer,
            collision_layer)


    def _get_floor_layer(self, start_quadrant: MapQuadrant, end_quadrant: MapQuadrant) -> list[list[int]]:
        floor_layer = copy.deepcopy(Map.FLOOR_LAYER)
        floor_layer[start_quadrant.main_index.y][start_quadrant.main_index.x] = 2 # start tile
        floor_layer[end_quadrant.main_index.y][end_quadrant.main_index.x] = 3 # start tile
        return floor_layer


    def _get_collision_layer(self, start_quadrant: MapQuadrant, end_quadrant: MapQuadrant, remaining_quadrant_1: MapQuadrant, remaining_quadrant_2: MapQuadrant) -> list[list[int]]:
        collision_layer = copy.deepcopy(Map.COLLISION_LAYER)
        collision_layer = self._apply_random_collisions(collision_layer, start_quadrant, 5)
        collision_layer = self._apply_random_collisions(collision_layer, end_quadrant, 5)
        collision_layer = self._apply_random_collisions(collision_layer, remaining_quadrant_1, random.randint(5, 15))
        collision_layer = self._apply_random_collisions(collision_layer, remaining_quadrant_2, random.randint(5, 15))

        # TODO: There is a possibility of blocking the goal path
        #       We can calculate if one still exists, and if not recalculate the collisions
        return collision_layer
