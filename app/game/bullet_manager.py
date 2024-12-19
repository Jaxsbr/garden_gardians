from dataclasses import dataclass, field
import pygame

from renderer import Renderer, RendererType
from constants import Constants
from events import Event, GlobalEventDispatcher


@dataclass
class BulletConfig:
    damage: int
    effect: str


class Bullet:
    def __init__(self, color, ttl, speed, size, position, direction, bullet_config):
        self.reset(color, ttl, speed, size, position, direction, bullet_config)


    def reset(self, color, ttl, speed, size, position, direction, bullet_config):
        self.color: str = color
        self.ttl: float = ttl
        self.speed: float = bullet_config["speed"]
        self.size: float = size
        self.position: pygame.Vector2 = position
        self.direction: pygame.Vector2 = direction
        self.bullet_config = bullet_config


    def update(self, dt):
        self.ttl -= 1 * dt
        if self.ttl <= 0:
            return

        normalized_direction = self.direction.normalize()
        move_speed = self.speed * dt
        velocity = normalized_direction * move_speed
        self.position.x += velocity.x
        self.position.y += velocity.y


    def draw(self, renderer: Renderer):
        if self.ttl <= 0:
            return

        # outline
        renderer.request_circle_draw(
            RendererType.BULLET_OUTER,
            "black",
            self.position,
            self.size * 1.5,
            0)

        # inner
        renderer.request_circle_draw(
            RendererType.BULLET_INNER,
            self.color,
            self.position,
            self.size,
            0)


@dataclass
class BulletManager:
    bullets: list[Bullet] = field(default_factory=list)

    def __post_init__(self):
        GlobalEventDispatcher.register_listener(self, "BulletManager")


    def _rect_contains_circle(self, rect, circle_center, circle_radius):
        # Unpack circle center
        cx, cy = circle_center

        # Check if the circle is within the rectangle bounds
        return (
            rect.left <= cx - circle_radius and  # Circle's leftmost point is inside
            rect.right >= cx + circle_radius and  # Circle's rightmost point is inside
            rect.top <= cy - circle_radius and  # Circle's topmost point is inside
            rect.bottom >= cy + circle_radius   # Circle's bottommost point is inside
        )


    def on_event(self, event: Event):
        if event.event_name == Constants.EVENT_SHOOT_BULLET:
            self.shoot(event.args["position"], event.args["target_pos"], event.args["bullet_config"])


    def shoot(self, position, target_pos, bullet_config):
        direction = target_pos - position
        if direction.x == 0 and direction.y == 0:
            return

        for bullet in self.bullets:
            if bullet.ttl < 0:
                bullet.reset(
                    bullet_config["color"],
                    Constants.BULLET_TTL,
                    Constants.BULLET_SPEED,
                    Constants.BULLET_SIZE,
                    position,
                    direction,
                    bullet_config)
                return

        bullet = Bullet(
            bullet_config["color"],
            Constants.BULLET_TTL,
            Constants.BULLET_SPEED,
            Constants.BULLET_SIZE,
            position,
            direction,
            bullet_config)
        self.bullets.append(bullet)


    def get_collisions(self, rect: pygame.Rect) -> Bullet | None:
        filtered_bullets = [bullet for bullet in self.bullets if bullet.ttl > 0]
        for bullet in filtered_bullets:
            if self._rect_contains_circle(rect, bullet.position, bullet.size):
                bullet.ttl = 0 # Deactivate bullet
                return bullet
        return None


    def update(self, dt):
        for bullet in self.bullets:
            bullet.update(dt)


    def draw(self, renderer: Renderer):
        for bullet in self.bullets:
            bullet.draw(renderer)

