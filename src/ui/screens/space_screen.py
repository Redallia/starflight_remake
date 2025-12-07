"""
Space navigation screen
Handles movement in space, starfield rendering, and navigation
"""
import pygame
from core.screen_manager import Screen
from ui.hud.hud_manager import HUDManager
from ui.hud.space_view_panel import SpaceViewPanel
from ui.hud.control_panel import ControlPanel
from ui.hud.auxiliary_view import AuxiliaryView
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

        # Main View - Space view panel (left side, above message log)
        space_view = SpaceViewPanel(0, 0, 500, 450)
        self.hud_manager.set_view_panel(space_view)

        # Auxiliary View - Mini-map (upper-right)
        auxiliary_view = AuxiliaryView(500, 0, right_column_width, 200)
        self.hud_manager.set_auxiliary_panel(auxiliary_view)

        # Control Panel - Ship status (right side, below mini-map, above message log)
        control_panel = ControlPanel(500, 200, right_column_width, 250)
        self.hud_manager.set_control_panel(control_panel)

        # Message Log (bottom, full width)
        message_log = MessageLogPanel(0, 450, 800, message_log_height)
        self.hud_manager.set_message_log_panel(message_log)

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

        # Check for docking/orbit entry at nearby planet
        if self.near_planet and input_handler.is_confirm_pressed():
            if self.near_planet['type'] == 'starport':
                # Dock at starport
                if self.game_state.return_to_starport():
                    self.hud_manager.add_message(f"Docking at {self.near_planet['name']}", (100, 255, 100))
                    self.screen_manager.change_screen("starport")
                    return
            else:
                # Enter orbit around planet
                if self.game_state.enter_orbit(self.near_planet):
                    self.hud_manager.add_message(f"Entering orbit around {self.near_planet['name']}", (100, 255, 100))
                    self.screen_manager.change_screen("orbit")
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

            # Check if movement would cause collision and modify movement accordingly
            allowed_dx, allowed_dy = self.check_movement_collision(dx, dy)

            # Move the ship with allowed movement (may be clamped at boundaries)
            if allowed_dx != 0 or allowed_dy != 0:
                self.game_state.move_ship(int(allowed_dx), int(allowed_dy))

            # Handle collision counter for wraparound (when trying to push through)
            if allowed_dx == 0 and allowed_dy == 0 and (dx != 0 or dy != 0):
                # Player is trying to move but collision blocked it
                self.handle_wraparound_counter(dx, dy)
            else:
                # No collision or moved successfully, reset counter
                self.collision_counter = 0

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
        ship_x = self.game_state.ship_x
        ship_y = self.game_state.ship_y
        old_near_planet = self.near_planet
        self.near_planet = None

        for planet in self.game_state.planets:
            # Convert planet coordinates to movement grid
            planet_x = planet['coord_x'] * 10
            planet_y = planet['coord_y'] * 10
            planet_radius = planet['radius'] * 10  # Convert to movement grid units

            # Calculate distance from ship to planet center
            dx = ship_x - planet_x
            dy = ship_y - planet_y
            distance = (dx**2 + dy**2) ** 0.5

            # Check if within docking range (at or very close to planet collision radius)
            # Add small buffer to catch ships at edge due to collision detection
            proximity_threshold = planet_radius + 2  # Small buffer for collision edge
            if distance <= proximity_threshold:
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

    def check_movement_collision(self, dx, dy):
        """Check if intended movement would collide with a planet, return allowed movement"""
        ship_x = self.game_state.ship_x
        ship_y = self.game_state.ship_y

        # Calculate new position
        new_x = ship_x + dx
        new_y = ship_y + dy

        for planet in self.game_state.planets:
            # Convert planet coordinates to movement grid
            planet_x = planet['coord_x'] * 10
            planet_y = planet['coord_y'] * 10
            planet_radius = planet['radius'] * 10  # Convert to movement grid units

            # Calculate current distance from ship to planet center
            current_distance = ((ship_x - planet_x)**2 + (ship_y - planet_y)**2) ** 0.5

            # Calculate distance from new position to planet center
            new_distance = ((new_x - planet_x)**2 + (new_y - planet_y)**2) ** 0.5

            # Only block movement if:
            # 1. New position would be inside planet AND
            # 2. We're moving closer to the planet (not moving away)
            if new_distance < planet_radius and new_distance <= current_distance:
                # Movement would cause collision or push further in - block it entirely
                return (0, 0)

        # No collision, allow full movement
        return (dx, dy)

    def handle_wraparound_counter(self, intended_dx, intended_dy):
        """Handle wraparound teleport when player persistently pushes into planet"""
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

            # Check if ship is at planet edge (within collision range)
            if abs(distance - planet_radius) < 5:  # Small tolerance for "at edge"
                # Increment collision counter
                self.collision_counter += 1

                if self.collision_counter > 30:  # ~0.5 seconds at 60fps
                    # Calculate normalized direction from planet to ship
                    if distance > 0:
                        norm_x = dx / distance
                        norm_y = dy / distance
                    else:
                        # Edge case: use opposite of intended movement
                        move_dist = (intended_dx**2 + intended_dy**2) ** 0.5
                        if move_dist > 0:
                            norm_x = -intended_dx / move_dist
                            norm_y = -intended_dy / move_dist
                        else:
                            return  # Can't determine direction

                    # Wraparound - teleport to opposite side
                    self.game_state.ship_x = int(planet_x - norm_x * planet_radius)
                    self.game_state.ship_y = int(planet_y - norm_y * planet_radius)
                    self.collision_counter = 0
                    self.hud_manager.add_message("Warped around planet", (255, 200, 100))
                break

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
