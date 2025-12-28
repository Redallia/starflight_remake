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
        elif action == "up":
            self._move_ship(0, 1)
        elif action == "down":
            self._move_ship(0, -1)
        elif action == "left":
            self._move_ship(-1, 0)
        elif action == "right":
            self._move_ship(1, 0)
        elif action == "up_left":
            self._move_ship(-1, 1)
        elif action == "down_left":
            self._move_ship(-1, -1)
        elif action == "up_right":
            self._move_ship(1, 1)
        elif action == "down_right":
            self._move_ship(1, -1)

    def update(self, dt):
        """Update space navigation state"""
        pass

    def render(self, surface):
        """Render space navigation view with the HUD """
        # Fill background
        surface.fill(SPACE_BLACK)

        # Render HUD
        self.hud_renderer.render(surface, self.state_manager.game_session)

        # # Title
        # title = self.font.render("SPACE NAVIGATION - PLACEHOLDER", True, TEXT_NORMAL)
        # title_rect = title.get_rect(center=(surface.get_width() // 2, 200))
        # surface.blit(title, title_rect)

        # # Show current location
        # current_region = self.state_manager.game_session.get_current_context().data.get("region")
        # hyperspace_coords = self.state_manager.game_session.get_hyperspace_coordinates()
        # location = self.small_font.render(f"Location: {current_region}({hyperspace_coords})", True, TEXT_NORMAL)
        # location_rect = location.get_rect(center=(surface.get_width() // 2, 250))
        # surface.blit(location, location_rect)

        # ## Show current ship position
        # current_ship_position = self.state_manager.game_session.ship_position
        # ship_position = self.small_font.render(f"Ship Position: {current_ship_position}", True, TEXT_NORMAL)
        # ship_position_rect = ship_position.get_rect(center=(surface.get_width() // 2, 300))
        # surface.blit(ship_position, ship_position_rect)

        # # Instructions
        # instruction = self.small_font.render("Press ESC to return to Starport", True, TEXT_NORMAL)
        # instruction_rect = instruction.get_rect(center=(surface.get_width() // 2, 350))
        # surface.blit(instruction, instruction_rect)

        # # Show game state info if available
        # if self.state_manager.game_state:
        #     ship_info = self.small_font.render(
        #         f"Ship: {self.state_manager.game_state.get('ship', {}).get('name', 'Unknown')}",
        #         True,
        #         TEXT_NORMAL
        #     )
        #     ship_rect = ship_info.get_rect(center=(surface.get_width() // 2, 350))
        #     surface.blit(ship_info, ship_rect)
        pass

    def _move_ship(self, dx, dy):
        """Move the ship by (dx, dy) in current context"""
        # Movement speed multiplier
        speed = 4 # Move 4 units per keypress instead of 1

        # get current position
        x,y = self.state_manager.game_session.ship_position

        # Update position
        new_x = x + (dx * speed)
        new_y = y + (dy * speed)

        # Update ship position in game session
        self.state_manager.game_session.ship_position = (new_x, new_y)
        pass