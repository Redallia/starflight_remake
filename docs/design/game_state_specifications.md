# Game State Specification

## Overview

This document defines the game state architecture - what states exist, how they relate to each other, and how transitions between them work.

The core insight: game state isn't just "what mode are we in" - it's a **nested coordinate context** that tracks where the player is at every level of the spatial hierarchy simultaneously. When you're on a planet's surface, the game still knows which system you're in, which planet you orbited, where you landed. Backing out restores each layer.

## State Architecture

### Top Level: Game Mode

```
MAIN_MENU    - Title screen, load/save, options
PLAYING      - Active gameplay  
GAME_OVER    - Player died or game ended (future)
```

Most of this document concerns what happens within `PLAYING`.

### The Context Stack

When playing, the game maintains a **FILO (First In, Last Out) stack** of coordinate contexts. This allows arbitrary nesting of spatial layers.

```
context_stack: [
    { type: HYPERSPACE, ... },      // Always the base
    { type: LOCAL_SPACE, ... },     // Star system
    { type: LOCAL_SPACE, ... },     // Inner system (optional)
    { type: LOCAL_SPACE, ... },     // Gas giant moon system (optional)
    { type: ORBIT, ... },           // Orbiting a body
]
```

**Push** a new context when entering a deeper layer.
**Pop** a context when backing out to the previous layer.

The **top of the stack** represents the current spatial context. The full stack represents the complete path from hyperspace to current location.

### Context Types

#### HYPERSPACE

The base layer. Always at the bottom of the stack. Interstellar space.

```
{
    type: HYPERSPACE,
    coords: (x, y),              // Position in sector
    velocity: (vx, vy),          // Current movement vector
}
```

**Contains:** Star systems, flux jumps, alien ships, anomalies

**Movement:** Free movement in 2D plane. Large scale (sector-sized).

**Transitions out:**
- Enter a star system → Push LOCAL_SPACE

#### LOCAL_SPACE

A region of space centered on a gravitational body. Stackable - can nest arbitrarily.

```
{
    type: LOCAL_SPACE,
    body: "Jupiter",             // What this space is centered on
    body_type: GAS_GIANT,        // Star, planet, moon, asteroid, station
    parent_coords: (x, y),       // Where we entered from parent context
    coords: (x, y),              // Current position in this local space
    velocity: (vx, vy),          // Current movement vector
}
```

**Contains:** Orbital bodies (planets, moons, stations), ships, anomalies, rings, asteroids, comets

**Movement:** Free movement in 2D plane. Smaller scale than hyperspace.

**Transitions out:**
- Enter a sub-body's local space → Push LOCAL_SPACE
- Enter orbit around a body → Push ORBIT
- Exit to parent context → Pop (restore parent_coords as position)

**Examples of LOCAL_SPACE nesting:**
- Sol System (star) → Inner System (region) → Earth (planet) → Moon (satellite)
- Sol System (star) → Outer System (region) → Jupiter (gas giant) → Europa (moon) → Station (orbital)

#### ORBIT

Locked in orbit around a specific body. No free movement - you're circling.

```
{
    type: ORBIT,
    body: "Europa",              // What we're orbiting
    body_type: MOON,             // Planet, moon, asteroid, station
    orbital_position: 0.0,       // Angle in orbit (0-360 or radians)
    parent_coords: (x, y),       // Where we were when we entered orbit
}
```

**Contains:** Just the player and the body being orbited (and maybe orbital stations/debris)

**Movement:** None (or slow orbital drift for visuals). Player is "parked."

**Transitions out:**
- Land on surface → Push SURFACE (if landable)
- Dock with station → Push DOCKED (if dockable)
- Leave orbit → Pop (restore parent_coords as position in LOCAL_SPACE)

#### SURFACE

On the surface of a landable body. Different game mode - terrain vehicle exploration.

```
{
    type: SURFACE,
    body: "Europa",              // What we're on
    planetary_coords: (x, y),    // Where on the planet (landing site)
    vehicle_coords: (x, y),      // Vehicle position relative to landing site
    ship_coords: (x, y),         // Where the ship is (usually same as planetary_coords)
}
```

**Contains:** Terrain, minerals, flora, fauna, ruins, structures, player vehicle, landed ship

