# Context Transitions

## Overview
This document defines how the player's ship moves between different navigation contexts (hyperspace, outer system, inner system, gas giant subsystems) and how ship positioning is calculated during these transitions.

**Prerequisites**: Read `docs/technical/coordinate_systems.md` first - this doc assumes familiarity with the standard Cartesian coordinate system.

## Navigation Context Hierarchy

Navigation contexts form a hierarchical stack (FILO - First In, Last Out):

```
[CONTEXT_HYPERSPACE]                           # Base level (galactic map)
    ↓ Enter star system
[CONTEXT_HYPERSPACE, CONTEXT_LOCAL_SPACE (outer)]   # Star system outer region
    ↓ Enter gas giant subsystem
[CONTEXT_HYPERSPACE, CONTEXT_LOCAL_SPACE (outer), CONTEXT_LOCAL_SPACE (gas_giant_4)]
    ↓ Exit subsystem
[CONTEXT_HYPERSPACE, CONTEXT_LOCAL_SPACE (outer)]   # Back to outer system
```

**Key Concept**: Each context has its own 5000×5000 coordinate grid with the same layout and center point (2500, 2500).

## Coordinate Space Transformations

### Parent and Child Contexts

When entering a "child" context (e.g., entering a gas giant subsystem from outer system):
- **Parent context**: Outer system where gas giant exists at specific coordinates
- **Child context**: Gas giant subsystem with its own 5000×5000 grid
- **Central object**: Gas giant itself, positioned at (2500, 2500) in child context

### Key Principle: Context Regeneration

**When entering a child context, ship position is calculated fresh based on entry direction.** Previous positions are not preserved when re-entering the same context.

**Example**:
1. Player enters gas giant subsystem from the west → ship appears at west edge of subsystem
2. Player explores, then exits via north boundary → returns to outer system
3. Player re-enters same gas giant from the south → ship appears at south edge (NOT where they were before)

## Transition Types

### Type 1: Entering Child Context (Push)

**Trigger**: Ship collides with an object that has its own navigable subsystem
- Gas giant planet → Enter gas giant subsystem
- Star system → Enter outer system

**Process**:
1. Identify entry direction based on ship's approach vector
2. Create new NavigationContext with fresh ship_coords
3. Push new context onto navigation stack
4. Position ship at appropriate edge of new context

**Entry Direction Calculation**:
```python
def calculate_entry_direction(ship_x, ship_y, object_x, object_y):
    """
    Determine which direction ship is approaching from.

    Returns: One of "north", "south", "east", "west"
    """
    dx = ship_x - object_x
    dy = ship_y - object_y

    # Determine dominant direction (cardinal, not diagonal for MVP)
    if abs(dx) > abs(dy):
        return "east" if dx > 0 else "west"
    else:
        return "north" if dy > 0 else "south"
```

**Ship Positioning on Entry**:
```python
# Example: Entering gas giant subsystem from the west
# Ship should appear at west edge (x=0) of subsystem, vertically centered

entry_positions = {
    "north": (2500, 5000),  # Top edge, horizontally centered
    "south": (2500, 0),     # Bottom edge, horizontally centered
    "east": (5000, 2500),   # Right edge, vertically centered
    "west": (0, 2500)       # Left edge, vertically centered
}

ship_coords = entry_positions[entry_direction]
```

### Type 2: Exiting to Parent Context (Pop)

**Trigger**: Ship crosses boundary of current context
- Ship reaches edge of gas giant subsystem → Return to outer system
- Ship reaches edge of outer system → Return to hyperspace

**Process**:
1. Identify which boundary was crossed (north/south/east/west)
2. Pop current context from stack
3. Calculate ship position in parent context based on exit direction
4. Update parent context's ship_coords

**Exit Positioning Algorithm**:

The ship should appear just outside the object it's exiting, in the radial direction corresponding to the boundary crossed.

