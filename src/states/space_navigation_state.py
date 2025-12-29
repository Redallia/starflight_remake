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
        ship_x, ship_y = self.state_manager.game_session.ship_position

        # Get current star system
        current_system = self.state_manager.game_session.current_system
        if not current_system:
            return
        
        # For now, check all planets (we'll filter by context later)
        all_planets = current_system.inner_planets + current_system.outer_planets

        # Check planet collisions
        planet_collision = self.collision_manager.check_planet_collision(
            ship_x, ship_y, all_planets
        )

        if planet_collision:
            self.state_manager.game_session.add_message(f"Collision detected with {planet_collision.name}!")
            print(f"Collision detected with {planet_collision.name}!")
        
        # Check boundary collisions
        boundary_hit = self.collision_manager.check_boundary_collision(ship_x, ship_y)
        if boundary_hit:
            self.state_manager.game_session.add_message(f"Boundary collision: {boundary_hit}")
            print(f"BOUNDARY! Hit {boundary_hit} edge")
        
        # Check central zone
        central_zone = self.collision_manager.check_central_zone_collision(ship_x, ship_y)
        if central_zone:
            self.state_manager.game_session.add_message(f"Entered central zone!")