**Movement:** Terrain vehicle movement on 2D surface grid.

**Transitions out:**
- Enter ship and launch → Pop (return to ORBIT)
- Enter structure → Push DOCKED (future - side-scroller mode)

#### DOCKED

Inside a structure - station, derelict, ruin, landed ship interior. Future expansion for side-scroller mode.

```
{
    type: DOCKED,
    structure: "Research Station Gamma",
    structure_type: STATION,     // Station, derelict, ruin, ship
    interior_position: (x, y),   // Position within the structure
}
```

**Contains:** Interior spaces, NPCs, interactable objects

**Movement:** Side-scroller movement (future) or menu navigation (MVP)

**Transitions out:**
- Exit structure → Pop (return to previous context - ORBIT or SURFACE)

### Current Location

Derived from the context stack, `current_location` is a simple enum for game systems that just need to know "what mode are we in" without caring about the full path:

```
current_location: HYPERSPACE | LOCAL_SPACE | ORBIT | SURFACE | DOCKED | STARPORT
```

Note: STARPORT is a special case - it's DOCKED at a specific structure (the starport), but has enough unique behavior that it warrants its own location value.

### State Modifiers

These layer on top of location state:

#### Sub-state

What's happening within the current location:

```
sub_state: NONE | MANEUVERING | LANDING_MODE | SCANNING | ...
```

| Sub-state | Valid Locations | Effect |
|-----------|-----------------|--------|
| NONE | Any | Default, menu navigation active |
| MANEUVERING | HYPERSPACE, LOCAL_SPACE, SURFACE | Movement controls active, menus locked |
| LANDING_MODE | ORBIT | Selecting landing site |
| SCANNING | HYPERSPACE, LOCAL_SPACE, ORBIT | Scan in progress |

#### Active Encounter

When in proximity to other ships (hostile or otherwise):

```
active_encounter: null | {
    ships: [...],           // Ships involved
    disposition: HOSTILE | NEUTRAL | FRIENDLY,
    initiated_by: PLAYER | OTHER,
}
```

Encounters can occur in HYPERSPACE or LOCAL_SPACE. They modify what's rendered and what events can fire, but don't change location.

#### Active Modal

When a modal interface is open:

```
active_modal: null | CARGO | STARMAP | COMMUNICATIONS | TRADE | MESSAGES | ...
```

Modals capture input until dismissed. They layer over the HUD without changing location.

## State Transitions

### Transition Table

| From | Action | To | Stack Operation |
|------|--------|----|-----------------|
| MAIN_MENU | New Game | STARPORT | Initialize stack with starting location |
| MAIN_MENU | Load Game | (varies) | Restore saved stack |
| STARPORT | Launch | LOCAL_SPACE | Push system context |
| HYPERSPACE | Enter system | LOCAL_SPACE | Push system context |
| LOCAL_SPACE | Enter sub-region | LOCAL_SPACE | Push region context |
| LOCAL_SPACE | Enter orbit | ORBIT | Push orbit context |
| LOCAL_SPACE | Exit to parent | (parent type) | Pop current context |
| LOCAL_SPACE | Exit to hyperspace | HYPERSPACE | Pop all LOCAL_SPACE contexts |
| ORBIT | Land | SURFACE | Push surface context |
| ORBIT | Dock | DOCKED | Push docked context |
| ORBIT | Leave orbit | LOCAL_SPACE | Pop orbit context |
| SURFACE | Launch | ORBIT | Pop surface context |
| SURFACE | Enter structure | DOCKED | Push docked context |
| DOCKED | Exit | (parent type) | Pop docked context |

### Transition Validation

Not all transitions are valid:

- Can't land on gas giants (warning prompt, but allowed if player insists - consequences follow)
- Can't enter orbit from hyperspace (must be in LOCAL_SPACE)
- Can't enter orbit around hostile aliens (must resolve encounter first)
- Can't land without selecting a landing site
- Can't dock with hostile stations (must resolve encounter first)

### Encounter Transitions

Encounters don't change location but do affect available actions:

| Trigger | Effect |
|---------|--------|
| Ship enters proximity | `active_encounter` set, Main View updates |
| Player hails / alien hails | `active_modal` = COMMUNICATIONS |
| Player flees successfully | `active_encounter` cleared |
| Combat ends | `active_encounter` cleared (or changes disposition) |
| Enter orbit of protected planet | Forced encounter, orbit blocked until resolved |

