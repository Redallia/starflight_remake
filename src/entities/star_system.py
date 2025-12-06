"""
Star system entity (collection of celestial bodies)
"""
from dataclasses import dataclass
from typing import Optional
from entities.celestial_body import CelestialBody
from entities.star import Star
from entities.planet import Planet
from entities.starport import Starport


@dataclass
class StarSystem:
    """Collection of celestial bodies in a star system"""
    name: str
    bodies: list[CelestialBody]

    def get_star(self) -> Optional[Star]:
        """Get primary star in system"""
        # In future, could support binary/multiple star systems
        return next((b for b in self.bodies if isinstance(b, Star)), None)

    def get_planets(self) -> list[Planet]:
        """Get all planets in system"""
        return [b for b in self.bodies if isinstance(b, Planet)]

    def get_starport(self) -> Optional[Starport]:
        """Get starport in system"""
        return next((b for b in self.bodies if isinstance(b, Starport)), None)

    def get_body_at(self, x: int, y: int) -> Optional[CelestialBody]:
        """
        Get celestial body at coordinates

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            CelestialBody if found at coordinates, None otherwise
        """
        for body in self.bodies:
            # Check if coordinates are within body's radius
            dx = abs(body.coord_x - x)
            dy = abs(body.coord_y - y)
            distance = (dx**2 + dy**2) ** 0.5
            if distance <= body.radius:
                return body
        return None

    def is_in_habitable_zone(self, planet: Planet) -> bool:
        """
        Check if planet is in star's habitable zone

        Args:
            planet: Planet to check

        Returns:
            True if planet is in habitable zone, False otherwise
        """
        star = self.get_star()
        if not star:
            return False

        # Calculate distance from star to planet
        dx = planet.coord_x - star.coord_x
        dy = planet.coord_y - star.coord_y
        distance = (dx**2 + dy**2) ** 0.5

        inner, outer = star.get_habitable_zone()
        return inner <= distance <= outer

    @staticmethod
    def from_dict(system_name: str, system_data: dict) -> 'StarSystem':
        """
        Create StarSystem from JSON data

        Args:
            system_name: Name of the star system
            system_data: Dictionary containing system configuration

        Returns:
            StarSystem entity
        """
        bodies = []

        # Load celestial bodies from JSON
        for body_data in system_data.get('bodies', system_data.get('planets', [])):
            body_type = body_data.get('type', 'planet')

            if body_type == 'star':
                from entities.star import StarClass
                star = Star(
                    name=body_data['name'],
                    coord_x=body_data['coord_x'],
                    coord_y=body_data['coord_y'],
                    radius=body_data['radius'],
                    color=tuple(body_data['color']) if isinstance(body_data['color'], list) else body_data['color'],
                    seed=body_data['seed'],
                    star_class=StarClass(body_data['star_class']),
                    temperature=body_data['temperature'],
                    luminosity=body_data['luminosity'],
                )
                bodies.append(star)
            elif body_type == 'starport':
                starport = Starport.from_dict(body_data)
                bodies.append(starport)
            else:
                # Planet types: magma, rocky, liquid, frozen, gas_giant
                planet = Planet.from_dict(body_data)
                bodies.append(planet)

        return StarSystem(name=system_name, bodies=bodies)
