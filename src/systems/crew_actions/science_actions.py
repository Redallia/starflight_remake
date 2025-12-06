"""
Science Officer actions
"""
from systems.crew_actions.base_action import BaseAction, ActionResult
from systems.crew_action_system import ActionContext
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
