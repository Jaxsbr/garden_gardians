from dataclasses import dataclass, field
import pygame

from renderer import Renderer, RendererType


class Particle:
    def __init__(self, position: pygame.Vector2, ttl: float, direction: pygame.Vector2, speed: float, size: float, color: pygame.Color, has_gravity: bool, gravity: float = 9.8):
        self.position = pygame.Vector2(0, 0)
        self.reset(position, ttl, direction, speed, size, color, has_gravity, gravity)


    def reset(self, position: pygame.Vector2, ttl: float, direction: pygame.Vector2, speed: float, size: float, color: pygame.Color, has_gravity: bool, gravity: float = 9.8):
        self.position.x = position.x
        self.position.y = position.y
        self.ttl = ttl
        self.original_ttl = ttl
        self.direction = direction
        self.speed = speed
        self.size = size
        self.color = pygame.Color(color.r, color.g, color.b, color.a)
        self.has_gravity = has_gravity
        self.velocity = self.direction * self.speed
        self.gravity = gravity


    def is_expired(self):
        return self.ttl < 0


    def update(self, dt):
        if self.is_expired():
            return

        self.ttl -= 1 * dt

        if self.has_gravity:
            self.velocity.x = self.direction.x * self.speed
            self.velocity.y += self.gravity
        else:
            self.velocity = self.direction * self.speed

        self.position += self.velocity * dt

        # Calculate the opacity based on the remaining TTL
        alpha = max(0, int(255 * (self.ttl / self.original_ttl)))
        self.color.a = alpha


    def draw(self, screen):
        if self.is_expired():
            return

        # Create a temporary surface with per-pixel alpha
        circle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        circle_surface = circle_surface.convert_alpha()  # Ensure it supports per-pixel alpha

        # Draw the circle on the temporary surface
        pygame.draw.circle(
            circle_surface,
            self.color,
            (self.size, self.size),  # Center of the surface
            self.size
        )

        # Blit the temporary surface onto the main screen at the correct position
        screen.blit(circle_surface, (self.position.x - self.size, self.position.y - self.size))


    def render(self, renderer: Renderer):
        if self.is_expired():
            return

        renderer.request_circle_alpha_draw(
            RendererType.PARTICLE,
            self.color,
            pygame.Vector2(self.position.x - self.size, self.position.y - self.size),
            self.size,
            0
        )


@dataclass
class ParticleEngine:
    particles: list[Particle] = field(default_factory=list)
    use_renderer: bool = field(default=False)

    def emit_particle(self, particle: Particle):
        self.emit(
            particle.position,
            particle.ttl,
            particle.direction,
            particle.speed,
            particle.size,
            particle.color,
            particle.has_gravity)


    def emit(self, position: pygame.Vector2, ttl: float, direction: pygame.Vector2, speed: float, size: float, color: pygame.Color, has_gravity: bool = False):
        for p in self.particles:
            if p.is_expired():
                p.reset(position, ttl, direction, speed, size, color, has_gravity)
                return p

        particle = Particle(position, ttl, direction, speed, size, color, has_gravity)
        self.particles.append(particle)
        return particle


    def reset(self):
        self.particles.clear()


    def update(self, dt):
        for p in self.particles:
            p.update(dt)


    def draw(self, screen, renderer: Renderer | None = None):
        for p in self.particles:
            if self.use_renderer and renderer:
                p.render(renderer)
            else:
                p.draw(screen)
