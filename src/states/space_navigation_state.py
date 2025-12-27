"""
Placeholder space navigation state for testing state transitions
"""
from core.game_state import GameState
from core.colors import SPACE_BLACK, TEXT_NORMAL
import pygame


class SpaceNavigationState(GameState):
    """Placeholder space navigation state - will be replaced with full implementation later"""

    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

    def on_enter(self):
        """Called when entering space navigation state"""
        print("Entering space navigation state")

    def handle_event(self, event):
        """Handle input events"""
        # Press ESC to return to starport
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state_manager.change_state("starport")

    def update(self, dt):
        """Update space navigation state"""
        pass

    def render(self, surface):
        """Render placeholder space view"""
        # Fill with space black background
        surface.fill(SPACE_BLACK)

        # Title
        title = self.font.render("SPACE NAVIGATION - PLACEHOLDER", True, TEXT_NORMAL)
        title_rect = title.get_rect(center=(surface.get_width() // 2, 200))
        surface.blit(title, title_rect)

        # Show current location
        hyperspace_coords = self.state_manager.game_session.get_hyperspace_coordinates()
        location = self.small_font.render(f"Location: {hyperspace_coords}", True, TEXT_NORMAL)
        location_rect = location.get_rect(center=(surface.get_width() // 2, 250))
        surface.blit(location, location_rect)

        # Instructions
        instruction = self.small_font.render("Press ESC to return to Starport", True, TEXT_NORMAL)
        instruction_rect = instruction.get_rect(center=(surface.get_width() // 2, 350))
        surface.blit(instruction, instruction_rect)

        # Show game state info if available
        if self.state_manager.game_state:
            ship_info = self.small_font.render(
                f"Ship: {self.state_manager.game_state.get('ship', {}).get('name', 'Unknown')}",
                True,
                TEXT_NORMAL
            )
            ship_rect = ship_info.get_rect(center=(surface.get_width() // 2, 350))
            surface.blit(ship_info, ship_rect)
