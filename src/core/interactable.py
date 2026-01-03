class Interactable:
    def __init__(self, x, y, interactable_type, shape_type, shape_data, data=None):
        self.x = x
        self.y = y
        self.type = interactable_type
        self.shape_type = shape_type
        self.shape_data = shape_data
        self.data = data
    
    def __eq__(self, other):
        if not isinstance(other, Interactable):
            return False
        if self.data is not None and other.data is not None:
            return self.data is other.data  # Compare the wrapped objects
        # Fallback: compare by position and type
        return (self.x == other.x and self.y == other.y and self.type == other.type)
    
    def __repr__(self):
        """String representation for debugging"""
        return f"Interactable(type={self.type}, x={self.x}, y={self.y}, shape={self.shape_type})"

    @classmethod
    def circle(cls, x, y, radius, interactable_type, data=None):
        """Create a circular interactable."""
        return cls(x, y, interactable_type, "circle", {"radius": radius}, data)
    
    @classmethod
    def rectangle(cls, x, y, width, height, interactable_type, data=None):
        """Create a rectangular interactable."""
        return cls(x, y, interactable_type, "rectangle", 
                   {"width": width, "height": height}, data)

# Usage:
# Interactable.circle(planet_x, planet_y, planet.size, INTERACTION_PLANET, planet)
# Interactable.rectangle(building_x, building_y, 10, 5, INTERACTION_BUILDING, building)