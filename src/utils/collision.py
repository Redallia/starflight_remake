"""
Collision detection utility
"""

import pygame

def point_in_circle(point_x, point_y, circle_x, circle_y, radius):
    """
    Check if a point is inside a circle.

    Args:
        point_x, point_y: Coordinates of the point
        circle_x, circle_y: Center of the circle
        radius: Radius of the circle

    Returns:
        bool: True if point is inside or on the circle boundary
    """
    dx = circle_x - point_x # Calculate the difference in x-coordinates between the object and the player
    dy = circle_y - point_y # Calculate the difference in y-coordinates between the object and the player
    distance_squared = dx * dx + dy * dy # Calculate the squared distance between the two
    return distance_squared <= radius * radius # Return whether the point is inside or on the boundary