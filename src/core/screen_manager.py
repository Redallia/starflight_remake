"""
Screen management system
Handles switching between different game screens/states
"""


class Screen:
    """Base class for all game screens"""

    def __init__(self, screen_manager):
        self.screen_manager = screen_manager

    def on_enter(self):
        """Called when entering this screen"""
        pass

    def on_exit(self):
        """Called when leaving this screen"""
        pass

    def update(self, delta_time, input_handler):
        """
        Update screen logic

        Args:
            delta_time: Time since last frame in seconds
            input_handler: InputHandler instance
        """
        pass

    def render(self, screen):
        """
        Render screen to display

        Args:
            screen: Pygame surface to draw on
        """
        pass


class ScreenManager:
    """Manages game screens and transitions"""

    def __init__(self):
        self.screens = {}
        self.current_screen = None

    def add_screen(self, name, screen):
        """
        Register a screen

        Args:
            name: Unique identifier for the screen
            screen: Screen instance
        """
        self.screens[name] = screen

    def change_screen(self, name):
        """
        Switch to a different screen

        Args:
            name: Name of screen to switch to
        """
        if name not in self.screens:
            raise ValueError(f"Screen '{name}' not found")

        # Exit current screen
        if self.current_screen:
            self.current_screen.on_exit()

        # Switch to new screen
        self.current_screen = self.screens[name]
        self.current_screen.on_enter()

    def update(self, delta_time, input_handler):
        """Update current screen"""
        if self.current_screen:
            self.current_screen.update(delta_time, input_handler)

    def render(self, screen):
        """Render current screen"""
        if self.current_screen:
            self.current_screen.render(screen)
