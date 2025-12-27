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
        self.star_density = 0.0015 # Stars per pixel

        # TODO: Maybe add star color tiers

    def renderer(self, ship_x, ship_y):
        """
        Render the starfield to the given surface.
        
        Args:
            surface: Pygame surface to render to
            ship_x: Ship's X coordinate in world space
            ship_y: Ship's Y coordinate in world space
        """

        # TODO: Generate and draw stars
        pass