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

The game uses different coordinate grids depending on the navigation context. All follow the same Cartesian conventions (Y-up, origin at bottom-left), but vary in size and scale.

### Summary Table

| Context Type | Grid Dimensions | Center Point | Notes |
|-------------|-----------------|--------------|-------|
| Local Space (System) | 5000 × 5000 units | (2500, 2500) | Outer system, inner system, gas giant subsystems |
| Hyperspace | 2000 × 1760 units | (1000, 880) | 250×220 tiles @ 8×8 units/tile |
| Planetary Surface | 5000 × 2000 units | (2500, 1000) | 500×200 tiles @ 10×10 units/tile |

### Local Space Contexts

All LOCAL_SPACE navigation contexts (outer system, inner system, gas giant subsystems) use the same grid size:
- **Grid size**: 100 × 100 units
- **Center point**: (50, 50)
- **Boundaries**:
  - North boundary: y = 100
  - South boundary: y = 0
  - East boundary: x = 100
  - West boundary: x = 0

**Source**: Defined in `src/core/constants.py` as `CONTEXT_GRID_SIZE = 5000` and `CONTEXT_CENTER = 2500`

**Design Note**: These dimensions were standardized at 5000×5000 for consistency after initial testing with variable sizes. This provides a good balance between exploration time and navigation feel. Early design docs mention "TBD" grid sizes - that exploration phase is complete, and 5000×5000 is the current standard.

### Hyperspace Context

Hyperspace uses a **tile-based** coordinate system with different movement characteristics:
- **Grid**: 250 × 220 tiles
- **Tile size**: 8 × 8 units (for rendering/positioning)
- **Total space**: 2000 × 1760 units
- **Center point**: (1000, 880)
- **Movement feel**: Intended to feel "weightier" than local space movement

**Coordinate Example**:
```json
{
    "name": "Sol",
    "tile_position": {"x": 125, "y": 110},
    "unit_position": {"x": 1000, "y": 880}  // Tile * 8
}
```

**Implementation Status**: ⚠️ Hyperspace movement mechanics still need tuning/playtesting to achieve desired feel.

**Data**: Star system data stored in galaxy JSON with tile-based coordinates.

### Planetary Surface Context

Planetary surfaces use a **rectangular grid** with unique display conventions:
- **Grid**: 500 × 200 tiles
- **Tile size**: 10 × 10 units (for terrain rendering)
- **Total space**: 5000 × 2000 units
- **Center point**: (2500, 1000)
- **Wrapping**: X-axis wraps (cylindrical planet surface)

**Why different dimensions?**
- **5000 width**: Matches system space for familiar scale
- **2000 height**: Rectangular to represent planet surface (not full sphere)
- **500×200 tiles**: Manageable data size for procedural terrain storage
- **10×10 tile size**: Balance between detail and performance

**Coordinate Display Format**:
Surface positions are displayed using **directional notation** rather than raw Cartesian coordinates:
- **Format**: `[distance][direction]` for each axis
- **Example**: `127W, 43N` means 127 units west of center, 43 units north of center
- **Center displayed as**: `0, 0` (not 2500, 1000)

**Why directional notation?**
More intuitive for players exploring planet surfaces - "100 units west" is clearer than "x=2400". Matches real-world navigation conventions.

**Conversion**:
```python
# Cartesian to directional display
def to_surface_display(x, y):
    center_x, center_y = 2500, 1000

    # Calculate offset from center
    offset_x = x - center_x
    offset_y = y - center_y

    # Convert to directional notation
    x_dir = "E" if offset_x >= 0 else "W"
    y_dir = "N" if offset_y >= 0 else "S"

    return f"{abs(offset_x)}{x_dir}, {abs(offset_y)}{y_dir}"

# Example: (2627, 1043) → "127E, 43N"
# Example: (2373, 957) → "127W, 43S"
```

**Terrain Grid**:
Each 10×10 unit tile contains terrain type data for procedural generation. See `docs/design/procedural_generation.md` for terrain system details.

**Implementation Status**: ⚠️ Planetary surface navigation not yet implemented.

### Context-Specific Design Rationale

Each coordinate system is sized intentionally based on gameplay needs:

| Context | Why This Size? |
|---------|---------------|
| **System Space (5000×5000)** | Square grid provides uniform exploration in all directions. Size chosen to balance travel time between planets with sense of scale. |
| **Hyperspace (2000×1760)** | Smaller than system space to create denser galaxy feel. Tile-based storage (250×220 tiles) keeps galaxy data manageable. Aspect ratio accommodates rectangular screen display. |
| **Surface (5000×2000)** | Width matches system space for familiar scale. Height is shorter (planet surface, not full sphere). Rectangular fits natural terrain exploration patterns. |

**Common Thread**: All use standard Cartesian (Y-up) coordinates internally, only varying in dimensions and display conventions. This consistency simplifies code - same collision detection, movement, and rendering patterns work across all contexts.

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
# Local Space (System) Contexts
CONTEXT_GRID_SIZE = 100               # Grid dimensions for system space (100 × 100)
CONTEXT_CENTER = 50                   # Center point for system grids
SYSTEM_ORBITS = [16, 24, 32, 40]      # Orbital radii from center
CENTRAL_OBJECT_SIZE = 6               # Visual radius of central objects

# Hyperspace Context
HYPERSPACE_GRID_TILES = (250, 220)     # Hyperspace grid in tiles
HYPERSPACE_TILE_SIZE = 8               # Units per tile (8×8)
HYPERSPACE_GRID_SIZE = (2000, 1760)    # Total units (250*8, 220*8)
HYPERSPACE_CENTER = (1000, 880)        # Center point for hyperspace

# Planetary Surface Context
SURFACE_GRID_TILES = (500, 200)        # Surface grid in tiles
SURFACE_TILE_SIZE = 10                 # Units per tile (10×10)
SURFACE_GRID_SIZE = (5000, 2000)       # Total units (500*10, 200*10)
SURFACE_CENTER = (2500, 1000)          # Center point for surface
```

**Note**: Not all constants may exist in `constants.py` yet - this represents the complete set that should be defined as each context is implemented.

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

### Recent Updates

**January 2026 - Grid Size Standardization**
- Clarified that all system space contexts use standardized 5000×5000 grid
- Added comprehensive coverage of Hyperspace (2000×1760) and Planetary Surface (5000×2000) coordinate systems
- Documented surface coordinate directional notation (127W, 43N format)
- Added design rationale for why each context uses different dimensions
- **Note for other docs**: Some design documents (e.g., `navigation_specification.md`) mention "TBD" for grid sizes. This exploration phase is complete - refer to this document for current grid dimensions.
