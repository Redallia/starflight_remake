"""
Placeholder space navigation state for testing state transitions
"""
import pygame
from ui.hud_renderer import HudRenderer
from core.game_state import GameState
from core.colors import SPACE_BLACK, TEXT_NORMAL
from core.input_manager import InputManager


class SpaceNavigationState(GameState):
    """ Space navigation state """

    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.input_manager = InputManager()
        self.hud_renderer = HudRenderer()

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