"""
Starflight Remake - Main Entry Point
"""
import pygame
import sys
import json
from pathlib import Path
from ui.menu_renderer import MenuRenderer


# Display constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def load_menu_data(menu_file):
    """Load menu configuration from JSON file"""
    menu_path = Path(__file__).parent / "data" / "static" / "menu" / menu_file
    with open(menu_path, 'r') as f:
        return json.load(f)


def main():
    """Main game loop"""
    # Initialize Pygame
    pygame.init()

    # Create resizable display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Starflight Remake")

    # Track current screen dimensions
    current_width = SCREEN_WIDTH
    current_height = SCREEN_HEIGHT

    # Clock for frame rate
    clock = pygame.time.Clock()

    # Load menu data
    menu_data = load_menu_data("main_menu.json")
    menu_title = menu_data["title"]
    menu_options = menu_data["options"]

    # Build menu option labels and disabled set
    option_labels = [opt["label"] for opt in menu_options]
    disabled_menu_items = {i for i, opt in enumerate(menu_options) if not opt["enabled"]}

    # Initialize menu
    menu_renderer = MenuRenderer()
    selected_menu_index = 0

    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Menu navigation - W/Up/Numpad8 = up, S/Down/Numpad2 = down
                elif event.key in (pygame.K_w, pygame.K_UP, pygame.K_KP8):
                    selected_menu_index = (selected_menu_index - 1) % len(option_labels)
                elif event.key in (pygame.K_s, pygame.K_DOWN, pygame.K_KP2):
                    selected_menu_index = (selected_menu_index + 1) % len(option_labels)
                # Menu selection - Enter or Space
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if selected_menu_index not in disabled_menu_items:
                        selected_option_id = menu_options[selected_menu_index]["id"]
                        if selected_option_id == "new_game":
                            print("New Game selected - TODO: implement")
                        elif selected_option_id == "exit_game":
                            running = False
            elif event.type == pygame.VIDEORESIZE:
                # Handle window resize
                current_width = event.w
                current_height = event.h
                screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)

        # Clear screen
        screen.fill(BLACK)

        # Render menu
        menu_renderer.render(
            screen,
            menu_title,
            option_labels,
            selected_menu_index,
            disabled_menu_items
        )

        # Update display
        pygame.display.flip()

        # Maintain frame rate
        clock.tick(FPS)

    # Cleanup
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
