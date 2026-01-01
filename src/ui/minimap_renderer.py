"""
Mini-map renderer for navigation contexts
"""
import pygame
from core.constants import SYSTEM_ORBITS

class MinimapRenderer:
    """Renders a mini-map showing the current navigation context"""
    
    def __init__(self):
        """Initialize the minimap renderer"""
        self.font = pygame.font.Font(None, 20)
    
    def render(self, surface, game_session):
        """
        Render the mini-map into the given surface, filling it completely.
        
        Args:
            surface: Pygame surface to render into (should be the aux view)
            game_session: Current game session
        """
        # Get surface dimensions - use ALL of it
        width = surface.get_width()
        height = surface.get_height()

        # Scale factors - separate X and Y to fill rectangular space
        scale_x = width / 5000.0
        scale_y = height / 5000.0
        
        # Fill background
        surface.fill((20, 20, 40))
        
        # Draw border around entire surface
        pygame.draw.rect(surface, (100, 100, 150), surface.get_rect(), 2)
        
        # Calculate center
        center_x = width // 2
        center_y = height // 2
        
        # Draw central object (star)
        pygame.draw.circle(surface, (255, 255, 0), (center_x, center_y), 5)
        
        # Draw orbital rings (ellipses to match stretched space)
        for orbit_radius in SYSTEM_ORBITS:
            if orbit_radius > 0:
                scaled_radius_x = int(orbit_radius * scale_x)
                scaled_radius_y = int(orbit_radius * scale_y)
                rect = pygame.Rect(
                    center_x - scaled_radius_x,
                    center_y - scaled_radius_y,
                    scaled_radius_x * 2,
                    scaled_radius_y * 2
                )
                pygame.draw.ellipse(surface, (60, 60, 80), rect, 1)
        
        # Get and draw planets
        planets = game_session.current_system.get_planets_for_context(game_session.current_context.type)
        for planet in planets:
            px, py = planet.get_coordinates()
            # Scale to mini-map coordinates (with Y-flip and separate X/Y scaling)
            minimap_px = int(px * scale_x)
            minimap_py = height - int(py * scale_y)
            pygame.draw.circle(surface, (150, 200, 255), (minimap_px, minimap_py), 3)
        
        # Draw player ship position
        ship_x, ship_y = game_session.ship_position
        minimap_ship_x = int(ship_x * scale_x)
        minimap_ship_y = height - int(ship_y * scale_y)
        pygame.draw.circle(surface, (0, 255, 0), (minimap_ship_x, minimap_ship_y), 4)