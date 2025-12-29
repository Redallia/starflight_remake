"""
Star entity class
The central body in a given star system
"""

import math
from core.constants import CONTEXT_CENTER

class Star:
    """
    Represents a star in a star system
    """

    def __init__(self, name, spectral_class, size):
        self.name = name
        self.spectral_class = spectral_class
        self.size = size

    def get_coordinates(self):
        return (CONTEXT_CENTER, CONTEXT_CENTER)