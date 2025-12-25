"""
State manager for handling game state transitions
"""


class StateManager:
    """Manages game states and transitions between them"""

    def __init__(self):
        """Initialize the state manager"""
        self.states = {}
        self.current_state = None
        self.game_state = None  # Runtime game state (ship, crew, location, etc.)

    def register_state(self, name, state):
        """
        Register a state with the manager

        Args:
            name: String identifier for the state
            state: GameState instance
        """
        self.states[name] = state

    def change_state(self, name):
        """
        Transition to a different state

        Args:
            name: String identifier of the state to transition to
        """
        if name not in self.states:
            raise ValueError(f"State '{name}' not registered")

        # Exit current state
        if self.current_state:
            self.current_state.on_exit()

        # Enter new state
        self.current_state = self.states[name]
        self.current_state.on_enter()

    def get_current_state(self):
        """Get the current active state"""
        return self.current_state
