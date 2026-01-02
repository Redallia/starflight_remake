from utils.collision import point_in_circle
from core.constants import CONTEXT_GRID_SIZE, CONTEXT_CENTER, CENTRAL_OBJECT_SIZE, RENDER_SCALE

class CollisionManager:
    """
    Manages collision detection and tracking across the game.
    Acts as the interface between game states and collision utilities
    """

    def __init__(self):
        # Track recent collisions to prevent repeated trigger
        self.last_planet_collision = None
        self.last_boundary_collision = None
        self.last_central_zone_collision = None
        

    def check_planet_collision(self, ship_x, ship_y, planets, ship_radius=None):
        """
        Check if ship collides with any planet

        Args:
            ship_x, ship_y: Ship's current position (in game units)
            planets: List of Planet objects
            ship_radius: Radius of the ship in game units (defaults to 22px / RENDER_SCALE)

        Returns:
            Planet object if collision detected, None otherwise
        """
        if ship_radius is None:
            # Ship sprite is 22 pixels, so radius is 11 pixels
            # Convert to game units
            ship_radius = 11 / RENDER_SCALE
        collision = None
        for planet in planets:
            if planet is None: # handle empty orbital slots
                continue

            planet_x, planet_y = planet.get_coordinates()
            collision_radius = planet.size + ship_radius

            if point_in_circle(ship_x, ship_y, planet_x, planet_y, collision_radius):
                collision = planet
                break

        # Track state to prevent repeated triggers
        if collision:
            if collision == self.last_planet_collision:
                return None # Same planet, don't trigger again
            else:
                self.last_planet_collision = collision
                return collision
        else:
            self.last_planet_collision = None
            return None
        
        
    
    def check_boundary_collision(self, ship_x, ship_y, grid_size=None):
        """
        Check if ship has reached the edge of current navigation context.

        Args:
            ship_x, ship_y: Ship position
            grid_size: Size of the navigation grid (defaults to CONTEXT_GRID_SIZE)

        Returns:
            String indicating which boundary was hit: "north", "south", "east", "west"
            Returns None if no boundary collision
        """
        if grid_size is None:
            grid_size = CONTEXT_GRID_SIZE

        collision = None
        if ship_x <= 0:
            collision = "west"
        elif ship_x >= grid_size:
            collision = "east"
        elif ship_y <= 0:
            collision ="south"
        elif ship_y >= grid_size:
            collision = "north"

        if collision:
            if collision == self.last_boundary_collision:
                return None
            else:
                self.last_boundary_collision = collision
                return collision
        else:
            self.last_boundary_collision = None
            return None    

    def check_central_zone_collision(self, ship_x, ship_y, center_x=None, center_y=None, zone_radius=None):
        """
        Check if ship has entered the central zone (for inner/outer system transitions).

        Args:
            ship_x, ship_y: Ship position
            center_x, center_y: Center of the zone (defaults to CONTEXT_CENTER)
            zone_radius: Radius of central zone (defaults to CENTRAL_OBJECT_SIZE)

        Returns:
            bool: True if inside central zone
        """
        if center_x is None:
            center_x = CONTEXT_CENTER
        if center_y is None:
            center_y = CONTEXT_CENTER
        if zone_radius is None:
            zone_radius = CENTRAL_OBJECT_SIZE

        collision = None
        if point_in_circle(ship_x, ship_y, center_x, center_y, zone_radius):
            collision = "central_zone"

        if collision:
            if collision == self.last_central_zone_collision:
                return None
            else:
                self.last_central_zone_collision = collision
                return collision
        
    
    def reset(self):
        """Clear all collision state (call when changing navigation contexts)"""
        self.last_planet_collision = None
        self.last_boundary_collision = None
        self.last_central_zone_collision = None