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

        # Frame caching for performance
        self.cached_frames = []  # List of pre-rendered frames
        self.num_cached_frames = 18  # 18 frames = 20 degree steps
        self.current_terrain_id = None  # Track which terrain we've cached

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

    def _generate_cached_frames(self, terrain_grid, terrain_generator):
        """Pre-render all rotation frames for smooth performance"""
        self.cached_frames = []
        diameter = int(self.radius * 2)

        for frame_idx in range(self.num_cached_frames):
            # Calculate rotation angle for this frame
            angle = (frame_idx / self.num_cached_frames) * 360

            # Create a surface for this frame
            frame_surface = pygame.Surface((diameter + 2, diameter + 2), pygame.SRCALPHA)

            # Render this rotation angle to the surface
            self._render_frame_to_surface(frame_surface, self.radius + 1, self.radius + 1,
                                          angle, terrain_grid, terrain_generator)

            # Store the frame
            self.cached_frames.append(frame_surface)

        # Mark this terrain as cached
        self.current_terrain_id = id(terrain_grid)

    def _render_frame_to_surface(self, surface, center_x, center_y, angle, terrain_grid, terrain_generator):
        """Render a single frame at a specific rotation angle to a surface"""
        grid_height = len(terrain_grid)
        grid_width = len(terrain_grid[0]) if grid_height > 0 else 0

        if grid_width == 0 or grid_height == 0:
            return

        # Same pixel rendering logic as render_optimized, but to a surface
        diameter = self.radius * 2

        for py in range(int(diameter) + 1):
            for px in range(int(diameter) + 1):
                dx = px - self.radius
                dy = py - self.radius

                distance_sq = dx * dx + dy * dy
                if distance_sq > self.radius * self.radius:
                    continue

                distance = math.sqrt(distance_sq)
                z_3d = math.sqrt(max(0, self.radius * self.radius - distance_sq))

                if z_3d <= 0:
                    continue

                lat_rad = math.asin(dy / self.radius)
                lat = math.degrees(lat_rad)

                if distance > 0:
                    lon_rad = math.atan2(dx, z_3d)
                    lon = math.degrees(lon_rad) + angle
                else:
                    lon = angle

                terrain_y = int(((lat + 90) / 180) * (grid_height - 1))
                terrain_lon = lon % 360
                terrain_x = int((terrain_lon / 360) * (grid_width - 1))

                terrain_y = max(0, min(grid_height - 1, terrain_y))
                terrain_x = max(0, min(grid_width - 1, terrain_x))

                terrain_type = terrain_grid[terrain_y][terrain_x]
                color = terrain_generator.get_terrain_color(terrain_type)

                # Simple shading based on depth
                shade_factor = (z_3d / self.radius) * 0.5 + 0.5
                shaded_color = tuple(int(c * shade_factor) for c in color)

                surface.set_at((int(px), int(py)), shaded_color)

    def render_optimized(self, screen, center_x, center_y, terrain_grid, terrain_generator):
        """
        Optimized sphere renderer using cached frames

        Args:
            screen: Pygame surface
            center_x, center_y: Center position of sphere
            terrain_grid: 2D array of terrain (500x200)
            terrain_generator: TerrainGenerator for colors
        """
        if not terrain_grid or not terrain_generator:
            return

        # Check if we need to generate cached frames
        terrain_id = id(terrain_grid)
        if not self.cached_frames or self.current_terrain_id != terrain_id:
            self._generate_cached_frames(terrain_grid, terrain_generator)

        # Determine which cached frame to use based on rotation angle
        # Each frame represents 20 degrees (360 / 18)
        frame_index = int((self.rotation_angle % 360) / 20)
        frame_index = min(frame_index, len(self.cached_frames) - 1)

        # Blit the cached frame to screen
        frame_surface = self.cached_frames[frame_index]

        # Calculate top-left position to center the frame
        frame_x = int(center_x - self.radius - 1)
        frame_y = int(center_y - self.radius - 1)

        screen.blit(frame_surface, (frame_x, frame_y))
