"""
Message Log Area
Scrolling log of text messages - bottom, full width
"""
import pygame
from collections import deque


class MessageLogArea:
    """Area that renders message log (state-independent)"""

    def __init__(self, x, y, width, height, max_messages=10):
        """
        Initialize Message Log Area

        Args:
            x: X position on screen
            y: Y position on screen
            width: Area width
            height: Area height
            max_messages: Maximum number of visible messages
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_messages = max_messages

        # Message storage using deque for efficient FIFO
        self.messages = deque(maxlen=max_messages)

        # Styling (matches HUDPanel styling)
        self.background_color = (0, 0, 20, 180)  # Semi-transparent dark blue
        self.border_color = (100, 150, 200)  # Light blue
        self.border_width = 2

    def add_message(self, text, color=(200, 200, 200)):
        """
        Add a message to the log

        Args:
            text: Message text
            color: RGB color tuple
        """
        self.messages.append({
            'text': text,
            'color': color
        })

    def clear_messages(self):
        """Clear all messages"""
        self.messages.clear()

    def update(self, delta_time, game_state):
        """
        Update area state

        Args:
            delta_time: Time since last frame
            game_state: Current game state
        """
        pass

    def render(self, screen, renderer, game_state, **kwargs):
        """
        Render message log content

        Args:
            screen: Pygame screen surface
            renderer: Renderer instance
            game_state: Current game state
            **kwargs: Additional rendering data
        """
        # Draw background
        pygame.draw.rect(
            screen,
            self.background_color,
            (self.x, self.y, self.width, self.height)
        )

        # Draw border
        pygame.draw.rect(
            screen,
            self.border_color,
            (self.x, self.y, self.width, self.height),
            self.border_width
        )

        # Calculate content area (inside border)
        padding = self.border_width + 5
        content_x = self.x + padding
        content_y = self.y + padding
        content_width = self.width - padding * 2
        content_height = self.height - padding * 2

        # Calculate line height
        line_height = 18

        # Render messages from bottom to top (newest at bottom)
        y_offset = content_y + content_height - line_height
        for message in reversed(self.messages):
            if y_offset < content_y:
                break  # Don't render off top of panel

            renderer.draw_text(
                message['text'],
                content_x + 5,
                y_offset,
                color=message['color'],
                font=renderer.small_font
            )
            y_offset -= line_height
