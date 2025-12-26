# Surface State

## Overview
Terrain vehicle exploration on a planet's surface. Player navigates a top-down grid, collects resources, discovers ruins, encounters creatures, and manages vehicle fuel/cargo.

**Related Documentation:**
- See [Navigation Context Framework](../navigation_context_framework.md) for navigation stack architecture
- See [Orbit State](orbit.md) for the state that transitions to/from surface
- This document provides implementation specifications for the SurfaceState class

## State Information
- **State Name**: `surface`
- **Implementation**: (Not yet created)
- **Uses HUD**: Yes (modified HUD layout - different from space HUD)
- **Status**: ❌ Not implemented

## HUD Layout
Different from space navigation - shallower menu structure, action-focused.

### Main View (Left, Large)
Top-down terrain view:
- Terrain vehicle (player-controlled icon)
- Terrain types (water, land, mountains, ice, lava, desert, etc.)
- Resource icons (minerals, flora/fauna, structures)
- Landed ship icon (where you landed)
- Ruins, alien buildings (if present)
- Creatures (fauna - may be hostile)

**Icon types:**
- Minerals (color-coded by type or value)
- Flora samples
- Fauna (creatures)
- Ruins
- Alien structures/settlements
- Player's landed ship
- Terrain vehicle (player)

### Auxiliary View (Upper-Right)
**Default**: Vehicle statistics
- Cargo capacity (used/total)
- Fuel/energy remaining
- Distance and direction to landed ship
- Current coordinates

**Toggle (Map action)**: Map view
- Local mini-map (nearby terrain) OR
- Regional map (wider area, structures visible from afar)
- Can overlay stats on map or toggle between them

### Control Panel (Right, Middle)
Shallow action-focused menu (NOT crew roles):

- **Move** → Engages movement mode, locks menu (no sub-menu)
- **Scan** →
  - Target (move cursor to select scan target)
  - Analysis (detailed readout, results in Message Log or modal)
  - Icons (reference modal showing what each icon represents)
- **Cargo** → Opens cargo modal (view inventory, pick up, jettison, examine)
- **Weapon** →
  - Mode (toggle Stun/Attack)
  - Target (move cursor to select, execute attack)
- **Medicine** →
  - Review (crew health status modal)
  - Treat (select crew member to heal; field treatment caps at 50-60% max health)
- **Map** → Toggles Auxiliary View between stats and map (no sub-menu)

### Message Log (Bottom, Full-Width)
- Event notifications ("Mineral deposit discovered")
- Scan results and descriptions
- Hazard warnings ("Radiation detected")
- Crew injury reports ("Navigator injured by hostile creature")
- Action results

## Movement System

### Move Mode
When "Move" is selected:
- Movement keys (WASD/arrows) control terrain vehicle
- Menu locked on "Move" option (highlighted)
- Spacebar disengages movement, unlocks menu
- Vehicle moves one grid square per key press (or continuous movement with held key)
- Fuel consumed per movement

### Terrain Types
Different terrain affects movement costs or passability:
- Water: May be impassable (unless vehicle has swim capability)
- Mountains: Higher fuel cost, slower movement
- Ice: Potentially slippery? Lower traction?
- Lava: Extreme hazard, requires special shielding
- Desert, Land: Normal movement

## Resource Collection

### Minerals
- Approach mineral icon
- Cargo → Pick up (transfers to vehicle cargo)
- Different minerals have different values (from minerals.json)
- Cargo capacity limits how much you can carry

### Flora/Fauna
- Flora: Approach and pick up (biological samples)
- Fauna: Must be subdued (stunned) before pickup
  - Weapon → Mode (Stun) → Target → Fire
  - Stunned creatures become pickable items
  - Hostile creatures may attack if approached

### Cargo Modal
Two-column design (see [hud_specification.md](../../technical/hud_specification.md)):
- Left: Scrollable item list (Nearby, Minerals, Lifeforms, Artifacts, Messages)
- Right: Description and available actions ([P]ick up, [J]ettison, [A]rchive)

## Combat & Creatures

### Hostile Fauna
- Some creatures are hostile and will attack if approached
- Weapon → Mode (Stun or Attack)
- Weapon → Target (cursor to select creature)
- Navigator skill affects weapon accuracy
  - Low skill: Shots miss or hit wrong target
  - High skill: Accurate targeting

### Crew Injuries
- Creature attacks or environmental hazards can injure crew
- Injuries reported in Message Log
- Medicine → Review shows crew health status
- Medicine → Treat allows field healing (limited to ~50-60% max HP)
- Full healing requires Doctor at Starport

## Scanning

### Scan → Target
- Move cursor to select object/terrain/creature
- Scan provides information
- Science Officer skill affects scan detail

### Scan → Analysis
- Extended analysis of selected target
- Detailed readout in Message Log

