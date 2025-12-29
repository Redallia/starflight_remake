"""
    Base renderer class for the HUD
"""

import pygame
from ui.space_view_renderer import SpaceViewRenderer
from ui.minimap_renderer import MinimapRenderer
from ui.message_log_renderer import MessageLogRenderer


class HudRenderer:

    def __init__(self):
        """
        Initialize the HUD renderer and its components
        """
        self.space_view_renderer = None # Created when needed
        self.minimap_renderer = None # Created when needed

    def _calculate_layout(self, surface):
        """Calculate HUD panel rectangle based on surface size"""
        width = surface.get_width()
        height = surface.get_height()
        
        # Main View: 62.5% wide, 75% tall, top-left
        main_view = pygame.Rect(0,0, int(width * 0.625), int(height * 0.75))

        # Auxiliary View: 37.5% wide, 33% tall, top-right
        auxiliary_view = pygame.Rect(int(width * 0.625), 0, int(width * 0.375), int(height * 0.33))

        # Command View: 37.5% wide, 33% tall, along the right side
        command_view = pygame.Rect(int(width * 0.625), int(height * 0.33), int(width * 0.375), int(height * 0.42))

        # Message Log: 100% wide, 33% tall, along the bottom
        message_log = pygame.Rect(0, int(height * 0.75), width, int(height * 0.25))

        return main_view, auxiliary_view, command_view, message_log
    
    def render(self, surface, game_session):
        """Render the HUD with content from game session
        
        Args:
            surface: Pygame surface to render to
            game_session: Current game session containing state
        """

        # Calculate Layout
        main_view, auxiliary_view, command_view, message_log = self._calculate_layout(surface)

        # Create space view renderer if not yet created
        if self.space_view_renderer is None:
            self.space_view_renderer = SpaceViewRenderer(main_view.width, main_view.height)
            self.minimap_renderer = MinimapRenderer()

        # Message Log Renderer
        message_log_renderer = MessageLogRenderer()
        message_log_surface = surface.subsurface(message_log)
        message_log_renderer.render(message_log_surface, game_session)

        main_surface = surface.subsurface(main_view)
        self.space_view_renderer.render(main_surface, game_session)

        # Render minimap in auxiliary view (inset for border)
        border_width = 2
        auxiliary_inset = auxiliary_view.inflate(-border_width * 2, -border_width * 2)
        auxiliary_surface = surface.subsurface(auxiliary_inset)
        self.minimap_renderer.render(auxiliary_surface, game_session)

        # Draw the panels
        pygame.draw.rect(surface, (0, 100, 50), command_view)
        # pygame.draw.rect(surface, (100, 50, 0), message_log)

        # Draw borders so we can see the edges
        pygame.draw.rect(surface, (255, 255, 255), main_view, 2)
        pygame.draw.rect(surface, (255, 255, 255), auxiliary_view, 2)
        pygame.draw.rect(surface, (255, 255, 255), command_view, 2)
        pygame.draw.rect(surface, (255, 255, 255), message_log, 2)