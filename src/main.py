"""
Starflight Remake - Main Entry Point
"""
import pygame
import sys
from core.input_handler import InputHandler
from core.screen_manager import ScreenManager
from core.game_state import GameState
from ui.screens.main_menu_screen import MainMenuScreen
from ui.screens.starport_screen import StarportScreen
from ui.screens.space_screen import SpaceScreen
from ui.screens.orbit_screen import OrbitScreen


def main():
    """Main game entry point"""
    # Initialize Pygame
    pygame.init()

    # Game configuration
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    FPS = 60

    # Create game window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Starflight Remake")
    clock = pygame.time.Clock()

    # Initialize systems
    input_handler = InputHandler()
    screen_manager = ScreenManager()
    game_state = GameState()

    # Create and register screens
    main_menu = MainMenuScreen(screen_manager, game_state)
    starport = StarportScreen(screen_manager, game_state)
    space = SpaceScreen(screen_manager, game_state)
    orbit = OrbitScreen(screen_manager, game_state)

    screen_manager.add_screen("main_menu", main_menu)
    screen_manager.add_screen("starport", starport)
    screen_manager.add_screen("space", space)
    screen_manager.add_screen("orbit", orbit)

    # Start with main menu
    screen_manager.change_screen("main_menu")

    # Main game loop
    running = True
    while running:
        # Calculate delta time
        delta_time = clock.tick(FPS) / 1000.0  # Convert to seconds

        # Collect events
        events = pygame.event.get()

        # Handle quit events
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Let screens handle ESC, or quit if at main menu
                    if screen_manager.current_screen == main_menu:
                        running = False

        # Update input
        input_handler.update(events)

        # Update current screen
        screen_manager.update(delta_time, input_handler)

        # Render current screen
        screen_manager.render(screen)

        # Update display
        pygame.display.flip()

    # Cleanup
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
