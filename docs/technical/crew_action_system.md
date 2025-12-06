# Crew Action System Architecture

## Overview

The crew action system provides a centralized, extensible framework for defining and executing crew member actions across all game screens. This separates game logic from UI code and enables reusable, testable action implementations.

## Problem Statement

### Current Issues

The initial implementation scattered action logic across screen files:
- Action execution logic embedded in `orbit_screen.py` (e.g., 32-line `_perform_sensor_scan()` method)
- String-based action matching (`if action == "Sensors":`) with no type safety
- No ability to reuse actions across different screens
- No crew entity representation - roles are just UI strings
- Violates separation of concerns - UI code contains game logic
- Difficult to test actions without instantiating entire screens
- No support for prerequisites, skill checks, or crew state

### Scalability Concerns

With 20-30+ planned actions across 5+ screens (orbit, space, planet surface, combat, communications), the current approach would lead to:
- Massive duplication of action-handling boilerplate
- Inconsistent behavior between similar actions
- Unmaintainable 500+ line screen files
- No path to advanced features (crew skills, fatigue, upgrades)

## Design Principles

1. **Separation of Concerns**: UI handles input/rendering, systems handle game logic
2. **Single Responsibility**: Each action class does one thing well
3. **Open/Closed**: Easy to add new actions without modifying existing code
4. **Dependency Injection**: Actions receive context (game state, HUD manager) rather than importing globally
5. **Testability**: Actions can be tested independently of UI
6. **Data-Driven**: Action definitions and crew roles eventually loadable from config files

## Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         UI Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ OrbitScreen  │  │ SpaceScreen  │  │ SurfaceScreen│      │
│  │              │  │              │  │              │      │
│  │ - Input      │  │ - Input      │  │ - Input      │      │
│  │ - Rendering  │  │ - Rendering  │  │ - Rendering  │      │
│  │ - Menus      │  │ - Menus      │  │ - Menus      │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
│         └──────────────────┼──────────────────┘              │
│                            │                                 │
└────────────────────────────┼─────────────────────────────────┘
                             │
                    ┌────────▼─────────┐
                    │  Action Request  │
                    │  (action_id,     │
                    │   context)       │
                    └────────┬─────────┘
                             │
┌────────────────────────────┼─────────────────────────────────┐
│                    Systems Layer                              │
│                    ┌────────▼─────────┐                       │
│                    │ CrewActionSystem │                       │
│                    │                  │                       │
│                    │ - Registry       │                       │
│                    │ - Validation     │                       │
│                    │ - Execution      │                       │
│                    └────────┬─────────┘                       │
│                             │                                 │
│         ┌───────────────────┼───────────────────┐            │
│         │                   │                   │            │
│    ┌────▼─────┐      ┌──────▼──────┐    ┌──────▼──────┐    │
│    │Navigation│      │   Science   │    │ Engineering │    │
│    │ Actions  │      │   Actions   │    │   Actions   │    │
│    │          │      │             │    │             │    │
│    │ -LeaveOrb│      │ -SensorScan │    │ -RepairSys  │    │
│    │ -SetCours│      │ -AnalyzeAno │    │ -PowerAlloc │    │
│    └──────────┘      └─────────────┘    └─────────────┘    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────┼─────────────────────────────────┐
│                     Core/Data Layer                           │
│                    ┌────────▼─────────┐                       │
│                    │    GameState     │                       │
│                    │                  │                       │
│                    │ - Crew roster    │                       │
│                    │ - Ship state     │                       │
│                    │ - Location       │                       │
│                    └──────────────────┘                       │
│                                                               │
│         ┌──────────────────┐        ┌──────────────────┐    │
│         │  CrewMember      │        │  ActionContext   │    │
│         │                  │        │                  │    │
│         │  - role          │        │  - game_state    │    │
│         │  - name          │        │  - screen_mgr    │    │
│         │  - skills        │        │  - hud_manager   │    │
│         │  - state         │        │  - initiator     │    │
│         └──────────────────┘        └──────────────────┘    │
└───────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
src/
├── entities/
│   └── crew.py                      # CrewMember, CrewRole classes
│
├── systems/
│   ├── crew_action_system.py       # Main action registry and executor
│   └── crew_actions/
│       ├── __init__.py
│       ├── base_action.py          # BaseAction abstract class
│       ├── navigation_actions.py   # LeaveOrbitAction, SetCourseAction, etc.
│       ├── science_actions.py      # SensorScanAction, AnalyzeAction, etc.
│       ├── engineering_actions.py  # RepairAction, PowerAllocationAction, etc.
│       ├── communications_actions.py
│       └── medical_actions.py
│
├── core/
│   └── game_state.py               # Add crew roster
│
└── ui/
    └── screens/
        ├── orbit_screen.py         # Simplified - delegates to action system
        └── space_screen.py         # Uses same action system
