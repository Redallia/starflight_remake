"""
Message Log Area
Scrolling log of text messages - bottom, full width
"""
import pygame


class MessageLogArea:
    """Area that renders message log (state-independent)"""

    def __init__(self, x, y, width, height):
        """
        Initialize Message Log Area

        Args:
            x: X position on screen
            y: Y position on screen
            width: Area width
            height: Area height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Message storage
        self.messages = []  # List of (text, color) tuples
        self.max_messages = 10  # Maximum messages to display

    def add_message(self, text, color=(200, 200, 200)):
        """
        Add a message to the log

        Args:
            text: Message text
            color: RGB color tuple
        """
        self.messages.append((text, color))
        # Trim old messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def clear_messages(self):
        """Clear all messages"""
        self.messages = []

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
        # TODO: Implement message log rendering
        pass
