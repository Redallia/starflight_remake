"""
Base class for game session
"""
from entities.ship import Ship
from entities.celestial_objects.star_system import StarSystem

from .constants import (
    CONTEXT_HYPERSPACE,
    CONTEXT_LOCAL_SPACE,
    CONTEXT_ORBIT,
    CONTEXT_DOCKED,
    REGION_INNER_SYSTEM,
    REGION_OUTER_SYSTEM,
    REGION_GAS_GIANT,
    LOCATION_STARPORT

)


class NavigationContext:
    """
    Represents a single navigation context in the location hierarchy.
    Each context knows its type and parent, forming a linked chain.
    """
    
    def __init__(self, context_type, **kwargs):
        """
        Initializes a new NavigationContext.

        Args:
            context_type (str): The type of navigation context (e.g., "starport", "inner_system", "hyperspace", etc).
            **kwargs: Additional data associated with the context.
        """
        self.type = context_type
        self.data = kwargs
        

class GameSession:

    def __init__(self):
        """
        Build the context chain from top to bottom
        """
        self.navigation_stack = [
            NavigationContext(CONTEXT_HYPERSPACE, ship_coords=[125, 110]),
            NavigationContext(CONTEXT_LOCAL_SPACE, region=REGION_INNER_SYSTEM, ship_coords=[500, 500]),
            NavigationContext(CONTEXT_ORBIT, planet_index=3),
            NavigationContext(CONTEXT_DOCKED, location=LOCATION_STARPORT)
        ]
         # Load the home star system
        self.home_system = StarSystem("data/systems/home_system.json")
        self.current_system = self.home_system # Track what system we're currently in

        # Give the player a new ship
        self.player_ship = Ship(ship_id=0)

        # Message log for player feedback
        self.messages = [] # list of message strings
        self.max_messages = 20 # Keep the last 20 messages
        
        # For getting at current hyperspace coordinates
        self.hyperspace_context = self.navigation_stack[0]

    def get_visible_planets(self):
        """
        Get the list of planets visible in the current navigation context
        """
        if self.current_context.type == CONTEXT_LOCAL_SPACE:
            # Get the region from context data
            region = self.current_context.data.get("region")
            if region == REGION_INNER_SYSTEM:
                return self.current_system.get_planets_for_context("inner_system")
            elif region == REGION_OUTER_SYSTEM:
                return self.current_system.get_planets_for_context("outer_system")

        # No planets visible in other contexts (hyperspace, orbit, etc.)
        return []

    def get_current_context(self):
        """Return the current context"""
        return self.current_context

    def leave_current_context(self):
        """Move up one level in the nav hierarchy"""
        if len(self.navigation_stack) > 1:
            return self.navigation_stack.pop()
        return None
    
    def get_hyperspace_coordinates(self):
        """Return the hyperspace coordinates from the current context"""
        return self.navigation_stack[0].data.get("coords")
    
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

    @property
    def ship_position(self):
        return self.current_context.data.get("ship_coords", [0, 0])
    
    @property
    def current_context(self):
        """Returns the top of the navigation stack"""
        return self.navigation_stack[-1] if self.navigation_stack else None
    
    @ship_position.setter
    def ship_position(self, value):
        self.current_context.data["ship_coords"] = value