```

## Component Specifications

### 1. CrewMember Entity (`src/entities/crew.py`)

Represents an individual crew member with skills and state. Crew members are generic - they can be assigned to any ship role based on their skills.

**Design Philosophy:**
- Crew members are **people**, not job titles
- Ship roles are **positions** that crew members fill
- Any crew member can work any station (with varying effectiveness based on skills)
- Better crew management: hire specialists, cross-train generalists, handle casualties

```python
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
    DECEASED = "deceased" # Cannot be revived

@dataclass
class CrewMember:
    """
    Represents a crew member - a generic person who can fill ship roles

    Crew members are NOT tied to specific roles. They're individuals with
    skills who can be assigned to any station. A skilled scientist can work
    the helm in an emergency (just not as well as a trained navigator).
    """
    name: str
    skills: CrewSkills
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
```

### 2. Action Context (`src/systems/crew_action_system.py`)

Provides context for action execution without tight coupling.

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class ActionContext:
    """Context provided to actions during execution"""
    game_state: 'GameState'           # Current game state
    screen_manager: 'ScreenManager'   # For screen transitions
    hud_manager: Optional['HUDManager'] = None  # For messages/UI updates
    initiating_crew: Optional['CrewMember'] = None  # Who triggered action

    # Screen-specific context (can be extended)
    extra_data: dict = None  # For screen-specific parameters
```

### 3. Base Action Class (`src/systems/crew_actions/base_action.py`)

Abstract base class for all crew actions.

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from entities.crew import ShipRole

class ActionResult:
    """Result of action execution"""
    def __init__(self, success: bool, message: str = "", data: dict = None):
        self.success = success
        self.message = message
        self.data = data or {}

class BaseAction(ABC):
    """Base class for all crew actions"""

    def __init__(self):
        self.action_id: str = ""          # Unique identifier
        self.display_name: str = ""       # UI display text
        self.description: str = ""        # Tooltip/help text
        self.required_roles: List[ShipRole] = []  # Ship stations that can perform
        self.required_location: List[str] = []    # Valid game locations
        self.skill_check: Optional[str] = None    # Skill to check (if any)
        self.skill_threshold: int = 0             # Minimum skill required

    def can_execute(self, context: ActionContext) -> tuple[bool, str]:
        """
        Check if action can be executed in current context

        Returns:
            (can_execute, reason_if_not)
        """
        # Check location
        if self.required_location and context.game_state.location not in self.required_location:
            return False, f"Must be in {', '.join(self.required_location)}"

        # Check crew role assignment
        if self.required_roles and context.initiating_crew:
            if context.initiating_crew.assigned_role not in self.required_roles:
                roles_str = ', '.join(r.value for r in self.required_roles)
                return False, f"Requires {roles_str}"

        # Check crew state
        if context.initiating_crew and not context.initiating_crew.can_perform_action():
            return False, f"{context.initiating_crew.name} is {context.initiating_crew.state.value}"

        # Check skill requirement
        if self.skill_check and self.skill_threshold > 0 and context.initiating_crew:
            skill_value = getattr(context.initiating_crew.skills, self.skill_check, 0)
            if skill_value < self.skill_threshold:
                return False, f"Requires {self.skill_check} skill {self.skill_threshold}+"

        # Subclass-specific checks
        return self._can_execute_impl(context)

    @abstractmethod
    def _can_execute_impl(self, context: ActionContext) -> tuple[bool, str]:
        """Subclass-specific validation logic"""
        pass

    @abstractmethod
    def execute(self, context: ActionContext) -> ActionResult:
        """Execute the action and return result"""
        pass

    def get_display_name(self, context: ActionContext) -> str:
        """Get display name (can be context-dependent)"""
        return self.display_name
