"""
Starflight Remake - Main Entry Point
"""
import pygame
import sys
from core.input_handler import InputHandler
from core.screen_manager import ScreenManager
from ui.screens.main_menu_screen import MainMenuScreen


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

    # Create and register screens
    main_menu = MainMenuScreen(screen_manager)
    screen_manager.add_screen("main_menu", main_menu)

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
