"""
Orbit screen
Handles planetary orbit interface
"""
import pygame
from core.screen_manager import Screen
from ui.hud.hud_manager import HUDManager
from ui.hud.planet_view_panel import PlanetViewPanel
from ui.hud.status_panel import StatusPanel
from ui.hud.minimap_panel import MiniMapPanel
from ui.hud.message_log_panel import MessageLogPanel


class OrbitScreen(Screen):
    """Orbital interface screen"""

    def __init__(self, screen_manager, game_state):
        super().__init__(screen_manager)
        self.game_state = game_state

        # HUD system
        self.hud_manager = HUDManager(800, 600)
        self._setup_hud()

    def _setup_hud(self):
        """Set up HUD panels for orbit view"""
        # Layout dimensions (same as space screen)
        right_column_width = 300
        message_log_height = 150

        # Planet view panel (left side, above message log)
        planet_view = PlanetViewPanel(0, 0, 500, 450)
        self.hud_manager.set_view_panel(planet_view)

        # Mini-map panel (upper-right, flush with edge)
        minimap_panel = MiniMapPanel(500, 0, right_column_width, 200)
        self.hud_manager.set_info_panel(minimap_panel)

        # Status panel (right side, below mini-map, above message log)
        status_panel = StatusPanel(500, 200, right_column_width, 250)
        self.hud_manager.set_status_panel(status_panel)

        # Message log panel (bottom, full width)
        message_log = MessageLogPanel(0, 450, 800, message_log_height)
        self.hud_manager.set_message_log_panel(message_log)

    def on_enter(self):
        """Called when entering orbit"""
        planet_name = self.game_state.orbiting_planet['name'] if self.game_state.orbiting_planet else "Unknown"
        self.hud_manager.add_message(f"Entered orbit around {planet_name}", (100, 200, 255))

    def update(self, delta_time, input_handler):
        """Update orbit screen"""
        # Update HUD
        self.hud_manager.update(delta_time, self.game_state)

        # Exit orbit with SPACE key
        if input_handler.is_confirm_pressed():
            if self.game_state.exit_orbit():
                self.hud_manager.add_message("Exiting orbit", (100, 255, 100))
                self.screen_manager.change_screen("space")
                return

    def render(self, screen):
        """Render orbit screen"""
        from ui.renderer import Renderer
        renderer = Renderer(screen)

        # Get current coordinates (ship position in space)
        coordinates = self.game_state.get_coordinate_position()

        # Prepare view data (empty for now, planet panel gets data from game_state)
        view_data = {}

        # Render everything through HUD manager
        # This will render: planet view panel, minimap, status, message log
        self.hud_manager.render(screen, renderer, self.game_state, coordinates, view_data)
