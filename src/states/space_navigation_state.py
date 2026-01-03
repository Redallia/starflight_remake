"""
Placeholder space navigation state for testing state transitions
"""
import pygame
from core import interactable
from ui.hud_renderer import HudRenderer
from core.game_state import GameState
from core.colors import SPACE_BLACK, TEXT_NORMAL
from core.input_manager import InputManager
from core.collision_manager import CollisionManager
from core.interactable import Interactable
from core.constants import (
    CONTEXT_CENTER,
    CENTRAL_OBJECT_SIZE,
    CONTEXT_OUTER_SYSTEM,
    CONTEXT_INNER_SYSTEM,
    CONTEXT_PLANETARY_SYSTEM,
    MOVEMENT_SPEED,
    CONTEXT_GRID_SIZE,
    INTERACTION_PLANET
)


class SpaceNavigationState(GameState):
    """ Space navigation state """

    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.input_manager = InputManager()
        self.hud_renderer = HudRenderer()
        self.collision_manager = CollisionManager()

    def on_enter(self):
        """Called when entering space navigation state"""
        print("Entering space navigation state")

    def handle_event(self, event):
        """Handle input events"""
        action = self.input_manager.get_action(event)
        
        if action == "cancel":
            self.state_manager.change_state("starport")

    def update(self, dt):
        """Update space navigation state"""
        # Check for movement input every frame
        dx, dy = self.input_manager.get_movement_vector()

        if dx != 0 or dy != 0:
            self._move_ship(dx, -dy)
            # Check for collisions after movement
            self._check_collisions()
        
    def render(self, surface):
        """Render space navigation view with the HUD """
        # Fill background
        surface.fill(SPACE_BLACK)

        # Render HUD
        self.hud_renderer.render(surface, self.state_manager.game_session)    
        
    def _move_ship(self, dx, dy):
        """Move the ship by (dx, dy) in current context"""
        # get current position
        x, y = self.state_manager.game_session.ship_position

        # Update position with scaled movement speed
        new_x = x + (dx * MOVEMENT_SPEED)
        new_y = y + (dy * MOVEMENT_SPEED)

        # Clamp to context grid boundaries
        new_x = max(0, min(CONTEXT_GRID_SIZE, new_x))
        new_y = max(0, min(CONTEXT_GRID_SIZE, new_y))

        # Update ship position in game session
        self.state_manager.game_session.ship_position = (new_x, new_y)

    def _check_collisions(self):
        self._check_interactables()
        self._check_boundary_collisions()
        """Check for all collision types"""
        # self._check_planet_collisions()
        # self._check_central_zone_collisions()

    def _get_current_interactables(self):
        """Get interactables for current context"""
        interactables = []
        current_system = self.state_manager.game_session.current_system
        context = self.state_manager.game_session.current_context

        if not current_system:
            return interactables
        
        # Get planets and wrap them as Interactable.circle()
        planets = current_system.get_planets_for_context(context.type, context.data)
        for planet in planets:
            if planet is None:
                continue

            planet_x, planet_y = planet.get_coordinates()
            interactables.append(Interactable.circle(
                planet_x,
                planet_y,
                planet.size,
                INTERACTION_PLANET,
                data=planet
            ))
        
        # Add central zone if in outer system
        if context.type == CONTEXT_OUTER_SYSTEM:
            interactables.append(Interactable.circle(
                CONTEXT_CENTER,
                CONTEXT_CENTER,
                CENTRAL_OBJECT_SIZE,
                CONTEXT_INNER_SYSTEM, None
            ))

        return interactables
    
    def _check_interactables(self):
        """Check for interactable collisions and handle proximity"""
        ship_x, ship_y = self.state_manager.game_session.ship_position
        interactables = self._get_current_interactables()

        # Check for no interactables in this context
        if not interactables:
            return

        collision = self.collision_manager.check_interactable_collision(ship_x, ship_y, interactables)

        if collision:
            self._handle_interactable_collision(collision)

    def _handle_interactable_collision(self, interactable):
        """Handle collision with an interactable"""
        if interactable.type == INTERACTION_PLANET:
            self._handle_planet_collision(interactable.data)
        elif interactable.type == CONTEXT_INNER_SYSTEM:
            # Handle entering inner system from central zone
            self._handle_central_zone_collision()

    def _handle_planet_collision(self, planet):
        """Handle collision with a planet"""
        # Check if it's a gas giant with moons
        if hasattr(planet, 'planetary_system') and planet.planetary_system:
            # Enter the planetary system context
            current_context = self.state_manager.game_session.current_context
            
            if self.state_manager.game_session.context_manager.enter_context(
                context_type="planetary_system",
                target_coords=planet.get_coordinates(),
                target_radius=planet.size,
                parent_region=current_context.type,
                planet_index=planet.orbital_index
            ):
                self.state_manager.game_session.add_message(f"Entering {planet.name} moon system")
                self.collision_manager.reset()
        else:
            # Regular planet - show orbit message
            self.state_manager.game_session.add_message(f"Approaching {planet.name}. Press Space to orbit.")

    def _check_boundary_collisions(self):
        """Check for boundary collisions and handle context transitions"""
        ship_x, ship_y = self.state_manager.game_session.ship_position
        boundary = self.collision_manager.check_boundary_collision(ship_x, ship_y)

        if boundary:
            self._handle_boundary_collision(boundary)

    def _handle_boundary_collision(self, boundary):
        """Handle collision with navigation context boundary"""
        current_context = self.state_manager.game_session.current_context

        # Get the parent object coords/radius from current context
        parent_coords = current_context.data.get("parent_object_coords", [CONTEXT_CENTER, CONTEXT_CENTER])
        parent_radius = current_context.data.get("parent_object_radius", CENTRAL_OBJECT_SIZE)

        # Attempt to exit inner system
        if self.state_manager.game_session.context_manager.exit_context(
            exit_boundary=boundary,
            parent_object_coords=parent_coords,
            parent_object_radius=parent_radius
        ):
            self.state_manager.game_session.add_message(f"Entering outer system from {boundary}")
            # Reset collision manager to prevent immediate re-trigger
            self.collision_manager.reset()
        else:
            # Handle other types of boundary exits later
            self.state_manager.game_session.add_message(f"Boundary collision at {boundary} (not implemented yet)")

    def _handle_central_zone_collision(self):
        """Handle entering the central zone (inner/outer system transition)"""
        # Attempt to enter inner system
        if self.state_manager.game_session.context_manager.enter_context(
            context_type=CONTEXT_INNER_SYSTEM,
            target_coords=[CONTEXT_CENTER, CONTEXT_CENTER],
            target_radius=CENTRAL_OBJECT_SIZE
        ):
            self.state_manager.game_session.add_message("Entering inner system")
            # Reset collision manager to prevent immediate re-trigger
            self.collision_manager.reset()
        else:
            # Handle other types of central zone collisions later
            self.state_manager.game_session.add_message("Central zone collision (not implemented yet)")