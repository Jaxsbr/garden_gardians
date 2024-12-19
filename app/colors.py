import pygame

# Background colors (already correct)
BACKGROUND_COLOR_MENU = pygame.Color(150, 50, 250, 255)  # Bright, cheerful purple
BACKGROUND_COLOR_GAME_OVER_WIN = pygame.Color(50, 220, 100, 255)  # Vibrant green for a happy win
BACKGROUND_COLOR_GAME_OVER_LOSE = pygame.Color(255, 80, 80, 255)  # Bright, warm red for a softer "lose" tone

# Text colors (light contrast or complementary for readability)
TEXT_COLOR_MENU = pygame.Color(230, 230, 255, 255)  # Light lavender to complement purple
TEXT_COLOR_GAME_OVER_WIN = pygame.Color(245, 255, 245, 255)  # Very light green for soft contrast with vibrant green
TEXT_COLOR_GAME_OVER_LOSE = pygame.Color(255, 240, 240, 255)  # Pale pink to soften the contrast with red

# Focus colors (vibrant contrast for emphasis)
FOCUS_COLOR_MENU = pygame.Color(255, 200, 50, 255)  # Bright orange-yellow for a strong pop against purple
FOCUS_COLOR_GAME_OVER_WIN = pygame.Color(255, 255, 50, 255)  # Bright yellow for vibrant contrast with green
FOCUS_COLOR_GAME_OVER_LOSE = pygame.Color(255, 255, 150, 255)  # Bright pastel yellow to contrast with red
