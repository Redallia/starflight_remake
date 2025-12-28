"""
Starfield renderer for space navigation view
"""

import pygame
import random

class StarfieldRenderer:
    """
    Renders a scrolling starfield background based on the ship's position

    Stars are generated deterministically based on position, so the 
    same stars appear at the same coordinates consistently.
    """

    def __init__(self, width, height):
        """
        Initialize the starfield renderer.
        
        Args:
            width: Width of the viewport in pixels
            height: Height of the viewport in pixels
        """

        self.width = width
        self.height = height

        # Star generation parameters
        self.star_density = 0.00015 # Stars per pixel

        # Star color tiers (brightness levels)
        # Each tier is (color, probability_weight)
        self.star_tiers = [
            ((100, 100, 100), 60), # dim gray @ 60%
            ((180, 180, 180), 30), # light gray @ 30%
            ((255, 255, 255), 10)  # white @ 10%
        ]

        # Grid-based star generation
        self.cell_size = 100 # Stars generated per 100x100 pixel cell
        self.stars_per_cell = int(self.cell_size * self.cell_size * self.star_density)


    def render(self, surface:pygame.Surface, ship_x:int, ship_y:int):
        """
        Render the starfield to the given surface.
        
        Args:
            surface: Pygame surface to render to
            ship_x: Ship's X coordinate in world space
            ship_y: Ship's Y coordinate in world space
        """

        # Fill background with black
        surface.fill((0, 0, 0))

        # Calculate camera offset (ship position centered in viewport)
        camera_x = ship_x - self.width // 2
        camera_y = - ship_y - self.height // 2

        # Calculate which grid cells are visible
        start_cell_x = camera_x // self.cell_size
        start_cell_y = camera_y // self.cell_size
        end_cell_x = (camera_x + self.width) // self.cell_size + 1
        end_cell_y = (camera_y + self.height) // self.cell_size + 1

        # Generate and draw stars
        for cell_x in range(start_cell_x, end_cell_x + 1):
            for cell_y in range(start_cell_y, end_cell_y + 1):
                self._render_stars_in_cell(surface, cell_x, cell_y, camera_x, camera_y)

    def _render_stars_in_cell(self, surface:pygame.Surface, cell_x:int, cell_y:int, camera_x:int, camera_y:int):
        """
        Render stars for a specific grid cell.

        Args:
            surface: Surface to draw to
            cell_x: Cell's X coordinate in grid
            cell_y: Cell's Y coordinate in grid
            camera_x: Camera's X offset in world space
            camera_y: Camera's Y offset in world space
        """
        # Use cell coordinates as random seed for deterministic generation
        random.seed(hash((cell_x, cell_y)))
        
        # Generate stars for this cell
        for _ in range(self.stars_per_cell):
            # Random position within the cell (0 to cell_size)
            local_x = random.randint(0, self.cell_size - 1)
            local_y = random.randint(0, self.cell_size - 1)
            
            # Convert to screen coordinates
            screen_x = (cell_x * self.cell_size) + local_x - camera_x
            screen_y = (cell_y * self.cell_size) + local_y - camera_y

            # Only draw if on screen
            if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
                # Select a color tier based on weighted probabilities
                color = self._choose_star_color()
                star_size = self._choose_star_size()
                if star_size == 1:
                    # 1-pixel star
                    surface.set_at((screen_x, screen_y), color)
                else:
                    # Draw larger stars
                    pygame.draw.circle(surface, color, (screen_x, screen_y), star_size)

    def _choose_star_color(self):
        """
        Choose a star color based on weighted probabilities

        Returns:
            RGB color tuple
        """
        total_weight = sum(weight for _, weight in self.star_tiers)
        choice = random.randint(1, total_weight)

        current = 0
        for color, weight in self.star_tiers:
            current += weight
            if choice <= current:
                return color
        return self.star_tiers[0][0] # Fallback for dim stars

    def _choose_star_size(self):
        """
        Choose a star size based on weighted probabilities.
        
        Returns:
            Star radius in pixels (1, 2, or 3)
        """
        choice = random.randint(1, 100)
        if choice <= 70:
            return 1  # 70% are 1-pixel dots
        elif choice <= 95:
            return 2  # 25% are 2-pixel circles
        else:
            return 3  # 5% are 3-pixel circles (bright stars)