```

### 4. Crew Action System (`src/systems/crew_action_system.py`)

Central registry and executor for all crew actions.

```python
from typing import Dict, List, Optional
from entities.crew import ShipRole
from systems.crew_actions.base_action import BaseAction, ActionContext, ActionResult

class CrewActionSystem:
    """Manages crew action registration and execution"""

    def __init__(self):
        self._actions: Dict[str, BaseAction] = {}
        self._actions_by_role: Dict[ShipRole, List[str]] = {
            role: [] for role in ShipRole
        }

    def register_action(self, action: BaseAction):
        """Register an action in the system"""
        self._actions[action.action_id] = action

        # Index by role for quick lookup
        for role in action.required_roles:
            if action.action_id not in self._actions_by_role[role]:
                self._actions_by_role[role].append(action.action_id)

    def get_actions_for_role(self, role: ShipRole, context: ActionContext) -> List[BaseAction]:
        """
        Get all available actions for a role in current context

        Filters by:
        - Role permissions
        - Current location
        - Crew state
        - Any other prerequisites
        """
        action_ids = self._actions_by_role.get(role, [])
        available_actions = []

        for action_id in action_ids:
            action = self._actions.get(action_id)
            if action:
                can_execute, _ = action.can_execute(context)
                if can_execute:
                    available_actions.append(action)

        return available_actions

    def execute_action(self, action_id: str, context: ActionContext) -> ActionResult:
        """Execute an action by ID"""
        action = self._actions.get(action_id)

        if not action:
            return ActionResult(False, f"Unknown action: {action_id}")

        # Validate before executing
        can_execute, reason = action.can_execute(context)
        if not can_execute:
            return ActionResult(False, f"Cannot execute: {reason}")

        # Execute
        try:
            return action.execute(context)
        except Exception as e:
            return ActionResult(False, f"Action failed: {str(e)}")

    def get_action_display_name(self, action_id: str, context: ActionContext) -> str:
        """Get display name for action"""
        action = self._actions.get(action_id)
        return action.get_display_name(context) if action else action_id
```

### 5. Example Actions

#### Science Officer: Sensor Scan (`src/systems/crew_actions/science_actions.py`)

```python
from systems.crew_actions.base_action import BaseAction, ActionContext, ActionResult
from entities.crew import ShipRole
from core.sensor_data_generator import generate_sensor_data

