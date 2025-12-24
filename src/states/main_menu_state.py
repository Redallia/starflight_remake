"""
Main menu state
"""
import pygame
import json
from pathlib import Path
from core.game_state import GameState
from ui.menu_renderer import MenuRenderer


class MainMenuState(GameState):
    """Main menu state - first screen player sees"""

    def __init__(self, state_manager):
        """Initialize the main menu state"""
        super().__init__(state_manager)

        # Initialize menu renderer
        self.menu_renderer = MenuRenderer()

        # Menu data (will be loaded in on_enter)
        self.menu_title = ""
        self.menu_options = []
        self.option_labels = []
        self.disabled_menu_items = set()
        self.selected_menu_index = 0

    def _load_menu_data(self):
        """Load menu configuration from JSON file"""
        menu_path = Path(__file__).parent.parent / "data" / "static" / "menu" / "main_menu.json"
        with open(menu_path, 'r') as f:
            menu_data = json.load(f)

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
        if event.type == pygame.KEYDOWN:
            # Menu navigation - W/Up/Numpad8 = up, S/Down/Numpad2 = down
            if event.key in (pygame.K_w, pygame.K_UP, pygame.K_KP8):
                self.selected_menu_index = (self.selected_menu_index - 1) % len(self.option_labels)
            elif event.key in (pygame.K_s, pygame.K_DOWN, pygame.K_KP2):
                self.selected_menu_index = (self.selected_menu_index + 1) % len(self.option_labels)

            # Menu selection - Enter or Space
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.selected_menu_index not in self.disabled_menu_items:
                    self._handle_selection()

    def _handle_selection(self):
        """Handle menu option selection"""
        selected_option_id = self.menu_options[self.selected_menu_index]["id"]

        if selected_option_id == "new_game":
            # TODO: Transition to starport state
            print("New Game selected - TODO: implement starport state")
        elif selected_option_id == "load_game":
            # TODO: Load game
            print("Load Game selected - TODO: implement")
        elif selected_option_id == "exit_game":
            # Signal to quit the game
            pygame.event.post(pygame.event.Event(pygame.QUIT))

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
