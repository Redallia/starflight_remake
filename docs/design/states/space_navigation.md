# Space Navigation State

## Overview
Flying through space - either in hyperspace (between star systems) or in system space (within a star system). Player can maneuver ship, encounter other vessels, and approach planets.

**Related Documentation:**
- See [Navigation Context Framework](../navigation_context_framework.md) for the high-level architectural design and navigation system philosophy
- This document provides implementation specifications for the SpaceNavigationState class

## State Information
- **State Name**: `space_navigation`
- **Implementation**: `src/states/space_navigation_state.py`
- **Uses HUD**: Yes (standard 4-area HUD)
- **Status**: 🚧 Placeholder implemented

## Context Types
This state handles multiple navigation contexts with different visual presentations and interaction models:

### Hyperspace
Flying between star systems in the galactic map.
- **Main View**: Stars visible as navigation targets
- **Collision with star**: Enters that star's outer system
- **Navigation**: Direct visual navigation toward stars

### System Space
Flying within a star system among planets and other objects. System space has three sub-types:

#### Outer System
The outer region of a star system containing gas giants and outer planets.
- **Main View**: Rolling starfield with planets visible as interactive elements when in range
- **Auxiliary View Mini-map**: Shows outer system planets/orbits + inner system zone (center)
- **Collisions**:
  - Gas giant planet → Enters gas giant sub-system context
  - Regular planet → Enters orbit
  - Inner system zone (center) → Enters inner system context
  - Outer edge → Returns to hyperspace
- **Navigation**: Mini-map for overall positioning, Main View for fine-grain planetary approach

#### Inner System
The inner region of a star system containing rocky planets near the primary star.
- **Main View**: Rolling starfield with planets visible as interactive elements when in range
- **Auxiliary View Mini-map**: Shows inner system planets/orbits + primary star (center, non-interactive)
- **Collisions**:
  - Gas giant planet → Enters gas giant sub-system context
  - Regular planet → Enters orbit
  - Outer edge → Returns to outer system context
- **Navigation**: Mini-map for overall positioning, Main View for fine-grain planetary approach
- **Note**: Primary star has no collision detection and is not orbitable

#### Gas Giant Sub-System
A localized region around a gas giant and its moons.
- **Main View**: Rolling starfield with moons visible as interactive elements when in range
- **Auxiliary View Mini-map**: Shows gas giant (center) + moons/orbits
- **Collisions**:
  - Moon → Enters orbit
  - Gas giant → Enters orbit (same as regular planet)
  - Outer edge → Returns to parent system context (outer or inner)
- **Navigation**: Mini-map for overall positioning, Main View for fine-grain moon approach

## HUD Layout

### Main View (Left, Large)
**Hyperspace:**
- Starfield background
- Player ship icon (centered)
- Visible star systems (as navigation targets)
- Nebulae
- Flux points (if discovered)

**System Space (all sub-types):**
- Starfield background
- Player ship icon (centered)
- Viewport showing region around player ship
  - Planets/moons visible when within viewport range
  - Objects slide into view as player moves toward their coordinates
  - Viewport corresponds to a portion of the Auxiliary View mini-map
- Starport (if in home system and within viewport)
- **MVP Note**: Planets/moons are stationary at fixed coordinates (no orbital mechanics)

### Auxiliary View (Upper-Right)
**Hyperspace:**
- Ship status diagram (fuel, system health)
- Cycles with mini hyperspace map snapshot every ~10 seconds

**System Space (all sub-types):**
- Context mini-map (always visible - essential for navigation)
  - Outer System: Shows outer planets/orbits + inner system zone (center)
  - Inner System: Shows inner planets/orbits + primary star (center)
  - Gas Giant: Shows gas giant (center) + moons/orbits
- Ship position indicator on mini-map
- Highlighted planets/moons show names on hover/proximity

**Override displays (via crew actions):**
- Science Officer → Sensors: Scanning animation, then scan results
- Science Officer → Analysis: Extended scan details in Message Log
- Engineer → Damage/Repair: Ship systems diagram
- Doctor → Examine: Crew health status

### Control Panel (Right, Middle)
Crew bridge with role-based hierarchical menu:
- Captain → (Ship-level actions, cargo management)
- Science Officer → Sensors, Analysis
- Navigator → Maneuver, Starmap (hyperspace only)
- Communications → Hail, Respond, Posture
- Engineer → Damage, Repair
- Doctor → Examine, Treat

### Message Log (Bottom, Full-Width)
Scrolling text log:
- Navigation updates ("Approaching Aqua")
- System messages ("Fuel low")
- Scan results
- Communication text
- Event notifications

## Movement & Navigation

### Navigator → Maneuver
- WASD or arrow keys control ship direction
- Ship remains centered in Main View
- Starfield scrolls in direction of movement to create sense of motion (all contexts)
- Objects (planets/moons/stars) move relative to centered ship
- Fuel consumed per distance unit traveled (hyperspace only for MVP)
- Spacebar disengages maneuver mode
- Control Panel locked on Navigator/Maneuver while active

### Proximity Detection
- Approaching planets triggers proximity indicator
- Option to enter orbit (transitions to OrbitState)
- Approaching Starport allows docking (transitions to StarportState)

### Context Transitions
When transitioning between navigation contexts:
- **Direction of approach is respected**: Ship orientation/heading determines which edge you enter from
- **On entering a context**: Ship appears at the edge of the new context corresponding to approach direction
- **On exiting a context**: Ship appears at the edge of the object being exited, positioned by exit direction
- **Flux jumps**: Special case, to be designed separately

