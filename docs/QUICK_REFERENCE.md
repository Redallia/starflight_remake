# Quick Reference Card

Quick lookup for common questions during implementation.

---

## Coordinate System

**Grid**: 5000×5000 units, center at (2500, 2500)

**Axes**:
- X: 0 (west) → 5000 (east)
- Y: 0 (south) → 5000 (north) - **NOT INVERTED**

**Directions**:
- North = +Y (up)
- South = -Y (down)
- East = +X (right)
- West = -X (left)

**Angles**:
- 0° = East
- 90° = North
- 180° = West
- 270° = South

**Boundaries**:
- North: y = 5000
- South: y = 0
- East: x = 5000
- West: x = 0

📖 **See**: [docs/technical/coordinate_systems.md](technical/coordinate_systems.md)

---

## Constants

**Ship**:
- Ship radius: 11 units (half of 22px sprite)
- Ship clearance from objects: 10 units

**Grid**:
- Grid size: 5000 (defined in `src/core/constants.py` as `CONTEXT_GRID_SIZE`)
- Center: 2500 (defined as `CONTEXT_CENTER`)
- Central object size: 300 (defined as `CENTRAL_OBJECT_SIZE`)

**Proximity**:
- Proximity pause duration: 1.0 seconds
- Proximity radius: planet.size + ship_radius
- Orbit exit clearance: 10 units
- Slingshot clearance: 10 units

**Orbits**:
- Standard orbital radii: [800, 1200, 1600, 2000]
- 4 orbital slots per system

📖 **See**: `src/core/constants.py`

---

## Positioning Formulas

### Radial Position from Angle
```python
import math

x = center_x + math.cos(math.radians(angle)) * distance
y = center_y + math.sin(math.radians(angle)) * distance
```

### Exit Position (Boundary → Radial)
```python
boundary_to_angle = {
    "north": 90,
    "south": 270,
    "east": 0,
    "west": 180
}

angle = boundary_to_angle[boundary]
distance = object_radius + clearance  # clearance = 10

ship_x = object_x + math.cos(math.radians(angle)) * distance
ship_y = object_y + math.sin(math.radians(angle)) * distance
```

### Entry Position (Direction → Edge)
```python
entry_positions = {
    "north": (2500, 5000),  # Top edge, centered horizontally
    "south": (2500, 0),     # Bottom edge, centered horizontally
    "east": (5000, 2500),   # Right edge, centered vertically
    "west": (0, 2500)       # Left edge, centered vertically
}

ship_coords = entry_positions[entry_direction]
```

📖 **See**: [docs/technical/context_transitions.md](technical/context_transitions.md)

---

## Navigation Context Stack

### Structure
```python
navigation_stack = [
    NavigationContext(CONTEXT_HYPERSPACE, ship_coords=[125, 110]),
    NavigationContext(CONTEXT_LOCAL_SPACE, region=REGION_OUTER_SYSTEM, ship_coords=[2500, 4000]),
    NavigationContext(CONTEXT_LOCAL_SPACE, region="planet_4_subsystem", ship_coords=[300, 300])
]
```

### Current Context
```python
current_context = navigation_stack[-1]
ship_position = current_context.data["ship_coords"]
```

### Push Context (Enter)
```python
new_context = NavigationContext(context_type, ship_coords=[x, y], **other_data)
navigation_stack.append(new_context)
collision_manager.reset()
```

### Pop Context (Exit)
```python
if len(navigation_stack) > 1:
    popped = navigation_stack.pop()
    collision_manager.reset()
```

📖 **See**: [docs/design/navigation_context_framework.md](design/navigation_context_framework.md)

---

## Collision Detection

### Planet Proximity
```python
distance = math.sqrt((ship_x - planet_x)**2 + (ship_y - planet_y)**2)
proximity_radius = planet.size + ship_radius  # ship_radius = 11

if distance <= proximity_radius:
    # Trigger proximity pause
```

### Boundary Check
```python
if ship_x <= 0:
    boundary = "west"
elif ship_x >= CONTEXT_GRID_SIZE:
    boundary = "east"
elif ship_y <= 0:
    boundary = "south"
elif ship_y >= CONTEXT_GRID_SIZE:
    boundary = "north"
```

### Central Zone
```python
distance_from_center = math.sqrt((ship_x - 2500)**2 + (ship_y - 2500)**2)

if distance_from_center <= CENTRAL_OBJECT_SIZE:  # 300
    # Entering central zone (inner/outer transition)
```

📖 **See**: `src/core/collision_manager.py`

---

## State Transitions

### Enter Orbit
```python
# 1. Push orbit context
planet_index = get_planet_index(planet)
game_session.push_context(CONTEXT_ORBIT, planet_index=planet_index)

# 2. Change state
state_manager.change_state("orbit")
```

