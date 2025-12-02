"""
Planet sphere renderer
Renders terrain onto a rotating sphere surface
"""
import pygame
import math


class PlanetSphereRenderer:
    """Renders a planet as a rotating textured sphere"""

    def __init__(self, radius=120):
        self.radius = radius
        self.rotation_angle = 0.0  # Current rotation in degrees
        self.rotation_speed = 10.0  # Degrees per second

    def update(self, delta_time):
        """Update rotation animation"""
        self.rotation_angle += self.rotation_speed * delta_time
        if self.rotation_angle >= 360:
            self.rotation_angle -= 360

    def render(self, screen, center_x, center_y, terrain_grid, terrain_generator):
        """
        Render the planet sphere with terrain mapped onto it

        Args:
            screen: Pygame surface
            center_x, center_y: Center position of sphere
            terrain_grid: 2D array of terrain (500x200)
            terrain_generator: TerrainGenerator for colors
        """
        if not terrain_grid or not terrain_generator:
            return

        grid_height = len(terrain_grid)
        grid_width = len(terrain_grid[0]) if grid_height > 0 else 0

        if grid_width == 0 or grid_height == 0:
            return

        # Draw sphere from back to front (simple painter's algorithm)
        # We'll sample the sphere surface and get colors from the terrain

        # Create a list of pixels to draw with their z-depth
        pixels = []

        # Sample the sphere surface
        # Use latitude/longitude grid
        lat_steps = 60  # Number of latitude lines
        lon_steps = 120  # Number of longitude lines

        for lat_i in range(lat_steps):
            # Latitude from -90 to +90 degrees
            lat = (lat_i / lat_steps) * 180 - 90
            lat_rad = math.radians(lat)

            for lon_i in range(lon_steps):
                # Longitude from 0 to 360 degrees (plus rotation offset)
                lon = (lon_i / lon_steps) * 360 + self.rotation_angle
                lon_rad = math.radians(lon)

                # Convert spherical to 3D Cartesian coordinates
                x_3d = self.radius * math.cos(lat_rad) * math.sin(lon_rad)
                y_3d = self.radius * math.sin(lat_rad)
                z_3d = self.radius * math.cos(lat_rad) * math.cos(lon_rad)

                # Only render front-facing pixels (z > 0)
                if z_3d > 0:
                    # Project to 2D screen coordinates
                    screen_x = int(center_x + x_3d)
                    screen_y = int(center_y - y_3d)  # Flip Y for screen coords

                    # Map lat/lon to terrain grid coordinates
                    # Latitude maps to Y (0 to grid_height)
                    # Longitude maps to X (0 to grid_width)
                    terrain_y = int(((lat + 90) / 180) * (grid_height - 1))
                    terrain_x = int((lon_i / lon_steps) * (grid_width - 1))

                    # Clamp to grid bounds
                    terrain_y = max(0, min(grid_height - 1, terrain_y))
                    terrain_x = max(0, min(grid_width - 1, terrain_x))

                    # Get terrain color
                    terrain_type = terrain_grid[terrain_y][terrain_x]
                    color = terrain_generator.get_terrain_color(terrain_type)

                    # Apply simple shading based on z-depth (closer = brighter)
                    # z_3d ranges from 0 to radius
                    brightness_factor = 0.4 + 0.6 * (z_3d / self.radius)
                    shaded_color = tuple(int(c * brightness_factor) for c in color)

                    # Store pixel with depth for sorting
                    pixels.append((z_3d, screen_x, screen_y, shaded_color))

        # Sort by depth (furthest first) for proper layering
        pixels.sort(key=lambda p: p[0])

        # Draw pixels
        for z, x, y, color in pixels:
            # Draw a small filled circle for each pixel (makes it look smoother)
            if 0 <= x < screen.get_width() and 0 <= y < screen.get_height():
                pygame.draw.circle(screen, color, (x, y), 2)

    def render_optimized(self, screen, center_x, center_y, terrain_grid, terrain_generator):
        """
        Optimized version - draws filled circles in horizontal bands

        Args:
            screen: Pygame surface
            center_x, center_y: Center position of sphere
            terrain_grid: 2D array of terrain (500x200)
            terrain_generator: TerrainGenerator for colors
        """
        if not terrain_grid or not terrain_generator:
            return

        grid_height = len(terrain_grid)
        grid_width = len(terrain_grid[0]) if grid_height > 0 else 0

        if grid_width == 0 or grid_height == 0:
            return

        # Draw horizontal circles (latitude lines) from top to bottom
        lat_steps = 80

        for lat_i in range(lat_steps):
            # Latitude from -90 to +90
            lat = (lat_i / lat_steps) * 180 - 90
            lat_rad = math.radians(lat)

            # Calculate radius of this latitude circle
            circle_radius = self.radius * math.cos(lat_rad)
            y_pos = int(center_y - self.radius * math.sin(lat_rad))

            if circle_radius <= 0:
                continue

            # Calculate z-depth at front of circle (for shading)
            z_front = self.radius * math.cos(lat_rad)
            brightness_factor = 0.4 + 0.6 * (z_front / self.radius)

            # Sample points around this circle
            circumference = 2 * math.pi * circle_radius
            num_points = max(int(circumference / 2), 12)  # Sample every ~2 pixels

            for i in range(num_points):
                # Longitude angle including rotation
                angle = (i / num_points) * 360 + self.rotation_angle
                angle_rad = math.radians(angle)

                # Calculate 3D position
                x_3d = circle_radius * math.sin(angle_rad)
                z_3d = circle_radius * math.cos(angle_rad)

                # Only draw if facing forward
                if z_3d > 0:
                    x_pos = int(center_x + x_3d)

                    # Map to terrain coordinates
                    terrain_y = int(((lat + 90) / 180) * (grid_height - 1))
                    # Normalize angle to 0-360 for terrain lookup
                    terrain_lon = angle % 360
                    terrain_x = int((terrain_lon / 360) * (grid_width - 1))

                    # Clamp
                    terrain_y = max(0, min(grid_height - 1, terrain_y))
                    terrain_x = max(0, min(grid_width - 1, terrain_x))

                    # Get color and shade it
                    terrain_type = terrain_grid[terrain_y][terrain_x]
                    color = terrain_generator.get_terrain_color(terrain_type)

                    # Local shading based on position around circle
                    local_brightness = 0.5 + 0.5 * (z_3d / circle_radius)
                    final_brightness = brightness_factor * local_brightness
                    shaded_color = tuple(int(c * final_brightness) for c in color)

                    # Draw pixel
                    if 0 <= x_pos < screen.get_width() and 0 <= y_pos < screen.get_height():
                        screen.set_at((x_pos, y_pos), shaded_color)