### Fuel Consumption by Context
- `"hyperspace"`: Engine class `power_consumption_rate` per coordinate traveled (Class 1 = 0.48 fuel/coordinate)
- `"system_space"` (all sub-types): No fuel consumption for MVP

## Encounters
Encounters occur when another ship comes within interaction range:
- Not a separate state - handled as context modifier within SpaceNavigationState
- Main View renders encounter mode (player ship + alien ships)
- All crew functions remain accessible
- Can hail/respond (transitions to CommunicationsState)
- Can flee, fight, or negotiate

## Input Handling

### While Maneuvering (Navigator → Maneuver active)
- **WASD/Arrows**: Control ship movement
- **Spacebar**: Disengage maneuver mode

### In Menus (maneuver not active)
- **W/S**: Navigate menu options
- **Space/Enter**: Select option
- **Backspace/ESC**: Back out of sub-menus

### Global
- **ESC** (when not in sub-menu): Return to Starport (temporary for testing)

## State Transitions
- **To Starport**: When docking at Starport or pressing ESC (temp)
- **To Orbit**: When approaching planet and selecting orbit option
- **To Communications**: When hailing another ship or being hailed
- **From Starport**: When "Launch" is selected
- **From Orbit**: When leaving planetary orbit

## Data Requirements
- Current star system data (planets, coordinates, other ships)
- Ship status (fuel, position, velocity)
- Scan data (what has been scanned)
- Encounter data (if ships present)

## Game State Requirements

### Navigation Context Stack
Navigation contexts are tracked using a FILO (stack) structure stored at the **top level of game_state**. This ensures the navigation context persists across state transitions (e.g., entering orbit, landing on planets, docking at starport).

**Key Design Decisions:**
- Hyperspace is the default base state and is NOT tracked in the stack (stack is empty when in hyperspace)
- Star systems are identified by galactic coordinates `{"x": int, "y": int}`, not names
- Celestial bodies (planets, moons, gas giants) are identified by orbital index (0-based, numbered from innermost to outermost orbit)
- Stack only contains system-level navigation contexts

```python
# Top-level game_state structure
{
    "current_system": {"x": 100, "y": 200},  # galactic coords of current star system, null when in hyperspace
    "navigation_stack": [
        "outer_system",
        "planet_4_subsystem"  # gas giant at orbital position 4
    ],
    "location": {
        "coordinates": {"x": 25, "y": 30},  # position within current navigation context
        "target_body": 2  # orbital index when in orbit/on surface (e.g., moon 2 of gas giant)
    },
    "current_state": "space_navigation",  # or "orbit", "surface", "starport", etc.
    "ship": {
        "fuel": 450,
        "max_fuel": 1000
    }
}
```

**Stack Examples:**

Player in hyperspace:
```python
"current_system": null,
"navigation_stack": []
```

Player in outer system (star at galactic coords 100, 200):
```python
"current_system": {"x": 100, "y": 200},
"navigation_stack": ["outer_system"]
```

Player in gas giant sub-system (planet at orbital position 4):
```python
"current_system": {"x": 100, "y": 200},
"navigation_stack": ["outer_system", "planet_4_subsystem"]
```

Player in inner system (navigated from outer system):
```python
"current_system": {"x": 100, "y": 200},
"navigation_stack": ["outer_system", "inner_system"]
```

**State Transition Example (Entering/Leaving Orbit):**

Player navigates to moon 2 of gas giant at position 4:
- `current_system`: `{"x": 100, "y": 200}`
- `navigation_stack`: `["outer_system", "planet_4_subsystem"]`
- `current_state`: `"space_navigation"`
- Collision with moon → transition to orbit

Player enters orbit around the moon:
- `current_system`: `{"x": 100, "y": 200}` (preserved)
- `navigation_stack`: `["outer_system", "planet_4_subsystem"]` (preserved)
- `location.target_body`: `2` (moon index)
- `current_state`: `"orbit"`

Player launches from the moon:
- `current_system`: `{"x": 100, "y": 200}` (preserved)
- `navigation_stack`: `["outer_system", "planet_4_subsystem"]` (preserved)
- `current_state`: `"space_navigation"`
- Ship appears near moon 2's coordinates in planet_4_subsystem context

**Context Transitions:**
- Entering hyperspace from system: Clear `current_system` (set to null) and empty `navigation_stack`
- Entering system from hyperspace: Set `current_system` to star's galactic coords, push "outer_system" onto stack
- Entering a new context within system: Push new context identifier onto stack
- Exiting a context: Pop current context off stack, return to previous context
- Ship appears at appropriate edge based on exit direction (coordinates not preserved in stack)

## Implementation Phases

### Phase 1 (Current - Placeholder)
- Black screen with text
- ESC returns to Starport
- Displays ship name from game state

### Phase 2 (Basic Rendering)
- Starfield background
- Ship icon rendered at center
- Simple planet icons at positions from star_systems.json
- WASD movement (no fuel consumption yet)

### Phase 3 (HUD & Navigation)
- Full 4-area HUD implemented
- Crew bridge menu functional
- Navigator → Maneuver working with fuel consumption
- Proximity detection for planets

### Phase 4 (Interaction)
- Entering orbit transitions to OrbitState
- Science Officer scanning functional
- Auxiliary View overrides working

### Phase 5 (Encounters)
- Other ships rendered
- Encounter detection
- Hailing/Communications transitions

## Notes
- This is where players spend most of their time
- Needs to feel smooth and responsive
- Fuel management creates tension and planning
- Starfield should give sense of movement when ship moves
- Consider: Minimap always visible vs toggle-able?
- Consider: Auto-slow when approaching planet vs manual only?