class SensorScanAction(BaseAction):
    """Perform detailed sensor scan of current planet"""

    def __init__(self):
        super().__init__()
        self.action_id = "science.sensor_scan"
        self.display_name = "Sensors"
        self.description = "Scan planet for atmospheric, hydrospheric, and mineral composition"
        self.required_roles = [ShipRole.SCIENCE_OFFICER]
        self.required_location = ["orbit"]
        self.skill_check = "science"
        self.skill_threshold = 0  # Basic action, no minimum skill

    def _can_execute_impl(self, context: ActionContext) -> tuple[bool, str]:
        """Check if we're orbiting a scannable planet"""
        if not context.game_state.orbiting_planet:
            return False, "No planet in orbit"

        # Starports can't be scanned this way
        if context.game_state.orbiting_planet.get('type') == 'starport':
            return False, "Cannot scan starport"

        return True, ""

    def execute(self, context: ActionContext) -> ActionResult:
        """Perform sensor scan"""
        planet = context.game_state.orbiting_planet
        planet_name = planet['name']

        # Check if already scanned
        if planet_name in context.game_state.scanned_planets:
            sensor_data = context.game_state.scanned_planets[planet_name]
        else:
            # Generate sensor data
            sensor_data = generate_sensor_data(planet)
            context.game_state.scanned_planets[planet_name] = sensor_data

        # Display results via HUD
        if context.hud_manager:
            context.hud_manager.add_message(
                f"Scanning {planet_name}...",
                (100, 200, 255)
            )

            # Atmosphere
            atmo_str = ", ".join(sensor_data.atmosphere)
            context.hud_manager.add_message(
                f"Atmosphere: {atmo_str}",
                (180, 180, 180)
            )

            # Hydrosphere
            hydro_str = ", ".join(sensor_data.hydrosphere)
            context.hud_manager.add_message(
                f"Hydrosphere: {hydro_str}",
                (180, 180, 180)
            )

            # Lithosphere
            litho_str = ", ".join(sensor_data.lithosphere)
            context.hud_manager.add_message(
                f"Lithosphere: {litho_str}",
                (180, 180, 180)
            )

            # Update auxiliary panel
            if context.hud_manager.auxiliary_panel:
                context.hud_manager.auxiliary_panel.set_sensor_data(sensor_data)

        return ActionResult(
            success=True,
            message=f"Scan of {planet_name} complete",
            data={'sensor_data': sensor_data}
        )
```

#### Navigator: Leave Orbit (`src/systems/crew_actions/navigation_actions.py`)

```python
from systems.crew_actions.base_action import BaseAction, ActionContext, ActionResult
from entities.crew import ShipRole

class LeaveOrbitAction(BaseAction):
    """Exit planetary orbit and return to space"""

    def __init__(self):
        super().__init__()
        self.action_id = "navigation.leave_orbit"
        self.display_name = "Leave Orbit"
        self.description = "Exit orbit and return to interstellar space"
        self.required_roles = [ShipRole.NAVIGATOR]
        self.required_location = ["orbit"]

    def _can_execute_impl(self, context: ActionContext) -> tuple[bool, str]:
        """Always available when in orbit"""
        return True, ""

    def execute(self, context: ActionContext) -> ActionResult:
        """Exit orbit"""
        if context.game_state.exit_orbit():
            # Notify user
            if context.hud_manager:
                context.hud_manager.add_message("Exiting orbit", (100, 255, 100))

            # Change screen
            if context.screen_manager:
                context.screen_manager.change_screen("space")

            return ActionResult(
                success=True,
                message="Exited orbit successfully"
            )
        else:
            return ActionResult(
                success=False,
                message="Failed to exit orbit"
            )
