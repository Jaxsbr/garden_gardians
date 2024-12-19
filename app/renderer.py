from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import pygame

from game.map import Map


class DrawType(Enum):
    IMAGE = "image"
    RECTANGLE = "rectangle"
    CIRCLE = "circle"
    CIRCLE_ALPHA = "circle_alpha"
    POLYGON = "polygon"
    TEXT = "text"


class RendererType(Enum):
    NONE = "none"
    DEBUG = "debug"
    PLACED = "placed"
    ENEMY = "enemy"
    ENEMY_HP_USED = "enemy_hp_used"
    ENEMY_HP_REMAINING = "enemy_hp_remaining"
    SUN_FLOWER_PLACEABLE = "sun_flower_placeable"
    FLOOR_TILE = "floor_tile"
    EFFECTS_TILE = "effects_tile"
    COLLISION_TILE = "collision_tile"
    CANT_PlACE = "cant_place"
    SELECTOR = "selector"
    BULLET_OUTER = "bullet_outer"
    BULLET_INNER = "bullet_inner"
    GOAL_PATH_OUTER = "goal_path_outer"
    GOAL_PATH_INNER = "goal_path_inner"
    WAVE_TEXT = "wave_text"
    WAVE_TEXT_SHADOW = "wave_text_shadow"
    DMG_TEXT_SHADOW = "dmg_txt_shadow"
    DMG_TEXT = "dmg_txt"
    FENCE_LEFT = "fence_left"
    FENCE_TOP = "fence_top"
    PARTICLE = "particle"


class TextFontType():
    @staticmethod
    def get_font(size: int) -> pygame.font.Font:
        return pygame.font.Font(pygame.font.get_default_font(), size)


