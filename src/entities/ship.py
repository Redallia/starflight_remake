"""
Ship entity class
"""

from typing import List, Optional

class Ship:
    """
    Represents a ship entity, whether player or NPC 

    This is a data container. Game systems will operate on ships, 
    rather than the ships themselves having complex behaviors.
    """

    def __init__(self, ship_id: int = 0):
        """
        Initialize a new ship
        
        Args:
            ship_id: Unique identifier for this ship

        Note: Creates a ship with a default "Survey Ship" configuration.
        Most values are placeholders for MVP, and will eventually be expanded for later.
        """
        # Core identity
        self.ship_id = ship_id
        
        # Ship details
        self.ship_name: str = ""
        self.ship_class: str = "Survey Ship"  # Ship class (e.g., "Survey", "Transport", "Frigate", etc.)
        self.ship_portrait: Optional[str] = None # Placeholder for later NPC ships, but mostly unusued
        
        # Resources
        self.fuel: int = 100 # placeholder, fuel will eventually be tracked as cargo
        self.max_fuel: int = 500
        self.cargo_capacity: int = 0 # placeholder, eventually move to a cargo pod model
        self.current_cargo: int = 0 # placeholder

        # Ship status
        self.hull_integrity: int = 100 # 0-100 percent
        # Equipment (placeholder for future implementation)
        self.engine_class: int = 1 # 1 to 5
        self.shield_class: int = 1 # 1 to 5
        self.armor_class: int = 1 # 1 to 5

        # Crew
        self.crew_roster: List[str] = []