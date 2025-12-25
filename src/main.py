"""
Starflight Remake - Main Entry Point
"""
import pygame
import sys
from core.state_manager import StateManager
from core.colors import BLACK
from states.main_menu_state import MainMenuState
from states.starport_menu_state import StarportMenuState
from states.space_navigation_state import SpaceNavigationState


# Display constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60


def main():
    """Main game loop"""
    # Initialize Pygame
    pygame.init()

    # Create resizable display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Starflight Remake")

    # Clock for frame rate
    clock = pygame.time.Clock()

    # Initialize state manager
    state_manager = StateManager()

    # Register game states
    state_manager.register_state("main_menu", MainMenuState(state_manager))
    state_manager.register_state("starport", StarportMenuState(state_manager))
    state_manager.register_state("space_navigation", SpaceNavigationState(state_manager))

    # Start with main menu
    state_manager.change_state("main_menu")

    # Main game loop
    running = True
    while running:
        # Calculate delta time
        dt = clock.tick(FPS) / 1000.0  # Convert to seconds

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.VIDEORESIZE:
                # Handle window resize
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            # Pass event to current state
            current_state = state_manager.get_current_state()
            if current_state:
                current_state.handle_event(event)

        # Update current state
        current_state = state_manager.get_current_state()
        if current_state:
            current_state.update(dt)

        # Clear screen
        screen.fill(BLACK)

        # Render current state
        if current_state:
            current_state.render(screen)

        # Update display
        pygame.display.flip()

    # Cleanup
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
