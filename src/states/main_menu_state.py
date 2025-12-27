"""
Main menu state
"""
import pygame
from core.game_state import GameState
from core.game_session import GameSession
from core.data_loader import DataLoader
from core.input_manager import InputManager
from ui.menu_renderer import MenuRenderer


class MainMenuState(GameState):
    """Main menu state - first screen player sees"""

    def __init__(self, state_manager):
        """Initialize the main menu state"""
        super().__init__(state_manager)

        # Initialize managers and renderers
        self.data_loader = DataLoader()
        self.input_manager = InputManager()
        self.menu_renderer = MenuRenderer()

        # Menu data (will be loaded in on_enter)
        self.menu_title = ""
        self.menu_options = []
        self.option_labels = []
        self.disabled_menu_items = set()
        self.selected_menu_index = 0

    def _load_menu_data(self):
        """Load menu configuration from JSON file"""
        # Use DataLoader to load the menu configuration
        menu_data = self.data_loader.load_static("menu", "main_menu.json")

        self.menu_title = menu_data["title"]
        self.menu_options = menu_data["options"]
        self.option_labels = [opt["label"] for opt in self.menu_options]
        self.disabled_menu_items = {i for i, opt in enumerate(self.menu_options) if not opt["enabled"]}
        self.selected_menu_index = 0

    def on_enter(self):
        """Called when entering the main menu state"""
        self._load_menu_data()

    def handle_event(self, event):
        """Handle menu input events"""
        # Convert event to action using InputManager
        action = self.input_manager.get_action(event)

        if action == "menu_up":
            self.selected_menu_index = (self.selected_menu_index - 1) % len(self.option_labels)
        elif action == "menu_down":
            self.selected_menu_index = (self.selected_menu_index + 1) % len(self.option_labels)
        elif action == "confirm":
            if self.selected_menu_index not in self.disabled_menu_items:
                self._handle_selection()

    def _handle_selection(self):
        """Handle menu option selection"""
        selected_option_id = self.menu_options[self.selected_menu_index]["id"]

        if selected_option_id == "new_game":
            # Create new game state
            self._create_new_game()
            # Transition to starport
            self.state_manager.change_state("starport")
        elif selected_option_id == "load_game":
            # TODO: Load game
            print("Load Game selected - TODO: implement")
        elif selected_option_id == "exit_game":
            # Signal to quit the game
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def _create_new_game(self):
        """Create a new game state with default values"""
        # Create minimal game state for now
        # Values are placeholders - will be replaced with actual defaults later
        self.state_manager.game_session = GameSession()

    def update(self, dt):
        """Update menu state (nothing to update for static menu)"""
        pass

    def render(self, surface):
        """Render the main menu"""
        self.menu_renderer.render(
            surface,
            self.menu_title,
            self.option_labels,
            self.selected_menu_index,
            self.disabled_menu_items
        )
