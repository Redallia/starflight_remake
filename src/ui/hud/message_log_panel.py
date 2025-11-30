"""
Message log panel for displaying scrolling text messages
Bottom of screen, 800x150
"""
from ui.hud.hud_panel import HUDPanel
from collections import deque


class MessageLogPanel(HUDPanel):
    """Scrolling message log at bottom of screen"""

    def __init__(self, x, y, width, height, max_messages=10):
        """
        Initialize message log panel

        Args:
            x: X position on screen
            y: Y position on screen
            width: Panel width (800)
            height: Panel height (150)
            max_messages: Maximum number of visible messages
        """
        super().__init__(x, y, width, height)
        self.messages = deque(maxlen=max_messages)
        self.max_messages = max_messages

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

    def render_content(self, screen, renderer):
        """Render message log content"""
        content_x, content_y, content_width, content_height = self.get_content_rect()

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