### Leave Orbit
```python
# 1. Pop orbit context
game_session.pop_context()

# 2. Position ship outside proximity
planet_x, planet_y = planet.get_coordinates()
angle = 90  # North
distance = planet.size + ship_radius + clearance

ship_x = planet_x + math.cos(math.radians(angle)) * distance
ship_y = planet_y + math.sin(math.radians(angle)) * distance
game_session.current_context.data["ship_coords"] = [ship_x, ship_y]

# 3. Change state
state_manager.change_state("space_navigation")
```

📖 **See**: [docs/technical/proximity_and_orbit.md](technical/proximity_and_orbit.md)

---

## Proximity State Machine

```
[Normal Navigation]
    ↓ (proximity detected)
[Proximity Pause] (1 second, inputs frozen)
    ↓ Space pressed              ↓ Timeout
[Enter Orbit]                [Slingshot]
    ↓                            ↓
OrbitState              Normal Navigation
```

### Slingshot Position
```python
# Vector from planet to ship
dx = ship_x - planet_x
dy = ship_y - planet_y
distance = math.sqrt(dx*dx + dy*dy)

# Normalize
dx /= distance
dy /= distance

# Opposite side
opposite_distance = distance + clearance  # clearance = 10
new_x = planet_x - dx * opposite_distance
new_y = planet_y - dy * opposite_distance
```

📖 **See**: [docs/technical/proximity_and_orbit.md](technical/proximity_and_orbit.md)

---

## Data Structures

### NavigationContext
```python
class NavigationContext:
    def __init__(self, context_type, **kwargs):
        self.type = context_type  # CONTEXT_HYPERSPACE, CONTEXT_LOCAL_SPACE, etc.
        self.data = kwargs        # ship_coords, region, planet_index, etc.
```

### Common Context Types
```python
CONTEXT_HYPERSPACE = "hyperspace"
CONTEXT_LOCAL_SPACE = "local_space"
CONTEXT_ORBIT = "orbit"
CONTEXT_SURFACE = "surface"
CONTEXT_DOCKED = "docked"
```

### Region Types
```python
REGION_INNER_SYSTEM = "inner_system"
REGION_OUTER_SYSTEM = "outer_system"
REGION_GAS_GIANT = "gas_giant"
```

📖 **See**: `src/core/constants.py`, `src/core/game_session.py`

---

## Common Patterns

### Calculate Entry Direction
```python
def calculate_entry_direction(ship_x, ship_y, object_x, object_y):
    dx = ship_x - object_x
    dy = ship_y - object_y

    if abs(dx) > abs(dy):
        return "east" if dx > 0 else "west"
    else:
        return "north" if dy > 0 else "south"
```

### Distance Between Points
```python
def distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx*dx + dy*dy)
```

### Point in Circle
```python
def point_in_circle(px, py, cx, cy, radius):
    return distance(px, py, cx, cy) <= radius
```

📖 **See**: `src/utils/collision.py`

---

## Rendering Notes

### Pygame Y-Inversion
Pygame uses inverted Y (Y increases downward). **Only invert Y when rendering**, never in game logic:

```python
# Game logic: standard Cartesian
game_x = 2500
game_y = 3500  # North of center

# Rendering: invert Y for pygame
screen_x = game_x
screen_y = SCREEN_HEIGHT - game_y  # Flip Y axis
```

**IMPORTANT**: All collision detection, movement, and position storage use standard Cartesian. Only the final render step inverts Y.

📖 **See**: [docs/technical/coordinate_systems.md](technical/coordinate_systems.md)

---

## Need More Details?

| Topic | Document |
|-------|----------|
| Coordinate system | [coordinate_systems.md](technical/coordinate_systems.md) |
| Context transitions | [context_transitions.md](technical/context_transitions.md) |
| Proximity & orbit | [proximity_and_orbit.md](technical/proximity_and_orbit.md) |
| State architecture | [state_architecture.md](technical/state_architecture.md) |
| Navigation framework | [navigation_context_framework.md](design/navigation_context_framework.md) |
| Space navigation | [space_navigation.md](design/states/space_navigation.md) |
| All technical docs | [technical/README.md](technical/README.md) |

---

## Common Gotchas

❌ **Don't** invert Y in game logic
✅ **Do** invert Y only when rendering to pygame surface

❌ **Don't** use degrees in `math.sin/cos`
✅ **Do** convert to radians: `math.radians(angle_degrees)`

❌ **Don't** forget to reset collision manager when changing contexts
✅ **Do** call `collision_manager.reset()` after push/pop

❌ **Don't** assume y=0 is at the top
✅ **Do** remember y=0 is south, y=5000 is north

❌ **Don't** preserve ship position when re-entering contexts
✅ **Do** regenerate position based on entry direction

---

**Last Updated**: 2025-12-29
