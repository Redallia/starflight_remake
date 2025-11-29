"""
Starport screen
Main hub where player manages ship and launches into space
"""
import pygame
from core.screen_manager import Screen


class StarportScreen(Screen):
    """Starport interface"""

    def __init__(self, screen_manager, game_state):
        super().__init__(screen_manager)
        self.game_state = game_state
        self.options = ["View Ship Status", "Launch to Space", "Exit to Main Menu"]
        self.selected_index = 0
        self.viewing_status = False

    def on_enter(self):
        """Called when entering starport"""
        print("Arrived at starport")
        self.viewing_status = False
        self.selected_index = 0

    def update(self, delta_time, input_handler):
        """Update starport logic"""
        if self.viewing_status:
            # In status view, any key returns to menu
            if input_handler.is_confirm_pressed() or input_handler.is_cancel_pressed():
                self.viewing_status = False
        else:
            # Navigate menu
            if input_handler.is_key_just_pressed(pygame.K_w):
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif input_handler.is_key_just_pressed(pygame.K_s):
                self.selected_index = (self.selected_index + 1) % len(self.options)

            # Select option
            if input_handler.is_confirm_pressed():
                self._handle_selection()

    def render(self, screen):
        """Render starport screen"""
        from ui.renderer import Renderer
        renderer = Renderer(screen)
        width, height = screen.get_size()

        # Clear screen
        renderer.clear((10, 10, 30))  # Darker blue

        if self.viewing_status:
            self._render_status_view(renderer, width, height)
        else:
            self._render_menu(renderer, width, height)

    def _render_menu(self, renderer, width, height):
        """Render the main menu"""
        # Title
        renderer.draw_text_centered(
            "STARPORT",
            width // 2,
            height // 4,
            color=(150, 200, 255),
            font=renderer.large_font
        )

        # Quick status display
        status = self.game_state.get_status_summary()
        y_offset = height // 3
        renderer.draw_text_centered(
            f"Fuel: {status['fuel']}  |  Credits: {status['credits']}  |  Cargo: {status['cargo']}",
            width // 2,
            y_offset,
            color=(200, 200, 200),
            font=renderer.small_font
        )

        # Menu options
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

        # Instructions
        renderer.draw_text_centered(
            "W/S to navigate, Enter to select",
            width // 2,
            height - 50,
            color=(150, 150, 150),
            font=renderer.small_font
        )

    def _render_status_view(self, renderer, width, height):
        """Render detailed status view"""
        renderer.draw_text_centered(
            "SHIP STATUS",
            width // 2,
            height // 6,
            color=(150, 200, 255),
            font=renderer.large_font
        )

        status = self.game_state.get_status_summary()
        y_start = height // 3

        # Display each status item
        renderer.draw_text(f"Fuel:     {status['fuel']}", width // 3, y_start, color=(200, 200, 200))
        renderer.draw_text(f"Credits:  {status['credits']}", width // 3, y_start + 40, color=(200, 200, 200))
        renderer.draw_text(f"Cargo:    {status['cargo']}", width // 3, y_start + 80, color=(200, 200, 200))
        renderer.draw_text(f"Location: {status['location']}", width // 3, y_start + 120, color=(200, 200, 200))

        # Instructions
        renderer.draw_text_centered(
            "Press Enter or ESC to return",
            width // 2,
            height - 50,
            color=(150, 150, 150),
            font=renderer.small_font
        )

    def _handle_selection(self):
        """Handle menu selection"""
        option = self.options[self.selected_index]

        if option == "View Ship Status":
            self.viewing_status = True
        elif option == "Launch to Space":
            if self.game_state.launch_to_space():
                print("Launching to space!")
                self.screen_manager.change_screen("space")
            else:
                print("Cannot launch - insufficient fuel!")
        elif option == "Exit to Main Menu":
            self.screen_manager.change_screen("main_menu")
