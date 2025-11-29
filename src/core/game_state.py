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

    def can_launch(self):
        """Check if ship has enough fuel to launch"""
        return self.fuel > 0

    def launch_to_space(self):
        """Launch from starport to space"""
        if self.location == "starport" and self.can_launch():
            self.location = "space"
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
