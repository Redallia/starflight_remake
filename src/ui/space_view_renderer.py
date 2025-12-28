"""
Renders space navigation view (starfield, ship, planets, other ships)
"""
import pygame
from ui.starfield_renderer import StarfieldRenderer


class SpaceViewRenderer:
    """
    Renders the space navigation main view.
    
    Shows starfield, player ship, planets, and other vessels.
    """
    
    def __init__(self, width: int, height: int):
        """
        Initialize space view renderer.
        
        Args:
            width: Width of viewport
            height: Height of viewport
        """
        self.width = width
        self.height = height
        self.starfield = StarfieldRenderer(width, height)
    
    def render(self, surface: pygame.Surface, game_session):
        """
        Render space view to surface.
        
        Args:
            surface: Surface to render to
            game_session: Current game session
        """
        # Get ship position
        ship_x, ship_y = game_session.ship_position
        
        # Render starfield
        self.starfield.render(surface, ship_x, ship_y)

        # Render ship icon at center
        center_x = self.width // 2
        center_y = self.height //2
        ship_size = 22

        # Triangle points (pointing up)
        points = [
            (center_x, center_y - ship_size // 2), #top
            (center_x - ship_size //2, center_y + ship_size // 2), #bottom left
            (center_x + ship_size //2, center_y + ship_size // 2) #bottom right
        ]

        # Draw filled triangle (cyan)
        pygame.draw.polygon(surface, (0, 255, 255), points)

        # Draw outline (white)
        pygame.draw.polygon(surface, (255, 255, 255), points, 2)

        # TODO: Render planets
        # TODO: Render other ships