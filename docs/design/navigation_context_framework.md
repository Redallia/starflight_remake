# Navigation Context Framework

## Overview
The Navigation Context Framework provides a hierarchical navigation system for space exploration. Players navigate through nested contexts: Hyperspace (Sector map) → Star System (Outer/Inner) → Orbital Zones → Orbit → Surface/Station.

This framework emerged from the game's core identity as a hierarchical navigation system with economy and narrative hooks at specific locations.

**Related Documentation:**
- See [Space Navigation State](states/space_navigation.md) for implementation specifications, HUD layout, input handling, and development phases
- This document provides the high-level architectural design and system philosophy

## Design Philosophy
- **Nested Navigation**: Each context can contain sub-contexts that players enter and exit
- **Consistent Mechanics**: Same movement and display paradigm across all contexts
- **Stack-based State**: FILO stack tracks navigation hierarchy
- **Persistent Location**: Navigation state survives across game state transitions (orbit, surface, etc.)

## Navigation Context Types

### Hyperspace
The default base navigation context for traveling between star systems.

**Characteristics:**
- Player navigates the galactic map
- Stars visible as navigation targets in Main View
- Fuel consumption active (engine class based)
- Not tracked in navigation stack (implicit base state)

**Transitions:**
- Collision with star → Enter that star's outer system

### System Space - Outer System
The outer region of a star system containing gas giants and outer planets.

**Characteristics:**
- Main View: Rolling starfield with planets visible when in viewport range
- Auxiliary View: Mini-map showing outer planets/orbits + inner system zone (center)
- No fuel consumption (MVP)

**Collisions:**
- Gas giant planet → Enter gas giant sub-system context
- Regular planet → Enter orbit (state transition)
- Inner system zone (center) → Enter inner system context
- Outer edge → Return to hyperspace

**Navigation:**
- Mini-map for overall system positioning
- Main View for fine-grain planetary approach

### System Space - Inner System
The inner region of a star system containing rocky planets near the primary star.

**Characteristics:**
- Main View: Rolling starfield with planets visible when in viewport range
- Auxiliary View: Mini-map showing inner planets/orbits + primary star (center, non-interactive)
- No fuel consumption (MVP)

**Collisions:**
- Gas giant planet → Enter gas giant sub-system context
- Regular planet → Enter orbit (state transition)
- Outer edge → Return to outer system context

**Special Notes:**
- Primary star has no collision detection
- Primary star is not orbitable

### System Space - Gas Giant Sub-System
A localized region around a gas giant and its moons.

**Characteristics:**
- Main View: Rolling starfield with moons visible when in viewport range
- Auxiliary View: Mini-map showing gas giant (center) + moons/orbits
- No fuel consumption (MVP)

**Collisions:**
- Moon → Enter orbit (state transition)
- Gas giant → Enter orbit (same as regular planet)
- Outer edge → Return to parent system context (outer or inner)

## Navigation Stack Architecture

### Stack Structure
Navigation contexts are tracked using a **FILO (First In, Last Out) stack** stored at the top level of `game_state`. This ensures navigation context persists across state transitions (entering orbit, landing on planets, docking at starport).

### Key Design Decisions
1. **Object-based contexts**: Stack contains NavigationContext objects (not strings) with `.type` and `.data` attributes
2. **Encapsulated coordinates**: Each NavigationContext stores its own ship coordinates in `.data["ship_coords"]`
3. **Hyperspace included**: Hyperspace is stored at index 0 of the stack (simplifies logic, more consistent)
4. **Rich system objects**: `current_system` is a StarSystem object, not just coordinates
5. **Index-based bodies**: Celestial bodies (planets, moons, gas giants) identified by orbital index (0-based, numbered from innermost to outermost orbit)

### Game State Structure

```python
# GameSession structure (in src/core/game_session.py)
class NavigationContext:
    """Represents a single navigation context"""
    def __init__(self, context_type, **kwargs):
        self.type = context_type  # e.g., CONTEXT_HYPERSPACE, CONTEXT_LOCAL_SPACE, CONTEXT_ORBIT
        self.data = kwargs        # context-specific data (ship_coords, region, planet_index, etc.)

class GameSession:
    def __init__(self):
        self.current_system = StarSystem(...)  # StarSystem object, not coordinate dict
        self.navigation_stack = [
            NavigationContext(CONTEXT_HYPERSPACE, ship_coords=[125, 110]),
            NavigationContext(CONTEXT_LOCAL_SPACE, region=REGION_OUTER_SYSTEM, ship_coords=[2500, 4000]),
            NavigationContext(CONTEXT_LOCAL_SPACE, region="planet_4_subsystem", ship_coords=[300, 300])
        ]
        self.player_ship = Ship(...)
        self.messages = []  # Message log for UI feedback

    @property
    def current_context(self):
        """Returns the top of the navigation stack"""
        return self.navigation_stack[-1] if self.navigation_stack else None

    @property
    def ship_position(self):
        """Gets ship coordinates from current context"""
        return self.current_context.data.get("ship_coords", [0, 0])
```

