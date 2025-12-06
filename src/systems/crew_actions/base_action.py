"""
Base action class for all crew actions
"""
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

    def can_execute(self, context: 'ActionContext') -> tuple[bool, str]:
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
    def _can_execute_impl(self, context: 'ActionContext') -> tuple[bool, str]:
        """Subclass-specific validation logic"""
        pass

    @abstractmethod
    def execute(self, context: 'ActionContext') -> ActionResult:
        """Execute the action and return result"""
        pass

    def get_display_name(self, context: 'ActionContext') -> str:
        """Get display name (can be context-dependent)"""
        return self.display_name
