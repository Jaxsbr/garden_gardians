import math
from particle_engine import ParticleEngine
from game.tile import Tile
from game.button_manager import ButtonManager
from enums import GameState
from game.combat_text_configs import get_combat_text
from game.spawner import Spawner
from events import Event, GlobalEventDispatcher
from asset_manager import get_asset_manager
from state_manager import StateManager
from utils.random_helper import get_variable_int
from game.combat_text import CombatTextEngine, CombatTextType
from game.map_generator import MapGenerator
from game.goal_path_helper import get_collision_grid, get_goal_path
from renderer import Renderer, RendererType
from game.enemy_spawner import EnemySpawner
from game.bullet_manager import Bullet, BulletManager
from game.tower import Tower, TowerConfig
from game.enemy import Enemy
from game.background_manager import BackgroundManager
from game.energy_manager import EnergyManager
from custom_types.int_vector2 import IntVector2
from custom_types.base_button import BaseButton
from constants import Constants
from game.tile_manager import TileManager
from state import State
import pygame


class Game(State):
    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager
        self.asset_manager = get_asset_manager()
        self.bounds = pygame.Rect(0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)
        self.map_generator = MapGenerator()
        GlobalEventDispatcher.register_listener(self, "Game")

        self.mouse_over_tile_map = False
        self.selector_index = IntVector2()
        self.tile_manager = TileManager(self.map_generator.map_config)

        self.button_manager = ButtonManager()
        self.combat_text_engine = CombatTextEngine()
        self.energy_manager = EnergyManager()
        self.background_manager = BackgroundManager()
        self.particle_engine = ParticleEngine(use_renderer=True)

        self.bullet_manager = BulletManager()
        self.towers: list[Tower] = []
        self.enemy_spawner = EnemySpawner(
            self.tile_manager,
            self.energy_manager,
            self.map_generator.map_config,
            self.map_generator.map_config.start_quadrant.main_index,
            self.map_generator.map_config.end_quadrant.main_index)
        self.spawner = Spawner()
        self.game_over = False
        self.is_restarted = False


    def selected(self, state_values: dict[str, str | int | bool | pygame.Color] | None):
        if state_values and not state_values.get("continue"):
            self.__init__(self.state_manager)


    def on_event(self, event: Event) -> bool:
        if event.event_name == Constants.EVENT_GAME_STATUS_CHANGED:
            self.game_over = True
            self.state_manager.change(
                event.args["next_state"],
                {"status_text": event.args["state_data"]["status_text"]})
            return True
        elif event.event_name == Constants.EVENT_EMIT_PARTICLE:
            particles = event.args["particles"]
            for particle in particles:
                self.particle_engine.emit_particle(particle)
        return False


    def place_tower(self, tile: Tile, tower_type: str):
        image: pygame.Surface
        shoot_rate = 0
        name = tower_type
        range = 0

        if name == Constants.SPRITE_SUN_FLOWER:
            image = self.asset_manager.tile_sprites[Constants.SPRITE_SUN_FLOWER]
            shoot_rate = Constants.TOWER_SUN_FLOWER_SHOOT_RATE
            range = Constants.TOWER_SUN_FLOWER_RANGE
        elif name == Constants.SPRITE_FREEZE_FLOWER:
            image = self.asset_manager.tile_sprites[Constants.SPRITE_FREEZE_FLOWER]
            shoot_rate = Constants.TOWER_FREEZE_FLOWER_SHOOT_RATE
            range = Constants.TOWER_FREEZE_FLOWER_RANGE
        else:
            raise Exception(f"no such button type {name}")

        tower_config = TowerConfig(name, image, shoot_rate, range)
        self.towers.append(Tower(tile, tower_config))


    def place(self, selected_button: BaseButton):
        tile = self.tile_manager.tiles[self.selector_index.y][self.selector_index.x]
        object_value = Constants.LAYER_PLACED_VALUES[selected_button.name]
        proposed_collision_grid = get_collision_grid(self.tile_manager)
        proposed_collision_grid[self.selector_index.x][self.selector_index.y] = 1 # 1 is a collision
        blocks_goal_path = len(get_goal_path(
            self.tile_manager,
            self.map_generator.map_config.start_quadrant.main_index,
            self.map_generator.map_config.end_quadrant.main_index,
            proposed_collision_grid)) <= 0
        can_place = tile.can_place()
        energy_value = selected_button.get_cost()

        if not blocks_goal_path and can_place and self.energy_manager.energy >= energy_value:
            tile.set_placed_layer_value(object_value)
            self.place_tower(tile, selected_button.name)
            selected_button.set_selection(False)
            self.energy_manager.reduce_energy(energy_value)
            GlobalEventDispatcher.dispatch(Event(
                Constants.EVENT_ADD_COMBAT_TEXT,
                { "combat_text": get_combat_text(CombatTextType.DAMAGE, f"-{energy_value}", tile.position.copy()) }))
            self.enemy_spawner.raise_place_notification()


    def find_weakest_in_range(self, from_pos: pygame.Vector2, range: float) -> Enemy | None:
        matching_enemy = None
        weakest_hp = math.inf
        living_enemies = [enemy for enemy in self.enemy_spawner.enemies if enemy.alive()]
        for enemy in living_enemies:
            distance = from_pos.distance_to(enemy.sprite_center)
            if distance <= range:
                if enemy._hp < weakest_hp:
                    matching_enemy = enemy
        return matching_enemy


    def update_selector(self, mouse_x, mouse_y):
        self.mouse_over_tile_map = False
        for row in range(Constants.ROW_COUNT):
            for col in range(Constants.COLUMN_COUNT):
                tile = self.tile_manager.tiles[row][col]
                if tile.contains_point(mouse_x, mouse_y):
                    self.mouse_over_tile_map = True
                    self.selector_index = tile.index
                    self.selector_tile_pos = self.tile_manager.tiles[self.selector_index.y][self.selector_index.x].position
                    return


    def update_buttons(self, dt):
        self.button_manager.update(dt, self.energy_manager.energy)
        selected_button = self.button_manager.get_selected_button()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        if selected_button and self.energy_manager.energy <= 0:
            selected_button.set_selection(False)

        if selected_button and not selected_button.is_over and not self.mouse_over_tile_map and mouse_clicked:
            selected_button.set_selection(False)

        if selected_button and self.mouse_over_tile_map and mouse_clicked:
            self.place(selected_button)


    def update_towers(self, dt):
        for tower in self.towers:
            target_enemy = self.find_weakest_in_range(tower.center, tower.config.range)
            if target_enemy is not None:
                tower.set_shoot_target(target_enemy.sprite_center.copy())
            else:
                tower.cancel_target()
            tower.update(dt)


    def update_bullet_hit(self, enemy: Enemy, colliding_bullet: Bullet):
        damage_variation = int(colliding_bullet.bullet_config["damage"] / 2)
        damage = get_variable_int(colliding_bullet.bullet_config["damage"], damage_variation)
        enemy.apply_damage(damage, colliding_bullet.bullet_config["effect"])


    def update_bullet_collisions(self, dt):
        self.bullet_manager.update(dt)
        living_enemies = [enemy for enemy in self.enemy_spawner.enemies if enemy.alive()]
        for enemy in living_enemies:
            colliding_bullet = self.bullet_manager.get_collisions(enemy.collision_bounds)
            if colliding_bullet is not None:
                self.update_bullet_hit(enemy, colliding_bullet)


    def update(self, dt):
        if self.game_over:
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.update_selector(mouse_x, mouse_y)
        self.update_buttons(dt)
        self.energy_manager.update(dt)
        self.background_manager.update(dt)
        self.spawner.update(dt)

        self.update_towers(dt)
        self.update_bullet_collisions(dt)
        self.enemy_spawner.update(dt)
        self.combat_text_engine.update(dt)
        self.particle_engine.update(dt)

        pressed_key = pygame.key.get_pressed()
        if pressed_key[pygame.K_p]:
            self.state_manager.change(GameState.PAUSE)


    def draw_selected_placeable(self, renderer: Renderer):
        selected_button = next((button for button in self.button_manager.buttons if button.is_selected), None)
        if not selected_button:
            return

        if not self.mouse_over_tile_map:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            renderer.request_off_map_image_draw(
                RendererType.SUN_FLOWER_PLACEABLE,
                self.asset_manager.tile_sprites[selected_button.name],
                (mouse_x - Constants.TILE_WIDTH / 2, mouse_y - Constants.TILE_HEIGHT / 2))
        elif self.mouse_over_tile_map:
            tile = self.tile_manager.tiles[self.selector_index.y][self.selector_index.x]
            proposed_collision_grid = get_collision_grid(self.tile_manager)
            proposed_collision_grid[self.selector_index.x][self.selector_index.y] = 1 # 1 is a collision
            if not tile.can_place():
                renderer.request_polygon_draw(
                    RendererType.CANT_PlACE,
                    "red",
                    tile.tile_points,
                    0)
            elif len(get_goal_path(
                    self.tile_manager,
                    self.map_generator.map_config.start_quadrant.main_index,
                    self.map_generator.map_config.end_quadrant.main_index,
                    proposed_collision_grid)) <= 0:
                        renderer.request_polygon_draw(
                        RendererType.CANT_PlACE,
                        "orange",
                        tile.tile_points,
                        0)
            else:
                renderer.request_on_map_image_draw(
                    RendererType.SUN_FLOWER_PLACEABLE,
                    self.asset_manager.tile_sprites[selected_button.name],
                    self.tile_manager.tiles[self.selector_index.y][self.selector_index.x].position,
                    self.selector_index.x,
                    self.selector_index.y)


    def draw_hud(self, screen, renderer: Renderer):
        self.button_manager.draw(screen, renderer)
        self.energy_manager.draw_energy(screen, renderer)

        escape_count = max(0, min(self.spawner.escaped, Constants.GAME_OVER_ESCAPE_COUNT - 1))
        screen.blit(
            self.asset_manager.health_sprites[f"{Constants.SPRITE_HEALTH}{escape_count}"],
            pygame.Vector2(Constants.BUTTON_OFFSET, Constants.BUTTON_OFFSET))


    def draw(self, screen, renderer):
        if self.game_over:
            return

        screen.fill("skyblue")
        self.background_manager.draw(screen)
        self.tile_manager.draw_floor_layer(renderer)
        self.tile_manager.draw_selector(renderer, self.selector_index.y, self.selector_index.x)
        self.tile_manager.draw_fence(renderer)

        for tower in self.towers:
            tower.draw(renderer)

        self.bullet_manager.draw(renderer)
        self.spawner.draw(renderer)
        self.enemy_spawner.draw(renderer)

        self.tile_manager.draw_collision_layer(renderer)

        self.draw_hud(screen, renderer)
        self.draw_selected_placeable(renderer)
        self.combat_text_engine.draw(renderer)
        self.particle_engine.draw(screen, renderer)
