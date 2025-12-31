"""
Base class for game session
"""
from operator import index
from entities.ship import Ship
from entities.celestial_objects.star_system import StarSystem

from .constants import (
    CONTEXT_HYPERSPACE,
    CONTEXT_OUTER_SYSTEM,
    CONTEXT_INNER_SYSTEM,
    CONTEXT_PLANETARY_SYSTEM,
    CONTEXT_SURFACE,
    CONTEXT_ENCOUNTER,
    INTERACTION_PLANET,
    INTERACTION_MOON,
    INTERACTION_ASTEROID,
    INTERACTION_STATION,
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

        # Player starts docked at Starport
        self.navigation_stack = [
            NavigationContext(CONTEXT_HYPERSPACE, ship_coords=[125, 110]),
            NavigationContext(CONTEXT_INNER_SYSTEM, ship_coords=homeworld_coords_list)
        ]
        # Current interaction (None when freely navigation)
        # self.interaction_target = None

        # Player starts at starport (docked)
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
        
        # For getting at current hyperspace coordinates
        self.hyperspace_context = self.navigation_stack[0]



    def get_visible_planets(self):
        """
        Get the list of planets visible in the current navigation context
        """
        # Check specific context types
        if self.current_context.type == CONTEXT_INNER_SYSTEM:
            return self.current_system.get_planets_for_context("inner_system")
        elif self.current_context.type == CONTEXT_OUTER_SYSTEM:
            return self.current_system.get_planets_for_context("outer_system")
        elif self.current_context.type == CONTEXT_PLANETARY_SYSTEM:
            # Get Moons of the gas giant
            planet_index = self.current_context.data.get("planet_index")
            if planet_index is not None:
                # TODO: Return moons for this planet
                return []

    def get_current_context(self):
        """Return the current context"""
        return self.current_context

    def leave_current_context(self):
        """Move up one level in the nav hierarchy"""
        if len(self.navigation_stack) > 1:
            return self.navigation_stack.pop()
        return None

    def launch_from_dock(self):
        """
        Launch from docked state (e.g., Starbase) into space.

        Uses interaction_target data to calcuate launch position
        then clears the interaction to return to free navigation

        Returns:
            bool: True if launch successful, False if not in docked state
        """
        import math

        # Clearance distance for ship positioning
        BOUNDARY_CLEARANCE = 10

        # Safety check: are we docked?
        if self.interaction_target is None:
            return False

        if self.interaction_target.get("type") != INTERACTION_STATION:
            return False
        
        # Get planet info from interaction target
        planet_coords = self.interaction_target.get("planet_coords")
        planet_radius = self.interaction_target.get("planet_radius")

        if planet_coords is None or planet_radius is None:
            return False
    
        # Calculate launch position - ship appears to the east of planet
        launch_angle = 0 # 0 degrees - east
        distance = planet_radius + BOUNDARY_CLEARANCE

        ship_x = int(planet_coords[0] + math.cos(math.radians(launch_angle)) * distance)
        ship_y = int(planet_coords[1] + math.sin(math.radians(launch_angle)) * distance)

        # Update ship position in parent LOCAL_SPACE context
        self.ship_position = [ship_x, ship_y]

        # Clear interaction - move back to free navigation
        self.clear_interaction()
        
        return True

    def exit_inner_system(self, exit_boundary):
        """
        Exit from inner system to outer system via boundary.

        The inner system is represented by the central zone in the outer system,
        so exiting positions the ship just outside that central zone.

        Args:
            exit_boundary (str): Which boundary was crossed ("north", "south", "east", "west")

        Returns:
            bool: True if exit successful, False otherwise
        """
        import math
        from core.constants import CONTEXT_CENTER, CENTRAL_OBJECT_SIZE

        # Clearance distance for ship positioning
        BOUNDARY_CLEARANCE = 10

        # Safety check: are we in inner system?
        if not self.current_context or self.current_context.type != CONTEXT_INNER_SYSTEM:
            return False

        # Map boundary to angle (from coordinate_systems.md)
        boundary_to_angle = {
            "east": 0,      # 0°
            "north": 90,    # 90°
            "west": 180,    # 180°
            "south": 270    # 270°
        }

        if exit_boundary not in boundary_to_angle:
            return False

        angle_degrees = boundary_to_angle[exit_boundary]
        angle_radians = math.radians(angle_degrees)

        # Calculate ship position just outside the central zone in outer system
        distance = CENTRAL_OBJECT_SIZE + BOUNDARY_CLEARANCE
        ship_x = int(CONTEXT_CENTER + math.cos(angle_radians) * distance)
        ship_y = int(CONTEXT_CENTER + math.sin(angle_radians) * distance)

        # Pop inner system context
        self.navigation_stack.pop()

        # Check if outer system context exists (it might not on first exit)
        if self.current_context.type == CONTEXT_OUTER_SYSTEM:
            # Outer system already exists, just update ship position
            self.ship_position = [ship_x, ship_y]
        else:
            # Need to create outer system context
            self.navigation_stack.append(
                NavigationContext(CONTEXT_OUTER_SYSTEM, ship_coords=[ship_x, ship_y])
            )

        return True

    def enter_inner_system(self):
        """
        Enter inner system from outer system via central zone collision.

        Determines approach direction and positions ship at corresponding edge
        of inner system.

        Returns:
            bool: True if entry successful, False otherwise
        """
        from core.constants import CONTEXT_CENTER, CONTEXT_GRID_SIZE

        # Safety check: are we in outer system?
        if not self.current_context or self.current_context.type != CONTEXT_OUTER_SYSTEM:
            return False

        # Get current ship position to determine approach direction
        ship_x, ship_y = self.ship_position

        # Calculate approach direction from center
        dx = ship_x - CONTEXT_CENTER
        dy = ship_y - CONTEXT_CENTER

        # Determine dominant direction (cardinal)
        if abs(dx) > abs(dy):
            entry_direction = "west" if dx < 0 else "east"
        else:
            entry_direction = "south" if dy < 0 else "north"

        # Map entry direction to ship position at edge of inner system
        entry_positions = {
            "north": (CONTEXT_CENTER, CONTEXT_GRID_SIZE),  # Top edge
            "south": (CONTEXT_CENTER, 0),                   # Bottom edge
            "east": (CONTEXT_GRID_SIZE, CONTEXT_CENTER),   # Right edge
            "west": (0, CONTEXT_CENTER)                     # Left edge
        }

        new_ship_coords = entry_positions[entry_direction]

        # Push new inner system context
        self.navigation_stack.append(
            NavigationContext(CONTEXT_INNER_SYSTEM, ship_coords=list(new_ship_coords))
        )

        return True

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
    def ship_position(self):
        return self.current_context.data.get("ship_coords", [0, 0])
    
    @property
    def current_context(self):
        """Returns the top of the navigation stack"""
        return self.navigation_stack[-1] if self.navigation_stack else None
    
    @ship_position.setter
    def ship_position(self, value):
        self.current_context.data["ship_coords"] = value