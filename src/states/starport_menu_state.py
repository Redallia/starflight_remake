"""
Starport menu state
"""
from core.game_state import GameState
from core.data_loader import DataLoader
from core.input_manager import InputManager
from core.constants import CONTEXT_LOCAL_SPACE
from ui.menu_renderer import MenuRenderer


class StarportMenuState(GameState):
    """Starport menu state - screen shown when player is at starport"""

    def __init__(self, state_manager):
        """Initialize the starport menu state"""
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
        menu_data = self.data_loader.load_static("menu", "starport_menu.json")

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

        if action == "up":
            self.selected_menu_index = (self.selected_menu_index - 1) % len(self.option_labels)
        elif action == "down":
            self.selected_menu_index = (self.selected_menu_index + 1) % len(self.option_labels)
        elif action == "return":
            if self.selected_menu_index not in self.disabled_menu_items:
                self._handle_selection()

    def _handle_selection(self):
        """Handle menu option selection"""
        selected_option_id = self.menu_options[self.selected_menu_index]["id"]

        if selected_option_id == "launch_to_space":
            # Launch from starport into space
            if self.state_manager.game_session.launch_from_dock():
                self.state_manager.change_state("space_navigation")
            else:
                # Launch failed - this shouldn't happen, but handle gracefully
                print("ERROR: Failed to launch from dock")

        elif selected_option_id == "exit_to_main_menu":
            # Return to main menu
            self.state_manager.change_state("main_menu")

    def update(self, dt):
        """Update menu state (nothing to update for static menu)"""
        pass

    def render(self, surface):
        """Render the starport menu"""
        self.menu_renderer.render(
            surface,
            self.menu_title,
            self.option_labels,
            self.selected_menu_index,
            self.disabled_menu_items
        )
