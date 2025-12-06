"""
Game state management
Holds the current state of the game (ship, location, resources)
"""
import json
import os
from entities.crew import CrewRoster
from entities.star_system import StarSystem
from entities.planet import Planet
from entities.starport import Starport


class GameState:
    """Manages overall game state"""

    def __init__(self, system_name="default_system"):
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

        # Current system (star system entity)
        self.current_star_system: StarSystem = None  # Set in _load_system_data

        # Orbit state
        self.orbiting_planet = None  # Which planet we're currently orbiting (Planet entity or dict for backward compat)

        # Backward compatibility: Keep planets as dict list
        self.planets = []  # Will be populated from star_system.bodies

        # Sensor scan data cache
        self.scanned_planets = {}  # Dictionary: planet_name -> SensorData

        # Crew roster
        self.crew_roster = CrewRoster()
        self.crew_roster.initialize_default_crew()

        # Load system data
        self._load_system_data(system_name)

        # Starport location (coordinate grid: 50x50)
        # Find starport planet to set coordinates
        starport_planet = next((p for p in self.planets if p['type'] == 'starport'), None)
        if starport_planet:
            self.starport_coord_x = starport_planet['coord_x']
            self.starport_coord_y = starport_planet['coord_y']
        else:
            # Fallback if no starport found
            self.starport_coord_x = 25
            self.starport_coord_y = 25

    def _load_system_data(self, system_name):
        """Load star system data from JSON file"""
        # Get path to data file
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        systems_file = os.path.join(data_dir, 'star_systems.json')

        try:
            with open(systems_file, 'r') as f:
                systems_data = json.load(f)

            # Get the requested system
            system_data = systems_data.get(system_name)
            if not system_data:
                raise ValueError(f"System '{system_name}' not found in star_systems.json")

            # Load as StarSystem entity
            self.current_star_system = StarSystem.from_dict(system_name, system_data)

            # Maintain backward compatibility: populate planets list with dicts
            self.planets = [body.to_dict() for body in self.current_star_system.bodies]

        except FileNotFoundError:
            print(f"Warning: Could not find {systems_file}, using default planets")
            # Fallback to hardcoded starport
            starport = Starport(
                name='Starport',
                coord_x=25,
                coord_y=25,
                radius=3,
                color=(150, 100, 200),
                seed=1000
            )
            self.current_star_system = StarSystem(name="Default System", bodies=[starport])
            self.planets = [starport.to_dict()]

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

    def enter_orbit(self, planet):
        """Enter orbit around a planet"""
        if self.location == "space":
            self.location = "orbit"
            self.orbiting_planet = planet
            return True
        return False

    def exit_orbit(self):
        """Exit orbit and return to space"""
        if self.location == "orbit":
            self.location = "space"
            self.orbiting_planet = None
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
