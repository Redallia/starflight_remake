"""
Renders space navigation view (starfield, ship, planets, other ships)
"""
import pygame
from ui.starfield_renderer import StarfieldRenderer
from core.constants import RENDER_SCALE


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
        # Get ship position (in game units)
        ship_x, ship_y = game_session.ship_position

        # Calculate camera offset (viewport centered on ship)
        # Convert screen pixels to game units for camera position
        camera_x = ship_x - (self.width / RENDER_SCALE) / 2
        camera_y = ship_y - (self.height / RENDER_SCALE) / 2
        
        # Render starfield
        self.starfield.render(surface, ship_x, ship_y)

        # Get visible planets and render them
        planets = game_session.current_system.get_planets_for_context(
            game_session.current_context.type,
            game_session.current_context.data
        )
        self._render_planets(surface, planets, camera_x, camera_y)

        # Render the central star
        self._render_star(surface, game_session.current_system.star, camera_x, camera_y)

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

    def _render_planets(self, surface, planets, camera_x, camera_y):
        """
        Render planets with viewport translation.
        
        Args:
            surface: Surface to render to
            planets: List of Planet objects
            camera_x: Camera X offset in world space
            camera_y: Camera Y offset in world space
        """
        # Define colors for different planet types
        planet_colors = {
            "molten": (255, 100, 0),      # Orange-red
            "terran": (100, 150, 255),    # Blue
            "desert": (200, 180, 100),    # Tan
            "gas_giant": (180, 150, 120), # Brown-ish
            "ice": (200, 220, 255),       # Light blue
            "rocky": (150, 150, 150),     # Gray
        }
        
        for planet in planets:
            # Get planet's world coordinates (in game units)
            world_x, world_y = planet.get_coordinates()

            # Translate to screen coordinates (convert game units to pixels)
            screen_x = (world_x - camera_x) * RENDER_SCALE
            screen_y_world = (world_y - camera_y) * RENDER_SCALE
            screen_y = self.height - screen_y_world

            # Scale planet size for rendering
            render_size = int(planet.size * RENDER_SCALE)

            # Viewport culling (with margin for planet size)
            margin = render_size + 50
            if (-margin <= screen_x <= self.width + margin and
                -margin <= screen_y <= self.height + margin):

                # Get color based on type
                color = planet_colors.get(planet.type, (255, 255, 255))

                # Draw planet as filled circle
                pygame.draw.circle(surface, color, (int(screen_x), int(screen_y)), render_size)

    def _render_star(self, surface, star, camera_x, camera_y):
        # Get star's world coordinates (in game units)
        world_x, world_y = star.get_coordinates()

        # Translate to screen coordinates (convert game units to pixels)
        screen_x = (world_x - camera_x) * RENDER_SCALE
        screen_y_world = (world_y - camera_y) * RENDER_SCALE
        screen_y = self.height - screen_y_world

        # Scale star size for rendering
        render_size = int(star.size * RENDER_SCALE)

        # Viewport culling (with margin for star size)
        margin = render_size + 100
        if (-margin <= screen_x <= self.width + margin and
            -margin <= screen_y <= self.height + margin):

            # Draw star as filled circle (yellow)
            pygame.draw.circle(surface, (255, 255, 0), (int(screen_x), int(screen_y)), render_size)
