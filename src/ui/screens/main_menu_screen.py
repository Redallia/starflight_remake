"""
Main menu screen
"""
import pygame
from core.screen_manager import Screen


class MainMenuScreen(Screen):
    """Simple main menu"""

    def __init__(self, screen_manager, game_state):
        super().__init__(screen_manager)
        self.game_state = game_state
        self.title = "STARFLIGHT REMAKE"
        self.options = ["New Game", "Load Game", "Quit"]
        self.selected_index = 0

    def on_enter(self):
        """Called when entering this screen"""
        print("Entered main menu")

    def update(self, delta_time, input_handler):
        """Update menu logic"""
        # Navigate menu with W/S
        if input_handler.is_key_just_pressed(pygame.K_w):
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif input_handler.is_key_just_pressed(pygame.K_s):
            self.selected_index = (self.selected_index + 1) % len(self.options)

        # Select option with Enter/Space
        if input_handler.is_confirm_pressed():
            self._handle_selection()

    def render(self, screen):
        """Render the menu"""
        width, height = screen.get_size()

        # Get renderer (we'll pass this properly later)
        from ui.renderer import Renderer
        renderer = Renderer(screen)

        # Clear screen
        renderer.clear((0, 0, 20))  # Dark blue

        # Draw title
        renderer.draw_text_centered(
            self.title,
            width // 2,
            height // 4,
            color=(100, 200, 255),
            font=renderer.large_font
        )

        # Draw menu options
        for i, option in enumerate(self.options):
            y_pos = height // 2 + i * 40
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            prefix = "> " if i == self.selected_index else "  "
            renderer.draw_text_centered(
                prefix + option,
                width // 2,
                y_pos,
                color=color
            )

        # Draw instructions
        renderer.draw_text_centered(
            "W/S to navigate, Enter to select, ESC to quit",
            width // 2,
            height - 50,
            color=(150, 150, 150),
            font=renderer.small_font
        )

    def _handle_selection(self):
        """Handle menu selection"""
        option = self.options[self.selected_index]
        if option == "Quit":
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif option == "New Game":
            print("Starting new game!")
            # Reset game state to new game
            from core.game_state import GameState
            new_state = GameState()
            # Copy new state into existing game_state object
            self.game_state.__dict__.update(new_state.__dict__)
            # Go to starport
            self.screen_manager.change_screen("starport")
        elif option == "Load Game":
            print("Load Game selected (not implemented yet)")
