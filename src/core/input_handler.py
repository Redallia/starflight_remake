"""
Input handling system
Abstracts input away from Pygame for easier future migration
"""
import pygame


class InputHandler:
    """Handles keyboard and other input"""

    def __init__(self):
        self.keys_pressed = set()
        self.keys_just_pressed = set()
        self.keys_just_released = set()

    def update(self, events):
        """
        Update input state based on events

        Args:
            events: List of pygame events
        """
        # Clear frame-specific input
        self.keys_just_pressed.clear()
        self.keys_just_released.clear()

        # Process events
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                self.keys_just_pressed.add(event.key)
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
                self.keys_just_released.add(event.key)

    def is_key_pressed(self, key):
        """Check if key is currently held down"""
        return key in self.keys_pressed

    def is_key_just_pressed(self, key):
        """Check if key was just pressed this frame"""
        return key in self.keys_just_pressed

    def is_key_just_released(self, key):
        """Check if key was just released this frame"""
        return key in self.keys_just_released

    # Convenience methods for common actions
    # Movement (continuous - for space navigation)
    def is_up_pressed(self):
        return self.is_key_pressed(pygame.K_w)

    def is_down_pressed(self):
        return self.is_key_pressed(pygame.K_s)

    def is_left_pressed(self):
        return self.is_key_pressed(pygame.K_a)

    def is_right_pressed(self):
        return self.is_key_pressed(pygame.K_d)

    # Menu navigation (single press - for menus and UI)
    def is_menu_up_pressed(self):
        """W or Up Arrow for menu navigation (single press)"""
        return self.is_key_just_pressed(pygame.K_w) or \
               self.is_key_just_pressed(pygame.K_UP)

    def is_menu_down_pressed(self):
        """S or Down Arrow for menu navigation (single press)"""
        return self.is_key_just_pressed(pygame.K_s) or \
               self.is_key_just_pressed(pygame.K_DOWN)

    def is_confirm_pressed(self):
        """Enter or Space to confirm"""
        return self.is_key_just_pressed(pygame.K_RETURN) or \
               self.is_key_just_pressed(pygame.K_SPACE)

    def is_cancel_pressed(self):
        """ESC to cancel"""
        return self.is_key_just_pressed(pygame.K_ESCAPE)
