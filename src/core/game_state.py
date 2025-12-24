"""
Base class for game states
"""


class GameState:
    """Base class for all game states in Starflight"""

    def __init__(self, state_manager):
        """
        Initialize the game state

        Args:
            state_manager: Reference to the StateManager for state transitions
        """
        self.state_manager = state_manager

    def handle_event(self, event):
        """
        Handle pygame events

        Args:
            event: Pygame event to process
        """
        pass

    def update(self, dt):
        """
        Update state logic

        Args:
            dt: Delta time since last update in seconds
        """
        pass

    def render(self, surface):
        """
        Render this state to the screen

        Args:
            surface: Pygame surface to render on
        """
        pass

    def on_enter(self):
        """Called when entering this state"""
        pass

    def on_exit(self):
        """Called when leaving this state"""
        pass
