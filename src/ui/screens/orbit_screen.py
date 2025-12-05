"""
Orbit screen
Handles planetary orbit interface
"""
import pygame
from core.screen_manager import Screen
from ui.hud.hud_manager import HUDManager
from ui.hud.planet_view_panel import PlanetViewPanel
from ui.hud.bridge_panel import BridgePanel
from ui.hud.terrain_map_panel import TerrainMapPanel
from ui.hud.message_log_panel import MessageLogPanel


class OrbitScreen(Screen):
    """Orbital interface screen"""

    def __init__(self, screen_manager, game_state):
        super().__init__(screen_manager)
        self.game_state = game_state

        # Crew role selection
        self.selected_role_index = 0  # Start with first role (Captain) selected
        self.selected_menu_index = 0  # Selected option in role menu

        # Loading state
        self.terrain_loaded = False

        # HUD system
        self.hud_manager = HUDManager(800, 600)
        self._setup_hud()

    def _setup_hud(self):
        """Set up HUD panels for orbit view"""
        # Layout dimensions (same as space screen)
        right_column_width = 300
        message_log_height = 150

        # Planet view panel (left side, above message log) - leave empty for now
        planet_view = PlanetViewPanel(0, 0, 500, 450)
        self.hud_manager.set_view_panel(planet_view)

        # Terrain map panel (upper-right, replaces mini-map in orbit)
        terrain_map = TerrainMapPanel(500, 0, right_column_width, 200)
        self.hud_manager.set_info_panel(terrain_map)

        # Bridge panel (right side, below terrain map, above message log)
        bridge_panel = BridgePanel(500, 200, right_column_width, 250)
        self.hud_manager.set_status_panel(bridge_panel)

        # Message log panel (bottom, full width)
        message_log = MessageLogPanel(0, 450, 800, message_log_height)
        self.hud_manager.set_message_log_panel(message_log)

    def on_enter(self):
        """Called when entering orbit"""
        planet_name = self.game_state.orbiting_planet['name'] if self.game_state.orbiting_planet else "Unknown"
        self.hud_manager.add_message(f"Entered orbit around {planet_name}", (100, 200, 255))

        # Reset loading state
        self.terrain_loaded = False

    def update(self, delta_time, input_handler):
        """Update orbit screen"""
        # If terrain not loaded yet, just update HUD (which triggers terrain generation)
        if not self.terrain_loaded:
            self.hud_manager.update(delta_time, self.game_state)
            # Check if terrain is now loaded
            planet_view = self.hud_manager.view_panel
            if planet_view and hasattr(planet_view, 'terrain_grid') and planet_view.terrain_grid:
                self.terrain_loaded = True
            return

        # Get bridge panel
        bridge_panel = self.hud_manager.status_panel
        if not bridge_panel:
            return

        # Check if we're in a role menu or on the bridge
        if bridge_panel.is_menu_active():
            # Handle role menu navigation
            self._handle_role_menu_input(input_handler, bridge_panel)
        else:
            # Handle bridge role selection
            self._handle_bridge_input(input_handler, bridge_panel)

        # Update HUD after handling input
        self.hud_manager.update(delta_time, self.game_state)

    def _handle_bridge_input(self, input_handler, bridge_panel):
        """Handle input when on the Bridge (role selection)"""
        num_roles = len(bridge_panel.roles)

        # Navigate crew roles with W/S keys
        if input_handler.is_key_just_pressed(pygame.K_w):
            self.selected_role_index = (self.selected_role_index - 1) % num_roles
        elif input_handler.is_key_just_pressed(pygame.K_s):
            self.selected_role_index = (self.selected_role_index + 1) % num_roles

        # Open role menu with Space/Enter
        if input_handler.is_confirm_pressed():
            bridge_panel.open_role_menu(self.selected_role_index)
            self.selected_menu_index = 0  # Reset menu selection

    def _handle_role_menu_input(self, input_handler, bridge_panel):
        """Handle input when in a role menu"""
        menu_options = bridge_panel.get_active_menu_options()
        num_options = len(menu_options)

        if num_options == 0:
            return

        # Navigate menu options with W/S keys
        if input_handler.is_key_just_pressed(pygame.K_w):
            self.selected_menu_index = (self.selected_menu_index - 1) % num_options
        elif input_handler.is_key_just_pressed(pygame.K_s):
            self.selected_menu_index = (self.selected_menu_index + 1) % num_options

        # Confirm selection with Space/Enter
        if input_handler.is_confirm_pressed():
            self._execute_menu_action(bridge_panel, menu_options[self.selected_menu_index])

        # ESC to return to Bridge
        if input_handler.is_cancel_pressed():
            bridge_panel.close_role_menu()

    def _execute_menu_action(self, bridge_panel, action):
        """Execute the selected menu action"""
        if action == "Return to Bridge":
            bridge_panel.close_role_menu()

    def render(self, screen):
        """Render orbit screen"""
        from ui.renderer import Renderer
        renderer = Renderer(screen)

        # Get current coordinates (ship position in space)
        coordinates = self.game_state.get_coordinate_position()

        # Prepare view data including selected role index, menu index, and loading state
        view_data = {
            'selected_role_index': self.selected_role_index,
            'selected_menu_index': self.selected_menu_index,
            'loading': not self.terrain_loaded
        }

        # Render everything through HUD manager
        # This will render: planet view panel, minimap, status, message log
        self.hud_manager.render(screen, renderer, self.game_state, coordinates, view_data)