### Stack Examples

**Player in hyperspace:**
```python
current_system: None
navigation_stack: [
    NavigationContext(CONTEXT_HYPERSPACE, ship_coords=[125, 110])
]
```

**Player in outer system (star at galactic coords 125, 110):**
```python
current_system: StarSystem("Arth")  # StarSystem object
navigation_stack: [
    NavigationContext(CONTEXT_HYPERSPACE, ship_coords=[125, 110]),
    NavigationContext(CONTEXT_LOCAL_SPACE, region=REGION_OUTER_SYSTEM, ship_coords=[2500, 4000])
]
```

**Player in gas giant sub-system (planet at orbital position 4):**
```python
current_system: StarSystem("Arth")
navigation_stack: [
    NavigationContext(CONTEXT_HYPERSPACE, ship_coords=[125, 110]),
    NavigationContext(CONTEXT_LOCAL_SPACE, region=REGION_OUTER_SYSTEM, ship_coords=[2500, 3000]),
    NavigationContext(CONTEXT_LOCAL_SPACE, region="planet_4_subsystem", ship_coords=[300, 300])
]
```

**Player in inner system (navigated from outer system):**
```python
current_system: StarSystem("Arth")
navigation_stack: [
    NavigationContext(CONTEXT_HYPERSPACE, ship_coords=[125, 110]),
    NavigationContext(CONTEXT_LOCAL_SPACE, region=REGION_OUTER_SYSTEM, ship_coords=[2500, 2500]),
    NavigationContext(CONTEXT_LOCAL_SPACE, region=REGION_INNER_SYSTEM, ship_coords=[2500, 2500])
]
```

## Context Transitions

### Navigation Context Transitions
- **Entering hyperspace from system**: Set `current_system` to None and pop all contexts until only CONTEXT_HYPERSPACE remains
- **Entering system from hyperspace**: Set `current_system` to StarSystem object, push new NavigationContext(CONTEXT_LOCAL_SPACE, region=REGION_OUTER_SYSTEM, ship_coords=[...])
- **Entering a new context within system**: Push new NavigationContext object onto stack with appropriate type and data
- **Exiting a context**: Pop current context off stack, return to previous context

### Positioning on Transition
- **Direction of approach is respected**: Ship orientation/heading determines which edge you enter from
- **On entering a context**: Ship appears at the edge of the new context corresponding to approach direction
- **On exiting a context**: Ship appears at the edge of the object being exited, positioned by exit direction
- **Coordinates not preserved**: Stack doesn't save position; positioning is calculated based on entry/exit direction
- **Flux jumps**: Special case, to be designed separately

### State Transition Example (Entering/Leaving Orbit)

**Player navigates to moon 2 of gas giant at position 4:**
- `current_system`: `StarSystem("Arth")`
- `navigation_stack`: `[NavigationContext(CONTEXT_HYPERSPACE, ...), NavigationContext(CONTEXT_LOCAL_SPACE, region=REGION_OUTER_SYSTEM, ...), NavigationContext(CONTEXT_LOCAL_SPACE, region="planet_4_subsystem", ship_coords=[350, 280])]`
- `current_context.type`: `CONTEXT_LOCAL_SPACE`
- Collision with moon → transition to orbit

**Player enters orbit around the moon:**
- `current_system`: `StarSystem("Arth")` (preserved)
- `navigation_stack`: Previous stack + `NavigationContext(CONTEXT_ORBIT, planet_index=2)` (moon 2 of gas giant)
- `current_context.type`: `CONTEXT_ORBIT`
- Game state transitions to OrbitState

**Player launches from the moon:**
- `current_system`: `StarSystem("Arth")` (preserved)
- `navigation_stack`: Pop CONTEXT_ORBIT, back to `[..., NavigationContext(CONTEXT_LOCAL_SPACE, region="planet_4_subsystem", ship_coords=[350, 280])]`
- `current_context.type`: `CONTEXT_LOCAL_SPACE`
- Ship appears near moon 2's coordinates in planet_4_subsystem context
- Game state transitions back to SpaceNavigationState

## Movement System

### Input and Control
- **WASD or arrow keys**: Control ship direction (tile-based movement)
- **Ship position**: Always centered in Main View
- **Starfield scrolling**: Scrolls in direction of movement to create sense of motion (all contexts)
- **Objects**: Planets/moons/stars move relative to centered ship
- **Spacebar**: Disengages maneuver mode
- **Control Panel**: Locked on Navigator/Maneuver while active

### Movement Characteristics
- **Tile-based**: No physics simulation or momentum (MVP)
- **No inertia**: Ship only moves when actively maneuvering
- **Keyboard-driven**: WASD/arrow key movement

### Fuel Consumption
- **Hyperspace**: Engine class `power_consumption_rate` per coordinate traveled (Class 1 = 0.48 fuel/coordinate)
- **System space** (all sub-types): No fuel consumption for MVP

## Visual Presentation

