from dataclasses import dataclass, field
from enemy_config import ENEMY_CONFIG
from renderer import RendererType
from constants import Constants
from colors import BACKGROUND_COLOR_GAME_OVER_LOSE, BACKGROUND_COLOR_GAME_OVER_WIN, FOCUS_COLOR_GAME_OVER_LOSE, FOCUS_COLOR_GAME_OVER_WIN, TEXT_COLOR_GAME_OVER_LOSE, TEXT_COLOR_GAME_OVER_WIN
from gui import GUI, GUIButton
from events import Event, GlobalEventDispatcher
from asset_manager import get_asset_manager
from enums import GameState
from state_manager import StateManager
from state import State
import pygame


@dataclass
class GameOverStatBunny:
    spawn: int
    killed: int
    escaped: int


@dataclass
class GameOverStatTower:
    count: int
    total_shoot_count: int


class GameOverStatsSingleton:
    _instance = None

    @dataclass
    class GameOverStats:
        bunny_stats: dict[str, GameOverStatBunny] = field(default_factory=dict)
        tower_stats: dict[str, GameOverStatTower] = field(default_factory=dict)
        shoot_damage = 0
        max_wave_number: int = 0

        def __post_init__(self):
            for config in ENEMY_CONFIG:
                name = config["name"]
                self.bunny_stats[name] = GameOverStatBunny(0, 0, 0)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = cls.GameOverStats()
        return cls._instance

GlobalGameOverStats = GameOverStatsSingleton()


class GameOver(State):
    EVENT_MENU = "game_over_state_menu"
    EVENT_QUIT = "game_over_state_quit"

    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager
        self.asset_manager = get_asset_manager()
        self.bounds = pygame.Rect(0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)
        self.stat_font_size = 16
        self.name_font_size = 24
        self.stat_font = pygame.font.Font(pygame.font.get_default_font(), self.stat_font_size)
        self.name_font = pygame.font.Font(pygame.font.get_default_font(), self.name_font_size)


        GlobalEventDispatcher.register_listener(self, "GameOver")

        buttons = [
            GUIButton(GameOver.EVENT_MENU, "Menu"),
            GUIButton(GameOver.EVENT_QUIT, "Exit")]

        self.game_over_screen = GUI(
            self.bounds,
            buttons)


    def on_event(self, event: Event) -> bool:
        if event.event_name == GameOver.EVENT_MENU:
            self.state_manager.change(GameState.MENU)
            return True
        elif event.event_name == GameOver.EVENT_QUIT:
            exit()
            return True
        return False


    def selected(self, state_values: dict[str, str | int | bool | pygame.Color] | None):
        if state_values:
            self.game_over_screen.title_text = str(state_values["status_text"])
            if self.game_over_screen.title_text == "YOU WIN":
                self.game_over_screen.text_color = TEXT_COLOR_GAME_OVER_WIN
                self.game_over_screen.focus_color = FOCUS_COLOR_GAME_OVER_WIN
                self.game_over_screen.background_color = BACKGROUND_COLOR_GAME_OVER_WIN
            else:
                self.game_over_screen.text_color = TEXT_COLOR_GAME_OVER_LOSE
                self.game_over_screen.focus_color = FOCUS_COLOR_GAME_OVER_LOSE
                self.game_over_screen.background_color = BACKGROUND_COLOR_GAME_OVER_LOSE

        print('game over selected')


    def update(self, dt):
        self.game_over_screen.update(dt)


    def draw(self, screen, renderer):
        self.game_over_screen.draw(screen)

        y = 20  # Initial Y position
        x_name = 64  # X offset for name
        y_name_center_align = 50  # Align name with image center
        image_offset = 24  # Offset to remove transparent margins
        y_spacing_after_image = 100  # Space after image
        stat_spacing = self.stat_font_size  # Spacing for stat lines
        magic_space = 40

        for i, config in enumerate(ENEMY_CONFIG):
            # Retrieve stats
            name = config["name"]
            wave = config['wave']
            image = self.asset_manager.enemy_frames_sprites[f"{Constants.SPRITE_BUNNY_RIGHT}{wave}"]
            spawn = GlobalGameOverStats.bunny_stats[name].spawn
            killed = GlobalGameOverStats.bunny_stats[name].killed
            escaped = GlobalGameOverStats.bunny_stats[name].escaped
            text_color = ("gray" if wave > GlobalGameOverStats.max_wave_number else "lime")

            # Adjust rendering positions
            image_y = y - image_offset if i > 0 else y  # Only apply image_offset for subsequent waves
            name_y = image_y + y_name_center_align

            # Render the bunny image
            renderer.request_off_map_image_draw(
                RendererType.NONE,
                image,
                pygame.Vector2(0, image_y)
            )

            # Render the name
            renderer.draw_text(screen, self.name_font, "black", f" {name}", (x_name + 1, name_y + 1))
            renderer.draw_text(screen, self.name_font, config["color"], f" {name}", (x_name, name_y))

            # Increment Y to position stats below the bunny
            stats_y = image_y + y_spacing_after_image

            # Render "killed" stats
            renderer.draw_text(screen, self.stat_font, "black", f"- killed: {killed}/{spawn}", (1, stats_y + 1))
            renderer.draw_text(screen, self.stat_font, text_color, f"- killed: {killed}/{spawn}", (0, stats_y))

            # Increment Y for "escaped" stats
            stats_y += stat_spacing

            renderer.draw_text(screen, self.stat_font, "black", f"- escaped: {escaped}/{spawn}", (1, stats_y + 1))
            renderer.draw_text(screen, self.stat_font, text_color, f"- escaped: {escaped}/{spawn}", (0, stats_y))

            # Increment Y for the next bunny
            y += y_spacing_after_image - (image_offset if i > 0 else 0) + magic_space



