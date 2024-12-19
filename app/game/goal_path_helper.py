from custom_types.int_vector2 import IntVector2
from game.astar import astar
from constants import Constants
from game.tile_manager import TileManager


def get_collision_grid(tile_manager: TileManager) -> list[list[int]]:
    grid = [[0 if tile_manager.tiles[row][col].can_place() else 1
            for row in range(Constants.ROW_COUNT)]
                for col in range(Constants.COLUMN_COUNT)]
    return grid


def get_goal_path(tile_manager: TileManager, start_tile_index: IntVector2, goal_tile_index: IntVector2, grid: list[list[int]] | None = None):
    collision_grid = (grid if grid else get_collision_grid(tile_manager))
    goal_path = astar(
        collision_grid,
        (start_tile_index.x, start_tile_index.y),
        (goal_tile_index.x, goal_tile_index.y))

    return goal_path
