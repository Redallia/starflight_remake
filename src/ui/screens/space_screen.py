"""
Space navigation screen
Handles movement in space, starfield rendering, and navigation
"""
import pygame
import random
from core.screen_manager import Screen


class SpaceScreen(Screen):
    """Space navigation screen with grid-based movement"""

    def __init__(self, screen_manager, game_state):
        super().__init__(screen_manager)
        self.game_state = game_state

        # Movement configuration
        self.ship_speed = 1.0  # Movement grid units per frame when key held
        self.fuel_consumption_rate = 0.01  # Fuel per movement grid unit traveled

        # Starfield for parallax effect
        self.stars = []
        self.generate_starfield()

        # Planet proximity tracking
        self.near_planet = None  # Currently nearby planet (for docking prompt)
        self.collision_counter = 0  # Track repeated collisions for wraparound

    def generate_starfield(self):
        """Generate random stars for background"""
        self.stars = []
        for _ in range(200):  # 200 stars
            star = {
                'x': random.randint(0, 800),
                'y': random.randint(0, 600),
                'brightness': random.randint(100, 255),
                'size': random.choice([1, 1, 1, 2])  # Mostly small stars, some bigger
            }
            self.stars.append(star)

    def on_enter(self):
        """Called when entering space"""
        print("Entered space")
        # Regenerate starfield for variety
        self.generate_starfield()

    def update(self, delta_time, input_handler):
        """Update space screen"""
        # Check for docking at nearby planet
        if self.near_planet and input_handler.is_confirm_pressed():
            if self.near_planet['type'] == 'starport':
                if self.game_state.return_to_starport():
                    print("Docking at starport")
                    self.screen_manager.change_screen("starport")
                    return

        # Return to starport (R key - backup method)
        if input_handler.is_key_just_pressed(pygame.K_r):
            if self.game_state.return_to_starport():
                print("Returning to starport")
                self.screen_manager.change_screen("starport")
                return

        # WASD movement
        dx = 0
        dy = 0

        if input_handler.is_up_pressed():  # W
            dy -= self.ship_speed
        if input_handler.is_down_pressed():  # S
            dy += self.ship_speed
        if input_handler.is_left_pressed():  # A
            dx -= self.ship_speed
        if input_handler.is_right_pressed():  # D
            dx += self.ship_speed

        # Apply movement if any
        if dx != 0 or dy != 0:
            # Store old position to calculate actual movement
            old_x = self.game_state.ship_x
            old_y = self.game_state.ship_y

            # Move the ship (may be clamped at boundaries)
            self.game_state.move_ship(int(dx), int(dy))

            # Check for planet collisions and handle
            self.handle_planet_collision(old_x, old_y, dx, dy)

            # Calculate actual movement that occurred (after clamping and collision)
            actual_dx = self.game_state.ship_x - old_x
            actual_dy = self.game_state.ship_y - old_y

            # Consume fuel based on actual distance traveled
            distance = (actual_dx**2 + actual_dy**2) ** 0.5
            fuel_used = distance * self.fuel_consumption_rate
            self.game_state.fuel = max(0, self.game_state.fuel - fuel_used)

            # Update starfield for parallax effect (stars drift opposite to movement)
            # Only scroll based on actual movement, not intended movement
            self.update_starfield(-actual_dx * 2, -actual_dy * 2)

        # Check proximity to planets for docking prompt
        self.check_planet_proximity()

    def check_planet_proximity(self):
        """Check if ship is near any planet for docking"""
        ship_coord = self.game_state.get_coordinate_position()
        self.near_planet = None

        for planet in self.game_state.planets:
            # Calculate distance in coordinate units
            dx = ship_coord[0] - planet['coord_x']
            dy = ship_coord[1] - planet['coord_y']
            distance = (dx**2 + dy**2) ** 0.5

            # Check if within docking range (planet radius + small buffer)
            if distance <= planet['radius'] + 1:
                self.near_planet = planet
                break

    def handle_planet_collision(self, old_x, old_y, intended_dx, intended_dy):
        """Handle collision with planets - hard stop or wraparound"""
        ship_x = self.game_state.ship_x
        ship_y = self.game_state.ship_y

        for planet in self.game_state.planets:
            # Convert planet coordinates to movement grid
            planet_x = planet['coord_x'] * 10
            planet_y = planet['coord_y'] * 10
            planet_radius = planet['radius'] * 10  # Convert to movement grid units

            # Calculate distance from ship to planet center
            dx = ship_x - planet_x
            dy = ship_y - planet_y
            distance = (dx**2 + dy**2) ** 0.5

            # Check if ship is inside planet radius
            if distance < planet_radius:
                # Hard stop - push ship back to edge of planet
                if distance > 0:
                    # Normalize direction and push to edge
                    norm_x = dx / distance
                    norm_y = dy / distance
                    self.game_state.ship_x = int(planet_x + norm_x * planet_radius)
                    self.game_state.ship_y = int(planet_y + norm_y * planet_radius)
                else:
                    # Ship exactly at center, push in opposite direction of movement
                    if intended_dx != 0 or intended_dy != 0:
                        move_dist = (intended_dx**2 + intended_dy**2) ** 0.5
                        if move_dist > 0:
                            norm_x = -intended_dx / move_dist
                            norm_y = -intended_dy / move_dist
                            self.game_state.ship_x = int(planet_x + norm_x * planet_radius)
                            self.game_state.ship_y = int(planet_y + norm_y * planet_radius)

                # Check if player is trying to push through (collision counter)
                self.collision_counter += 1
                if self.collision_counter > 30:  # ~0.5 seconds at 60fps
                    # Wraparound - teleport to opposite side
                    self.game_state.ship_x = int(planet_x - norm_x * planet_radius)
                    self.game_state.ship_y = int(planet_y - norm_y * planet_radius)
                    self.collision_counter = 0
                    print("Wrapping around planet")
                break
        else:
            # No collision, reset counter
            self.collision_counter = 0

    def update_starfield(self, dx, dy):
        """Move stars to create parallax effect"""
        for star in self.stars:
            star['x'] += dx
            star['y'] += dy

            # Wrap stars around screen edges
            if star['x'] < 0:
                star['x'] += 800
            elif star['x'] > 800:
                star['x'] -= 800

            if star['y'] < 0:
                star['y'] += 600
            elif star['y'] > 600:
                star['y'] -= 600

    def render(self, screen):
        """Render space screen"""
        from ui.renderer import Renderer
        renderer = Renderer(screen)
        width, height = screen.get_size()

        # Clear to black (space!)
        renderer.clear((0, 0, 0))

        # Draw starfield
        self.render_starfield(screen)

        # Draw planets
        self.render_planets(renderer, width, height)

        # Draw ship at center of screen
        self.render_ship(renderer, width, height)

        # Draw HUD
        self.render_hud(renderer, width, height)

        # Draw docking prompt if near planet
        if self.near_planet:
            self.render_docking_prompt(renderer, width, height)

    def render_starfield(self, screen):
        """Render the starfield background"""
        for star in self.stars:
            brightness = star['brightness']
            color = (brightness, brightness, brightness)
            if star['size'] == 1:
                screen.set_at((int(star['x']), int(star['y'])), color)
            else:
                pygame.draw.circle(screen, color, (int(star['x']), int(star['y'])), star['size'])

    def render_ship(self, renderer, width, height):
        """Render the player's ship at screen center"""
        ship_x = width // 2
        ship_y = height // 2

        # Simple triangle ship pointing up
        ship_color = (100, 200, 255)
        points = [
            (ship_x, ship_y - 10),      # Top point
            (ship_x - 8, ship_y + 10),  # Bottom left
            (ship_x + 8, ship_y + 10)   # Bottom right
        ]
        pygame.draw.polygon(renderer.screen, ship_color, points)

        # Outline
        pygame.draw.polygon(renderer.screen, (255, 255, 255), points, 1)

    def render_hud(self, renderer, width, height):
        """Render HUD with coordinates and status"""
        # Get coordinate position
        coord_x, coord_y = self.game_state.get_coordinate_position()

        # Top-left HUD panel
        hud_x = 10
        hud_y = 10
        line_height = 25

        # Coordinates (most important)
        renderer.draw_text(
            f"Coordinates: {coord_x}, {coord_y}",
            hud_x,
            hud_y,
            color=(255, 255, 100),
            font=renderer.default_font
        )

        # Fuel
        fuel_color = (255, 100, 100) if self.game_state.fuel < 20 else (200, 200, 200)
        renderer.draw_text(
            f"Fuel: {self.game_state.fuel:.1f}",
            hud_x,
            hud_y + line_height,
            color=fuel_color,
            font=renderer.small_font
        )

        # Credits
        renderer.draw_text(
            f"Credits: {self.game_state.credits}",
            hud_x,
            hud_y + line_height * 2,
            color=(200, 200, 200),
            font=renderer.small_font
        )

        # Cargo
        renderer.draw_text(
            f"Cargo: {self.game_state.cargo_used}/{self.game_state.cargo_capacity}",
            hud_x,
            hud_y + line_height * 3,
            color=(200, 200, 200),
            font=renderer.small_font
        )

        # Instructions at bottom
        renderer.draw_text_centered(
            "WASD: Move  |  R: Return to Starport",
            width // 2,
            height - 20,
            color=(150, 150, 150),
            font=renderer.small_font
        )

    def render_planets(self, renderer, width, height):
        """Render planets relative to ship position"""
        # Use movement grid for smooth rendering
        ship_x = self.game_state.ship_x
        ship_y = self.game_state.ship_y

        for planet in self.game_state.planets:
            # Convert planet coordinate position to movement grid
            planet_x = planet['coord_x'] * 10
            planet_y = planet['coord_y'] * 10

            # Calculate planet position relative to ship (camera centered on ship)
            # Use movement grid for smooth scrolling
            movement_dx = planet_x - ship_x
            movement_dy = planet_y - ship_y

            # Scale to screen space (2 pixels per movement unit = 20 pixels per coordinate unit)
            screen_x = width // 2 + movement_dx * 2
            screen_y = height // 2 + movement_dy * 2  # Positive Y = down on screen

            # Only draw if on screen (with margin)
            margin = 100
            if -margin < screen_x < width + margin and -margin < screen_y < height + margin:
                # Draw planet
                planet_radius = planet['radius'] * 20  # Scale radius to screen
                pygame.draw.circle(
                    renderer.screen,
                    planet['color'],
                    (int(screen_x), int(screen_y)),
                    int(planet_radius)
                )

                # Draw outline
                pygame.draw.circle(
                    renderer.screen,
                    (255, 255, 255),
                    (int(screen_x), int(screen_y)),
                    int(planet_radius),
                    2
                )

                # Draw planet name
                renderer.draw_text_centered(
                    planet['name'],
                    int(screen_x),
                    int(screen_y - planet_radius - 15),
                    color=(200, 200, 200),
                    font=renderer.small_font
                )

    def render_docking_prompt(self, renderer, width, height):
        """Render prompt to dock at nearby planet"""
        prompt_text = f"Press SPACE to dock at {self.near_planet['name']}"

        # Draw with highlighted background
        renderer.draw_text_centered(
            prompt_text,
            width // 2,
            height // 2 + 60,
            color=(255, 255, 0),
            font=renderer.default_font
        )
