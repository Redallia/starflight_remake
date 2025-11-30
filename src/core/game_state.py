"""
Game state management
Holds the current state of the game (ship, location, resources)
"""


class GameState:
    """Manages overall game state"""

    def __init__(self):
        # Ship resources
        self.fuel = 100.0  # Starting fuel
        self.max_fuel = 100.0
        self.credits = 1000  # Starting credits
        self.cargo_capacity = 50  # Max cargo space
        self.cargo_used = 0  # Current cargo used

        # Location
        self.location = "starport"  # starport, space, orbit, planet_surface

        # Cargo holds (dictionary of resource type -> quantity)
        self.cargo = {}

        # Ship position (movement grid: 500x500, only tracked in space)
        self.ship_x = 0  # Movement grid position
        self.ship_y = 0  # Movement grid position

        # Starport location (coordinate grid: 50x50)
        self.starport_coord_x = 25  # Center of system for now
        self.starport_coord_y = 25

        # Planets in current system (list of dicts)
        # For now, just the starport planet
        self.planets = [
            {
                'name': 'Starport',
                'coord_x': 25,
                'coord_y': 25,
                'radius': 3,  # In coordinate units
                'color': (150, 100, 200),  # Purple
                'type': 'starport'
            }
        ]

    def can_launch(self):
        """Check if ship has enough fuel to launch"""
        return self.fuel > 0

    def launch_to_space(self):
        """Launch from starport to space"""
        if self.location == "starport" and self.can_launch():
            self.location = "space"
            # Initialize ship position at starport coordinates (converted to movement grid)
            self.ship_x = self.starport_coord_x * 10
            self.ship_y = self.starport_coord_y * 10
            return True
        return False

    def return_to_starport(self):
        """Return to starport from space"""
        if self.location == "space":
            self.location = "starport"
            return True
        return False

    def get_cargo_free_space(self):
        """Get remaining cargo capacity"""
        return self.cargo_capacity - self.cargo_used

    def get_status_summary(self):
        """Get a summary of ship status for display"""
        return {
            "fuel": f"{self.fuel:.1f} / {self.max_fuel}",
            "credits": self.credits,
            "cargo": f"{self.cargo_used} / {self.cargo_capacity}",
            "location": self.location.replace("_", " ").title()
        }

    def get_coordinate_position(self):
        """Convert movement grid position to coordinate grid position

        Returns coordinates with 0,0 at bottom-left corner
        """
        coord_x = self.ship_x // 10
        # Flip Y-axis so 0 is at bottom (49 - y gives us bottom-left origin)
        coord_y = 49 - (self.ship_y // 10)
        return (coord_x, coord_y)

    def move_ship(self, dx, dy):
        """Move ship on movement grid (internal coordinates)

        Args:
            dx: Change in x position (movement grid units)
            dy: Change in y position (movement grid units)
        """
        self.ship_x += dx
        self.ship_y += dy

        # Clamp to coordinate grid boundaries (0-49 coordinates = 0-499 movement grid)
        # This keeps the ship within the playable coordinate system
        self.ship_x = max(0, min(499, self.ship_x))
        self.ship_y = max(0, min(499, self.ship_y))
