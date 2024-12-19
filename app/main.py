from enums import GameState
from game.game import Game
from screens.game_over import GameOver
from screens.menu import MenuState
from screens.pause import Pause
from constants import Constants
from renderer import Renderer
from state_manager import StateManager
import pygame

class Main:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        self.renderer = Renderer() # TODO: make global singleton
        self.state_manager = StateManager(GameState.MENU)
        self.state_manager.state_objects = {
            GameState.MENU: MenuState(self.state_manager),
            GameState.GAME: Game(self.state_manager),
            GameState.GAME_OVER: GameOver(self.state_manager),
            GameState.PAUSE: Pause(self.state_manager)
        }


    def update(self):
        dt = self.clock.tick(30) / 1000
        self.state_manager.update(dt)
        self.renderer.update()


    def draw(self):
        self.state_manager.draw(self.screen, self.renderer)
        self.renderer.draw(self.screen)
        pygame.display.flip()


    def update_game_state(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True


    def run_game_loop(self):
        while True:
            running = self.update_game_state()
            if not running:
                break

            self.update()
            self.draw()


if __name__ == "__main__":
    main = Main()
    main.run_game_loop()
