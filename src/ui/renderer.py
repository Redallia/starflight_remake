"""
Simple rendering utilities
Basic drawing functions for Pygame
"""
import pygame


class Renderer:
    """Collection of rendering utilities"""

    def __init__(self, screen):
        self.screen = screen
        self.default_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 18)

    def draw_text(self, text, x, y, color=(255, 255, 255), font=None):
        """
        Draw text at position

        Args:
            text: String to draw
            x, y: Position
            color: RGB tuple
            font: Font to use (default if None)
        """
        if font is None:
            font = self.default_font

        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    def draw_text_centered(self, text, x, y, color=(255, 255, 255), font=None):
        """Draw text centered at position"""
        if font is None:
            font = self.default_font

        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)

    def draw_rect(self, x, y, width, height, color, filled=True):
        """Draw a rectangle"""
        rect = pygame.Rect(x, y, width, height)
        if filled:
            pygame.draw.rect(self.screen, color, rect)
        else:
            pygame.draw.rect(self.screen, color, rect, 2)

    def draw_circle(self, x, y, radius, color, filled=True):
        """Draw a circle"""
        if filled:
            pygame.draw.circle(self.screen, color, (x, y), radius)
        else:
            pygame.draw.circle(self.screen, color, (x, y), radius, 2)

    def draw_line(self, x1, y1, x2, y2, color, width=1):
        """Draw a line"""
        pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), width)

    def draw_grid(self, x, y, cell_size, rows, cols, color=(50, 50, 50)):
        """
        Draw a grid

        Args:
            x, y: Top-left position
            cell_size: Size of each cell
            rows, cols: Grid dimensions
            color: Grid line color
        """
        # Vertical lines
        for col in range(cols + 1):
            x_pos = x + col * cell_size
            self.draw_line(x_pos, y, x_pos, y + rows * cell_size, color)

        # Horizontal lines
        for row in range(rows + 1):
            y_pos = y + row * cell_size
            self.draw_line(x, y_pos, x + cols * cell_size, y_pos, color)

    def clear(self, color=(0, 0, 0)):
        """Clear screen to color"""
        self.screen.fill(color)
