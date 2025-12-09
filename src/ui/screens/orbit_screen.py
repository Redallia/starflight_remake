"""
Orbit screen
Handles planetary orbit interface
"""
import pygame
from core.screen_manager import Screen
from systems.crew_action_system import ActionContext
from entities.crew import ShipRole
from ui.hud.planet_view_panel import PlanetViewPanel
from ui.hud.bridge_panel import BridgePanel
from ui.hud.terrain_map_panel import TerrainMapPanel


class OrbitScreen(Screen):
    """Orbital interface screen"""

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

        # Landing mode state
        self.landing_mode = False  # Are we in landing mode?
        self.selected_landing_option = 0  # Selected option in landing menu (Site Select/Descend/Abort)
        self.selected_landing_site = None  # Selected landing site (None = not yet selected)

        # Gas giant warning state
        self.gas_giant_warning_mode = False  # Are we showing gas giant warning?
        self.selected_warning_option = 1  # Selected option (0=Proceed, 1=Abort) - default to Abort

        # Use shared HUD manager from game state
        self.hud_manager = game_state.hud_manager

    def _register_orbit_actions(self):
        """Register actions needed for orbit screen"""
        from systems.crew_actions.science_actions import SensorScanAction
        from systems.crew_actions.navigation_actions import LeaveOrbitAction
        from systems.crew_actions.captain_actions import LandOnPlanetAction

        # Only register if not already registered
        if not self.action_system._actions.get('science.sensor_scan'):
            self.action_system.register_action(SensorScanAction())
        if not self.action_system._actions.get('navigation.leave_orbit'):
            self.action_system.register_action(LeaveOrbitAction())
        if not self.action_system._actions.get('captain.land_on_planet'):
            self.action_system.register_action(LandOnPlanetAction())

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

        # Message Log is now handled by MessageLogArea in HUDManager - no setup needed

    def on_enter(self):
        """Called when entering orbit"""
        # Set up HUD panels for this screen
        self._setup_hud()

        planet_name = self.game_state.orbiting_planet['name'] if self.game_state.orbiting_planet else "Unknown"
        self.hud_manager.add_message(f"Entered orbit around {planet_name}", (100, 200, 255))

        # Reset loading state
        self.terrain_loaded = False

        # Build dynamic menus from action system
        self._build_role_menus()

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

        # Check if we're in gas giant warning mode
        if self.gas_giant_warning_mode:
            self._handle_gas_giant_warning_input(input_handler)
        # Check if we're in landing mode
        elif self.landing_mode:
            self._handle_landing_input(input_handler)
        else:
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

    def _handle_gas_giant_warning_input(self, input_handler):
        """Handle input when in gas giant warning mode"""
        # Navigate warning options with W/S keys (Proceed/Abort)
        if input_handler.is_key_just_pressed(pygame.K_w):
            self.selected_warning_option = (self.selected_warning_option - 1) % 2
        elif input_handler.is_key_just_pressed(pygame.K_s):
            self.selected_warning_option = (self.selected_warning_option + 1) % 2

        # Execute selected warning option with Space/Enter
        if input_handler.is_confirm_pressed():
            self._execute_warning_option()

    def _execute_warning_option(self):
        """Execute the selected gas giant warning option"""
        options = ["Proceed", "Abort"]
        selected = options[self.selected_warning_option]

        if selected == "Abort":
            # Exit both warning mode and landing mode, return to bridge
            self._exit_gas_giant_warning()
            if self.hud_manager:
                self.hud_manager.add_message("Landing aborted", (255, 150, 100))

        elif selected == "Proceed":
            # User accepts the risk - exit warning mode and continue to landing
            self._exit_gas_giant_warning()
            self._enter_landing_mode()
            if self.hud_manager:
                self.hud_manager.add_message(
                    "Proceeding with landing sequence - USE CAUTION",
                    (255, 150, 100)
                )

    def _handle_landing_input(self, input_handler):
        """Handle input when in landing mode"""
        # Navigate landing options with W/S keys
        if input_handler.is_key_just_pressed(pygame.K_w):
            self.selected_landing_option = (self.selected_landing_option - 1) % 3
        elif input_handler.is_key_just_pressed(pygame.K_s):
            self.selected_landing_option = (self.selected_landing_option + 1) % 3

        # Execute selected landing option with Space/Enter
        if input_handler.is_confirm_pressed():
            self._execute_landing_option()

    def _execute_landing_option(self):
        """Execute the selected landing option"""
        options = ["Site Select", "Descend", "Abort"]
        selected = options[self.selected_landing_option]

        if selected == "Abort":
            # Exit landing mode
            self._exit_landing_mode()
            if self.hud_manager:
                self.hud_manager.add_message("Landing aborted", (255, 150, 100))

        elif selected == "Descend":
            # Check if landing site has been selected
            if self.selected_landing_site is None:
                if self.hud_manager:
                    self.hud_manager.add_message(
                        "Please choose landing coordinates before descending",
                        (255, 200, 100)
                    )
                return

            # Land at selected site
            planet = self.game_state.orbiting_planet
            planet_name = planet['name']

            # Update game state
            self.game_state.location = "planet_surface"

            if self.hud_manager:
                self.hud_manager.add_message(
                    f"Descending to {planet_name} surface...",
                    (100, 255, 100)
                )

            # TODO: Transition to planet surface screen when implemented
            # For now, just exit landing mode
            self._exit_landing_mode()

        elif selected == "Site Select":
            # TODO: Enter site selection mode (Phase 4)
            if self.hud_manager:
                self.hud_manager.add_message(
                    "Site selection not yet implemented",
                    (200, 200, 100)
                )

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

    def _execute_menu_action(self, bridge_panel, action_display_name):
        """Execute the selected menu action"""
        # Special case: Return to Bridge is UI-only
        if action_display_name == "Return to Bridge":
            bridge_panel.close_role_menu()
            return

        # Get current crew member for the selected role
        current_role = bridge_panel.roles[self.selected_role_index]
        crew_member = self._get_crew_for_role(current_role)
        ship_role = self._map_role_name_to_ship_role(current_role)

        # Create action context
        context = ActionContext(
            game_state=self.game_state,
            screen_manager=self.screen_manager,
            hud_manager=self.hud_manager,
            initiating_crew=crew_member
        )

        # Get actions for this role and find the one matching the display name
        actions = self.action_system.get_actions_for_role(ship_role, context)
        action_to_execute = None

        for action in actions:
            if action.get_display_name(context) == action_display_name:
                action_to_execute = action
                break

        # Execute the action if found
        if action_to_execute:
            result = self.action_system.execute_action(action_to_execute.action_id, context)

            # Check if action wants to enter landing mode
            if result.success and result.data.get('enter_landing_mode'):
                # Check if this is a gas giant requiring warning
                if result.data.get('gas_giant_warning'):
                    self._enter_gas_giant_warning()
                else:
                    self._enter_landing_mode()

            # Show result message if action failed
            if not result.success and self.hud_manager:
                self.hud_manager.add_message(result.message, (255, 100, 100))

        bridge_panel.close_role_menu()

    def _map_role_name_to_ship_role(self, role_name: str) -> ShipRole:
        """Map UI role name to ShipRole enum"""
        role_map = {
            "Science Officer": ShipRole.SCIENCE_OFFICER,
            "Navigator": ShipRole.NAVIGATOR,
            "Engineer": ShipRole.ENGINEER,
            "Communications": ShipRole.COMMUNICATIONS,
            "Doctor": ShipRole.DOCTOR,
            "Captain": ShipRole.CAPTAIN
        }
        return role_map.get(role_name, ShipRole.CAPTAIN)

    def _get_crew_for_role(self, role_name: str):
        """Get crew member assigned to a ship station"""
        ship_role = self._map_role_name_to_ship_role(role_name)
        return self.game_state.crew_roster.get_crew_at_station(ship_role)

    def _build_role_menus(self):
        """Build role menus dynamically from action system"""
        bridge_panel = self.hud_manager.control_panel
        if not bridge_panel:
            return

        # Build menu for each role
        for role_name in bridge_panel.roles:
            ship_role = self._map_role_name_to_ship_role(role_name)
            crew_member = self._get_crew_for_role(role_name)

            # Create context for this role
            context = ActionContext(
                game_state=self.game_state,
                screen_manager=self.screen_manager,
                hud_manager=self.hud_manager,
                initiating_crew=crew_member
            )

            # Get available actions from action system
            actions = self.action_system.get_actions_for_role(ship_role, context)

            # Build menu from action display names
            menu_options = [action.get_display_name(context) for action in actions]

            # Always add "Return to Bridge" at the end
            menu_options.append("Return to Bridge")

            # Set menu on bridge panel
            bridge_panel.set_role_menu(role_name, menu_options)

    def _enter_gas_giant_warning(self):
        """Enter gas giant warning mode - show warning panel"""
        from ui.hud.generic_menu_panel import GenericMenuPanel, MenuConfig

        planet = self.game_state.orbiting_planet
        planet_name = planet['name']

        self.gas_giant_warning_mode = True
        self.selected_warning_option = 1  # Default to "Abort"

        # Create warning config
        warning_config = MenuConfig(
            title="WARNING",
            title_color=(255, 100, 100),  # Red title
            items=["Proceed", "Abort"],
            warning_lines=[
                f"Attempting to land on {planet_name}",
                "is inadvisable.",
                "",
                "Gas giants have no solid surface.",
                "Ship destruction is likely."
            ],
            danger_items=["Proceed"]  # Mark "Proceed" as dangerous
        )

        # Swap control panel to gas giant warning panel
        warning_panel = GenericMenuPanel(500, 200, 300, 250, warning_config)
        self.hud_manager.set_control_panel(warning_panel)

    def _exit_gas_giant_warning(self):
        """Exit gas giant warning mode - return to bridge view"""
        self.gas_giant_warning_mode = False

        # Swap control panel back to bridge panel
        bridge_panel = BridgePanel(500, 200, 300, 250)
        self.hud_manager.set_control_panel(bridge_panel)

        # Rebuild bridge menus
        self._build_role_menus()

    def _enter_landing_mode(self):
        """Enter landing mode - swap control panel to landing interface"""
        from ui.hud.generic_menu_panel import GenericMenuPanel, MenuConfig

        self.landing_mode = True
        self.selected_landing_option = 0
        self.selected_landing_site = None  # Reset landing site selection

        # Create landing config
        landing_config = MenuConfig(
            title="Landing Interface",
            items=["Site Select", "Descend", "Abort"]
        )

        # Swap control panel to landing control panel
        landing_panel = GenericMenuPanel(500, 200, 300, 250, landing_config)
        self.hud_manager.set_control_panel(landing_panel)

    def _exit_landing_mode(self):
        """Exit landing mode - return to bridge view"""
        self.landing_mode = False

        # Swap control panel back to bridge panel
        bridge_panel = BridgePanel(500, 200, 300, 250)
        self.hud_manager.set_control_panel(bridge_panel)

        # Rebuild bridge menus
        self._build_role_menus()

    def render(self, screen):
        """Render orbit screen"""
        from ui.renderer import Renderer
        renderer = Renderer(screen)

        # Get current coordinates (ship position in space)
        coordinates = self.game_state.get_coordinate_position()

        # Prepare view data including selected indices based on current mode
        view_data = {
            'loading': not self.terrain_loaded
        }

        # Add appropriate selection index based on current mode
        if self.gas_giant_warning_mode:
            view_data['selected_warning_option'] = self.selected_warning_option
        elif self.landing_mode:
            view_data['selected_landing_option'] = self.selected_landing_option
        else:
            # Bridge mode (role list or role menu)
            view_data['selected_role_index'] = self.selected_role_index
            view_data['selected_menu_index'] = self.selected_menu_index

        # Render everything through HUD manager
        # This will render: planet view panel, minimap, status, message log
        self.hud_manager.render(screen, renderer, self.game_state, coordinates, view_data)
