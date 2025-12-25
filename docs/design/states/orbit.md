# Orbit State

## Overview
Orbiting a planet. Player can scan the planet, select a landing site, and descend to the surface or leave orbit back to space.

## State Information
- **State Name**: `orbit`
- **Implementation**: (Not yet created)
- **Uses HUD**: Yes (standard 4-area HUD)
- **Status**: ❌ Not implemented

## HUD Layout

### Main View (Left, Large)
- Rotating planet visualization
- Planet slowly rotates to give sense of orbit
- Visual style based on planet type (ocean, rocky, gas giant, etc.)
- Possibly shows atmosphere glow if present

### Auxiliary View (Upper-Right)
- **Default**: Terrain heightmap of planet surface
  - Static elevation map
  - Helps player choose landing sites
  - Shows general terrain features

- **Override (Science Officer → Sensors)**: Scanning animation, then scan results
- **Override (Navigator landing site selection)**: Highlighted landing site with "blow up lines" connecting to terrain map

### Control Panel (Right, Middle)
Crew bridge menu (same as space navigation):
- Captain → Land (transitions to LandingMode sub-state)
- Science Officer → Sensors, Analysis (scan planet for resources, life, hazards)
- Navigator → Leave Orbit (return to SpaceNavigationState)
- Engineer → (standard ship functions)
- Doctor → (standard crew functions)

**In LandingMode sub-state:**
- Site Select: Choose landing coordinates
- Descend: Land at selected site (transitions to SurfaceState)
- Abort: Return to orbit

### Message Log (Bottom, Full-Width)
- Orbit entry message ("Entering orbit around Aqua")
- Scan results (detailed planetary analysis)
- Landing warnings (gas giant warning, hazard alerts)
- System messages

## Sub-States

### Normal Orbit
Player can scan, examine, decide whether to land.

### Landing Mode
Activated when Captain → Land is selected.
- Control Panel shows landing interface (Site Select, Descend, Abort)
- Auxiliary View may show landing site selection overlay
- Player chooses coordinates for landing
- Descend transitions to SurfaceState

### Gas Giant Warning
Special sub-state when orbiting a gas giant.
- Modal prompt: "This is a gas giant. Landing is extremely dangerous. Proceed? Y/N"
- Proceed → Landing Mode
- Abort → Stay in orbit
- (Special equipment allows gas giant "landing" in future)

## Scanning System

### Science Officer → Sensors
Initiates scan of the orbited planet.

**Scan quality affected by:**
- Science Officer's skill level
- Ship's sensor equipment class
- Planet's atmospheric interference

**Scan results show:**
- Planet type and composition
- Atmosphere type and density
- Temperature, gravity
- Mineral presence and richness
- Life form presence (flora/fauna percentages)
- Ruins or settlements (if present)
- Hazards (weather, radiation, etc.)

**Results appear in:**
- Auxiliary View (summary)
- Message Log (detailed breakdown)

### Science Officer → Analysis
Extended analysis of scan data, more detailed breakdown.

## Landing Site Selection

### Site Select (Navigator or Captain action)
- Player chooses coordinates for landing
- Terrain map highlights selected location
- May show terrain difficulty or hazard warnings
- Coordinates stored for landing

### Descend
- Validates selected site (some locations may be invalid - water on ocean world if vehicle can't swim)
- Transitions to SurfaceState at chosen coordinates
- Fuel consumed for descent (TBD amount)

## Input Handling
- **W/S**: Navigate menu
- **Space/Enter**: Select option
- **Backspace/ESC**: Back out of sub-menus or leave orbit

## State Transitions
- **To Space Navigation**: Via Navigator → Leave Orbit
- **To Surface**: Via Captain → Land → Descend
- **From Space Navigation**: When approaching planet and selecting orbit

## Data Requirements
- Planet data (from star_systems.json or procedural generation)
  - Type, atmosphere, temperature, gravity
  - Terrain heightmap or generation seed
  - Resources, life, ruins placement
- Scan data (what has been discovered about this planet)
- Landing site coordinates (when selected)

## Game State Requirements
```python
{
    "location": {
        "type": "orbit",
        "system": "sol",
        "planet": "aqua"
    },
    "scan_data": {
        "aqua": {
            "scanned": True,
            "type": "ocean",
            "minerals": ["iron", "nickel"],
            "life": {"flora": 60, "fauna": 30},
            # ... more scan results
        }
    },
    "landing_site": {"x": 45, "y": -23}  # when in landing mode
}
```

## Protected Planets
Some planets may be protected by alien factions:
- Attempting to enter orbit triggers encounter with defenders
- Player must negotiate, fight, or flee
- Only after resolution can orbit be entered
- See [hud_specification.md](../../technical/hud_specification.md) for encounter flow

## Special Planet Types

### Gas Giants
- Can orbit normally
- Landing requires special equipment (not in MVP)
- Warning modal shown if landing attempted
- May have special "landable" coordinates (platforms, derelicts)

### Moons
- Planets with moons can be entered as sub-systems (like gas giants)
- Not in MVP - treat as separate planets for now

## Implementation Phases

### Phase 1 (Basic Orbit)
- Simple rotating planet sprite/circle
- Crew bridge menu functional
- Leave Orbit returns to space
- No scanning yet

### Phase 2 (Scanning)
- Science Officer → Sensors functional
- Basic scan results in Message Log
- Terrain heightmap in Auxiliary View

### Phase 3 (Landing)
- Landing Mode sub-state
- Site selection (simple coordinate input)
- Descend transitions to SurfaceState

### Phase 4 (Polish)
- Gas giant warning modal
- Protected planet detection
- Enhanced scan visuals
- Landing site preview/validation

## Notes
- Safe state - no threats while in orbit
- Scanning is crucial for deciding where to land
- Terrain map helps strategic landing site selection
- Should feel like a preparation/planning phase before surface exploration
- Consider: Show other ships in orbit? (Future)
- Consider: Orbital scan vs. surface scan differences?
