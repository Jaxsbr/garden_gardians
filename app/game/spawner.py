import math
import pygame
from enums import GameState
from enemy_config import ENEMY_CONFIG
from renderer import Renderer, RendererType, TextFontType
from constants import Constants
from events import Event, GlobalEventDispatcher
from screens.game_over import GlobalGameOverStats

# TODO: rename waves/rounds/level etc
class Spawner:
    STATE_COUNTING = "counting"
    STATE_SPAWNING = "spawning"
    STATE_WAITING = "waiting"
    COUNTING_TICK = Constants.WAVE_COUNTING_TICK
    SPAWNING_TICK = Constants.ENEMY_SPAWN_RATE
    SPAWN_COUNT = Constants.ENEMY_SPAWN_COUNT

    def __init__(self):
        GlobalEventDispatcher.register_listener(self, "Spawner")

        self.wave_state = Spawner.STATE_COUNTING
        self.counting_elapsed = Spawner.COUNTING_TICK
        self.spawning_elapsed = 0
        self.total_spawn_count = 0 # enemies that where spawned for the current wave
        self.spawn_processed_count = 0 # total enemies died and escaped per wave
        self.wave_number = 0
        self.killed = 0
        self.escaped = 0
        self.enemy_config = None
        self.wave_count = len(ENEMY_CONFIG)
        self.done = False


    def on_event(self, event: Event) -> bool:
        if self.done:
            return False

        enemy_config = self._get_enemy_config_by_wave(self.wave_number)
        if not enemy_config:
            return False

        GlobalGameOverStats.max_wave_number = self.wave_number

        if event.event_name == Constants.EVENT_ENEMY_PROCESSED:
            self.spawn_processed_count += 1
            GlobalGameOverStats.bunny_stats[enemy_config["name"]].spawn += 1
            return True

        if event.event_name == Constants.EVENT_ENEMY_DIED:
            self.killed += 1
            GlobalGameOverStats.bunny_stats[enemy_config["name"]].killed += 1
            return True

        if event.event_name == Constants.EVENT_ENEMY_ESCAPED:
            self.escaped += 1
            GlobalGameOverStats.bunny_stats[enemy_config["name"]].escaped += 1
            return True

        return False


    def update(self, dt):
        if self.wave_number > 0:
            self.enemy_config = self._get_enemy_config_by_wave(self.wave_number)
        self._update_counting(dt)
        self._update_spawning(dt)
        self._update_waiting(dt)

        if self.wave_number > self.wave_count:
            self.done = True
            GlobalEventDispatcher.dispatch(Event(
                Constants.EVENT_GAME_STATUS_CHANGED, {
                    "next_state": GameState.GAME_OVER,
                    "state_data": {"status_text": "YOU WIN"}}))

        if self.escaped >= Constants.GAME_OVER_ESCAPE_COUNT:
            self.done = True
            print('lose game')
            GlobalEventDispatcher.dispatch(Event(
                Constants.EVENT_GAME_STATUS_CHANGED, {
                    "next_state": GameState.GAME_OVER,
                    "state_data": {"status_text": "YOU LOSE"}}))


    def _get_enemy_config_by_wave(self, wave_number):
        for config in ENEMY_CONFIG:
            if config["wave"] == wave_number:
                return config


    def _update_counting(self, dt):
        if self.wave_state != Spawner.STATE_COUNTING:
            return

        self.counting_elapsed -= 1 * dt
        if self.counting_elapsed <= 0:
            self.counting_elapsed = Spawner.COUNTING_TICK
            self.wave_number += 1
            GlobalEventDispatcher.dispatch(Event(
                Constants.EVENT_WAVE_NUMBER_CHANGED, {"wave_number": self.wave_number}))
            self.wave_state = Spawner.STATE_SPAWNING


    def _update_spawning(self, dt):
        if self.wave_state != Spawner.STATE_SPAWNING or self.enemy_config is None:
            return

        self.spawning_elapsed += 1 * dt
        if self.spawning_elapsed >= self.enemy_config["rate"]:
            self.spawning_elapsed = 0
            GlobalEventDispatcher.dispatch(Event(
                Constants.EVENT_SPAWN_NEW_ENEMY, { "enemy_config": self.enemy_config}))
            self.total_spawn_count += 1

        if self.total_spawn_count >= self.enemy_config["count"]:
            self.wave_state = Spawner.STATE_WAITING


    def _update_waiting(self, dt):
        if self.wave_state != Spawner.STATE_WAITING or self.enemy_config is None:
            return

        if self.spawn_processed_count >= self.enemy_config["count"]:
            self.spawn_processed_count = 0
            self.total_spawn_count = 0
            self.wave_state = Spawner.STATE_COUNTING


    def draw(self, renderer: Renderer):
        count_down_text = f"wave {self.wave_number + 1}: {math.ceil(self.counting_elapsed)}"
        bottom_offset = 32
        bunny_name_offset = 20
        if self.wave_state == Spawner.STATE_COUNTING:
            renderer.request_text_draw(
                RendererType.WAVE_TEXT_SHADOW,
                "black",
                count_down_text,
                TextFontType.get_font(72),
                pygame.Vector2(
                    Constants.SCREEN_WIDTH / 2 + 2,
                    Constants.SCREEN_HEIGHT - bottom_offset + 2))

            renderer.request_text_draw(
                RendererType.WAVE_TEXT,
                "yellow",
                count_down_text,
                TextFontType.get_font(72),
                pygame.Vector2(
                    Constants.SCREEN_WIDTH / 2,
                    Constants.SCREEN_HEIGHT - bottom_offset))
        else:
            if self.enemy_config is None:
                return

            renderer.request_text_draw(
                RendererType.WAVE_TEXT_SHADOW,
                "black",
                self.enemy_config["name"],
                TextFontType.get_font(32),
                pygame.Vector2(
                    Constants.SCREEN_WIDTH / 2 + 2,
                    Constants.SCREEN_HEIGHT - bunny_name_offset + 2))

            renderer.request_text_draw(
                RendererType.WAVE_TEXT,
                self.enemy_config["color"],
                self.enemy_config["name"],
                TextFontType.get_font(32),
                pygame.Vector2(
                    Constants.SCREEN_WIDTH / 2,
                    Constants.SCREEN_HEIGHT - bunny_name_offset))
