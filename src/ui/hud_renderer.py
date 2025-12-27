"""
    Base class for the HUD
"""

import pygame

class HudRenderer:
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
    
    def render(self, surface):
        """Render the HUD with simple rectangles to show the layout"""

        # Calculate Layout
        main_view, auxiliary_view, command_view, message_log = self._calculate_layout(surface)

        # Draw the panels
        pygame.draw.rect(surface, (0, 50, 100), main_view)
        pygame.draw.rect(surface, (50, 0, 100), auxiliary_view)
        pygame.draw.rect(surface, (0, 100, 50), command_view)
        pygame.draw.rect(surface, (100, 50, 0), message_log)

        # Draw borders so we can see the edges
        pygame.draw.rect(surface, (255, 255, 255), main_view, 2)
        pygame.draw.rect(surface, (255, 255, 255), auxiliary_view, 2)
        pygame.draw.rect(surface, (255, 255, 255), command_view, 2)
        pygame.draw.rect(surface, (255, 255, 255), message_log, 2)