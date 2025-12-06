"""
Crew management entities
Defines crew members, roles, and roster management

MVP Stub: Simplified for basic crew action support only.
Full crew management (skills, health, progression) will be added later.
"""
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class ShipRole(Enum):
    """Ship station roles - positions on the bridge"""
    CAPTAIN = "Captain"
    SCIENCE_OFFICER = "Science Officer"
    NAVIGATOR = "Navigator"
    ENGINEER = "Engineer"
    COMMUNICATIONS = "Communications"
    DOCTOR = "Doctor"


@dataclass
class CrewMember:
    """
    Represents a crew member assigned to a ship role

    MVP Stub: Simplified crew member for basic crew action support.
    Skills, health, and progression will be implemented when needed.
    """
    name: str
    assigned_role: Optional[ShipRole] = None  # Current station assignment

    def can_perform_action(self) -> bool:
        """Check if crew member is available to act (MVP stub: always True)"""
        return True


class CrewRoster:
    """Manages the ship's crew roster and station assignments

    MVP Stub: Simplified to support crew actions only.
    Full crew management will be implemented when needed.
    """

    def __init__(self):
        self.station_assignments: dict[ShipRole, Optional[CrewMember]] = {
            role: None for role in ShipRole
        }

    def get_crew_at_station(self, role: ShipRole) -> Optional[CrewMember]:
        """Get crew member currently assigned to a station"""
        return self.station_assignments.get(role)

    def initialize_default_crew(self):
        """Initialize default crew at stations (MVP stub)"""
        # For MVP: Just create placeholder crew members at each station
        # Real crew management will be implemented later
        for role in ShipRole:
            # Create a simple crew member for each role
            crew = CrewMember(
                name=f"{role.value}",  # e.g., "Science Officer"
                assigned_role=role
            )
            self.station_assignments[role] = crew
