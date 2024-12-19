from dataclasses import dataclass, field
import math
import random
from typing import Optional

import pygame

from particle_engine import ParticleEngine
from custom_types.int_vector2 import IntVector2
from renderer import TextFontType
from events import Event, GlobalEventDispatcher


@dataclass
class GUIButton:
    action_event_name: str
    button_text: str
    focused: bool = field(default=False)

    def invoke_action(self):
        GlobalEventDispatcher.dispatch(Event(self.action_event_name))


@dataclass
class GUI:
    bounds: pygame.Rect
    buttons: list[GUIButton]
    title_text: Optional[str] = ""
    text_color: Optional[pygame.Color] = None
    focus_color: Optional[pygame.Color] = None
    background_color: Optional[pygame.Color] = None
    particle_engine: ParticleEngine = field(init=False)
    enabled: bool = field(default=True)
    COLOR_GRAY = pygame.Color(190, 190, 190, 255)
    COLOR_WHITE = pygame.Color(255, 255, 255, 255)

    def __post_init__(self):
        self.particle_engine = ParticleEngine()
        self.font_normal = TextFontType.get_font(32)
        self.font_focused = TextFontType.get_font(36)
        self.center = pygame.Vector2(
            self.bounds.width / 2, self.bounds.height / 2)

        self.button_size = IntVector2(200, 75)
        total_button_height = 0
        self.offset = 10
        for _ in self.buttons:
            total_button_height += self.button_size.y + self.offset

        self.layout_y_start = self.center.y - total_button_height / 2
        self.layout_x = self.center.x - self.button_size.x / 2

        self.keyboard_focused_button_index = -1
        self.elapsed_keyboard_check = 0
        self.tick_keyboard_check = 0.06
        self.previous_pressed_key = pygame.key.get_pressed()


    def check_index(self):
        if self.keyboard_focused_button_index > len(self.buttons) - 1:
            self.keyboard_focused_button_index = 0

        if self.keyboard_focused_button_index < 0:
            self.keyboard_focused_button_index = len(self.buttons) - 1


    def update(self, dt):
        self.particle_engine.update(dt)

        do_action = False
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYUP:
                if self.previous_pressed_key[pygame.K_UP] and not keys[pygame.K_UP]:
                    self.keyboard_focused_button_index -= 1
                if self.previous_pressed_key[pygame.K_DOWN] and not keys[pygame.K_DOWN]:
                    self.keyboard_focused_button_index += 1
                if self.previous_pressed_key[pygame.K_RETURN] and not keys[pygame.K_RETURN]:
                    do_action = True
                self.check_index()
            self.previous_pressed_key = keys


        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        current_y = self.layout_y_start
        for button in self.buttons:
            rect = pygame.Rect(
                self.layout_x,
                current_y,
                self.button_size.x,
                self.button_size.y)
            keyboard_focused = self.keyboard_focused_button_index != -1 and self.buttons[self.keyboard_focused_button_index] == button
            is_over = rect.collidepoint(mouse_pos[0], mouse_pos[1])
            button.focused = is_over or keyboard_focused
            current_y += self.button_size.y + self.offset

            if is_over:
                self.keyboard_focused_button_index = -1

            if (mouse_clicked or do_action) and (is_over or keyboard_focused) and self.enabled:
                button.invoke_action()
            elif (not mouse_clicked and is_over) or (keyboard_focused):
                self._update_focused_effect(rect)


    def _update_focused_effect(self, rect: pygame.Rect):
        angle = random.choice(range(0, 361, 6))
        radians = math.radians(angle)
        ttl = random.choice([0.7, 0.9, 1.3])
        direction = pygame.Vector2(math.cos(radians), math.sin(radians))
        speed = random.choice([75, 100, 150])
        size = random.choice([2, 3, 4])
        color = pygame.Color(255, 255, 255, 255)

        self.particle_engine.emit(
            pygame.Vector2(rect.center[0], rect.center[1]),
            ttl,
            direction,
            speed,
            size,
            color,
            False)


    def draw(self, screen: pygame.Surface):
        if self.background_color:
            screen.fill(self.background_color)

        self.particle_engine.draw(screen)
        self._draw_title(screen)
        self._draw_buttons(screen)


    def _draw_title(self, screen: pygame.Surface):
        if self.title_text == "":
            return

        color = (self.text_color if self.text_color is not None else GUI.COLOR_GRAY)

        text_surface = self.font_normal.render(
            self.title_text,
            True,
            color)

        text_rect = text_surface.get_rect(topleft=(
            self.bounds.x + self.offset,
            self.bounds.y + self.offset
        ))

        screen.blit(text_surface, text_rect)


    def _draw_buttons(self, screen: pygame.Surface):
        focus_color = (self.focus_color if self.focus_color is not None else GUI.COLOR_WHITE)
        color = (self.text_color if self.text_color is not None else GUI.COLOR_GRAY)
        current_y = self.layout_y_start
        for button in self.buttons:
            font = (self.font_focused if button.focused else self.font_normal)

            text_surface = font.render(
                button.button_text,
                True,
                (focus_color if button.focused else color))

            text_rect = text_surface.get_rect(center=(
                self.layout_x + self.button_size.x / 2,
                current_y + self.button_size.y / 2,
            ))

            screen.blit(text_surface, text_rect)

            current_y += self.button_size.y + self.offset