@dataclass
class Renderer:
    render_queue: list[dict[str, Any]] = field(default_factory=list)


    def _get_depth(self, col, row):
        return Map.DEPTH_LAYER[row][col]


    def update(self):
        self.render_queue.clear()


    def request_off_map_image_draw(self, renderer_type: RendererType, image, position):
        depth = ""

        match renderer_type:
            case RendererType.SUN_FLOWER_PLACEABLE:
                depth = "A0"
            case RendererType.FENCE_LEFT:
                depth = "A0"
            case RendererType.FENCE_TOP:
                depth = "A0"
            case RendererType.EFFECTS_TILE:
                depth = f"C{depth}" # This should render ontop of existing floor tiles but under enemies

        self.render_queue.append({
            'name': renderer_type,
            'type': DrawType.IMAGE,
            'image': image,
            'position': position,
            'depth': depth,
        })


    def request_on_map_image_draw(self, renderer_type: RendererType, image, position, col, row):
        depth = self._get_depth(col, row)
        match renderer_type:
            case RendererType.PLACED:
                depth = depth
            case RendererType.ENEMY:
                depth = depth
            case RendererType.SUN_FLOWER_PLACEABLE:
                depth = depth
            case RendererType.FLOOR_TILE:
                depth = f"B{depth}"
            case RendererType.EFFECTS_TILE:
                depth = f"D{depth}" # This should render ontop of existing floor tiles but under enemies
            case RendererType.COLLISION_TILE:
                depth = depth
            case _:
                raise Exception("unknown render type")

        self.render_queue.append({
            'name': renderer_type,
            'type': DrawType.IMAGE,
            'image': image,
            'position': position,
            'depth': depth,
        })


    def request_rectangle_draw(self, renderer_type: RendererType, color, rect, width):
        depth = "A"

        match renderer_type:
            case RendererType.ENEMY_HP_USED:
                depth = "xa"
            case RendererType.ENEMY_HP_REMAINING:
                depth = "xb" # Prefix with B so that used bar is drawn first
            case RendererType.DEBUG:
                depth = "z"
            case _:
                raise Exception("unknown render type")

        self.render_queue.append({
            'name': renderer_type,
            'type': DrawType.RECTANGLE,
            'color': color,
            'rect': rect,
            'width': width,
            'depth': depth,
        })


    def request_circle_draw(self, renderer_type: RendererType, color, center, radius, width):
        depth = "A"

        match renderer_type:
            case RendererType.DEBUG:
                depth = "Z"
            case RendererType.BULLET_OUTER:
                depth = "xa"
            case RendererType.BULLET_INNER:
                depth = "xb"
            case RendererType.GOAL_PATH_OUTER:
                depth = "CA" # Above tile layer B, below obstacles starting on layer D
            case RendererType.GOAL_PATH_INNER:
                depth = "CB" # Above tile layer B, below obstacles starting on layer D
            case _:
                raise Exception("unknown render type")

        self.render_queue.append({
            'name': renderer_type,
            'type': DrawType.CIRCLE,
            'color': color,
            'center': center,
            'radius': radius,
            'width': width,
            'depth': depth,
        })


    def request_circle_alpha_draw(self, renderer_type: RendererType, color, position, radius, width):
        depth = "A"

        match renderer_type:
            case RendererType.PARTICLE:
                depth = "za" # ontop of all things
            case _:
                raise Exception("unknown render type")

        self.render_queue.append({
            'name': renderer_type,
            'type': DrawType.CIRCLE_ALPHA,
            'color': color,
            'position': position,
            'radius': radius,
            'width': width,
            'depth': depth
        })


    def request_polygon_draw(self, renderer_type: RendererType, color, points, width, col = -1, row = -1):
        depth = "A"
        if col > 0 and row > 0:
            depth = self._get_depth(col, row)

        match renderer_type:
            case RendererType.DEBUG:
                depth = "Z"
            case RendererType.SELECTOR | RendererType.CANT_PlACE:
                depth = f"C{depth}" # Above tile layer, below obstacles
            case _:
                raise Exception("unknown render type")

        self.render_queue.append({
            'name': renderer_type,
            'type': DrawType.POLYGON,
            'color': color,
            'points': points,
            'width': width,
            'depth': depth,
        })


    def request_text_draw_alpha(self, renderer_type: RendererType, color: pygame.Color, text, font_type: pygame.font.Font, center_pos: pygame.Vector2):
        depth = "A"

        match renderer_type:
            case RendererType.DEBUG:
                depth = "Z"
            case RendererType.DMG_TEXT_SHADOW:
                depth = "za"
            case RendererType.DMG_TEXT:
                depth = "zb"
            case RendererType.WAVE_TEXT_SHADOW:
                depth = "zy"
            case RendererType.WAVE_TEXT:
                depth = "zz"
            case _:
                raise Exception("unknown render type")

        self.render_queue.append({
            'name': renderer_type,
            'type': DrawType.TEXT,
            'color': color,
            'text': text,
            'font_type': font_type,
            'center_pos': center_pos,
            'depth': depth,
        })


    def request_text_draw(self, renderer_type: RendererType, color: str, text, font_type: pygame.font.Font, center_pos: pygame.Vector2):
        self.request_text_draw_alpha(
            renderer_type,
            pygame.Color(color),
            text,
            font_type,
            center_pos)


    def draw_text(self, screen, font, color, text, text_position):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=(text_position[0], text_position[1]))
        screen.blit(text_surface, text_rect)


    def draw(self, screen: pygame.Surface):
        # Sort render queue by depth
        self.render_queue.sort(key=lambda item: item['depth'])

        # TODO: Review if moving from upper to lower depth needs custom sort. e.g. Z to a
        #self.render_queue.sort(key=lambda item: (item['depth'].lower(), item['depth'].islower()))

        # Draw all items in order
        for item in self.render_queue:
            if item['type'] == DrawType.IMAGE:
                screen.blit(item['image'], item['position'])
            elif item['type'] == DrawType.RECTANGLE:
                pygame.draw.rect(screen, item['color'], item['rect'], item['width'])
            elif item['type'] == DrawType.CIRCLE:
                pygame.draw.circle(screen, item['color'], item['center'], item['radius'], item['width'])
            elif item['type'] == DrawType.CIRCLE_ALPHA:
                self.draw_alpha_circle(screen, item)
            elif item['type'] == DrawType.POLYGON:
                pygame.draw.polygon(screen, item['color'], item['points'], item['width'])
            elif item['type'] == DrawType.TEXT:
                font: pygame.font.Font = item['font_type']
                text_surface = font.render(item["text"], True, item["color"])
                text_surface.set_alpha(item["color"].a)
                text_rect = text_surface.get_rect(center=(item["center_pos"].x, item["center_pos"].y))
                screen.blit(text_surface, text_rect)

    def draw_alpha_circle(self, screen: pygame.Surface, item):
        size = item['radius']
        position = item['position']
        color = item['color']

        # Create a temporary surface with per-pixel alpha
        circle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        circle_surface = circle_surface.convert_alpha()  # Ensure it supports per-pixel alpha

        # Draw the circle on the temporary surface
        pygame.draw.circle(
            circle_surface,
            color,
            (size, size),  # Center of the surface
            size
        )

        # Blit the temporary surface onto the main screen at the correct position
        screen.blit(circle_surface, (position.x - size, position.y - size))
