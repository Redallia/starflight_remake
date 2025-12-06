"""
Crew action system - central registry and executor for crew actions
"""
from dataclasses import dataclass
from typing import Dict, List, Optional
from entities.crew import ShipRole
from systems.crew_actions.base_action import BaseAction, ActionResult


@dataclass
class ActionContext:
    """Context provided to actions during execution"""
    game_state: 'GameState'           # Current game state
    screen_manager: 'ScreenManager'   # For screen transitions
    hud_manager: Optional['HUDManager'] = None  # For messages/UI updates
    initiating_crew: Optional['CrewMember'] = None  # Who triggered action
    extra_data: dict = None  # For screen-specific parameters

    def __post_init__(self):
        if self.extra_data is None:
            self.extra_data = {}


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
