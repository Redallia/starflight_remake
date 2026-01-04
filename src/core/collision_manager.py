from utils.collision import point_in_circle
from core.constants import (
    CONTEXT_GRID_SIZE, 
    RENDER_SCALE
)

class CollisionManager:
    """
    Manages collision detection and tracking across the game.
    Acts as the interface between game states and collision utilities
    """

    def __init__(self):
        # Track recent collisions to prevent repeated trigger
        self.last_boundary_collision = None
        self.last_interactable_collision = None

    def check_interactable_collision(self, ship_x, ship_y, interactables, ship_radius=None):
        """
        Check if ship collides with any interactable object

        Args:
            ship_x, ship_y: Ship's current position (in game units)
            interactables: List of Interactable objects
            ship_radius: Radius of the ship in game units (defaults to 22px / RENDER_SCALE)

        Returns:
            Interactable object if collision detected, None otherwise
        """
        if ship_radius is None:
            # Ship sprite is 22 pixels, so radius is 11 pixels
            # Convert to game units
            ship_radius = 11 / RENDER_SCALE

        collision = None
        for interactable in interactables:
            if interactable.shape_type == "circle":
                collision_radius = interactable.shape_data["radius"] + ship_radius
                if point_in_circle(ship_x, ship_y, interactable.x, interactable.y, collision_radius):
                    collision = interactable
                    break
            elif interactable.shape_type == "rectangle":
                width = interactable.shape_data["width"]
                height = interactable.shape_data["height"]
                # Check rectangle collision (AABB)
                if (ship_x + ship_radius > interactable.x - width / 2 and
                    ship_x - ship_radius < interactable.x + width / 2 and
                    ship_y + ship_radius > interactable.y - height / 2 and
                    ship_y - ship_radius < interactable.y + height / 2):
                    collision = interactable
                    break

        # Track state to prevent repeated triggers
        if collision:
            if collision == self.last_interactable_collision:
                return None # Same interactable, don't trigger again
            else:
                self.last_interactable_collision = collision
                return collision
        else:
            self.last_interactable_collision = None
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
        
    
    def reset(self):
        """Clear all collision state (call when changing navigation contexts)"""
        self.last_boundary_collision = None
        self.last_interactable_collision = None