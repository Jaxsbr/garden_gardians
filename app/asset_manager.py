import pygame

from enemy_config import ENEMY_CONFIG
from constants import Constants

class AssetManagerSingleton:
    _instance = None
    ASSETS_PATH_BUTTONS = "assets/buttons.png"
    ASSETS_PATH_TILES = "assets/tiles.png"
    ASSETS_PATH_BACKGROUNDS = "assets/backgrounds.png"
    ASSETS_PATH_ENEMY = "assets/enemy.png"
    ASSETS_PATH_HEALTH = "assets/health.png"

    class AssetManager:
        def __init__(self) -> None:
            buttons = pygame.image.load(AssetManagerSingleton.ASSETS_PATH_BUTTONS).convert_alpha()
            tiles = pygame.image.load(AssetManagerSingleton.ASSETS_PATH_TILES).convert_alpha()
            backgrounds = pygame.image.load(AssetManagerSingleton.ASSETS_PATH_BACKGROUNDS).convert_alpha()
            enemy_frames = pygame.image.load(AssetManagerSingleton.ASSETS_PATH_ENEMY).convert_alpha()
            health = pygame.image.load(AssetManagerSingleton.ASSETS_PATH_HEALTH).convert_alpha()

            self.button_sprites = {
                Constants.SPRITE_BUTTON_SUN_FLOWER: buttons.subsurface(pygame.Rect(0, 0, 64, 64)),
                Constants.SPRITE_BUTTON_SUN_FLOWER_NO_MONEY: buttons.subsurface(pygame.Rect(64, 0, 64, 64)),
                Constants.SPRITE_BUTTON_FREEZE_FLOWER: buttons.subsurface(pygame.Rect(0, 64, 64, 64)),
                Constants.SPRITE_BUTTON_FREEZE_FLOWER_NO_MONEY: buttons.subsurface(pygame.Rect(64, 64, 64, 64))
            }

            self.tile_sprites: dict[str, pygame.Surface] = {
                Constants.SPRITE_GRASS: tiles.subsurface(pygame.Rect(0, 0, Constants.TILE_WIDTH, Constants.TILE_HEIGHT)),
                Constants.SPRITE_DIRT: tiles.subsurface(pygame.Rect(Constants.TILE_WIDTH, 0, Constants.TILE_WIDTH, Constants.TILE_HEIGHT)),
                Constants.SPRITE_START: tiles.subsurface(pygame.Rect(Constants.TILE_WIDTH * 2, 0, Constants.TILE_WIDTH, Constants.TILE_HEIGHT)),
                Constants.SPRITE_END: tiles.subsurface(pygame.Rect(Constants.TILE_WIDTH * 3, 0, Constants.TILE_WIDTH, Constants.TILE_HEIGHT)),
                Constants.SPRITE_FREEZE_TILE: tiles.subsurface(pygame.Rect(Constants.TILE_WIDTH * 4, 0, Constants.TILE_WIDTH, Constants.TILE_HEIGHT)),
                Constants.SPRITE_TALL_TREE: tiles.subsurface(pygame.Rect(0, Constants.TILE_HEIGHT, Constants.TILE_WIDTH, Constants.TILE_HEIGHT * 2)),
                Constants.SPRITE_SHORT_TREE: tiles.subsurface(pygame.Rect(Constants.TILE_WIDTH, Constants.TILE_HEIGHT, Constants.TILE_WIDTH, Constants.TILE_HEIGHT * 2)),
                Constants.SPRITE_FREEZE_FLOWER: tiles.subsurface(pygame.Rect(0, Constants.TILE_HEIGHT * 3, Constants.TILE_WIDTH, Constants.TILE_HEIGHT)),
                Constants.SPRITE_SUN_FLOWER: tiles.subsurface(pygame.Rect(Constants.TILE_WIDTH, Constants.TILE_HEIGHT * 3, Constants.TILE_WIDTH, Constants.TILE_HEIGHT)),
                Constants.SPRITE_FENCE_LEFT: tiles.subsurface(pygame.Rect(Constants.TILE_WIDTH * 2, Constants.TILE_HEIGHT, Constants.TILE_WIDTH, Constants.TILE_HEIGHT * 2)),
                Constants.SPRITE_FENCE_TOP: tiles.subsurface(pygame.Rect(Constants.TILE_WIDTH * 3, Constants.TILE_HEIGHT, Constants.TILE_WIDTH, Constants.TILE_HEIGHT * 2)),
            }

            self.tile_sprites[Constants.SPRITE_GRASS] = pygame.transform.scale(
                        self.tile_sprites[Constants.SPRITE_GRASS], (Constants.TILE_RENDER_WIDTH, Constants.TILE_RENDER_HEIGHT))
            self.tile_sprites[Constants.SPRITE_DIRT] = pygame.transform.scale(
                        self.tile_sprites[Constants.SPRITE_DIRT], (Constants.TILE_RENDER_WIDTH, Constants.TILE_RENDER_HEIGHT))
            self.tile_sprites[Constants.SPRITE_START] = pygame.transform.scale(
                        self.tile_sprites[Constants.SPRITE_START], (Constants.TILE_RENDER_WIDTH, Constants.TILE_RENDER_HEIGHT))
            self.tile_sprites[Constants.SPRITE_END] = pygame.transform.scale(
                        self.tile_sprites[Constants.SPRITE_END], (Constants.TILE_RENDER_WIDTH, Constants.TILE_RENDER_HEIGHT))
            self.tile_sprites[Constants.SPRITE_FREEZE_TILE] = pygame.transform.scale(
                        self.tile_sprites[Constants.SPRITE_FREEZE_TILE], (Constants.TILE_RENDER_WIDTH, Constants.TILE_RENDER_HEIGHT))
            self.tile_sprites[Constants.SPRITE_TALL_TREE] = pygame.transform.scale(
                        self.tile_sprites[Constants.SPRITE_TALL_TREE], (Constants.TILE_RENDER_WIDTH, Constants.TILE_RENDER_HEIGHT * 2))
            self.tile_sprites[Constants.SPRITE_SHORT_TREE] = pygame.transform.scale(
                        self.tile_sprites[Constants.SPRITE_SHORT_TREE], (Constants.TILE_RENDER_WIDTH, Constants.TILE_RENDER_HEIGHT * 2))
            self.tile_sprites[Constants.SPRITE_FREEZE_FLOWER] = pygame.transform.scale(
                        self.tile_sprites[Constants.SPRITE_FREEZE_FLOWER], (Constants.TILE_RENDER_WIDTH, Constants.TILE_RENDER_HEIGHT))
            self.tile_sprites[Constants.SPRITE_SUN_FLOWER] = pygame.transform.scale(
                        self.tile_sprites[Constants.SPRITE_SUN_FLOWER], (Constants.TILE_RENDER_WIDTH, Constants.TILE_RENDER_HEIGHT))
            self.tile_sprites[Constants.SPRITE_FENCE_LEFT] = pygame.transform.scale(
                        self.tile_sprites[Constants.SPRITE_FENCE_LEFT], (Constants.TILE_RENDER_WIDTH, Constants.TILE_RENDER_HEIGHT * 2))
            self.tile_sprites[Constants.SPRITE_FENCE_TOP] = pygame.transform.scale(
                        self.tile_sprites[Constants.SPRITE_FENCE_TOP], (Constants.TILE_RENDER_WIDTH, Constants.TILE_RENDER_HEIGHT * 2))

            self.backgrounds_sprites: dict[str, pygame.Surface] = {
                Constants.SPRITE_BACKGROUND_1: backgrounds.subsurface(pygame.Rect(0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)),
                Constants.SPRITE_BACKGROUND_2: backgrounds.subsurface(pygame.Rect(0, Constants.SCREEN_HEIGHT, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)),
            }

            self.enemy_frames_sprites = {}
            for config in ENEMY_CONFIG:
                wave_number = config["wave"]
                down = f"{Constants.SPRITE_BUNNY_DOWN}{wave_number}"
                right = f"{Constants.SPRITE_BUNNY_RIGHT}{wave_number}"
                up = f"{Constants.SPRITE_BUNNY_UP}{wave_number}"
                left = f"{Constants.SPRITE_BUNNY_LEFT}{wave_number}"

                start_x = (wave_number - 1) * Constants.SPRITE_ENEMY_WIDTH # wave needs to start on 0 to calculate x sprite properly
                self.enemy_frames_sprites[down] = enemy_frames.subsurface(pygame.Rect(start_x, 0, Constants.SPRITE_ENEMY_WIDTH, Constants.SPRITE_ENEMY_HEIGHT))
                self.enemy_frames_sprites[right] = enemy_frames.subsurface(pygame.Rect(start_x, Constants.SPRITE_ENEMY_HEIGHT, Constants.SPRITE_ENEMY_WIDTH, Constants.SPRITE_ENEMY_HEIGHT))
                self.enemy_frames_sprites[up] = enemy_frames.subsurface(pygame.Rect(start_x, Constants.SPRITE_ENEMY_HEIGHT * 2, Constants.SPRITE_ENEMY_WIDTH, Constants.SPRITE_ENEMY_HEIGHT))
                self.enemy_frames_sprites[left] = enemy_frames.subsurface(pygame.Rect(start_x, Constants.SPRITE_ENEMY_HEIGHT * 3, Constants.SPRITE_ENEMY_WIDTH, Constants.SPRITE_ENEMY_HEIGHT))

                render_size = (Constants.SPRITE_ENEMY_RENDER_WIDTH, Constants.SPRITE_ENEMY_RENDER_HEIGHT)
                self.enemy_frames_sprites[down] = pygame.transform.scale(self.enemy_frames_sprites[down], render_size)
                self.enemy_frames_sprites[right] = pygame.transform.scale(self.enemy_frames_sprites[right], render_size)
                self.enemy_frames_sprites[up] = pygame.transform.scale(self.enemy_frames_sprites[up], render_size)
                self.enemy_frames_sprites[left] = pygame.transform.scale(self.enemy_frames_sprites[left], render_size)

            self.health_sprites = {}
            for i in range(15):
                self.health_sprites[f"{Constants.SPRITE_HEALTH}{i}"] = health.subsurface(
                    pygame.Rect(
                        0,
                        Constants.HEALTH_SPRITE_HEIGHT * i,
                        Constants.HEALTH_SPRITE_WIDTH,
                        Constants.HEALTH_SPRITE_HEIGHT))
                self.health_sprites[f"{Constants.SPRITE_HEALTH}{i}"] = pygame.transform.scale(
                    self.health_sprites[f"{Constants.SPRITE_HEALTH}{i}"],
                    (Constants.HEALTH_WIDTH, Constants.HEALTH_HEIGHT))

    def __new__(cls):
        if cls._instance is None:
            # Create a new EventDispatcher instance if not already created
            cls._instance = cls.AssetManager()
        return cls._instance

        # TODO: Call State.selected

def get_asset_manager():
    return AssetManagerSingleton()
