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
        Optimized sphere renderer with better coverage

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

        # Draw using a pixel grid approach for better coverage
        # Cover a square area around the sphere
        diameter = self.radius * 2
        start_x = int(center_x - self.radius)
        start_y = int(center_y - self.radius)

        for py in range(int(diameter) + 1):
            for px in range(int(diameter) + 1):
                # Calculate position relative to center
                dx = px - self.radius
                dy = py - self.radius

                # Check if this pixel is within the sphere
                distance_sq = dx * dx + dy * dy
                if distance_sq > self.radius * self.radius:
                    continue

                # Calculate 3D position on sphere
                distance = math.sqrt(distance_sq)

                # Get the z coordinate (depth)
                z_3d = math.sqrt(max(0, self.radius * self.radius - distance_sq))

                # Only render front half
                if z_3d <= 0:
                    continue

                # Calculate latitude (based on y position)
                lat_rad = math.asin(dy / self.radius)
                lat = math.degrees(lat_rad)

                # Calculate longitude (based on x position and z depth)
                if distance > 0:
                    lon_rad = math.atan2(dx, z_3d)
                    lon = math.degrees(lon_rad) + self.rotation_angle
                else:
                    lon = self.rotation_angle

                # Map to terrain coordinates
                terrain_y = int(((lat + 90) / 180) * (grid_height - 1))
                terrain_lon = lon % 360
                terrain_x = int((terrain_lon / 360) * (grid_width - 1))

                # Clamp
                terrain_y = max(0, min(grid_height - 1, terrain_y))
                terrain_x = max(0, min(grid_width - 1, terrain_x))

                # Get terrain color
                terrain_type = terrain_grid[terrain_y][terrain_x]
                color = terrain_generator.get_terrain_color(terrain_type)

                # Apply shading based on depth and angle
                # Light source from front-top
                light_dir_z = 0.7
                light_dir_y = -0.3

                # Surface normal (pointing outward from sphere)
                norm_x = dx / self.radius
                norm_y = dy / self.radius
                norm_z = z_3d / self.radius

                # Simple diffuse shading
                brightness = max(0.3, norm_z * light_dir_z + norm_y * light_dir_y)
                shaded_color = tuple(int(c * brightness) for c in color)

                # Draw the pixel
                screen_x = start_x + px
                screen_y = start_y + py
                if 0 <= screen_x < screen.get_width() and 0 <= screen_y < screen.get_height():
                    screen.set_at((int(screen_x), int(screen_y)), shaded_color)
