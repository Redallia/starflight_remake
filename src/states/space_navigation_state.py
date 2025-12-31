"""
Placeholder space navigation state for testing state transitions
"""
import pygame
from ui.hud_renderer import HudRenderer
from core.game_state import GameState
from core.colors import SPACE_BLACK, TEXT_NORMAL
from core.input_manager import InputManager
from core.collision_manager import CollisionManager


class SpaceNavigationState(GameState):
    """ Space navigation state """

    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.input_manager = InputManager()
        self.hud_renderer = HudRenderer()
        self.collision_manager = CollisionManager()

    def on_enter(self):
        """Called when entering space navigation state"""
        print("Entering space navigation state")

    def handle_event(self, event):
        """Handle input events"""
        action = self.input_manager.get_action(event)
        
        if action == "cancel":
            self.state_manager.change_state("starport")

    def update(self, dt):
        """Update space navigation state"""
        # Check for movement input every frame
        dx, dy = self.input_manager.get_movement_vector()

        if dx != 0 or dy != 0:
            self._move_ship(dx, -dy)
            # Check for collisions after movement
            self._check_collisions()
        
    def render(self, surface):
        """Render space navigation view with the HUD """
        # Fill background
        surface.fill(SPACE_BLACK)

        # Render HUD
        self.hud_renderer.render(surface, self.state_manager.game_session)    
        
    def _move_ship(self, dx, dy):
        """Move the ship by (dx, dy) in current context"""
        # Movement speed multiplier
        speed = 6 # Move 4 units per keypress instead of 1

        # get current position
        x,y = self.state_manager.game_session.ship_position

        # Update position
        new_x = x + (dx * speed)
        new_y = y + (dy * speed)

        # Clamp to context grid boundaries
        from core.constants import CONTEXT_GRID_SIZE
        new_x = max(0, min(CONTEXT_GRID_SIZE, new_x))
        new_y = max(0, min(CONTEXT_GRID_SIZE, new_y))

        # Update ship position in game session
        self.state_manager.game_session.ship_position = (new_x, new_y)
    
    def _check_collisions(self):
        """Check for all collision types"""
        self._check_planet_collisions()
        self._check_boundary_collisions()
        self._check_central_zone_collisions()

    def _check_planet_collisions(self):
        """Check for planet collisions and handle proximity"""
        ship_x, ship_y = self.state_manager.game_session.ship_position
        current_system = self.state_manager.game_session.current_system
        if not current_system:
            return

        # For now, check all planets (we'll filter by context later)
        all_planets = current_system.inner_planets + current_system.outer_planets
        planet = self.collision_manager.check_planet_collision(ship_x, ship_y, all_planets)

        if planet:
            self._handle_planet_collision(planet)

    def _handle_planet_collision(self, planet):
        """Handle collision with a planet"""
        self.state_manager.game_session.add_message(f"Approaching {planet.name}. Press Space to orbit.")
        # TODO: Check for Space key press, then transition to orbit state

    def _check_boundary_collisions(self):
        """Check for boundary collisions and handle context transitions"""
        ship_x, ship_y = self.state_manager.game_session.ship_position
        boundary = self.collision_manager.check_boundary_collision(ship_x, ship_y)

        if boundary:
            self._handle_boundary_collision(boundary)

    def _handle_boundary_collision(self, boundary):
        """Handle collision with navigation context boundary"""
        # Attempt to exit inner system
        if self.state_manager.game_session.exit_inner_system(boundary):
            self.state_manager.game_session.add_message(f"Entering outer system from {boundary}")
            # Reset collision manager to prevent immediate re-trigger
            self.collision_manager.reset()
        else:
            # Handle other types of boundary exits later
            self.state_manager.game_session.add_message(f"Boundary collision at {boundary} (not implemented yet)")

    def _check_central_zone_collisions(self):
        """Check for central zone collisions and handle inner/outer transitions"""
        ship_x, ship_y = self.state_manager.game_session.ship_position
        central_zone = self.collision_manager.check_central_zone_collision(ship_x, ship_y)

        if central_zone:
            self._handle_central_zone_collision()

    def _handle_central_zone_collision(self):
        """Handle entering the central zone (inner/outer system transition)"""
        # Attempt to enter inner system
        if self.state_manager.game_session.enter_inner_system():
            self.state_manager.game_session.add_message("Entering inner system")
            # Reset collision manager to prevent immediate re-trigger
            self.collision_manager.reset()
        else:
            # Handle other types of central zone collisions later
            self.state_manager.game_session.add_message("Central zone collision (not implemented yet)")