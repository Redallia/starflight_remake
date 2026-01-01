"""
Base class for game session
"""
from operator import index
from entities.ship import Ship
from entities.celestial_objects.star_system import StarSystem
from core.context_manager import ContextManager, NavigationContext

from .constants import (
    CONTEXT_HYPERSPACE,
    CONTEXT_OUTER_SYSTEM,
    CONTEXT_INNER_SYSTEM,
    CONTEXT_PLANETARY_SYSTEM,
    CONTEXT_SURFACE,
    CONTEXT_ENCOUNTER,
    CONTEXT_CENTER,
    INTERACTION_PLANET,
    INTERACTION_MOON,
    INTERACTION_ASTEROID,
    INTERACTION_STATION,
    LOCATION_STARPORT
)     

class GameSession:

    def __init__(self):
        """
        Build the context chain from top to bottom
        """
        self.home_system = StarSystem("data/systems/home_system.json")
        self.current_system = self.home_system

        # Find the planet with Starport (should be Homeworld)
        homeworld = None
        for planet in self.home_system.inner_planets:
            if planet and planet.has_starport():
                homeworld = planet
                break

        if homeworld is None:
            raise ValueError("No starport found in home system!")

        # Get homeworld coordinates
        homeworld_coords = homeworld.get_coordinates()
        homeworld_coords_list = [int(homeworld_coords[0]), int(homeworld_coords[1])]

        # Build initial navigation stack - player starts docked at Starport
        initial_stack = [
            NavigationContext(CONTEXT_HYPERSPACE, ship_coords=[125, 110]),
            NavigationContext(CONTEXT_OUTER_SYSTEM, ship_coords=[CONTEXT_CENTER, CONTEXT_CENTER]),
            NavigationContext(CONTEXT_INNER_SYSTEM, ship_coords=homeworld_coords_list)
        ]

        # Initialize context manager with the stack
        self.context_manager = ContextManager(navigation_stack=initial_stack)
        
        # Player starts at starport (docked)
        # TODO: This will eventually move to StarportState
        self.interaction_target = {
            "type": INTERACTION_STATION,
            "station_id": LOCATION_STARPORT,
            "planet_index": 1, # Homeworld is index 1
            "planet_coords": homeworld_coords_list,
            "planet_radius": homeworld.size
        }

        # Give the player a new ship
        self.player_ship = Ship(ship_id=0)

        # Message log for player feedback
        self.messages = [] # list of message strings
        self.max_messages = 20 # Keep the last 20 messages

    def get_current_context(self):
        """Return the current context"""
        return self.current_context

    def leave_current_context(self):
        """Move up one level in the nav hierarchy"""
        if len(self.context_manager.navigation_stack) > 1:
            return self.context_manager.navigation_stack.pop()
        return None

    def get_hyperspace_coordinates(self):
        """Return the hyperspace coordinates from the current context"""
        return self.context_manager.navigation_stack[0].data.get("ship_coords")
    
    def add_message(self, message):
        """
        Add a message to the message log.

        Args:
            message (str): The message to add to the log.
        """
        self.messages.append(message)

        # Keep only the most recent messages
        if len(self.messages) > self.max_messages:
            self.messages.pop(0) # Remove oldest message

    def set_interaction(self, target_type, **kwargs):
        """
        Set the current interaction target.

        Args:
            target_type (str): The type of interaction target.
            **kwargs: Additional data for the interaction.
        """
        self.interaction_target = {"type": target_type, **kwargs}

    def clear_interaction(self):
        """Clear interaction (return to navigation)"""
        self.interaction_target = None

    @property
    def current_context(self):
        """Returns the top of the navigation stack"""
        return self.context_manager.current_context

    @property
    def ship_position(self):
        """Gets ship coordinates from current context"""
        return self.context_manager.ship_position

    @ship_position.setter
    def ship_position(self, value):
        """Sets ship coordinates in current context"""
        self.context_manager.ship_position = value