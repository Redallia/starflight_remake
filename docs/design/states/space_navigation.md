# Space Navigation State

## Overview
Flying through space - either in hyperspace (between star systems) or in system space (within a star system). Player can maneuver ship, encounter other vessels, and approach planets.

## State Information
- **State Name**: `space_navigation`
- **Implementation**: `src/states/space_navigation_state.py`
- **Uses HUD**: Yes (standard 4-area HUD)
- **Status**: 🚧 Placeholder implemented

## Context Types
This state handles two different contexts:

### Hyperspace
Flying between star systems in the galactic map.

### System Space
Flying within a star system among planets and other objects.

## HUD Layout

### Main View (Left, Large)
**Hyperspace:**
- Starfield background
- Player ship icon
- Visible star systems (as navigation targets)
- Nebulae, flux points (if discovered)

**System Space:**
- Starfield background
- Player ship icon
- Planets and moons at their orbital positions
- Other ships (if present)
- Starport (if in home system)

### Auxiliary View (Upper-Right)
**Hyperspace:**
- Ship status diagram (fuel, system health)
- Cycles with mini hyperspace map snapshot every ~10 seconds

**System Space:**
- System mini-map showing planets, orbits, ship position
- Highlighted planets show names on hover/proximity

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
- Fuel consumed per distance unit traveled
- Spacebar disengages maneuver mode
- Control Panel locked on Navigator/Maneuver while active

### Proximity Detection
- Approaching planets triggers proximity indicator
- Option to enter orbit (transitions to OrbitState)
- Approaching Starport allows docking (transitions to StarportState)

### Hyperspace vs System Space
Differentiation based on `game_state.location.type`:
- `"hyperspace"`: Show stars as navigation targets, allow starmap access
- `"system_space"`: Show planets, disable starmap, enable orbit

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
```python
{
    "location": {
        "type": "hyperspace" | "system_space",
        "system": "sol",  # current star system
        "coordinates": {"x": 25, "y": 30}
    },
    "ship": {
        "fuel": 450,
        "max_fuel": 1000,
        "position": {"x": 25, "y": 30},
        "velocity": {"dx": 0, "dy": 0}  # if implementing momentum
    }
}
```

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
