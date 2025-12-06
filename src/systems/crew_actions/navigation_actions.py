"""
Navigator actions
"""
from systems.crew_actions.base_action import BaseAction, ActionResult
from systems.crew_action_system import ActionContext
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
