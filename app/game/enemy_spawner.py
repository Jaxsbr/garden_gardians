from dataclasses import dataclass, field

from enemy_config import ENEMY_CONFIG
from events import Event, GlobalEventDispatcher
from game.energy_manager import EnergyManager
from utils.random_helper import get_variable_int
from game.map_generator import MapConfig
from renderer import Renderer
from custom_types.int_vector2 import IntVector2
from constants import Constants
from game.enemy import Enemy
from game.tile_manager import TileManager


@dataclass
class EnemySpawner:
    tile_manager: TileManager
    energy_manager: EnergyManager
    map_config: MapConfig
    start_tile_index: IntVector2
    goal_tile_index: IntVector2
    enemies: list[Enemy] = field(default_factory=list)
    spawn_id: int = field(default=0)

    def __post_init__(self):
        GlobalEventDispatcher.register_listener(self, "EnemySpawner")


    def on_event(self, event) -> bool:
        if event.event_name == Constants.EVENT_SPAWN_NEW_ENEMY:
            self.spawn_enemy(event.args["enemy_config"])
            return True
        return False


    def spawn_enemy(self, enemy_config):
        wave_number = enemy_config["wave"]
        hp = enemy_config["hp"]
        move_speed = enemy_config["speed"]
        reward = enemy_config["reward"]

        hp_variation = int(hp / 10) # ensure only slight difference in speed
        variable_hp = get_variable_int(int(hp), hp_variation)

        move_speed_variation = int(move_speed / 15) # ensure only slight difference in speed
        variable_move_speed = get_variable_int(int(move_speed), move_speed_variation)

        self.spawn_id += 1
        enemy = Enemy(
            self.tile_manager,
            self.map_config,
            self.start_tile_index,
            self.goal_tile_index,
            variable_hp,
            variable_move_speed,
            f"id-{self.spawn_id}",
            wave_number,
            reward)
        self.enemies.append(enemy)


    def raise_place_notification(self):
        for enemy in self.enemies:
            enemy.calculate_goal_path()


    def update(self, dt, ):
        # NOTE: loop a copy of enemies, delete from enemies
        for enemy in self.enemies[:]:
            enemy.update(dt)

            if not enemy.alive():
                self.enemies.remove(enemy)
                GlobalEventDispatcher.dispatch(Event(Constants.EVENT_ENEMY_PROCESSED))


    def draw(self, renderer: Renderer):
        for enemy in self.enemies:
            enemy.draw(renderer)


