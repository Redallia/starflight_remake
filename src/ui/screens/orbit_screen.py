"""
Orbit screen
Handles planetary orbit interface
"""
import pygame
from core.screen_manager import Screen
from systems.crew_action_system import ActionContext
from entities.crew import ShipRole
from ui.hud.hud_manager import HUDManager
from ui.hud.planet_view_panel import PlanetViewPanel
from ui.hud.bridge_panel import BridgePanel
from ui.hud.terrain_map_panel import TerrainMapPanel
from ui.hud.message_log_panel import MessageLogPanel


class OrbitScreen(Screen):
    """Orbital interface screen"""

    # Define which actions are available in orbit for each role
    AVAILABLE_ACTIONS = {
        ShipRole.SCIENCE_OFFICER: ['science.sensor_scan'],
        ShipRole.NAVIGATOR: ['navigation.leave_orbit'],
        ShipRole.ENGINEER: [],
        ShipRole.COMMUNICATIONS: [],
        ShipRole.DOCTOR: [],
        ShipRole.CAPTAIN: [],
    }

    def __init__(self, screen_manager, game_state, action_system):
        super().__init__(screen_manager)
        self.game_state = game_state
        self.action_system = action_system

        # Register orbit-specific actions
        self._register_orbit_actions()

        # Crew role selection
        self.selected_role_index = 0  # Start with first role (Captain) selected
        self.selected_menu_index = 0  # Selected option in role menu

        # Loading state
        self.terrain_loaded = False

        # HUD system
        self.hud_manager = HUDManager(800, 600)
        self._setup_hud()

    def _register_orbit_actions(self):
        """Register actions needed for orbit screen"""
        from systems.crew_actions.science_actions import SensorScanAction
        from systems.crew_actions.navigation_actions import LeaveOrbitAction

        # Only register if not already registered
        if not self.action_system._actions.get('science.sensor_scan'):
            self.action_system.register_action(SensorScanAction())
        if not self.action_system._actions.get('navigation.leave_orbit'):
            self.action_system.register_action(LeaveOrbitAction())

    def _setup_hud(self):
        """Set up HUD panels for orbit view"""
        # Layout dimensions (same as space screen)
        right_column_width = 300
        message_log_height = 150

        # Main View - Planet view panel (left side, above message log)
        planet_view = PlanetViewPanel(0, 0, 500, 450)
        self.hud_manager.set_view_panel(planet_view)

        # Auxiliary Panel - Terrain map (upper-right, replaces mini-map in orbit)
        terrain_map = TerrainMapPanel(500, 0, right_column_width, 200)
        self.hud_manager.set_auxiliary_panel(terrain_map)

        # Control Panel - Bridge (right side, below terrain map, above message log)
        bridge_panel = BridgePanel(500, 200, right_column_width, 250)
        self.hud_manager.set_control_panel(bridge_panel)

        # Message Log (bottom, full width)
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

        # Get bridge panel from control panel
        bridge_panel = self.hud_manager.control_panel
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
        # Special case: Return to Bridge is UI-only
        if action == "Return to Bridge":
            bridge_panel.close_role_menu()
            return

        # Get current crew member for the selected role
        current_role = bridge_panel.roles[self.selected_role_index]
        crew_member = self._get_crew_for_role(current_role)

        # Create action context
        context = ActionContext(
            game_state=self.game_state,
            screen_manager=self.screen_manager,
            hud_manager=self.hud_manager,
            initiating_crew=crew_member
        )

        # Map UI action text to action ID
        action_map = {
            "Sensors": "science.sensor_scan",
            "Leave Orbit": "navigation.leave_orbit"
        }

        action_id = action_map.get(action)
        if action_id:
            result = self.action_system.execute_action(action_id, context)

            # Show result message if action failed
            if not result.success and self.hud_manager:
                self.hud_manager.add_message(result.message, (255, 100, 100))

        bridge_panel.close_role_menu()

    def _get_crew_for_role(self, role_name: str):
        """Get crew member assigned to a ship station"""
        # Map UI role name to ShipRole
        role_map = {
            "Science Officer": ShipRole.SCIENCE_OFFICER,
            "Navigator": ShipRole.NAVIGATOR,
            "Engineer": ShipRole.ENGINEER,
            "Communications": ShipRole.COMMUNICATIONS,
            "Doctor": ShipRole.DOCTOR,
            "Captain": ShipRole.CAPTAIN
        }
        ship_role = role_map.get(role_name, ShipRole.CAPTAIN)

        # Get crew member assigned to this station
        return self.game_state.crew_roster.get_crew_at_station(ship_role)

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
