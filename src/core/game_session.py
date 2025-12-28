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
    
    def __init__(self, context_type, parent=None, **kwargs):
        """
        Initializes a new NavigationContext.

        Args:
            context_type (str): The type of navigation context (e.g., "starport", "inner_system", "hyperspace", etc).
            parent (NavigationContext): The parent navigation context.
            **kwargs: Additional data associated with the context.
        """
        self.type = context_type
        self.parent = parent
        self.data = kwargs
        

class GameSession:
    """
    Build the context chain from top to bottom
    """

    def __init__(self):
        # Let's start us off at Starport 
        hyperspace_ctx = NavigationContext(CONTEXT_HYPERSPACE, parent=None, ship_coords=[125, 110])
        local_space_ctx = NavigationContext(CONTEXT_LOCAL_SPACE, parent=hyperspace_ctx, region=REGION_INNER_SYSTEM, ship_coords=[500, 500])
        orbit_context = NavigationContext(CONTEXT_ORBIT, parent=local_space_ctx, planet_index=3)
        docked_ctx = NavigationContext(CONTEXT_DOCKED, parent=orbit_context, location=LOCATION_STARPORT)

         # Load the home star system
        self.home_system = StarSystem("data/systems/home_system.json")
        self.current_system = self.home_system # Track what system we're currently in

        # For a new game, player is currently docked at Starport
        self.current_context = docked_ctx

        # Give the player a new ship
        self.player_ship = Ship(ship_id=0)
        
        # For getting at current hyperspace coordinates
        self.hyperspace_context = hyperspace_ctx

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
        if self.current_context.parent:
            self.current_context = self.current_context.parent
    
    def get_hyperspace_coordinates(self):
        """Return the hyperspace coordinates from the current context"""
        return self.hyperspace_context.data.get("coords")
    
    @property
    def ship_position(self):
        return self.current_context.data.get("ship_coords", [0, 0])
    
    @ship_position.setter
    def ship_position(self, value):
        self.current_context.data["ship_coords"] = value

        