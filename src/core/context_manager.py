"""
Context Manager for handling navigation context transitions

Manages pushing/popping navigation contexts and calculating 
ship/player position during transitions between contexts
"""

import math
import utils.position_calculator as pos_calc

from core.constants import(
    CONTEXT_CENTER,
    CONTEXT_GRID_SIZE,
    BOUNDARY_INSET,
    INTERACTION_STATION,
    RENDER_SCALE,
    BOUNDARY_CLEARANCE
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

class ContextManager:
    """
    Manages navigation context transitions and calculations

    Responsibilities:
    - Handle context transitions (push/pop to the navigation stack)
    - Calculate ship/player positions during transitions
    - Validate transitions are legal from current context
    """    

    def __init__(self, navigation_stack=None):
        """
        Initialize context manager

        Args:
            navigation_stack: Optional initial navigation stack. If None, creates empty stack.
        """
        self.navigation_stack = navigation_stack if navigation_stack is not None else []

    def launch_from_dock(self, dock_coords, dock_radius):
        """
        Launch from docked state (station/orbit) into space.
        
        Calculates launch position to the east of the docked object,
        then updates ship position in current context.
        
        Args:
            dock_coords: [x, y] coordinates of the station/planet being launched from
            dock_radius: Collision radius of the docked object
        
        Returns:
            bool: True if launch successful
        """
        launch_pos = pos_calc.calculate_launch_position(
            dock_coords, dock_radius, BOUNDARY_CLEARANCE, 0)
        
        # Update ship position in current navigation context
        self.ship_position = [launch_pos[0], launch_pos[1]]

        return True

    def calculate_launch_position(self, interaction_data):
        """
        Calculate launch position from interaction data.
        
        Args:
            interaction_data: Dictionary with keys: type, planet_coords, planet_radius
        
        Returns:
            tuple: (success: bool, position: [x, y] or None)
        """
        # Validation
        if interaction_data is None:
            return (False, None)
        
        if interaction_data.get("type") != INTERACTION_STATION:
            return (False, None)
        
        # Extract data
        planet_coords = interaction_data.get("planet_coords")
        planet_radius = interaction_data.get("planet_radius")

        if planet_coords is None or planet_radius is None:
            return (False, None)
        
        # Calculate launch position using utility
        launch_post = pos_calc.calculate_launch_position(
            planet_coords, 
            planet_radius,
            BOUNDARY_CLEARANCE,
            0 #east
        )

        # Return the calculated position - DON'T modify state
        return (True, [int(launch_post[0]), int(launch_post[1])])

    def enter_context(self, context_type, target_coords, target_radius, **context_data):
        """
        Enter a new navigation context (generic method for any context type).
        
        Calculates ship entry position based on approach direction to target,
        then pushes new context onto navigation stack.
        
        Args:
            context_type: Type of context (CONTEXT_INNER_SYSTEM, CONTEXT_PLANETARY_SYSTEM, etc.)
            target_coords: [x, y] coordinates of the object being entered
            target_radius: Collision radius of target object (currently unused but kept for future)
            **context_data: Additional context-specific data (e.g., planet_index=4, region="outer_system")
        
        Returns:
            bool: True if entry successful, False otherwise
        """
        # Check if we're already in this context type; no duplicate inner systems
        if self.current_context and self.current_context.type == context_type:
            return False  # Already in this context, don't push duplicate
    
        # Calculate approach direction based on current ship position
        entry_direction = self._calculate_entry_direction(
            self.ship_position,
            target_coords
        )
        
        # Calculate where ship appears at edge of new context
        entry_position = self._calculate_entry_position(entry_direction)
        
        # Push new context onto stack
        self.navigation_stack.append(
            NavigationContext(
                context_type, 
                ship_coords=list(entry_position),
                parent_object_coords=target_coords,
                parent_object_radius=target_radius,
                **context_data
            )
        )
        
        return True
    
    def exit_context(self, exit_boundary, parent_object_coords, parent_object_radius):
        """
        Exit current context and return to parent context.
        
        Calculates ship position in parent context based on exit boundary,
        then pops current context from stack.
        
        Args:
            exit_boundary: Which boundary was crossed ("north", "south", "east", "west")
            parent_object_coords: [x, y] coordinates of the object in parent context
            parent_object_radius: Collision radius of the parent object
        
        Returns:
            bool: True if exit successful, False if already at base context
        """
        # Safety check: don't pop the base context/ hyperspace
        if len(self.navigation_stack) <= 2:
            return False
        
        # Calculate where ship should appear in parent context
        new_ship_coords = self._calculate_exit_position(
            exit_boundary,
            parent_object_coords,
            parent_object_radius
        )
        
        # Pop current context
        self.navigation_stack.pop()
        
        # Update ship position in parent context
        self.ship_position = list(new_ship_coords)
        
        return True

    def _calculate_entry_direction(self, ship_coords, object_coords):
        return pos_calc.get_cardinal_direction(ship_coords, object_coords)
        
    def _calculate_entry_position(self, entry_direction):
        """
        Calculates the entry position for a ship entering a context from given direction.

        Ship appears at the edge of the next context corresponding to the entry direction.

        Args:
            entry_direction: "north", "south", "east", or "west"

        returns:
            tuple: (ship_x, ship_y) - the new context position
        """
        entry_positions = {
            "north": (CONTEXT_CENTER, CONTEXT_GRID_SIZE - BOUNDARY_INSET), # Top edge, centered
            "south": (CONTEXT_CENTER, BOUNDARY_INSET),                      # Bottom edge, centered
            "east": (CONTEXT_GRID_SIZE - BOUNDARY_INSET, CONTEXT_CENTER),   # Right edge, centered
            "west": (BOUNDARY_INSET, CONTEXT_CENTER)                        # Left edge, centered
        }
        return entry_positions[entry_direction]
    
    def _calculate_exit_position(self, exit_boundary, object_coords, object_radius):
        """
        Calculate ship position in parent context when exiting via boundary.

        Ship appears just outside the central object of the context being exited,
        positioned at the angle corresponding to the exist boundary

        Args:
            exit_boundary: "north", "south", "east", or "west"
            object_coords: [x, y] of the central object in the context being exited
            object_radius: radius of the central object

        Returns:
            tuple: (ship_x, ship_y) - position in parent context
        """

        # Map boundary to angle in degrees (from coordinate_systems.md) 
        boundary_to_angle = {
            "east": 0, 
            "north": 90, 
            "west": 180,
            "south": 270            
        }
        angle_degrees = boundary_to_angle[exit_boundary]
        angle_radians = math.radians(angle_degrees)

        # Position ship at angle
        ship_radius = 11 / RENDER_SCALE  # Ship radius in game units
        distance = object_radius + BOUNDARY_CLEARANCE + ship_radius
        return pos_calc.polar_to_cartesian(
            object_coords[0], 
            object_coords[1],
            angle_degrees,
            distance
        )
    
    @property
    def current_context(self):
        """Returns the top of the navigation stack"""
        return self.navigation_stack[-1] if self.navigation_stack else None

    @property
    def ship_position(self):
        """Gets ship coordinates from current context"""
        ctx = self.current_context
        return ctx.data.get("ship_coords", [0, 0]) if ctx else [0, 0]

    @ship_position.setter
    def ship_position(self, value):
        """Sets ship coordinates in current context"""
        ctx = self.current_context
        if ctx:
            ctx.data["ship_coords"] = value