```python
import math

def calculate_exit_position(exit_boundary, object_x, object_y, object_radius, clearance=10):
    """
    Calculate ship position in parent context when exiting child context.

    Args:
        exit_boundary: "north", "south", "east", "west"
        object_x, object_y: Object's position in parent context
        object_radius: Collision radius of the object
        clearance: Extra distance beyond collision radius (default 10)

    Returns:
        tuple: (ship_x, ship_y) in parent context coordinates
    """
    # Map boundary to angle (see coordinate_systems.md)
    boundary_to_angle = {
        "east": 0,      # 0°
        "north": 90,    # 90°
        "west": 180,    # 180°
        "south": 270    # 270°
    }

    angle_degrees = boundary_to_angle[exit_boundary]
    angle_radians = math.radians(angle_degrees)

    # Position ship at angle, just outside object's radius
    distance = object_radius + clearance
    ship_x = object_x + math.cos(angle_radians) * distance
    ship_y = object_y + math.sin(angle_radians) * distance

    return (ship_x, ship_y)
```

**Example**:
```python
# Gas giant at (3200, 1800) in outer system, radius 100
# Player exits via north boundary of gas giant subsystem

ship_x, ship_y = calculate_exit_position("north", 3200, 1800, 100, 10)
# Result: (3200, 1910)  # Positioned 110 units north of gas giant center
```

### Type 3: Inner/Outer System Transition (Special Case)

**Status**: 🚧 Design in progress - considering alternatives

Inner system and outer system are conceptually sibling contexts, not parent/child. However, the current design treats them as nested:

**Current Approach (Nested)**:
```python
# Outer → Inner: Push new context
navigation_stack = [
    CONTEXT_HYPERSPACE,
    CONTEXT_LOCAL_SPACE(region=REGION_OUTER_SYSTEM),
    CONTEXT_LOCAL_SPACE(region=REGION_INNER_SYSTEM)  # Pushed on top
]

# Inner → Outer: Pop context
```

**Alternative Approach (Sibling Swap)**:
```python
# Only one active at a time
navigation_stack = [CONTEXT_HYPERSPACE, CONTEXT_LOCAL_SPACE(region=REGION_OUTER_SYSTEM)]
# OR
navigation_stack = [CONTEXT_HYPERSPACE, CONTEXT_LOCAL_SPACE(region=REGION_INNER_SYSTEM)]

# Transition = pop current, push new (swap operation)
```

**Open Question**: Which approach better supports future binary/trinary star systems?

**Positioning During Inner/Outer Transition**:

Regardless of approach, ship positioning follows the same rule as other transitions:

**Entering central zone** (outer → inner):
- Ship crosses into CENTRAL_OBJECT_SIZE radius at center of outer system
- Ship should appear at closest cardinal direction edge of inner system context
- Example: Approaching from south → appear at south edge (2500, 0) of inner system

**Exiting to outer boundary** (inner → outer):
- Ship crosses edge of inner system grid
- Ship should appear at corresponding position in outer system
- Example: Exit north boundary → appear just outside central zone's north edge in outer system

```python
# Entering inner system from the south
ship_in_outer = (2500, 2100)  # Just south of central zone
# Calculate entry direction, ship appears at:
ship_in_inner = (2500, 0)  # South edge of inner system

# Exiting inner system via north
ship_in_inner = (2500, 5000)  # North edge
# Ship appears at:
ship_in_outer = (2500, 2500 + CENTRAL_OBJECT_SIZE + clearance)
```

### Type 4: Entering Orbit (State Transition, Not Context)

**Important**: Entering orbit around a planet is both:
1. A **navigation context push** (adds CONTEXT_ORBIT to stack)
2. A **game state transition** (SpaceNavigationState → OrbitState)

This is different from other context transitions which stay in SpaceNavigationState.

**See**: `docs/technical/proximity_and_orbit.md` for details on orbit mechanics.

## Transition Edge Cases

### Approaching Central Zone from Gas Giant Subsystem

**Scenario**: Player is in a gas giant subsystem located in the inner system. They exit the gas giant subsystem toward the star.

**Expected behavior**:
1. Exit gas giant subsystem (pop context)
2. Return to inner system context
3. Ship positioned near gas giant
4. If ship is now inside central star zone → no automatic transition (player must manually navigate away)

### Re-entering Previously Visited Context

**Scenario**: Player enters gas giant subsystem, explores, exits, then immediately re-enters.

**Current design**: Context is regenerated - ship position resets based on entry direction (not preserved).

**Alternative consideration**: Track "last visited position" per context for X seconds/minutes?
- **Pros**: Less disorienting for accidental exits
- **Cons**: More complex state management, unclear timeout duration

**Decision**: Stick with regeneration for MVP. Revisit if playtest feedback indicates frustration.

