# Coordinate Systems

## Overview
This document defines the coordinate system conventions used throughout the Starflight Remake project. All code, design docs, and data files should follow these conventions.

**IMPORTANT**: This is the single source of truth for coordinate system definitions. All other documents should reference this file rather than redefining coordinate conventions.

## Standard Cartesian Grid

The game uses a **standard Cartesian coordinate system** across all navigation contexts:

- **X-axis**: Increases from left (0) to right (5000)
  - West ← 0 ... 2500 (center) ... 5000 → East
- **Y-axis**: Increases from bottom (0) to top (5000) - **NOT INVERTED**
  - South ↓ 0 ... 2500 (center) ... 5000 ↑ North
- **Origin**: Bottom-left corner at (0, 0)
- **Center**: Always at (2500, 2500) for all 5000×5000 grids

### Visual Reference
```
        North (Y = 5000)
              ↑
              |
    (0,5000)  |  (5000,5000)
         +----+----+
         |    |    |
West ←---+-(2500,--+--→ East
(X=0)    | 2500)   |  (X=5000)
         |    |    |
         +----+----+
    (0,0)     |  (5000,0)
              |
              ↓
        South (Y = 0)
```

## Grid Dimensions

All navigation contexts use the same grid size:
- **Grid size**: 5000 × 5000 units
- **Center point**: (2500, 2500)
- **Boundaries**:
  - North boundary: y = 5000
  - South boundary: y = 0
  - East boundary: x = 5000
  - West boundary: x = 0

**Source**: Defined in `src/core/constants.py` as `CONTEXT_GRID_SIZE = 5000` and `CONTEXT_CENTER = 2500`

## Angular Conventions

When calculating positions using angles (for radial positioning, orbital mechanics, etc.):

- **0° / 360°**: East (positive X direction)
- **90°**: North (positive Y direction)
- **180°**: West (negative X direction)
- **270°**: South (negative Y direction)

### Cardinal Direction to Angle Mapping

| Cardinal Direction | Angle | Radial Vector (from center) |
|-------------------|-------|------------------------------|
| East              | 0°    | (+1, 0)                      |
| North             | 90°   | (0, +1)                      |
| West              | 180°  | (-1, 0)                      |
| South             | 270°  | (0, -1)                      |

### Calculating Positions from Angles

For positioning objects at a specific angle and distance from a center point:

```python
import math

def position_at_angle(center_x, center_y, angle_degrees, distance):
    """
    Calculate position at specified angle and distance from center.

    Args:
        center_x, center_y: Center point coordinates
        angle_degrees: Angle in degrees (0° = East, 90° = North)
        distance: Distance from center

    Returns:
        tuple: (x, y) position
    """
    angle_radians = math.radians(angle_degrees)
    x = center_x + math.cos(angle_radians) * distance
    y = center_y + math.sin(angle_radians) * distance
    return (x, y)
```

**Example**:
```python
# Position object 1000 units north of center
x, y = position_at_angle(2500, 2500, 90, 1000)
# Result: (2500, 3500)
```

## Boundary Collision to Angular Direction

When a ship exits a navigation context via a boundary, the boundary direction maps to a radial angle for positioning in the parent context:

| Boundary Hit | Context Edge | Maps to Angle | Meaning |
|-------------|--------------|---------------|---------|
| North       | y = 5000     | 90°           | Exit straight up from object center |
| South       | y = 0        | 270°          | Exit straight down from object center |
| East        | x = 5000     | 0°            | Exit straight right from object center |
| West        | x = 0        | 180°          | Exit straight left from object center |

**See**: `docs/technical/context_transitions.md` for how these angles are used in parent context positioning.

## Rendering Considerations

### Pygame Screen Coordinates vs. Game Coordinates

**Important**: Pygame's screen coordinate system has Y increasing downward (inverted from our game coordinates).

When rendering to the screen:
```python
# Game coordinates: Y increases upward (North)
game_x = 2500
game_y = 3500  # North of center

# Pygame screen: Y increases downward
# Must invert Y when rendering
screen_y = SCREEN_HEIGHT - game_y  # Flip Y axis
```

**All game logic** (movement, collision detection, data storage) uses the standard Cartesian system defined above. **Only rendering code** should perform Y-axis conversion for Pygame.

### Viewport and Camera

The main view shows a viewport centered on the player's ship:
- Ship sprite rendered at screen center
- Background (starfield) scrolls to create motion illusion
- Other objects (planets, stations) rendered relative to ship position

**Viewport coordinates** still follow standard Cartesian convention. Only final screen rendering inverts Y.

## Distance Calculations

For distance between two points:
```python
import math

def distance(x1, y1, x2, y2):
    """Calculate Euclidean distance between two points"""
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx*dx + dy*dy)
```

## Movement Vectors

Movement vectors follow standard Cartesian conventions:
- **North**: (0, +speed)
- **South**: (0, -speed)
- **East**: (+speed, 0)
- **West**: (-speed, 0)
- **Northeast**: (+speed, +speed)
- **Northwest**: (-speed, +speed)
- **Southeast**: (+speed, -speed)
- **Southwest**: (-speed, -speed)

**Note**: Input handling may need to negate Y values from keyboard input to match this convention (e.g., "up arrow" increases Y).

## Data File Conventions

All JSON data files storing coordinates use this same system:
- Planet positions in star system files
- Ship positions in save files
- Navigation context ship_coords

**Example** (from `star_systems.json`):
```json
{
    "name": "Aqua",
    "coordinates": {"x": 2500, "y": 3500}  // North of center
}
```

## Key Constants Reference

All coordinate-related constants are defined in `src/core/constants.py`:

```python
CONTEXT_GRID_SIZE = 5000    # Grid dimensions (5000 × 5000)
CONTEXT_CENTER = 2500        # Center point for all grids
SYSTEM_ORBITS = [800, 1200, 1600, 2000]  # Orbital radii from center
CENTRAL_OBJECT_SIZE = 300    # Visual radius of central objects
```

## Related Documentation

- **Context Transitions**: `docs/technical/context_transitions.md` - How ship repositions between contexts
- **Navigation Framework**: `docs/design/navigation_context_framework.md` - High-level navigation system design
- **Collision Detection**: `src/core/collision_manager.py` - Implementation of collision using these coordinates

## Common Pitfalls

1. **Don't invert Y in game logic** - Only invert when rendering to Pygame surface
2. **Don't mix degrees and radians** - Standard library `math.sin/cos` use radians, always convert
3. **Don't assume screen coords = game coords** - Always be explicit about which system you're using
4. **Boundary checks**: Remember y=0 is SOUTH, y=5000 is NORTH (not inverted)

## Migration Notes

If you encounter code or docs that use inverted Y coordinates (y=0 at top), they need to be updated to follow this standard. Mark with TODO and reference this document.