```

### 6. Screen Integration

Screens become much simpler - they handle UI and delegate to the action system.

#### Updated OrbitScreen (`src/ui/screens/orbit_screen.py`)

```python
class OrbitScreen(Screen):
    """Orbital interface screen"""

    def __init__(self, screen_manager, game_state, action_system):
        super().__init__(screen_manager)
        self.game_state = game_state
        self.action_system = action_system  # Injected dependency

        # ... rest of init

    def _execute_menu_action(self, bridge_panel, action):
        """Execute the selected menu action"""

        # Special case: Return to Bridge is UI-only
        if action == "Return to Bridge":
            bridge_panel.close_role_menu()
            return

        # Get current crew member (simplified - in full implementation,
        # track which role was selected)
        current_role = bridge_panel.roles[self.selected_role_index]
        crew_member = self._get_crew_for_role(current_role)

        # Create action context
        context = ActionContext(
            game_state=self.game_state,
            screen_manager=self.screen_manager,
            hud_manager=self.hud_manager,
            initiating_crew=crew_member
        )

        # Map UI action text to action ID
        # (In production, bridge panel would provide action IDs directly)
        action_map = {
            "Sensors": "science.sensor_scan",
            "Leave Orbit": "navigation.leave_orbit"
        }

        action_id = action_map.get(action)
        if action_id:
            result = self.action_system.execute_action(action_id, context)

            # Show result message if action failed
            if not result.success and self.hud_manager:
                self.hud_manager.add_message(result.message, (255, 100, 100))

        bridge_panel.close_role_menu()

    def _get_crew_for_role(self, role_name: str) -> CrewMember:
        """Get crew member assigned to a ship station"""
        # Map UI role name to ShipRole
        from entities.crew import CrewMember, ShipRole, CrewSkills
        role_map = {
            "Science Officer": ShipRole.SCIENCE_OFFICER,
            "Navigator": ShipRole.NAVIGATOR,
            "Engineer": ShipRole.ENGINEER,
            "Communications": ShipRole.COMMUNICATIONS,
            "Doctor": ShipRole.DOCTOR,
            "Captain": ShipRole.CAPTAIN
        }
        ship_role = role_map.get(role_name, ShipRole.CAPTAIN)

        # Get crew member assigned to this station
        crew_member = self.game_state.crew_roster.get_crew_at_station(ship_role)

        # If no one assigned, create temporary placeholder
        # (In production, you'd handle this more gracefully)
        if not crew_member:
            crew_member = CrewMember(
                name="Acting " + role_name,
                skills=CrewSkills(),
                assigned_role=ship_role
            )

        return crew_member
```

## Crew Management Benefits

The separation of crew members from ship roles enables interesting gameplay:

### Gameplay Scenarios

**1. Emergency Station Reassignment**
```
Your science officer is injured during combat. You can:
- Assign your engineer to the science station (reduced effectiveness)
- Assign a junior crew member with basic science skills
- Continue without a science officer (no sensor scans)
```

**2. Specialist vs. Generalist Hiring**
```python
# Hire a science specialist
specialist = CrewMember(
    name="Dr. Chen",
    skills=CrewSkills(science=95, engineering=30, navigation=25)
)

# Hire a well-rounded generalist
generalist = CrewMember(
    name="Lt. Rodriguez",
    skills=CrewSkills(science=60, engineering=60, navigation=65)
)

# Specialist better at their job, but inflexible
# Generalist can fill multiple roles adequately
```

**3. Skill-Based Outcomes**
```python
# Experienced science officer gets better scan results
high_skill_crew = game_state.crew_roster.get_crew_at_station(ShipRole.SCIENCE_OFFICER)
effectiveness = high_skill_crew.get_effectiveness(ShipRole.SCIENCE_OFFICER)  # 0.92

# Scan detail scales with effectiveness
if effectiveness > 0.8:
    # Reveal rare minerals, anomalies
elif effectiveness > 0.5:
    # Standard scan data
else:
    # Basic scan, may miss details
```

**4. Crew Management Screen**
```
Current Assignments:
- Captain: Cpt. Smith (Leadership 85)
- Science Officer: Dr. Chen (Science 95)
- Navigator: Lt. Kim (Navigation 88)
- Engineer: [EMPTY]
- Communications: Ens. Patel (Communications 45)
- Doctor: Dr. Martinez (Medical 82)

Available Crew:
- Lt. Rodriguez (Generalist, all skills 60)
- Ens. Taylor (Engineering 70, inexperienced)

[Player can reassign crew between stations]
```

**5. Progression System**
```python
# Crew improves skills through use
def on_action_success(crew_member, action):
    if action.skill_check:
        # Small skill increase when successfully using a skill
        current_skill = crew_member.skills.get_skill(action.skill_check)
        if current_skill < 100:
            crew_member.skills[action.skill_check] += 1
