import random
import pygame
from game.combat_text import CombatText, CombatTextType
from constants import Constants


@staticmethod
def _get_move_speed(combat_text_type: CombatTextType) -> float:
    if combat_text_type == CombatTextType.DAMAGE:
        return Constants.COMBAT_TEXT_ENEMY_DAMAGE_MOVE_SPEED
    elif (combat_text_type == CombatTextType.ENERGY_ADD
        or combat_text_type == CombatTextType.ENERGY_REMOVE):
            return Constants.COMBAT_TEXT_ENERGY_MOVE_SPEED
    elif combat_text_type == CombatTextType.FREEZE:
         return Constants.COMBAT_TEXT_FREEZE_SPEED
    raise Exception(f"invalid combat text type: {combat_text_type}")


@staticmethod
def _get_color(combat_text_type: CombatTextType) -> pygame.Color | str:
    if combat_text_type == CombatTextType.DAMAGE:
        return random.choice(Constants.COMBAT_TEXT_ENEMY_DAMAGE_COLORS)
    elif (combat_text_type == CombatTextType.ENERGY_ADD
        or combat_text_type == CombatTextType.ENERGY_REMOVE):
            return random.choice(Constants.COMBAT_TEXT_ENERGY_REDUCED_COLORS)
    elif combat_text_type == CombatTextType.FREEZE:
         return Constants.COMBAT_TEXT_FREEZE_COLORS[0]
    raise Exception(f"invalid combat text type: {combat_text_type}")


@staticmethod
def _get_ttl(combat_text_type: CombatTextType) -> float:
    if combat_text_type == CombatTextType.DAMAGE:
        return Constants.COMBAT_TEXT_ENEMY_DAMAGE_TTL
    elif (combat_text_type == CombatTextType.ENERGY_ADD
        or combat_text_type == CombatTextType.ENERGY_REMOVE):
            return Constants.COMBAT_TEXT_ENERGY_TTL
    elif combat_text_type == CombatTextType.FREEZE:
         return Constants.COMBAT_TEXT_FREEZE_TTL
    raise Exception(f"invalid combat text type: {combat_text_type}")


@staticmethod
def _get_font_size(combat_text_type: CombatTextType) -> int:
    if combat_text_type == CombatTextType.DAMAGE:
        return 24
    elif (combat_text_type == CombatTextType.ENERGY_ADD
        or combat_text_type == CombatTextType.ENERGY_REMOVE):
         return 48
    elif combat_text_type == CombatTextType.FREEZE:
        return 32
    raise Exception(f"invalid combat text type: {combat_text_type}")

@staticmethod
def _get_direction(combat_text_type: CombatTextType) -> pygame.Vector2:
    if combat_text_type == CombatTextType.DAMAGE:
        return pygame.Vector2(random.randint(-1, 1), -1)
    elif combat_text_type == CombatTextType.ENERGY_ADD:
         return pygame.Vector2(0, -1) # TODO: direction to total energy
    elif combat_text_type == CombatTextType.ENERGY_REMOVE:
            return pygame.Vector2(0, -1) # TODO: from total downwards/ place pos
    elif combat_text_type == CombatTextType.FREEZE:
        return pygame.Vector2(0, -1)
    raise Exception(f"invalid combat text type: {combat_text_type}")


@staticmethod
def get_combat_text(combat_text_type: CombatTextType, text: str, position: pygame.Vector2) -> CombatText:
    clr = _get_color(combat_text_type)
    ttl = _get_ttl(combat_text_type)
    move_speed = _get_move_speed(combat_text_type)
    font_size = _get_font_size(combat_text_type)
    direction = _get_direction(combat_text_type)

    return CombatText(
        combat_text_type,
        text,
        position,
        direction,
        move_speed,
        ttl,
        clr,
        font_size
    )
