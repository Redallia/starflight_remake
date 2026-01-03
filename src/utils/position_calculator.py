"""
Position calculation utility
"""

import math

def polar_to_cartesian(center_x, center_y, angle_degrees, distance):
    """
    Convert polar coordinates to Cartesian coordinates.

    Args:
        center_x, center_y: Center point coordinates
        angle_degrees: Angle in degrees
        distance: Distance from the center point

    Returns:
        (x, y): Cartesian coordinates
    """
    angle_radians = math.radians(angle_degrees)
    x = int(center_x + distance * math.cos(angle_radians))
    y = int(center_y + distance * math.sin(angle_radians))
    return (x, y)

def calculate_launch_position(dock_coords, dock_radius, clearance, launch_angle=0):
    """
    Calculate ship launch position from a dock.

    Args:
        dock_coords: (x, y) coordinates of the dock
        dock_radius: Radius of the dock
        clearance: Clearance distance from the dock
        launch_angle: Angle in degrees for the launch direction (default is 0)
    Returns:
        (x, y): Launch position coordinates
    """
    distance = dock_radius + clearance
    return polar_to_cartesian(dock_coords[0], dock_coords[1], launch_angle, distance)

def get_cardinal_direction(from_coords, to_coords):
    """
    Get the cardinal direction from one point to another.

    Args:
        from_coords: (x, y) starting coordinates
        to_coords: (x, y) target coordinates
    Returns:
        str: Cardinal direction ("N", "S", "E", "W", "NE", "NW", "SE", "SW")
    """
    dx = from_coords[0] - to_coords[0]
    dy = from_coords[1] - to_coords[1]

    if dx == 0 and dy == 0:
        return "Same"

    if abs(dx) > abs(dy):
        return "east" if dx > 0 else "west"
    else:
        return "north" if dy > 0 else "south"

def distance_squared(p1, p2):
    """
    Calculate squared distance between two points.

    Args:
        p1: (x, y) coordinates of the first point
        p2: (x, y) coordinates of the second point
    Returns:
        float: Squared distance between the points
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return float(dx * dx + dy * dy)

def distance(p1, p2):
    """
    Calculate distance between two points.

    Args:
        p1: (x, y) coordinates of the first point
        p2: (x, y) coordinates of the second point
    Returns:
        float: Distance between the points
    """
    return math.sqrt(distance_squared(p1, p2))
