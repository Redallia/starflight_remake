"""
Planet entity class
Represents celestial bodies (planets and moons) in star systems
"""

import math
import utils.position_calculator as pos_calc
from core.constants import SYSTEM_ORBITS, CONTEXT_CENTER


class Planet:
    """
    Represents a planet or moon in a star system.
    
    Planets are positioned on circular orbits around a central object.
    The orbital_index determines which orbit (0-3), and orbit_angle 
    determines position on that orbit (0-360 degrees).
    """
    
    def __init__(self, name, planet_type, orbit_angle, size, landable=True,
                 orbital_index=None, moons=None, stations=None):
        """
        Initialize a planet.

        Args:
            name (str): Planet name
            planet_type (str): Type of planet (rocky, gas_giant, terran, etc.)
            orbit_angle (float): Starting angle on orbit in degrees (0-360)
            size (int): Visual radius for rendering
            landable (bool): Whether the planet can be landed on
            orbital_index (int): Which orbital slot (0-3), set by parent system
            moons (list): List of Planet objects representing moons
            stations (list): List of station dicts (name, type) orbiting this planet
        """
        self.name = name # Useful, but not strictly necessary
        self.type = planet_type
        self.orbit_angle = orbit_angle
        self.size = size
        self.landable = landable
        self.orbital_index = orbital_index
        self.moons = moons or []
        self.stations = stations or []
    
    def has_starport(self):
        """
        Check if this planet has a starport station in orbit.

        Returns:
            bool: True if planet has a starport, False otherwise
        """
        return any(station.get("type") == "starport" for station in self.stations)

    def get_coordinates(self):
        """
        Calculate the planet's x,y coordinates based on its orbital position.

        Returns:
            tuple: (x, y) coordinates in context grid
        """
        if self.orbital_index is None:
            raise ValueError(f"Planet {self.name} has no orbital_index set")

        # Get orbital radius from constants
        orbit_radius = SYSTEM_ORBITS[self.orbital_index]
        return pos_calc.polar_to_cartesian(
            CONTEXT_CENTER,
            CONTEXT_CENTER,
            self.orbit_angle,
            orbit_radius
        )
    
    def __repr__(self):
        """String representation for debugging"""
        return f"Planet({self.name}, orbit={self.orbital_index}, angle={self.orbit_angle})"