"""
Crew management entities
Defines crew members, roles, skills, and roster management
"""
from enum import Enum
from dataclasses import dataclass, field
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
class CrewSkills:
    """Crew member skill levels (0-100)"""
    science: int = 50
    navigation: int = 50
    engineering: int = 50
    communications: int = 50
    medical: int = 50
    combat: int = 50

    def get_skill(self, skill_name: str) -> int:
        """Get skill value by name"""
        return getattr(self, skill_name, 0)


class CrewMemberState(Enum):
    """Current state of crew member"""
    READY = "ready"           # Available for duty
    BUSY = "busy"             # Currently executing action
    INJURED = "injured"       # Injured, reduced effectiveness
    INCAPACITATED = "incapacitated"  # Cannot perform actions


@dataclass
class CrewMember:
    """
    Represents a crew member - a generic person who can fill ship roles

    Crew members are NOT tied to specific roles. They're individuals with
    skills who can be assigned to any station. A skilled scientist can work
    the helm in an emergency (just not as well as a trained navigator).
    """
    name: str
    skills: CrewSkills = field(default_factory=CrewSkills)
    state: CrewMemberState = CrewMemberState.READY
    health: int = 100  # 0-100
    fatigue: int = 0   # 0-100, higher = more tired
    assigned_role: Optional[ShipRole] = None  # Current station assignment

    def can_perform_action(self) -> bool:
        """Check if crew member is available to act"""
        return self.state in (CrewMemberState.READY, CrewMemberState.BUSY)

    def get_skill_for_role(self, role: ShipRole) -> int:
        """Get skill level relevant to a ship role"""
        skill_map = {
            ShipRole.SCIENCE_OFFICER: self.skills.science,
            ShipRole.NAVIGATOR: self.skills.navigation,
            ShipRole.ENGINEER: self.skills.engineering,
            ShipRole.COMMUNICATIONS: self.skills.communications,
            ShipRole.DOCTOR: self.skills.medical,
            ShipRole.CAPTAIN: max(self.skills.science, self.skills.navigation,
                                 self.skills.engineering, self.skills.communications)
        }
        return skill_map.get(role, 50)

    def get_effectiveness(self, role: ShipRole) -> float:
        """
        Get effectiveness multiplier for performing a role (0.0-1.0)

        Accounts for:
        - Skill level
        - Health
        - Fatigue
        - State (injured, etc.)
        """
        base_skill = self.get_skill_for_role(role) / 100.0
        health_factor = self.health / 100.0
        fatigue_factor = 1.0 - (self.fatigue / 200.0)  # Fatigue has less impact

        # State penalties
        state_factor = 1.0
        if self.state == CrewMemberState.INJURED:
            state_factor = 0.5
        elif self.state == CrewMemberState.INCAPACITATED:
            state_factor = 0.0

        return base_skill * health_factor * fatigue_factor * state_factor


class CrewRoster:
    """Manages the ship's crew roster and station assignments"""

    def __init__(self):
        self.crew_members: list[CrewMember] = []
        self.station_assignments: dict[ShipRole, Optional[CrewMember]] = {
            role: None for role in ShipRole
        }

    def add_crew_member(self, crew_member: CrewMember):
        """Add a crew member to the roster"""
        self.crew_members.append(crew_member)

    def assign_to_station(self, crew_member: CrewMember, role: ShipRole):
        """Assign crew member to a ship station"""
        # Remove from old assignment
        if crew_member.assigned_role:
            self.station_assignments[crew_member.assigned_role] = None

        # Remove whoever was at this station
        old_crew = self.station_assignments.get(role)
        if old_crew:
            old_crew.assigned_role = None

        # Assign to new station
        crew_member.assigned_role = role
        self.station_assignments[role] = crew_member

    def get_crew_at_station(self, role: ShipRole) -> Optional[CrewMember]:
        """Get crew member currently assigned to a station"""
        return self.station_assignments.get(role)

    def get_available_crew(self) -> list[CrewMember]:
        """Get crew members not currently assigned to stations"""
        assigned = set(self.station_assignments.values())
        return [c for c in self.crew_members if c not in assigned and c.can_perform_action()]

    def initialize_default_crew(self):
        """Initialize a default crew roster for new game"""
        # Create default crew members with varied skills
        default_crew = [
            CrewMember(
                name="Captain Hayes",
                skills=CrewSkills(
                    science=65,
                    navigation=70,
                    engineering=60,
                    communications=75,
                    medical=50,
                    combat=80
                ),
                assigned_role=ShipRole.CAPTAIN
            ),
            CrewMember(
                name="Dr. Sarah Chen",
                skills=CrewSkills(
                    science=90,
                    navigation=40,
                    engineering=55,
                    communications=60,
                    medical=70,
                    combat=30
                ),
                assigned_role=ShipRole.SCIENCE_OFFICER
            ),
            CrewMember(
                name="Lt. Marcus Kim",
                skills=CrewSkills(
                    science=45,
                    navigation=85,
                    engineering=60,
                    communications=55,
                    medical=40,
                    combat=70
                ),
                assigned_role=ShipRole.NAVIGATOR
            ),
            CrewMember(
                name="Chief Alexei Volkov",
                skills=CrewSkills(
                    science=50,
                    navigation=55,
                    engineering=95,
                    communications=45,
                    medical=50,
                    combat=65
                ),
                assigned_role=ShipRole.ENGINEER
            ),
            CrewMember(
                name="Ens. Amara Okafor",
                skills=CrewSkills(
                    science=55,
                    navigation=50,
                    engineering=45,
                    communications=80,
                    medical=40,
                    combat=55
                ),
                assigned_role=ShipRole.COMMUNICATIONS
            ),
            CrewMember(
                name="Dr. James Park",
                skills=CrewSkills(
                    science=65,
                    navigation=35,
                    engineering=40,
                    communications=50,
                    medical=95,
                    combat=40
                ),
                assigned_role=ShipRole.DOCTOR
            )
        ]

        # Add all crew and assign to stations
        for crew in default_crew:
            self.add_crew_member(crew)
            if crew.assigned_role:
                self.station_assignments[crew.assigned_role] = crew
