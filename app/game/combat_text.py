from dataclasses import dataclass, field
from enum import Enum

import pygame

from events import Event, GlobalEventDispatcher
from constants import Constants
from renderer import Renderer, RendererType, TextFontType

class CombatTextType(Enum):
    DAMAGE = "damage"
    ENERGY_ADD = "energy_add"
    ENERGY_REMOVE = "energy_remove"
    FREEZE = "freeze_effect"


@dataclass
class CombatText:
    combat_text_type: CombatTextType
    text: str
    position: pygame.Vector2
    direction: pygame.Vector2
    move_speed: float
    ttl: float
    color: str | pygame.Color
    font_size: int

    def __post_init__(self):
        self.reset()


    def reset(self):
        self.original_ttl = self.ttl
        self.color_obj = pygame.Color(self.color)
        self.color_black_obj = pygame.Color("black")


    def update(self, dt):
        if self.ttl <= 0:
            return

        self.ttl -= 1 * dt
        self.position.x += self.direction.x * (dt * self.move_speed)
        self.position.y += self.direction.y * (dt * self.move_speed)
        self.shadow_pos = self.position.copy()
        self.shadow_pos.x += 1.5
        self.shadow_pos.y += 1.5

        alpha = max(0, int(255 * (self.ttl / self.original_ttl)))
        self.color_obj.a = alpha
        self.color_black_obj.a = alpha


    def draw(self, renderer: Renderer):
        if self.ttl <= 0:
            return

        font = TextFontType.get_font(self.font_size)

        renderer.request_text_draw_alpha(
            RendererType.DMG_TEXT_SHADOW,
            self.color_black_obj,
            self.text,
            font,
            self.shadow_pos)

        renderer.request_text_draw_alpha(
            RendererType.DMG_TEXT,
            self.color_obj,
            self.text,
            font,
            self.position)


@dataclass
class CombatTextEngine:
    texts: list[CombatText] = field(default_factory=list)

    def __post_init__(self):
        GlobalEventDispatcher.register_listener(self, "CombatTextEngine")


    def on_event(self, event: Event) -> bool:
        if event.event_name == Constants.EVENT_ADD_COMBAT_TEXT:
            self._add_text(event.args["combat_text"])
            return True
        return False


    def _add_text(self, combat_text):
        for txt in self.texts:
            if txt.ttl <= 0:
                txt.combat_text_type = combat_text.combat_text_type
                txt.text = combat_text.text
                txt.direction = combat_text.direction
                txt.ttl = combat_text.ttl
                txt.move_speed = combat_text.move_speed
                txt.position = combat_text.position
                txt.color = combat_text.color
                txt.font_size = combat_text.font_size
                txt.reset()
                return txt

        txt = combat_text
        self.texts.append(txt)
        return txt


    def update(self, dt):
        for txt in self.texts:
            txt.update(dt)


    def draw(self, renderer: Renderer):
        for txt in self.texts:
            txt.draw(renderer)
