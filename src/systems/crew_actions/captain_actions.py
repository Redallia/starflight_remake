"""
Captain actions
"""
from systems.crew_actions.base_action import BaseAction, ActionResult
from systems.crew_action_system import ActionContext
from entities.crew import ShipRole


class LandOnPlanetAction(BaseAction):
    """Land on the planet surface"""

    def __init__(self):
        super().__init__()
        self.action_id = "captain.land_on_planet"
        self.display_name = "Land"
        self.description = "Land on the planet surface for exploration"
        self.required_roles = [ShipRole.CAPTAIN]
        self.required_location = ["orbit"]

    def _can_execute_impl(self, context: ActionContext) -> tuple[bool, str]:
        """Check if we can land on this planet"""
        if not context.game_state.orbiting_planet:
            return False, "No planet in orbit"

        # Get the planet entity
        planet = context.game_state.orbiting_planet

        # Check if this is a starport (can't land on starports this way)
        if planet.get('type') == 'starport':
            return False, "Cannot land on starport"

        # Check if planet allows landing (from celestial body entity)
        # For now, we'll allow landing on all non-starport planets
        # Later this could check can_land() on the planet entity
        return True, ""

    def execute(self, context: ActionContext) -> ActionResult:
        """Initiate landing sequence"""
        planet = context.game_state.orbiting_planet
        planet_name = planet['name']

        # Update game state to planet surface
        context.game_state.location = "planet_surface"

        # Notify user
        if context.hud_manager:
            context.hud_manager.add_message(
                f"Landing on {planet_name}...",
                (100, 255, 100)
            )

        # TODO: When planet surface screen is implemented, transition to it
        # For now, we'll just change the location state
        # if context.screen_manager:
        #     context.screen_manager.change_screen("planet_surface")

        return ActionResult(
            success=True,
            message=f"Landed on {planet_name}",
            data={'planet': planet}
        )