```

## Action Registration Architecture

### Hybrid Approach (Implemented)

The system uses a **hybrid approach** for action registration to keep `main.py` clean while allowing screens to own their specific actions:

**Design:**
- Actions are registered globally in `CrewActionSystem` (single source of truth)
- Each screen declares which actions it uses via `AVAILABLE_ACTIONS` catalog
- Screens register their actions lazily when initialized
- Duplicate registration is prevented via existence checks

**Benefits:**
- `main.py` stays minimal - just creates empty `CrewActionSystem()`
- Screens own their action dependencies (clear encapsulation)
- No action bloat as more screens/actions are added
- Actions registered once globally, reused across screens if needed

**Example Implementation (OrbitScreen):**

```python
class OrbitScreen(Screen):
    # Declare which actions are available in orbit for each role
    AVAILABLE_ACTIONS = {
        ShipRole.SCIENCE_OFFICER: ['science.sensor_scan'],
        ShipRole.NAVIGATOR: ['navigation.leave_orbit'],
        ShipRole.ENGINEER: [],
        ShipRole.COMMUNICATIONS: [],
        ShipRole.DOCTOR: [],
        ShipRole.CAPTAIN: [],
    }

    def __init__(self, screen_manager, game_state, action_system):
        super().__init__(screen_manager)
        self.game_state = game_state
        self.action_system = action_system

        # Register orbit-specific actions
        self._register_orbit_actions()

    def _register_orbit_actions(self):
        """Register actions needed for orbit screen"""
        from systems.crew_actions.science_actions import SensorScanAction
        from systems.crew_actions.navigation_actions import LeaveOrbitAction

        # Only register if not already registered (prevents duplicates)
        if not self.action_system._actions.get('science.sensor_scan'):
            self.action_system.register_action(SensorScanAction())
        if not self.action_system._actions.get('navigation.leave_orbit'):
            self.action_system.register_action(LeaveOrbitAction())
```

**Main.py Simplification:**

```python
# Initialize crew action system (empty, screens will populate)
action_system = CrewActionSystem()

# Create and register screens
orbit = OrbitScreen(screen_manager, game_state, action_system)
# OrbitScreen registers its own actions in __init__
```

### Alternative Approaches Considered

1. **Global Registration (Rejected)** - All actions registered in `main.py`
   - Problem: Would bloat `main.py` as actions grow

2. **Per-Role Lazy Loading (Future)** - Load actions only when role menu opens
   - Benefit: Even more granular, loads only what's needed
   - Trade-off: More complexity, only worth it if we have hundreds of actions

## Implementation Plan

### Phase 1: Foundation ✓ (Complete)

1. **Create entity classes** ✓
   - `src/entities/crew.py` with CrewMember, CrewRole, CrewSkills
   - Add crew roster to GameState

2. **Create action system core** ✓
   - `src/systems/crew_action_system.py` with CrewActionSystem, ActionContext
   - `src/systems/crew_actions/base_action.py` with BaseAction, ActionResult

3. **Create action modules** ✓
   - `src/systems/crew_actions/science_actions.py` with SensorScanAction
   - `src/systems/crew_actions/navigation_actions.py` with LeaveOrbitAction

### Phase 2: Migration ✓ (Complete)

4. **Refactor OrbitScreen** ✓
   - Remove `_perform_sensor_scan()` method
   - Update `_execute_menu_action()` to use action system
   - Inject action_system dependency

5. **Initialize action system** ✓
   - Create empty action system in main.py
   - Screens register their own actions
   - Hybrid approach prevents bloat

### Phase 3: Expansion (Future)

6. **Add more actions**
   - Space navigation actions (set course, warp, etc.)
   - Engineering actions (repair, power management)
   - Communications actions (hail, trade)

7. **Add crew management**
   - Crew roster screen
   - Skill progression
   - Crew hiring/firing

8. **Data-driven actions**
   - Move action definitions to JSON
   - Dynamic action loading
   - Modding support

## Testing Strategy

### Unit Tests

Actions can be tested independently:

```python
def test_sensor_scan_requires_orbit():
    action = SensorScanAction()
    game_state = GameState()
    game_state.location = "space"  # Not in orbit

    context = ActionContext(game_state=game_state)
    can_execute, reason = action.can_execute(context)

    assert not can_execute
    assert "orbit" in reason.lower()

