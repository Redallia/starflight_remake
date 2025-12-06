"""
Ship entities - player and NPC ships
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class ShipClass(Enum):
    """Ship classification/design"""
    TERRAN_SCOUT = "terran_scout"          # Human scout ship (player default)
    TERRAN_FREIGHTER = "terran_freighter"  # Human cargo hauler
    TERRAN_WARSHIP = "terran_warship"      # Human combat vessel
    # Future: Alien ship types
    # VELOXI_JAVELIN = "veloxi_javelin"
    # THRYNN_DESTROYER = "thrynn_destroyer"
    # etc.


class Species(Enum):
    """Species that build/operate ships"""
    HUMAN = "human"
    STARPORT = "starport"  # Special case for stations
    # Future alien species
    # VELOXI = "veloxi"
    # THRYNN = "thrynn"
    # G_NOK = "g_nok"
    # etc.


@dataclass
class ShipStats:
    """Ship capabilities and specifications"""
    max_fuel: float = 100.0
    max_cargo: int = 50
    max_crew: int = 6
    max_armor: int = 100
    max_shields: int = 0
    weapon_slots: int = 0
    engine_power: float = 1.0  # Movement speed multiplier


@dataclass
class Ship(ABC):
    """Base class for all ships (player and NPC)"""
    name: str
    ship_class: ShipClass
    species: Species
    stats: ShipStats

    # Current ship state
    fuel: float = 100.0
    cargo_used: int = 0
    armor: int = 100
    shields: int = 0

    # Position (movement grid coordinates)
    x: float = 0.0
    y: float = 0.0

    # Cargo holds (resource_type -> quantity)
    cargo: dict = field(default_factory=dict)

    def can_move(self) -> bool:
        """Check if ship has fuel to move"""
        return self.fuel > 0

    def get_cargo_free_space(self) -> int:
        """Get remaining cargo capacity"""
        return self.stats.max_cargo - self.cargo_used

    def add_cargo(self, resource: str, quantity: int) -> bool:
        """
        Add cargo to ship

        Returns:
            True if cargo was added, False if insufficient space
        """
        if quantity > self.get_cargo_free_space():
            return False

        self.cargo[resource] = self.cargo.get(resource, 0) + quantity
        self.cargo_used += quantity
        return True

    def remove_cargo(self, resource: str, quantity: int) -> bool:
        """
        Remove cargo from ship

        Returns:
            True if cargo was removed, False if insufficient quantity
        """
        current = self.cargo.get(resource, 0)
        if current < quantity:
            return False

        self.cargo[resource] = current - quantity
        self.cargo_used -= quantity

        # Remove empty entries
        if self.cargo[resource] == 0:
            del self.cargo[resource]

        return True

    def consume_fuel(self, amount: float) -> bool:
        """
        Consume fuel

        Returns:
            True if fuel was consumed, False if insufficient fuel
        """
        if self.fuel < amount:
            return False

        self.fuel -= amount
        return True

    def refuel(self, amount: float):
        """Add fuel (capped at max_fuel)"""
        self.fuel = min(self.stats.max_fuel, self.fuel + amount)

    def get_position(self) -> tuple[float, float]:
        """Get ship position"""
        return (self.x, self.y)

    def set_position(self, x: float, y: float):
        """Set ship position"""
        self.x = x
        self.y = y


@dataclass
class PlayerShip(Ship):
    """Player-controlled ship with additional game state"""
    credits: int = 1000  # Player money

    # Additional player-specific state could go here:
    # - Installed modules/upgrades
    # - Reputation with factions
    # - Quest flags
    # etc.

    def can_afford(self, cost: int) -> bool:
        """Check if player can afford a purchase"""
        return self.credits >= cost

    def spend_credits(self, amount: int) -> bool:
        """
        Spend credits

        Returns:
            True if credits were spent, False if insufficient funds
        """
        if not self.can_afford(amount):
            return False

        self.credits -= amount
        return True

    def earn_credits(self, amount: int):
        """Add credits"""
        self.credits += amount


# Ship factory functions for common configurations

def create_terran_scout(name: str = "Starflight") -> PlayerShip:
    """Create default Terran scout ship (player starting ship)"""
    stats = ShipStats(
        max_fuel=100.0,
        max_cargo=50,
        max_crew=6,
        max_armor=100,
        max_shields=0,
        weapon_slots=2,
        engine_power=1.0
    )

    return PlayerShip(
        name=name,
        ship_class=ShipClass.TERRAN_SCOUT,
        species=Species.HUMAN,
        stats=stats,
        fuel=100.0,
        armor=100,
        credits=1000
    )


def create_terran_freighter(name: str = "Hauler") -> Ship:
    """Create Terran freighter (high cargo, slow)"""
    stats = ShipStats(
        max_fuel=120.0,
        max_cargo=200,  # Much more cargo
        max_crew=4,
        max_armor=80,
        max_shields=0,
        weapon_slots=1,
        engine_power=0.7  # Slower
    )

    return Ship(
        name=name,
        ship_class=ShipClass.TERRAN_FREIGHTER,
        species=Species.HUMAN,
        stats=stats,
        fuel=120.0,
        armor=80
    )


def create_terran_warship(name: str = "Defender") -> Ship:
    """Create Terran warship (combat focused)"""
    stats = ShipStats(
        max_fuel=100.0,
        max_cargo=30,
        max_crew=8,
        max_armor=150,
        max_shields=100,
        weapon_slots=4,
        engine_power=1.2  # Faster
    )

    return Ship(
        name=name,
        ship_class=ShipClass.TERRAN_WARSHIP,
        species=Species.HUMAN,
        stats=stats,
        fuel=100.0,
        armor=150,
        shields=100
    )
