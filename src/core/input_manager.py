"""
Input management and key binding system
"""
import pygame


class InputManager:
    """
    Maps raw input events to game actions

    Provides abstraction layer between pygame events and game logic,
    making it easier to rebind keys or add controller support later.
    """

    def __init__(self):
        """Initialize the input manager with default key bindings"""
        # Define action mappings
        # Each action maps to a list of keys that trigger it
        self.key_bindings = {
            # Menu navigation
            "menu_up": [pygame.K_w, pygame.K_UP, pygame.K_KP8],
            "menu_down": [pygame.K_s, pygame.K_DOWN, pygame.K_KP2],
            "menu_left": [pygame.K_a, pygame.K_LEFT, pygame.K_KP4],
            "menu_right": [pygame.K_d, pygame.K_RIGHT, pygame.K_KP6],
            "confirm": [pygame.K_RETURN, pygame.K_SPACE],
            "cancel": [pygame.K_ESCAPE, pygame.K_BACKSPACE],

            # Ship navigation (will use same keys as menu in different context)
            "nav_up": [pygame.K_w, pygame.K_UP, pygame.K_KP8],
            "nav_down": [pygame.K_s, pygame.K_DOWN, pygame.K_KP2],
            "nav_left": [pygame.K_a, pygame.K_LEFT, pygame.K_KP4],
            "nav_right": [pygame.K_d, pygame.K_RIGHT, pygame.K_KP6],

            # Diagonal navigation (single keypad keys)
            "nav_up_left": [pygame.K_KP7],
            "nav_up_right": [pygame.K_KP9],
            "nav_down_left": [pygame.K_KP1],
            "nav_down_right": [pygame.K_KP3],

            "nav_toggle": [pygame.K_SPACE],  # Toggle navigation mode on/off

            # TODO: Add more action mappings as needed
            # "fire_weapon": [pygame.K_SPACE],
            # "raise_shields": [pygame.K_r],
            # "scan": [pygame.K_e],
        }

    def get_action(self, event):
        """
        Convert a pygame event to a game action

        Args:
            event: pygame.Event to process

        Returns:
            str: Action name if the event matches a binding, None otherwise

        Example:
            action = input_manager.get_action(event)
            if action == "menu_up":
                move_selection_up()
        """
        # Only process key down events
        if event.type != pygame.KEYDOWN:
            return None

        # Check each action mapping
        for action, keys in self.key_bindings.items():
            if event.key in keys:
                return action

        return None

    def is_key_pressed(self, action):
        """
        Check if a key for the given action is currently pressed

        Useful for continuous input (like ship movement)

        Args:
            action: Action name to check

        Returns:
            bool: True if any key bound to this action is pressed

        Example:
            if input_manager.is_key_pressed("nav_up"):
                move_ship_forward()
        """
        if action not in self.key_bindings:
            return False

        pressed_keys = pygame.key.get_pressed()
        for key in self.key_bindings[action]:
            if pressed_keys[key]:
                return True

        return False

    def add_binding(self, action, key):
        """
        Add a new key binding to an action

        Args:
            action: Action name
            key: pygame key constant (e.g., pygame.K_j)

        Example:
            # Add J as an alternative "up" key
            input_manager.add_binding("menu_up", pygame.K_j)
        """
        if action not in self.key_bindings:
            self.key_bindings[action] = []

        if key not in self.key_bindings[action]:
            self.key_bindings[action].append(key)

    def remove_binding(self, action, key):
        """
        Remove a key binding from an action

        Args:
            action: Action name
            key: pygame key constant to remove

        Example:
            # Remove W from menu_up
            input_manager.remove_binding("menu_up", pygame.K_w)
        """
        if action in self.key_bindings and key in self.key_bindings[action]:
            self.key_bindings[action].remove(key)

    def get_bindings_for_action(self, action):
        """
        Get all keys bound to an action

        Args:
            action: Action name

        Returns:
            list: List of pygame key constants, or empty list if action not found

        Example:
            keys = input_manager.get_bindings_for_action("menu_up")
            # Returns: [pygame.K_w, pygame.K_UP, pygame.K_KP8]
        """
        return self.key_bindings.get(action, [])

    def get_action_display_name(self, action):
        """
        Get a human-readable display name for the first key bound to an action

        Useful for showing controls to the player

        Args:
            action: Action name

        Returns:
            str: Display name of the first bound key, or "Unbound" if no keys

        Example:
            name = input_manager.get_action_display_name("confirm")
            # Returns: "RETURN" or "Enter"
        """
        keys = self.get_bindings_for_action(action)
        if not keys:
            return "Unbound"

        # Get the name of the first bound key
        return pygame.key.name(keys[0]).upper()

    def get_movement_vector(self):
        """
        Get the current movement direction as a normalized vector

        Checks for combined key presses to support diagonal movement.
        For example, W+A pressed together = moving up-left diagonally.

        Returns:
            tuple: (x, y) where each component is -1, 0, or 1
                   Returns (0, 0) if no movement keys are pressed

        Example:
            dx, dy = input_manager.get_movement_vector()
            ship_x += dx * speed * dt
            ship_y += dy * speed * dt

        Movement mapping:
            - nav_up or nav_up_left or nav_up_right: y = -1
            - nav_down or nav_down_left or nav_down_right: y = 1
            - nav_left or nav_up_left or nav_down_left: x = -1
            - nav_right or nav_up_right or nav_down_right: x = 1
        """
        dx = 0
        dy = 0

        # Check for diagonal keys first (numpad 1, 3, 7, 9)
        # These take priority over combined WASD/arrow keys
        if self.is_key_pressed("nav_up_left"):
            return (-1, -1)
        elif self.is_key_pressed("nav_up_right"):
            return (1, -1)
        elif self.is_key_pressed("nav_down_left"):
            return (-1, 1)
        elif self.is_key_pressed("nav_down_right"):
            return (1, 1)

        # Check cardinal directions (WASD/arrows/numpad 2468)
        # These can be combined for diagonals
        if self.is_key_pressed("nav_up"):
            dy = -1
        elif self.is_key_pressed("nav_down"):
            dy = 1

        if self.is_key_pressed("nav_left"):
            dx = -1
        elif self.is_key_pressed("nav_right"):
            dx = 1

        return (dx, dy)
