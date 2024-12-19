import math
import random
import pygame
from particle_engine import Particle


def get_freeze_particle(x_pos: float, y_pos: float) -> Particle:
    angle = random.choice(range(0, 361, 6))
    radians = math.radians(angle)
    ttl = random.choice([0.2, 0.4, 0.5])
    direction = pygame.Vector2(math.cos(radians), math.sin(radians))
    speed = random.choice([70, 90, 150])
    size = random.choice([3, 4, 5, 6])
    color = random.choice([
        pygame.Color(0, 51, 102, 255),    # Dark Blue
        pygame.Color(0, 76, 153, 255),    # Deep Ice Blue
        pygame.Color(25, 25, 112, 255),   # Midnight Blue
        pygame.Color(0, 102, 153, 255),   # Steel Blue
        pygame.Color(0, 128, 128, 255),   # Teal
        pygame.Color(16, 52, 166, 255),   # Iceberg Blue
        pygame.Color(0, 51, 102, 180),    # Dark Blue with Transparency
        pygame.Color(10, 75, 125, 220)    # Frosted Blue
    ])
    gravity = 0.1
    return Particle(pygame.Vector2(x_pos, y_pos), ttl, direction, speed, size, color, True, gravity)


def get_death_particle(x_pos: float, y_pos: float, base_color: pygame.Color) -> Particle:
    angle = random.choice(range(0, 361, 6))
    radians = math.radians(angle)
    ttl = random.choice([0.2, 0.3, 0.4])
    direction = pygame.Vector2(math.cos(radians), math.sin(radians))
    speed = random.randint(200, 300)
    size = random.randint(2, 7)
    # Generate a range of colors based on the base color
    color = random.choice(generate_color_range(base_color))
    return Particle(pygame.Vector2(x_pos, y_pos), ttl, direction, speed, size, color, False)


def generate_color_range(base_color: pygame.Color, num_variations: int = 8) -> list:
    """
    Generate a range of colors based on the input color by adjusting brightness and saturation.

    :param base_color: The input color (pygame.Color).
    :param num_variations: Number of color variations to generate.
    :return: List of pygame.Color objects.
    """
    print(f"base_color: {base_color}")
    # Convert the base color to HSV (Hue, Saturation, Value)
    base_hsv = pygame.Color(base_color.r, base_color.g, base_color.b, base_color.a).hsva
    base_hue, base_sat, base_val, base_alpha = base_hsv

    colors = []
    for _ in range(num_variations):
        # Slightly vary hue, saturation, and value
        hue = (base_hue + random.uniform(-10, 10)) % 360  # Keep hue within 0-360
        saturation = max(0, min(100, base_sat + random.uniform(-20, 20)))  # Clamp between 0 and 100
        value = max(0, min(100, base_val + random.uniform(-20, 20)))  # Clamp between 0 and 100
        color = pygame.Color(0, 0, 0, int(base_alpha))  # Initialize a new color
        color.hsva = (hue, saturation, value, base_alpha)  # Set modified HSV values
        colors.append(color)

    # Extra base colors
    colors.extend([
        pygame.Color(255, 105, 180),  # Hot Pink
        pygame.Color(135, 206, 250),  # Light Sky Blue
        pygame.Color(255, 223, 0),    # Bright Yellow
        pygame.Color(50, 205, 50),    # Lime Green
        pygame.Color(255, 69, 0),     # Red-Orange
        pygame.Color(75, 0, 130),     # Indigo
        pygame.Color(255, 182, 193),  # Light Pink
        pygame.Color(240, 230, 140),  # Khaki
        pygame.Color(173, 216, 230),  # Light Blue
        pygame.Color(128, 0, 128)])    # Purple

    return colors

