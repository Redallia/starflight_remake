import pytest
from src.utils.collision import point_in_circle

def test_point_at_center():
    """Point at exact center of circle should be inside"""
    # Point at (100, 100), circle at (100, 100), radius 50
    assert point_in_circle(100, 100, 100, 100, 50) == True

def test_point_on_boundary():
    """Point exactly on the circle edge should be inside (edge case, literally)"""
    # Point is exactly 50 units away from center
    assert point_in_circle(150, 100, 100, 100, 50) == True

def test_point_clearly_inside():
    """Point well within the cirlce"""
    assert point_in_circle(110, 100, 100, 100, 50) == True

def test_point_clearly_outside():
    """Point clearly outside the circle"""
    assert point_in_circle(200, 100, 100, 100, 50) == False

def test_point_just_outside():
    """Point just barely outside the circle"""
    # 51 units away horizontally, radius is 50
    assert point_in_circle(151, 100, 100, 100, 50) == False

def test_negative_coordinates():
    """Should work with negative coordinates"""
    assert point_in_circle(-10, -10, 0, 0, 20) == True