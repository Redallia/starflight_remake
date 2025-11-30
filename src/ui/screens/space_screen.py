"""
Space navigation screen
Handles movement in space, starfield rendering, and navigation
"""
import pygame
from core.screen_manager import Screen
from ui.hud.hud_manager import HUDManager
from ui.hud.space_view_panel import SpaceViewPanel
from ui.hud.status_panel import StatusPanel
from ui.hud.minimap_panel import MiniMapPanel
from ui.hud.message_log_panel import MessageLogPanel


class SpaceScreen(Screen):
    """Space navigation screen with grid-based movement"""

    def __init__(self, screen_manager, game_state):
        super().__init__(screen_manager)
        self.game_state = game_state

        # Movement configuration
        self.ship_speed = 1.0  # Movement grid units per frame when key held
        self.fuel_consumption_rate = 0.01  # Fuel per movement grid unit traveled

        # Planet proximity tracking
        self.near_planet = None  # Currently nearby planet (for docking prompt)
        self.collision_counter = 0  # Track repeated collisions for wraparound

        # HUD system
        self.hud_manager = HUDManager(800, 600)
        self._setup_hud()

    def _setup_hud(self):
        """Set up HUD panels for space navigation"""
        # Layout dimensions
        right_column_width = 300
        message_log_height = 150

        # Space view panel (left side, above message log)
        # Takes up the space not occupied by right column and message log
        space_view = SpaceViewPanel(0, 0, 500, 450)
        self.hud_manager.set_view_panel(space_view)

        # Mini-map panel (upper-right, flush with edge)
        minimap_panel = MiniMapPanel(500, 0, right_column_width, 200)
        self.hud_manager.set_info_panel(minimap_panel)

        # Status panel (right side, below mini-map, above message log)
        # Extends from bottom of mini-map to top of message log
        status_panel = StatusPanel(500, 200, right_column_width, 250)
        self.hud_manager.set_status_panel(status_panel)

        # Message log panel (bottom, full width)
        message_log = MessageLogPanel(0, 450, 800, message_log_height)
        self.hud_manager.set_message_log_panel(message_log)

        # Set instructions
        self.hud_manager.set_instructions("WASD: Move  |  R: Return to Starport")

    def on_enter(self):
        """Called when entering space"""
        # Regenerate starfield for variety
        if self.hud_manager.view_panel:
            self.hud_manager.view_panel.regenerate_starfield()
        # Add welcome message
        self.hud_manager.add_message("Entered space", (100, 200, 255))

    def update(self, delta_time, input_handler):
        """Update space screen"""
        # Update HUD
        self.hud_manager.update(delta_time, self.game_state)

        # Check for docking at nearby planet
        if self.near_planet and input_handler.is_confirm_pressed():
            if self.near_planet['type'] == 'starport':
                if self.game_state.return_to_starport():
                    self.hud_manager.add_message(f"Docking at {self.near_planet['name']}", (100, 255, 100))
                    self.screen_manager.change_screen("starport")
                    return

        # Return to starport (R key - backup method)
        if input_handler.is_key_just_pressed(pygame.K_r):
            if self.game_state.return_to_starport():
                self.hud_manager.add_message("Returning to starport", (100, 255, 100))
                self.screen_manager.change_screen("starport")
                return

        # WASD movement
        dx = 0
        dy = 0

        if input_handler.is_up_pressed():  # W
            dy -= self.ship_speed
        if input_handler.is_down_pressed():  # S
            dy += self.ship_speed
        if input_handler.is_left_pressed():  # A
            dx -= self.ship_speed
        if input_handler.is_right_pressed():  # D
            dx += self.ship_speed

        # Apply movement if any
        if dx != 0 or dy != 0:
            # Store old position to calculate actual movement
            old_x = self.game_state.ship_x
            old_y = self.game_state.ship_y

            # Move the ship (may be clamped at boundaries)
            self.game_state.move_ship(int(dx), int(dy))

            # Check for planet collisions and handle
            self.handle_planet_collision(old_x, old_y, dx, dy)

            # Calculate actual movement that occurred (after clamping and collision)
            actual_dx = self.game_state.ship_x - old_x
            actual_dy = self.game_state.ship_y - old_y

            # Consume fuel based on actual distance traveled
            distance = (actual_dx**2 + actual_dy**2) ** 0.5
            fuel_used = distance * self.fuel_consumption_rate
            self.game_state.fuel = max(0, self.game_state.fuel - fuel_used)

            # Update starfield for parallax effect (stars drift opposite to movement)
            # Only scroll based on actual movement, not intended movement
            if self.hud_manager.view_panel:
                self.hud_manager.view_panel.update_starfield(-actual_dx * 2, -actual_dy * 2)

        # Check proximity to planets for docking prompt
        self.check_planet_proximity()

    def check_planet_proximity(self):
        """Check if ship is near any planet for docking"""
        ship_coord = self.game_state.get_coordinate_position()
        old_near_planet = self.near_planet
        self.near_planet = None

        for planet in self.game_state.planets:
            # Calculate distance in coordinate units
            dx = ship_coord[0] - planet['coord_x']
            dy = ship_coord[1] - planet['coord_y']
            distance = (dx**2 + dy**2) ** 0.5

            # Check if within docking range (planet radius + small buffer)
            if distance <= planet['radius'] + 1:
                self.near_planet = planet
                break

        # Add message when entering planet proximity
        if self.near_planet and self.near_planet != old_near_planet:
            if self.near_planet['type'] == 'starport':
                self.hud_manager.add_message(
                    f"Press SPACE to dock at {self.near_planet['name']}",
                    (255, 255, 0)
                )
            else:
                self.hud_manager.add_message(
                    f"Press SPACE to enter orbit around {self.near_planet['name']}",
                    (255, 255, 0)
                )

    def handle_planet_collision(self, old_x, old_y, intended_dx, intended_dy):
        """Handle collision with planets - hard stop or wraparound"""
        ship_x = self.game_state.ship_x
        ship_y = self.game_state.ship_y

        for planet in self.game_state.planets:
            # Convert planet coordinates to movement grid
            planet_x = planet['coord_x'] * 10
            planet_y = planet['coord_y'] * 10
            planet_radius = planet['radius'] * 10  # Convert to movement grid units

            # Calculate distance from ship to planet center
            dx = ship_x - planet_x
            dy = ship_y - planet_y
            distance = (dx**2 + dy**2) ** 0.5

            # Check if ship is inside planet radius
            if distance < planet_radius:
                # Hard stop - push ship back to edge of planet
                if distance > 0:
                    # Normalize direction and push to edge
                    norm_x = dx / distance
                    norm_y = dy / distance
                    self.game_state.ship_x = int(planet_x + norm_x * planet_radius)
                    self.game_state.ship_y = int(planet_y + norm_y * planet_radius)
                else:
                    # Ship exactly at center, push in opposite direction of movement
                    if intended_dx != 0 or intended_dy != 0:
                        move_dist = (intended_dx**2 + intended_dy**2) ** 0.5
                        if move_dist > 0:
                            norm_x = -intended_dx / move_dist
                            norm_y = -intended_dy / move_dist
                            self.game_state.ship_x = int(planet_x + norm_x * planet_radius)
                            self.game_state.ship_y = int(planet_y + norm_y * planet_radius)

                # Check if player is trying to push through (collision counter)
                self.collision_counter += 1
                if self.collision_counter > 30:  # ~0.5 seconds at 60fps
                    # Wraparound - teleport to opposite side
                    self.game_state.ship_x = int(planet_x - norm_x * planet_radius)
                    self.game_state.ship_y = int(planet_y - norm_y * planet_radius)
                    self.collision_counter = 0
                    print("Wrapping around planet")
                break
        else:
            # No collision, reset counter
            self.collision_counter = 0

    def render(self, screen):
        """Render space screen"""
        from ui.renderer import Renderer
        renderer = Renderer(screen)

        # Get current coordinates
        coordinates = self.game_state.get_coordinate_position()

        # Prepare view data for space view panel
        view_data = {
            'near_planet': self.near_planet
        }

        # Render everything through HUD manager
        # This will render: view panel (starfield, planets, ship) then HUD overlays
        self.hud_manager.render(screen, renderer, self.game_state, coordinates, view_data)
