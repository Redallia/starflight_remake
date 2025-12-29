"""
Renderer for the message log display
"""
import pygame
from core.colors import TEXT_NORMAL

class MessageLogRenderer:
    """Renders the scrolling message log"""
    
    def __init__(self):
        """Initialize the message log renderer"""
        self.font = pygame.font.Font(None, 22)  # Small font for messages
        self.line_height = 15  # Pixels between lines
        self.padding = 10  # Padding from edges
    
    def render(self, surface, game_session):
        """
        Render the message log.
        
        Args:
            surface: Pygame surface to render to (the message log panel)
            game_session: Game session containing messages
        """
        # Get dimensions
        width = surface.get_width()
        height = surface.get_height()
        
        # Calculate how many lines fit in the panel
        max_visible_lines = (height - self.padding * 2) // self.line_height
        
        # Get the most recent messages that fit
        messages = game_session.messages[-max_visible_lines:]

        # Start from the bottom and work upward
        y = height - self.padding - self.line_height
        
        # Render messages in reverse order (newest at bottom)
        for message in reversed(messages):
            text_surface = self.font.render(message, True, TEXT_NORMAL)
            surface.blit(text_surface, (self.padding, y))
            y -= self.line_height
            
            # Stop if we've gone above the visible area
            if y < self.padding:
                break