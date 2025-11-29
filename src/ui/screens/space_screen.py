"""
Space screen (placeholder)
Will be expanded in Phase 2 with actual navigation
"""
import pygame
from core.screen_manager import Screen


class SpaceScreen(Screen):
    """Placeholder space navigation screen"""

    def __init__(self, screen_manager, game_state):
        super().__init__(screen_manager)
        self.game_state = game_state

    def on_enter(self):
        """Called when entering space"""
        print("Entered space")

    def update(self, delta_time, input_handler):
        """Update space screen"""
        # For now, just allow returning to starport
        if input_handler.is_key_just_pressed(pygame.K_r):
            if self.game_state.return_to_starport():
                print("Returning to starport")
                self.screen_manager.change_screen("starport")

    def render(self, screen):
        """Render space screen"""
        from ui.renderer import Renderer
        renderer = Renderer(screen)
        width, height = screen.get_size()

        # Clear to black (space!)
        renderer.clear((0, 0, 0))

        # Title
        renderer.draw_text_centered(
            "IN SPACE",
            width // 2,
            height // 4,
            color=(100, 150, 255),
            font=renderer.large_font
        )

        # Status
        status = self.game_state.get_status_summary()
        y_start = height // 2 - 40
        renderer.draw_text_centered(
            f"Fuel: {status['fuel']}",
            width // 2,
            y_start,
            color=(200, 200, 200)
        )
        renderer.draw_text_centered(
            f"Credits: {status['credits']}",
            width // 2,
            y_start + 40,
            color=(200, 200, 200)
        )
        renderer.draw_text_centered(
            f"Cargo: {status['cargo']}",
            width // 2,
            y_start + 80,
            color=(200, 200, 200)
        )

        # Placeholder message
        renderer.draw_text_centered(
            "Space navigation coming in Phase 2!",
            width // 2,
            height - 100,
            color=(150, 150, 150),
            font=renderer.small_font
        )

        # Instructions
        renderer.draw_text_centered(
            "Press R to return to starport",
            width // 2,
            height - 50,
            color=(255, 255, 0),
            font=renderer.small_font
        )