### Main View
All contexts share the same visual paradigm:
- **Starfield background**: Scrolls to create motion feedback
- **Player ship icon**: Centered in view
- **Viewport**: Shows region around player ship
- **Objects**: Visible when within viewport range, slide into view as player moves

**Context-Specific Elements:**
- **Hyperspace**: Stars as navigation targets, nebulae, flux points
- **System Space**: Planets/moons at their coordinates, starport (if in home system)

**MVP Note**: Planets/moons are stationary at fixed coordinates (no orbital mechanics)

### Auxiliary View Mini-Map
**Always visible in system space contexts** (essential for navigation)

**Context-Specific Displays:**
- **Hyperspace**: Ship status diagram (fuel, system health), cycles with mini hyperspace map every ~10 seconds
- **Outer System**: Outer planets/orbits + inner system zone (center)
- **Inner System**: Inner planets/orbits + primary star (center)
- **Gas Giant**: Gas giant (center) + moons/orbits

**Common Elements:**
- Ship position indicator on mini-map
- Highlighted planets/moons show names on hover/proximity

**Override displays** (via crew actions):
- Science Officer → Sensors: Scanning animation, then scan results
- Science Officer → Analysis: Extended scan details in Message Log
- Engineer → Damage/Repair: Ship systems diagram
- Doctor → Examine: Crew health status

## Data Management

### Galaxy Data
- **Scope**: Single sector (250 width × 220 height in tiles)
  - Tile-based coordinates: 250×220 tiles
  - Each tile is 8×8 units for rendering/positioning
  - Total space: 2000×1760 units
- **Star count**: ~180 star systems
- **Body count**: ~1000-2000 celestial bodies total
- **Generation**: Pre-generated at development time (MVP)
- **Storage**: Single galaxy JSON file
- **Loading**: Lazy-loaded per system when player enters
- **Content**: Majority procedurally generated "filler" locations (dead worlds, empty moons)

### Future Expansion
- **Hybrid approach**: Hand-crafted story/lore sectors + procedurally generated sandbox sectors
- **Multi-sector travel**: Ability to travel between sectors

### Star System Data Loading
When player enters a star system:
1. Look up system data from galaxy JSON using `current_system` coordinates
2. Cache system data for duration of visit
3. Access planet/moon data via orbital indices

Example data structure:
```python
{
    "system_coords": {"x": 100, "y": 200},
    "star_type": "G2V",
    "inner_planets": [
        {"index": 0, "type": "rocky", "coordinates": {"x": 10, "y": 5}},
        {"index": 1, "type": "rocky", "coordinates": {"x": 20, "y": 10}}
    ],
    "outer_planets": [
        {"index": 2, "type": "gas_giant", "coordinates": {"x": 50, "y": 30}, "moons": [
            {"index": 0, "coordinates": {"x": 5, "y": 2}},
            {"index": 1, "coordinates": {"x": 8, "y": 6}}
        ]},
        {"index": 3, "type": "ice_giant", "coordinates": {"x": 80, "y": 60}}
    ]
}
```

## Collision Detection

### Proximity Detection
- Approaching planets triggers proximity indicator
- Option to enter orbit (transitions to OrbitState)
- Approaching Starport allows docking (transitions to StarportState)

### Collision Behavior by Context

**Hyperspace:**
- Star collision → Enter outer system of that star

**Outer System:**
- Gas giant → Enter gas giant sub-system
- Regular planet → Enter orbit
- Inner system zone → Enter inner system
- Outer edge → Return to hyperspace

**Inner System:**
- Gas giant → Enter gas giant sub-system
- Regular planet → Enter orbit
- Outer edge → Return to outer system

**Gas Giant Sub-System:**
- Moon → Enter orbit
- Gas giant → Enter orbit
- Outer edge → Return to parent context (outer or inner system)

## Implementation Considerations

### Rendering
- **Viewport calculation**: Main View shows portion of mini-map based on player position
- **Object culling**: Only render objects within viewport range
- **Starfield parallax**: Single layer scrolling (MVP), potential for multi-layer depth later

### Performance
- **Data caching**: Cache current system data, release when leaving system
- **Coordinate calculations**: Simple tile-based math, no complex physics
- **Context switching**: Minimal overhead (push/pop stack operations)

### Edge Cases
- **Nested gas giants**: Gas giants in inner system follow same rules as outer system
- **Empty systems**: Systems with no planets still have outer/inner contexts
- **Starport positioning**: Starport treated as special object in outer system of home system

## Future Enhancements (Post-MVP)

### Potential Features
- **Orbital mechanics**: Planets move along orbits over time
- **Multi-layer parallax**: Multiple starfield layers for depth
- **Velocity preservation**: Momentum/inertia across context transitions
- **Dynamic viewport sizing**: Viewport size varies by context or zoom level
- **Context mini-map zoom**: Ability to zoom in/out on mini-map
- **Auto-navigation**: Plot course to target, auto-pilot follows course

### Expansion for Multi-Sector
- **Sector boundaries**: Detection and transition mechanics
- **Sector data structure**: Hybrid pre-generated + procedural approach
- **Cross-sector navigation**: Extended stack or sector history tracking