## Implementation Requirements

### GameSession Methods Needed

```python
class GameSession:
    def push_context(self, context_type, **kwargs):
        """
        Enter a new navigation context.

        Args:
            context_type: Type of context (e.g., CONTEXT_LOCAL_SPACE)
            **kwargs: Context-specific data (region, ship_coords, etc.)
        """
        # Create and push new NavigationContext
        # Reset collision tracking
        pass

    def pop_context(self):
        """
        Exit current context, return to parent.

        Returns:
            The popped NavigationContext, or None if at base level
        """
        # Pop from stack
        # Reset collision tracking
        # Return popped context
        pass

    def calculate_entry_position(self, entry_direction):
        """Calculate ship position when entering a context"""
        pass

    def calculate_exit_position(self, exit_boundary, object_coords, object_radius):
        """Calculate ship position when exiting to parent context"""
        pass
```

### CollisionManager Updates Needed

When transitioning contexts, collision state must be reset:

```python
class CollisionManager:
    def reset(self):
        """Clear all collision state (call when changing contexts)"""
        self.last_planet_collision = None
        self.last_boundary_collision = None
        self.last_central_zone_collision = None
```

**Important**: Call `collision_manager.reset()` after every context push/pop to prevent stale collision triggers.

## Data Requirements

### Object Data Needed for Transitions

To calculate exit positions, we need:
- Object's position in parent context
- Object's collision radius

**For planets/gas giants**:
- Coordinates stored in star system JSON
- Radius calculated from planet.size attribute

**For central zones** (inner/outer system transitions):
- Zone center: (2500, 2500) in all system contexts
- Zone radius: CENTRAL_OBJECT_SIZE (300 from constants.py)

### Navigation Context Data Structure

```python
class NavigationContext:
    def __init__(self, context_type, **kwargs):
        self.type = context_type  # "hyperspace", "local_space", "orbit", etc.
        self.data = kwargs

# Example contexts:
NavigationContext(CONTEXT_HYPERSPACE, ship_coords=[125, 110])
NavigationContext(CONTEXT_LOCAL_SPACE, region=REGION_OUTER_SYSTEM, ship_coords=[2500, 4000])
NavigationContext(CONTEXT_LOCAL_SPACE, region="planet_4_subsystem", ship_coords=[0, 2500])
NavigationContext(CONTEXT_ORBIT, planet_index=2)  # No ship_coords (handled by OrbitState)
```

## Testing Scenarios

### Scenario 1: Gas Giant Round Trip
1. Start in outer system
2. Approach gas giant from west
3. Enter subsystem → verify ship at (0, 2500)
4. Navigate to north edge
5. Exit via north → verify ship appears north of gas giant in outer system

### Scenario 2: Inner/Outer Transitions
1. Start in outer system
2. Approach central zone from south
3. Enter inner system → verify ship at (2500, 0)
4. Navigate to west edge
5. Exit via west → verify ship appears west of central zone in outer system

### Scenario 3: Nested Context Chain
1. Start in outer system
2. Enter gas giant subsystem (depth 2)
3. Verify navigation_stack has 3 contexts
4. Exit via boundary → verify stack has 2 contexts
5. Verify ship positioned correctly in outer system

## Related Documentation

- **Coordinate Systems**: `docs/technical/coordinate_systems.md` - Foundation for all positioning math
- **Navigation Framework**: `docs/design/navigation_context_framework.md` - High-level architecture
- **Proximity and Orbit**: `docs/technical/proximity_and_orbit.md` - Planet proximity and orbit entry
- **Space Navigation State**: `docs/design/states/space_navigation.md` - Implementation of navigation state

## Open Design Questions

1. **Inner/outer system architecture**: Nested vs. sibling approach?
2. **Context position caching**: Should we preserve ship position when re-entering contexts?
3. **Binary/trinary systems**: How to handle multiple inner system contexts?
4. **Diagonal entry directions**: Should we support NE/NW/SE/SW entry, or round to cardinal directions?

## Future Enhancements

- **Smooth transitions**: Fade/zoom animation when changing contexts
- **Velocity preservation**: Carry momentum across context boundaries
- **Flux points**: Special hyperspace shortcuts with unique transition mechanics
- **Wormholes/gates**: Non-radial exit positioning (teleport-style transitions)
