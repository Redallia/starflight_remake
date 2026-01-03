import pytest
from src.utils.position_calculator import (
    polar_to_cartesian, 
    calculate_launch_position, 
    get_cardinal_direction, 
    distance_squared, 
    distance)

def test_polar_to_cartesian():
    """Test polar to cartesian conversion"""
    x, y = polar_to_cartesian(0, 0, 0, 10)
    assert (x, y) == (10, 0)

    x, y = polar_to_cartesian(0, 0, 90, 10)
    assert (x, y) == (0, 10)

    x, y = polar_to_cartesian(0, 0, 180, 10)
    assert (x, y) == (-10, 0)

    x, y = polar_to_cartesian(0, 0, 270, 10)
    assert (x, y) == (0, -10)

def test_calculate_launch_position():
    """Test launch position calculation"""
    dock_coords = (100, 100)
    dock_radius = 20
    clearance = 10

    launch_pos = calculate_launch_position(dock_coords, dock_radius, clearance, 0)
    assert launch_pos == (130, 100)  # East

    launch_pos = calculate_launch_position(dock_coords, dock_radius, clearance, 90)
    assert launch_pos == (100, 130)  # North

    launch_pos = calculate_launch_position(dock_coords, dock_radius, clearance, 180)
    assert launch_pos == (70, 100)   # West

    launch_pos = calculate_launch_position(dock_coords, dock_radius, clearance, 270)
    assert launch_pos == (100, 70)   # South

def test_get_cardinal_direction():
    """Test cardinal direction calculation"""
    assert get_cardinal_direction((10, 0), (0, 0)) == "east"
    assert get_cardinal_direction((-10, 0), (0, 0)) == "west"
    assert get_cardinal_direction((0, 10), (0, 0)) == "north"
    assert get_cardinal_direction((0, -10), (0, 0)) == "south"
    assert get_cardinal_direction((10, 10), (0, 0)) == "north"
    assert get_cardinal_direction((-10, 10), (0, 0)) == "north"
    assert get_cardinal_direction((10, -10), (0, 0)) == "south"
    assert get_cardinal_direction((-10, -10), (0, 0)) == "south"
    assert get_cardinal_direction((0, 0), (0, 0)) == "Same"

def test_distance_functions():
    """Test distance and distance squared calculations"""
    p1 = (0, 0)
    p2 = (3, 4)

    assert distance_squared(p1, p2) == 25.0
    assert distance(p1, p2) == 5.0
    p3 = (-1, -1)
    p4 = (2, 3)
    assert distance_squared(p3, p4) == 25.0
    assert distance(p3, p4) == 5.0