## Entity Relationships

Different entities exist at different context levels:

| Entity Type | Exists In |
|-------------|-----------|
| Star systems | HYPERSPACE |
| Flux jumps | HYPERSPACE |
| Planets | LOCAL_SPACE (stellar) |
| Moons | LOCAL_SPACE (planetary) |
| Stations | LOCAL_SPACE or ORBIT |
| Ships (alien) | HYPERSPACE, LOCAL_SPACE |
| Ships (player) | All (represented differently) |
| Minerals | SURFACE |
| Flora/Fauna | SURFACE |
| Ruins | SURFACE, LOCAL_SPACE (as signal) |
| Structures | SURFACE |

### Entity Persistence

When pushing/popping contexts:

**Persists across all transitions:**
- Player ship state (hull, fuel, cargo, crew)
- Discovered information (scanned planets, known systems)
- Game time

**Persists within session but resets on reload:**
- Alien ship positions (they move around)
- Encounter states

**Generated fresh each visit:**
- Surface flora/fauna (procedural, seed-based)
- Mineral deposits (procedural, seed-based)

**Fixed:**
- Planet/moon/system positions
- Ruin locations
- Station locations

## MVP State Scope

For MVP, the following states are required:

**Game Modes:**
- MAIN_MENU
- PLAYING

**Context Types:**
- HYPERSPACE
- LOCAL_SPACE (at least 2 levels: system + inner/outer)
- ORBIT
- SURFACE

**Special Locations:**
- STARPORT (simplified - menu interface)

**Sub-states:**
- NONE
- MANEUVERING
- LANDING_MODE

**Modals:**
- CARGO
- STARMAP
- COMMUNICATIONS
- SHIP (at Starport)
- MESSAGES (at Starport)

**Deferred for post-MVP:**
- DOCKED (side-scroller mode)
- GAME_OVER state
- Complex encounter states
- Combat sub-state
- Trade modal (planetary)

## Implementation Notes

### Stack Operations

```python
def push_context(context):
    """Enter a deeper spatial layer."""
    # Store current coords in new context's parent_coords
    context.parent_coords = current_context().coords
    context_stack.append(context)
    update_current_location()
    emit_event('context_changed', context)

def pop_context():
    """Return to parent spatial layer."""
    if len(context_stack) <= 1:
        return  # Can't pop hyperspace
    old_context = context_stack.pop()
    # Restore position in parent context
    current_context().coords = old_context.parent_coords
    update_current_location()
    emit_event('context_changed', current_context())

def current_context():
    """Get the top of the stack."""
    return context_stack[-1]

def update_current_location():
    """Derive current_location from stack."""
    top = current_context()
    current_location = top.type
```

### State Queries

Common queries the game needs to answer:

```python
def is_in_space():
    """Are we in any space navigation mode?"""
    return current_location in [HYPERSPACE, LOCAL_SPACE, ORBIT]

def is_on_ground():
    """Are we on a planetary surface?"""
    return current_location == SURFACE

def can_save():
    """Is saving allowed right now?"""
    return current_location == STARPORT or current_location == ORBIT

def get_system():
    """What star system are we in?"""
    for context in context_stack:
        if context.type == LOCAL_SPACE and context.body_type == STAR:
            return context.body
    return None

def get_depth():
    """How many levels deep are we?"""
    return len(context_stack)
```

## Open Questions

1. **Coordinate scales:** What are the actual coordinate ranges for each context type? Hyperspace might be 0-1000, system space might be 0-500, etc.

2. **Time passage:** Does time pass differently at different context levels? Is there time compression in hyperspace travel?

3. **Persistence granularity:** Exactly what state persists when you leave and return to a location? If you leave a system and return, are alien ships in the same place?

4. **Multi-star systems:** How do binary/trinary star systems work? Multiple LOCAL_SPACE regions at the stellar level?

5. **Fast travel:** How do flux jumps work with the stack model? Pop all the way to hyperspace, then push directly to destination system?

6. **Starport location:** Is Starport in a system (pop once to LOCAL_SPACE) or a special hyperspace location (pop once to HYPERSPACE)?