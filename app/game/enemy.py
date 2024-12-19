from dataclasses import dataclass, field
import random
import pygame

from particle_collection import get_death_particle, get_freeze_particle
from enemy_config import ENEMY_CONFIG
from game.combat_text import CombatTextType
from game.combat_text_configs import get_combat_text
from events import Event, GlobalEventDispatcher
from game.map_generator import MapConfig
from game.goal_path_helper import get_goal_path
from game.tile import Tile
from renderer import Renderer, RendererType
from custom_types.int_vector2 import IntVector2
from asset_manager import get_asset_manager
from constants import Constants
from game.tile_manager import TileManager


@dataclass
class Enemy:
    tile_manager: TileManager
    map_config: MapConfig
    start_tile_index: IntVector2
    goal_tile_index: IntVector2
    _hp: int
    move_speed: float
    id: str
    wave_number: int
    reward: int
    direction_sprite: str = field(default="")
    max_hp: int = field(init=False)
    direction: pygame.Vector2 = field(init=False)
    goal_path: list[list[int]] = field(init=False)
    bounds: pygame.Rect = field(init=False)
    target_reached: bool = field(init=False)
    processed: bool = field(init=False)
    _target_pos: pygame.Vector2 = field(init = False)
    _remaining_health_bar_width: float = field(init=False)
    _is_freeze: bool = field(default=False)
    _freeze_elapsed: float = 0


    def __post_init__(self):
        self.reset(self.map_config, self.start_tile_index, self.goal_tile_index, self._hp, self.move_speed, self.wave_number)
        self.asset_manager = get_asset_manager()


    def alive(self):
        return self._hp > 0 and not self.target_reached


    def is_dead(self):
        return self._hp <= 0


    def calculate_goal_path(self):
        current_tile = self.get_tile()
        if current_tile:
            self.goal_path = get_goal_path(self.tile_manager, current_tile.index, self.goal_tile_index)


    def apply_damage(self, damage: int, effect: str = ""):
        self._hp -= damage

        is_freeze_bunny = any(e["wave"] == self.wave_number and e["name"] == "ice bunny" for e in ENEMY_CONFIG)
        if effect == Constants.SPRITE_FREEZE_FLOWER and not self._is_freeze and not is_freeze_bunny:
            if random.randint(0, 100) > Constants.TOWER_FREEZE_CHANCE:
                self._is_freeze = True
                GlobalEventDispatcher.dispatch(Event(
                    Constants.EVENT_ADD_COMBAT_TEXT,
                        { "combat_text": get_combat_text(CombatTextType.FREEZE, "~freeze~", self.sprite_center.copy())}))

        GlobalEventDispatcher.dispatch(Event(
            Constants.EVENT_ADD_COMBAT_TEXT,
                { "combat_text": get_combat_text(CombatTextType.DAMAGE, f"-{damage}", self.sprite_center.copy())}))
        self.update_death()


    def reset(self, map_config: MapConfig, start_tile_index: IntVector2, goal_tile_index: IntVector2, hp: int, move_speed: float, wave_number: int):
        self.map_config = map_config
        self.start_tile_index = start_tile_index
        self.goal_tile_index = goal_tile_index
        self._hp = hp
        self.max_hp = hp
        self.move_speed = move_speed
        self.wave_number = wave_number
        self.target_reached = False
        self.processed = False

        start_tile_index = self.map_config.start_quadrant.main_index
        target_position = self.tile_manager.tiles[start_tile_index.y][start_tile_index.x].position.copy()

        self.position = target_position.copy()
        self.bounds = pygame.Rect(
            self.position.x,
            self.position.y,
            Constants.SPRITE_ENEMY_RENDER_WIDTH,
            Constants.SPRITE_ENEMY_RENDER_HEIGHT
        )

        self.sprite_center = pygame.Vector2(
            self.bounds.center[0],
            self.bounds.center[1] - (Constants.SPRITE_ENEMY_RENDER_HEIGHT / 3) * 2
        )
        self.y_sprite_pos = self.position.y - (Constants.SPRITE_ENEMY_RENDER_HEIGHT / 3) * 2
        # NOTE:
        # Unsure about why this is the magic calculation, but I've
        # called it the y_foot_pos as this is where the enemy's foot is positioned when
        # rendered with the adjusted y_sprite_pos
        self.y_foot_pos = self.bounds.center[1] - (Constants.SPRITE_ENEMY_RENDER_HEIGHT / 3) * 1
        self.collision_bounds = pygame.Rect(
            self.position.x,
            self.y_foot_pos - ((Constants.SPRITE_ENEMY_RENDER_HEIGHT / 3) * 2),
            Constants.SPRITE_ENEMY_RENDER_WIDTH,
            Constants.SPRITE_ENEMY_RENDER_HEIGHT)

        self.calculate_goal_path()
        self._target_pos = target_position.copy()
        self.direction = pygame.Vector2(0, 0)

        self.update_hp_bar()


    def update_position(self, dt):
        self.direction = self._target_pos - self.position
        if self.direction.x == 0 and self.direction.y == 0:
            return

        normalized_direction = self.direction.normalize()

        move_speed = self.move_speed * dt
        if self._is_freeze:
            move_speed -= move_speed / Constants.TOWER_FREEZE_SPEED_REDUCTION_DIVISION # Slow down move speed "freeze"

        velocity = normalized_direction * move_speed
        self.position.x += velocity.x
        self.position.y += velocity.y
        self.bounds.x = int(self.position.x)
        self.bounds.y = int(self.position.y)
        self.y_sprite_pos = self.position.y - (Constants.SPRITE_ENEMY_RENDER_HEIGHT / 3) * 2
        self.y_foot_pos = self.bounds.center[1] - (Constants.SPRITE_ENEMY_RENDER_HEIGHT / 3) * 1
        self.sprite_center.x = self.bounds.center[0]
        self.sprite_center.y = self.bounds.center[1] - (Constants.SPRITE_ENEMY_RENDER_HEIGHT / 3) * 2
        self.collision_bounds.x = int(self.position.x)
        self.collision_bounds.y = int(self.y_foot_pos - ((Constants.SPRITE_ENEMY_RENDER_HEIGHT / 3) * 2))


    def update_move_target(self):
        distance = self._target_pos.distance_to(self.position)
        if distance <= Constants.ENEMY_REACHED_DISTANCE:
            if len(self.goal_path) <= 0:
                # No more targets in path, end reached
                self.target_reached = True
                GlobalEventDispatcher.dispatch(Event(Constants.EVENT_ENEMY_ESCAPED))
                return
            else:
                # Move to next target path tile
                next_target = self.goal_path.pop(0)
                self._target_pos = self.tile_manager.tiles[next_target[1]][next_target[0]].position.copy()


    def update_sprite_direction(self):
        if self.direction.x < 0 and self.direction.y < 0:
            self.direction_sprite = f"{Constants.SPRITE_BUNNY_LEFT}{self.wave_number}"
        elif self.direction.x > 0 and self.direction.y > 0:
            self.direction_sprite = f"{Constants.SPRITE_BUNNY_RIGHT}{self.wave_number}"
        elif self.direction.x < 0 and self.direction.y > 0:
            self.direction_sprite = f"{Constants.SPRITE_BUNNY_DOWN}{self.wave_number}"
        elif self.direction.x > 0 and self.direction.y < 0:
            self.direction_sprite = f"{Constants.SPRITE_BUNNY_UP}{self.wave_number}"


    def update_hp_bar(self):
        remain_percentage = (self._hp * 100) / self.max_hp
        self._remaining_health_bar_width = (Constants.ENEMY_HP_BAR_WIDTH * remain_percentage) / 100

        self.used_hp_bar_rect = pygame.Rect(
            self.position.x,
            self.y_sprite_pos,
            Constants.ENEMY_HP_BAR_WIDTH,
            Constants.ENEMY_HP_BAR_HEIGHT
        )
        self.remaining_hp_bar_rect = pygame.Rect(
            self.position.x,
            self.y_sprite_pos,
            self._remaining_health_bar_width,
            Constants.ENEMY_HP_BAR_HEIGHT
        )


    def update_death(self):
        if not self.processed and self.is_dead():
            self.processed = True
            GlobalEventDispatcher.dispatch(Event(Constants.EVENT_ENEMY_DIED, {"enemy": self}))

            color = next((e["color"] for e in ENEMY_CONFIG if e["wave"] == self.wave_number), None)
            color = (pygame.Color(color) if color is not None else pygame.Color(255, 255, 255, 255))

            GlobalEventDispatcher.dispatch(Event(Constants.EVENT_EMIT_PARTICLE, {
                "particles": [get_death_particle(self.sprite_center.x, self.sprite_center.y, color) for _ in range(Constants.ENEMY_DEATH_PARTICLE_COUNT)]
            }))


    def update_freeze_effect(self, dt):
        if self._is_freeze:
            GlobalEventDispatcher.dispatch(Event(Constants.EVENT_EMIT_PARTICLE, {
                "particles": [get_freeze_particle(self.sprite_center.x, self.sprite_center.y)]
            }))
            self._freeze_elapsed += 1 * dt
            if self._freeze_elapsed >= Constants.TOWER_FREEZE_TICK:
                self._freeze_elapsed = 0
                self._is_freeze = False


    def update(self, dt):
        self.update_death()

        if not self.alive():
            return

        self.update_move_target()
        self.update_position(dt)
        self.update_sprite_direction()
        self.update_hp_bar()
        self.update_freeze_effect(dt)


    def get_tile(self) -> Tile | None:
        for row in range(Constants.ROW_COUNT):
            for col in range(Constants.COLUMN_COUNT):
                tile = self.tile_manager.tiles[row][col]
                if tile.contains_point(self.bounds.center[0], self.y_foot_pos):
                    return tile
        return None


    def draw_enemy_bounds(self, renderer: Renderer):
        renderer.request_rectangle_draw(
            RendererType.DEBUG,
            "blue",
            self.bounds,
            3)

        renderer.request_rectangle_draw(
            RendererType.DEBUG,
            "purple",
            self.collision_bounds,
            3)

        renderer.request_circle_draw(
            RendererType.DEBUG,
            "blue",
            self.bounds.center,
            5,
            0)

        renderer.request_circle_draw(
            RendererType.DEBUG,
            "purple",
            (self.bounds.center[0], self.y_foot_pos),
            5,
            0)


    def draw_goal_path(self, renderer: Renderer):
        for index in self.goal_path:
            tile = self.tile_manager.tiles[index[1]][index[0]]
            # renderer.request_on_map_image_draw(
            #     RendererType.FLOOR_TILE,
            #     self.asset_manager.tile_sprites[Constants.SPRITE_START],
            #     tile.position,
            #     tile.index.x,
            #     tile.index.y)
            renderer.request_circle_draw(
                RendererType.GOAL_PATH_OUTER,
                "yellow",
                tile.bounds.center,
                5,
                0)

            renderer.request_circle_draw(
                RendererType.GOAL_PATH_INNER,
                "orange",
                tile.bounds.center,
                4,
                0)


    def draw_hp(self, renderer: Renderer):
        renderer.request_rectangle_draw(
            RendererType.ENEMY_HP_USED,
            "red",
            self.used_hp_bar_rect,
            0)

        renderer.request_rectangle_draw(
            RendererType.ENEMY_HP_REMAINING,
            "green",
            self.remaining_hp_bar_rect,
            0)


    def draw(self, renderer: Renderer):
        if not self.alive() or self.direction_sprite == "":
            return

        tile = self.get_tile()
        if tile:
            if Constants.DEBUG:
                renderer.request_polygon_draw(
                    RendererType.DEBUG,
                    "orange",
                    tile.tile_points,
                    5)

            if self._is_freeze:
                renderer.request_on_map_image_draw(
                    RendererType.EFFECTS_TILE,
                    self.asset_manager.tile_sprites[Constants.SPRITE_FREEZE_TILE],
                    tile.position,
                    tile.index.x,
                    tile.index.y)

            renderer.request_on_map_image_draw(
                RendererType.ENEMY,
                self.asset_manager.enemy_frames_sprites[self.direction_sprite],
                pygame.Vector2(self.position.x, self.y_sprite_pos),
                tile.index.x,
                tile.index.y)

        self.draw_hp(renderer)
        self.draw_goal_path(renderer)

        if Constants.DEBUG:
            self.draw_enemy_bounds(renderer)
