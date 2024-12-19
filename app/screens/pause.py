from constants import Constants
from colors import BACKGROUND_COLOR_MENU, FOCUS_COLOR_MENU, TEXT_COLOR_MENU
from gui import GUI, GUIButton
from events import Event, GlobalEventDispatcher
from enums import GameState
from state_manager import StateManager
from state import State
import pygame

class Pause(State):
    EVENT_CONTINUE = "pause_state_continue"
    EVENT_MENU = "pause_state_menu"
    EVENT_QUIT = "pause_state_quit"

    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager
        self.bounds = pygame.Rect(0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)
        GlobalEventDispatcher.register_listener(self, "Pause")

        buttons = [
            GUIButton(Pause.EVENT_CONTINUE, "Continue"),
            GUIButton(Pause.EVENT_MENU, "Menu"),
            GUIButton(Pause.EVENT_QUIT, "Exit")]

        self.pause_screen = GUI(
            self.bounds,
            buttons,
            "PAUSE",
            text_color=TEXT_COLOR_MENU,
            focus_color=FOCUS_COLOR_MENU,
            background_color=BACKGROUND_COLOR_MENU)


    def on_event(self, event: Event) -> bool:
        if event.event_name == Pause.EVENT_CONTINUE:
            self.state_manager.change(GameState.GAME, {"continue": True})
            return True
        elif event.event_name == Pause.EVENT_MENU:
            self.state_manager.change(GameState.MENU)
            return True
        elif event.event_name == Pause.EVENT_QUIT:
            exit()
            return True
        return False


    def selected(self, state_values: dict[str, str | int | bool | pygame.Color] | None):
        pass


    def update(self, dt):
        self.pause_screen.update(dt)


    def draw(self, screen, renderer):
        self.pause_screen.draw(screen)
