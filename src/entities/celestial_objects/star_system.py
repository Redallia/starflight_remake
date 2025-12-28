"""
StarSystem entity class
Loads and manages star system data including planets and moons
"""

import json
from entities.celestial_objects.planet import Planet


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
        
        # Basic system info
        self.name = data["name"]
        self.hyperspace_coords = data["hyperspace_coords"]
        self.star = data["star"]
        
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
                    orbital_index=index
                )
                
                # Load moons if present
                if "moons" in planet_data:
                    planet.moons = self._load_moons(planet_data["moons"])
                
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
    
    def get_planets_for_context(self, context_type):
        """
        Get the list of planets visible in a given navigation context.
        
        Args:
            context_type (str): "inner_system", "outer_system", or "gas_giant_system"
        
        Returns:
            list: List of Planet objects (filters out None/empty orbits)
        """
        if context_type == "inner_system":
            return [p for p in self.inner_planets if p is not None]
        elif context_type == "outer_system":
            return [p for p in self.outer_planets if p is not None]
        # For gas giant system, caller would pass specific planet's moons
        return []
    
    def __repr__(self):
        """String representation for debugging"""
        return f"StarSystem({self.name}, {len([p for p in self.inner_planets if p])} inner, {len([p for p in self.outer_planets if p])} outer)"