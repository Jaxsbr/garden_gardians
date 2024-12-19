from constants import Constants
from colors import BACKGROUND_COLOR_MENU, FOCUS_COLOR_MENU, TEXT_COLOR_MENU
from events import Event, GlobalEventDispatcher
from gui import GUIButton, GUI
from enums import GameState
from state_manager import StateManager
from state import State
import pygame

class MenuState(State):
    EVENT_PlAY = "menu_state_play"
    EVENT_QUIT = "menu_state_quit"

    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager
        self.bounds = pygame.Rect(0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)
        GlobalEventDispatcher.register_listener(self, "MenuState")
        self.enabled = False
        self.elasped = 0
        self.tick = 0.5 # disable mechanism, prevents fast click from game over to menu/play

        buttons = [
            GUIButton(MenuState.EVENT_PlAY, "Play"),
            GUIButton(MenuState.EVENT_QUIT, "Exit")]

        self.menu_screen = GUI(
            self.bounds,
            buttons,
            "MENU",
            text_color=TEXT_COLOR_MENU,
            focus_color=FOCUS_COLOR_MENU,
            background_color=BACKGROUND_COLOR_MENU)


    def selected(self, state_values: dict[str, str | int | bool | pygame.Color] | None):
        print('menu selected')
        self.enabled = False
        self.elasped = 0


    def on_event(self, event: Event) -> bool:
        if event.event_name == MenuState.EVENT_PlAY:
            self.state_manager.change(GameState.GAME, {"is_new": True})
            return True
        elif event.event_name == MenuState.EVENT_QUIT:
            exit()
            return True
        return False


    def update(self, dt):
        self.elasped += dt * 1
        if self.elasped >= self.tick:
            self.enabled = True

        self.menu_screen.enabled = self.enabled
        self.menu_screen.update(dt)


    def draw(self, screen, renderer):
        self.menu_screen.draw(screen)
