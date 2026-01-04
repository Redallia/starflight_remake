"""
StarSystem entity class
Loads and manages star system data including planets and moons
"""

import json
from entities.celestial_objects.planet import Planet
from entities.celestial_objects.star import Star
from core.constants import (
    CONTEXT_OUTER_SYSTEM,
    CONTEXT_INNER_SYSTEM,
    CONTEXT_PLANETARY_SYSTEM,
    CENTRAL_OBJECT_SIZE,
    INNER_ZONE_MULTIPLIER
)

class StarSystem:
    """
    Represents a complete star system with inner planets, outer planets, and a central star.
    
    Loads system data from JSON and creates Planet objects with proper orbital indices.
    """
    
    def __init__(self, system_data_path):
        """
        Load a star system from a JSON file.
        
        Args:
            system_data_path (str): Path to the system JSON file
        """
        # Load JSON data
        with open(system_data_path, 'r') as f:
            data = json.load(f)
        
        # Create Star Object
        star_data = data["star"]
        self.star = Star(
            name = star_data["name"],
            spectral_class=star_data["spectral_class"],
            size=star_data.get("size", CENTRAL_OBJECT_SIZE) # Default to scaled constant
        )
        
        # Load planets (with orbital indices set)
        self.inner_planets = self._load_planets(data.get("inner_planets", []))
        self.outer_planets = self._load_planets(data.get("outer_planets", []))
    
    def _load_planets(self, planet_list):
        """
        Load a list of planets from JSON data, setting orbital indices.
        
        Args:
            planet_list (list): List of planet data dicts (or None for empty orbits)
        
        Returns:
            list: List of Planet objects (or None for empty orbits)
        """
        planets = []
        for index, planet_data in enumerate(planet_list):
            if planet_data is None:
                # Empty orbital slot
                planets.append(None)
            else:
                # Create planet with orbital index
                planet = Planet(
                    name=planet_data["name"],
                    planet_type=planet_data["type"],
                    orbit_angle=planet_data["orbit_angle"],
                    size=planet_data["size"],
                    landable=planet_data.get("landable", True),
                    orbital_index=index,
                    stations=planet_data.get("stations", [])
                )

                # Load moons if present
                if "moons" in planet_data:
                    planet.moons = self._load_moons(planet_data["moons"])
                    planet.planetary_system = True

                planets.append(planet)
        
        return planets
    
    def _load_moons(self, moon_list):
        """
        Load moons for a planet (similar to planets, but for moons).
        
        Args:
            moon_list (list): List of moon data dicts
        
        Returns:
            list: List of Planet objects representing moons
        """
        moons = []
        for index, moon_data in enumerate(moon_list):
            moon = Planet(
                name=moon_data["name"],
                planet_type=moon_data["type"],
                orbit_angle=moon_data["orbit_angle"],
                size=moon_data["size"],
                landable=moon_data.get("landable", True),
                orbital_index=index
            )
            moons.append(moon)
        
        return moons
    
    def get_planets_for_context(self, context_type, context_data=None):
        """
        Get the list of planets visible in a given navigation context.

        Args:
            context_type: CONTEXT_INNER_SYSTEM, CONTEXT_OUTER_SYSTEM, or CONTEXT_PLANETARY_SYSTEM
            context_data: Optional dict with 'parent_region' and 'planet_index' for planetary systems

        Returns:
            list: List of Planet objects visible in this context
        """
        if context_type == CONTEXT_INNER_SYSTEM:
            return [p for p in self.inner_planets if p is not None]

        elif context_type == CONTEXT_OUTER_SYSTEM:
            return [p for p in self.outer_planets if p is not None]

        elif context_type == CONTEXT_PLANETARY_SYSTEM:
            # Need to know which planet's moons to return
            if not context_data:
                return []

            parent_region = context_data.get("parent_region")
            planet_index = context_data.get("planet_index")

            if parent_region is None or planet_index is None:
                return []

            # Select the correct planet array based on parent region
            if parent_region == CONTEXT_INNER_SYSTEM:
                planet_list = self.inner_planets
            elif parent_region == CONTEXT_OUTER_SYSTEM:
                planet_list = self.outer_planets
            else:
                return []

            # Get the planet at that index
            if 0 <= planet_index < len(planet_list) and planet_list[planet_index]:
                planet = planet_list[planet_index]
                if hasattr(planet, 'moons') and planet.moons:
                    return planet.moons

            return []

        return []
    
    @property
    def inner_zone_radius(self):
        """Collision radius for inner system transition zone"""
        return self.star.size * INNER_ZONE_MULTIPLIER
    
    def __repr__(self):
        """String representation for debugging"""
        return f"StarSystem({self.name}, {len([p for p in self.inner_planets if p])} inner, {len([p for p in self.outer_planets if p])} outer)"