### Scan → Icons
- Reference modal showing what each icon type represents
- Helpful for new players

## Returning to Ship

### Proximity to Landed Ship
When terrain vehicle moves adjacent to landed ship icon:
- Contextual prompt: "Enter Ship? Y/N"
- Y: Transitions back to OrbitState
  - Cargo transferred to ship
  - Crew returns to ship
  - Vehicle fuel consumption recorded

## Structures & Ruins

### Ruins
- Approach ruins icon
- Contextual prompt: "Enter? Y/N" (future feature)
- May contain artifacts, messages, ancient technology
- May require crew skills to access (Engineer, Communications)

### Alien Settlements/Trade Outposts
- Approach settlement icon
- Prompt: "Do you wish to trade? Y/N"
- Opens Trade Outpost modal (see [hud_specification.md](../../technical/hud_specification.md))
- Not in MVP - no planetary settlements initially

## Input Handling

### Move Mode Active
- **WASD/Arrows**: Control terrain vehicle
- **Spacebar**: Disengage move mode
- Menu locked

### Menu Navigation
- **W/S**: Navigate menu options
- **Space/Enter**: Select option
- **Escape/Backspace**: Back out of sub-menus

### Target Mode (Weapon/Scan)
- **Cursor keys**: Move targeting cursor
- **Space/Enter**: Confirm target
- **Escape**: Cancel targeting

### Modals (Cargo, Health, etc.)
- **W/S**: Navigate items
- **Hotkeys**: [P]ick up, [J]ettison, [A]rchive, etc.
- **Escape**: Close modal

## State Transitions
- **To Orbit**: When entering landed ship
- **From Orbit**: When descending to surface via Captain → Land → Descend

## Data Requirements
- Planet terrain data (procedurally generated from seed or heightmap)
- Resource placement (minerals, flora/fauna distribution)
- Ruins/settlement locations (if present)
- Terrain vehicle stats (fuel capacity, cargo capacity)
- Crew health status

## Game State Requirements
The surface state preserves the navigation stack from space navigation:

```python
{
    "current_system": {"x": 100, "y": 200},  # galactic coords, preserved
    "navigation_stack": [
        "outer_system",
        "planet_4_subsystem"  # if on a moon in a gas giant system
    ],  # preserved from space navigation
    "location": {
        "coordinates": {"x": 45, "y": -23},  # landing site on planet surface
        "target_body": 2  # orbital index of body player is on
    },
    "current_state": "surface",
    "vehicle": {
        "fuel": 80,
        "max_fuel": 100,
        "position": {"x": 50, "y": -20},  # vehicle position on surface
        "cargo": [
            {"type": "mineral", "name": "iron", "quantity": 5},
            {"type": "flora", "name": "spore_sample", "quantity": 2}
        ],
        "cargo_capacity": 20
    },
    "crew_health": {
        "navigator": {"current": 85, "max": 100},
        "science_officer": {"current": 100, "max": 100},
        # ... etc
    }
}
```

**Key Points:**
- Navigation stack is preserved (not modified by landing on surface)
- `current_system` is preserved
- `target_body` uses orbital index to identify which body you're on
- `location.coordinates` is the landing site
- `vehicle.position` tracks vehicle movement across surface

## Crew Skills on Surface

Skills don't appear in menu but affect outcomes:
- **Science Officer**: Scan detail and analysis quality
- **Navigator**: Weapon accuracy
- **Doctor**: Healing effectiveness
- **Engineer**: Vehicle repair (if damage system implemented)
- **Communications**: (Future) Interaction with alien structures

## Implementation Phases

### Phase 1 (Basic Movement)
- Simple grid-based terrain
- Terrain vehicle icon
- WASD movement
- Return to ship prompt
- Transition back to orbit

### Phase 2 (Resources)
- Mineral/flora icons on terrain
- Cargo modal
- Pick up/jettison functionality
- Cargo capacity limits

### Phase 3 (Scanning & Info)
- Scan system functional
- Auxiliary View vehicle stats
- Map toggle
- Message Log integration

### Phase 4 (Combat & Hazards)
- Fauna (creatures) on terrain
- Weapon system (stun/attack)
- Crew injury mechanics
- Medicine system

### Phase 5 (Structures)
- Ruins placeholders
- (Future) Trade outposts
- (Future) Explorable structures

## Notes
- Different gameplay feel from space - more tactical, resource-focused
- Grid size should be large enough to feel like exploration (50x50? 100x100?)
- Procedural generation crucial for variety
- Fuel management creates risk: Go farther or play it safe?
- Crew injuries add tension and consequences
- Consider: Fog of war (unexplored areas hidden)?
- Consider: Time-based hazards (radiation building up over time)?
- Consider: Different vehicle types in future (wheeled, hover, amphibious)?