def test_sensor_scan_generates_data():
    action = SensorScanAction()
    game_state = GameState()
    game_state.location = "orbit"
    game_state.orbiting_planet = {
        'name': 'Test Planet',
        'type': 'rocky',
        'seed': 1234
    }

    context = ActionContext(game_state=game_state)
    result = action.execute(context)

    assert result.success
    assert 'Test Planet' in game_state.scanned_planets
```

### Integration Tests

Test action system as a whole:

```python
def test_action_system_registration():
    system = CrewActionSystem()
    action = SensorScanAction()

    system.register_action(action)

    actions = system.get_actions_for_role(CrewRole.SCIENCE_OFFICER, context)
    assert len(actions) > 0
    assert actions[0].action_id == "science.sensor_scan"
```

## Future Enhancements

### Context-Sensitive Actions

Actions that appear/disappear based on game state:

```python
class AnalyzeAnomalyAction(BaseAction):
    """Analyze detected anomaly"""

    def _can_execute_impl(self, context: ActionContext) -> tuple[bool, str]:
        # Only show when anomaly is detected
        if not context.game_state.current_anomaly:
            return False, "No anomaly detected"
        return True, ""
```

### Skill-Based Outcomes

Action success/quality depends on crew skill:

```python
def execute(self, context: ActionContext) -> ActionResult:
    skill = context.initiating_crew.get_skill_for_role()

    # Higher skill = better scan detail
    detail_level = "basic" if skill < 50 else "detailed" if skill < 80 else "comprehensive"

    # Generate sensor data with appropriate detail
    sensor_data = generate_sensor_data(planet, detail_level=detail_level)
```

### Action Cooldowns/Costs

Actions that consume resources or have cooldowns:

```python
class WarpJumpAction(BaseAction):
    def execute(self, context: ActionContext) -> ActionResult:
        fuel_cost = calculate_fuel_cost(context.game_state.warp_distance)

        if context.game_state.fuel < fuel_cost:
            return ActionResult(False, "Insufficient fuel")

        context.game_state.fuel -= fuel_cost
        # ... perform jump
```

### Chained Actions

Actions that trigger other actions:

```python
class LandOnPlanetAction(BaseAction):
    def execute(self, context: ActionContext) -> ActionResult:
        # First, check sensors
        if planet_name not in context.game_state.scanned_planets:
            # Auto-scan before landing
            scan_action = SensorScanAction()
            scan_result = scan_action.execute(context)
            if not scan_result.success:
                return ActionResult(False, "Unable to scan planet before landing")

        # Now land
        # ...
```

## Migration Checklist

- [ ] Create `src/entities/crew.py`
- [ ] Create `src/systems/crew_action_system.py`
- [ ] Create `src/systems/crew_actions/base_action.py`
- [ ] Create `src/systems/crew_actions/science_actions.py`
- [ ] Create `src/systems/crew_actions/navigation_actions.py`
- [ ] Add crew roster to GameState
- [ ] Initialize CrewActionSystem in main.py
- [ ] Refactor OrbitScreen to use action system
- [ ] Remove `_perform_sensor_scan()` from OrbitScreen
- [ ] Update BridgePanel to provide action IDs (optional enhancement)
- [ ] Write unit tests for actions
- [ ] Write integration tests for action system
- [ ] Update architecture.md with crew action system
- [ ] Document in-code examples for future action authors

## References

- Original implementation: `src/ui/screens/orbit_screen.py` lines 127-174
- Architecture principles: `docs/technical/architecture.md`
- Crew management design: `docs/design/working/05_crew_management.md`
