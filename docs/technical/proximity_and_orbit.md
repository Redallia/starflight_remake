# Proximity Detection and Orbit Entry

## Overview
This document defines how planet proximity detection works and how players enter orbital state. Unlike most context transitions which are automatic, orbit entry requires player confirmation during a proximity pause window.

## Key Distinction

**Planet proximity is NOT automatic orbit entry.** Instead:
- Proximity detection triggers a **pause and prompt**
- Player can **choose** to enter orbit (press Space) or **fly past** (continue moving)

## Proximity Detection

### Detection Radius

Each planet has two relevant radii:
- **Visual radius** (`planet.size`): The visual size of the planet sprite
- **Proximity radius**: Larger radius that triggers proximity detection

**For MVP**: Proximity radius = visual radius + ship radius
```python
proximity_radius = planet.size + ship_radius  # ship_radius = 11 (half of 22px sprite)
```

This means proximity triggers when ship sprite would visually overlap planet sprite.

**Future enhancement**: Could increase proximity radius for easier orbit entry (less precision required).

### Detection Logic

Proximity detection uses circular collision:
```python
def check_planet_proximity(ship_x, ship_y, planet_x, planet_y, proximity_radius):
    """
    Check if ship is within proximity range of planet.

    Returns:
        Planet object if in proximity, None otherwise
    """
    distance = math.sqrt((ship_x - planet_x)**2 + (ship_y - planet_y)**2)
    return distance <= proximity_radius
```

**Implemented in**: `CollisionManager.check_planet_collision()` (see `src/core/collision_manager.py`)

**Important**: Proximity detection should only trigger once per approach. If player flies past and loops back, it can trigger again.

## Proximity Pause Behavior

### When Proximity Triggers

**Sequence**:
1. Ship enters proximity radius of planet
2. **All movement freezes**:
   - Ship sprite remains at current position (stationary in main view)
   - Background starfield stops scrolling (no parallax)
   - All directional inputs (WASD/arrows) are ignored
3. Message displays: `"Approaching [Planet Name]. Press Space to orbit."`
4. **Pause window**: ~1 second (exact duration TBD during implementation/playtesting)
5. **Two possible outcomes**:
   - **Player presses Space**: Enter orbit (transition to OrbitState)
   - **Pause expires**: Resume movement, "slingshot" past planet

### Input Handling During Pause

**Frozen inputs**:
- WASD/arrow keys: Ignored
- Other movement commands: Ignored

**Active inputs**:
- **Spacebar**: Triggers orbit entry (see Orbit Entry section below)
- **ESC**: Still allows emergency exit to main menu/starport? (TBD)

**Pause timer implementation**:
```python
class SpaceNavigationState:
    def __init__(self):
        self.proximity_planet = None      # Currently proximate planet
        self.proximity_timer = 0.0        # Time remaining in pause
        self.proximity_duration = 1.0     # Pause duration in seconds
        self.in_proximity_pause = False   # Flag for pause state

    def update(self, dt):
        if self.in_proximity_pause:
            self.proximity_timer -= dt
            if self.proximity_timer <= 0:
                # Pause expired, trigger slingshot
                self._handle_proximity_timeout()
        else:
            # Normal movement and collision detection
            pass
```

## Slingshot Behavior

### When Pause Expires Without Orbit Entry

If the player doesn't press Space during the proximity pause, they "slingshot" past the planet.

**Original Starflight approach**: Simply redraw ship on opposite side of planet.

**MVP Implementation (Keep It Simple)**:
1. Calculate opposite side of planet from ship's current position
2. Teleport ship to that position (instant, no animation)
3. Resume normal movement

```python
def calculate_slingshot_position(ship_x, ship_y, planet_x, planet_y, clearance=10):
    """
    Calculate ship position on opposite side of planet.

    Args:
        ship_x, ship_y: Current ship position (at proximity trigger)
        planet_x, planet_y: Planet center
        clearance: Distance beyond planet radius

    Returns:
        tuple: (new_ship_x, new_ship_y)
    """
    # Vector from planet to ship
    dx = ship_x - planet_x
    dy = ship_y - planet_y

    # Distance from planet center
    distance = math.sqrt(dx*dx + dy*dy)

    # Normalize vector
    if distance > 0:
        dx /= distance
        dy /= distance

    # Position on opposite side
    # Negate the vector and place at same distance + clearance
    opposite_distance = distance + clearance
    new_x = planet_x - dx * opposite_distance
    new_y = planet_y - dy * opposite_distance

    return (new_x, new_y)
```

**Example**:
```
Planet at (2500, 2500), radius 50
Ship approaching from west at (2400, 2500)
↓
Proximity triggers
↓
Pause expires (no Space pressed)
↓
Ship teleports to (2600, 2500)  # East side of planet, mirrored position
```

### Future Enhancement: Vector Preservation

**Post-MVP consideration**: Instead of simple mirroring, preserve ship's movement vector:
- Track ship's velocity/direction before pause
- After slingshot, resume movement in same direction
- Creates more realistic "flyby" feel

**For now**: Keep it simple. Just teleport to opposite side.

## Orbit Entry

### Triggering Orbit State

When player presses Space during proximity pause:

1. **Push orbit context** onto navigation stack:
   ```python
   planet_index = get_planet_index(proximity_planet)
   game_session.push_context(CONTEXT_ORBIT, planet_index=planet_index)
   ```

2. **Transition to OrbitState**:
   ```python
   self.state_manager.change_state("orbit")
   ```

3. **Pass planet data** to OrbitState (via game_session):
   - `current_system`: Already available in game_session
   - `planet_index`: Stored in CONTEXT_ORBIT context data
   - OrbitState retrieves planet from `current_system.get_planet_by_index(planet_index)`

### What Happens in OrbitState

**Not covered in this doc** - see `docs/design/states/orbit.md` for orbit mechanics.

**Key points**:
- OrbitState has its own rendering, input handling, update loop
- Player can scan planet, select landing sites, launch back to space
- Launching from orbit pops CONTEXT_ORBIT and transitions back to SpaceNavigationState

### Returning from Orbit

When player launches from orbit:

1. **OrbitState** calls `game_session.pop_context()` (removes CONTEXT_ORBIT)
2. **OrbitState** transitions back to SpaceNavigationState: `state_manager.change_state("space_navigation")`
3. **SpaceNavigationState.on_enter()** is called
4. Ship appears near planet in space navigation context

**Ship positioning on orbit exit**:
```python
# Ship should appear just outside planet's proximity radius
# at a "safe" position (e.g., north of planet)

planet_x, planet_y = planet.get_coordinates()
exit_angle = 90  # North (can randomize or base on launch trajectory)
distance = planet.size + ship_radius + clearance  # Just outside proximity

ship_x = planet_x + math.cos(math.radians(exit_angle)) * distance
ship_y = planet_y + math.sin(math.radians(exit_angle)) * distance

game_session.current_context.data["ship_coords"] = [ship_x, ship_y]
```

**Important**: Position ship outside proximity radius to prevent immediately re-triggering proximity detection.

## Collision Manager Integration

### Preventing Repeated Triggers

The `CollisionManager` tracks the last planet that triggered proximity to prevent spam:

```python
class CollisionManager:
    def check_planet_collision(self, ship_x, ship_y, planets, ship_radius=11):
        # ... collision detection logic ...

        if collision:
            if collision == self.last_planet_collision:
                return None  # Same planet, don't trigger again
            else:
                self.last_planet_collision = collision
                return collision
        else:
            self.last_planet_collision = None  # Clear when no collision
            return None
```

**Key behavior**: `last_planet_collision` clears when ship is no longer in proximity, allowing re-triggering on next approach.

### Resetting Collision State

When transitioning contexts or states, collision state must reset:

```python
# When entering/exiting orbit
collision_manager.reset()

# When pushing/popping navigation contexts
collision_manager.reset()
```

This prevents stale collision data from affecting new context.

## State Machine for Proximity

### Proximity States

The SpaceNavigationState needs to track proximity state:

```
[Normal Navigation]
    ↓ (enter proximity)
[Proximity Pause]
    ↓ (Space pressed)
  [Enter Orbit] → Transition to OrbitState
    ↓ (timeout)
  [Slingshot] → Return to Normal Navigation
```

### Implementation Approach

**Option A: Simple Flag-Based** (recommended for MVP)
```python
class SpaceNavigationState:
    def __init__(self):
        self.in_proximity_pause = False
        self.proximity_planet = None
        self.proximity_timer = 0.0

    def update(self, dt):
        if self.in_proximity_pause:
            self._update_proximity_pause(dt)
        else:
            self._update_normal_navigation(dt)
```

**Option B: Dedicated ProximityManager** (future enhancement)
- Separate class to encapsulate proximity state machine
- Cleaner separation of concerns
- More complex for MVP needs

**Decision**: Use Option A for MVP. Can refactor to Option B if complexity grows.

## Visual Feedback

### During Proximity Pause

**Main View**:
- Ship sprite frozen at current position
- Background starfield frozen (no scrolling)
- Planet visible at relative position

**Message Log**:
- Display message: `"Approaching [Planet Name]. Press Space to orbit."`
- Message should be prominent (possibly different color/highlight?)

**HUD**:
- Control panel locked (no crew actions during pause)
- Auxiliary view still visible (shows context mini-map)

**Future enhancement**: Add visual indicator (flashing border, proximity ring around planet, etc.)

## Edge Cases

### Multiple Planets in Proximity

**Scenario**: Two planets close together, ship enters proximity of both simultaneously.

**MVP behavior**: Trigger proximity for whichever planet is detected first (iteration order in planet list).

**Future enhancement**: Prioritize closest planet, or allow player to choose target.

### Proximity While in Encounter

**Scenario**: Ship is in an encounter with aliens and drifts into planet proximity.

**MVP behavior**: Proximity pause still triggers (encounter continues after pause/slingshot).

**Alternative**: Disable proximity detection during encounters? (TBD based on playtesting)

### Exiting Context During Proximity Pause

**Scenario**: Ship in proximity pause, but also at edge of context boundary.

**Should not happen**: Proximity radius is much smaller than context grid (planets are nowhere near boundaries).

**If it happens**: Context boundary takes priority (pop context, cancel proximity pause).

## Testing Checklist

- [ ] Proximity triggers at correct radius
- [ ] Movement freezes during pause (ship and background stationary)
- [ ] Message displays with correct planet name
- [ ] Spacebar during pause enters orbit successfully
- [ ] Timeout causes slingshot to opposite side
- [ ] Ship positioned correctly after slingshot (outside proximity radius)
- [ ] Repeated approach re-triggers proximity correctly
- [ ] Launching from orbit positions ship outside proximity radius
- [ ] Collision state resets when entering/exiting orbit
- [ ] No repeated triggers for same planet without leaving proximity

## Configuration Constants

**Recommended additions to `src/core/constants.py`**:

```python
# Proximity and Orbit
SHIP_RADIUS = 11  # Half of 22px ship sprite
PROXIMITY_PAUSE_DURATION = 1.0  # Seconds
ORBIT_EXIT_CLEARANCE = 10  # Distance beyond planet radius when launching
SLINGSHOT_CLEARANCE = 10  # Extra distance when slingshotting past planet
```

## Related Documentation

- **Context Transitions**: `docs/technical/context_transitions.md` - General context transition mechanics
- **Coordinate Systems**: `docs/technical/coordinate_systems.md` - Positioning calculations
- **Orbit State**: `docs/design/states/orbit.md` - What happens in orbit
- **Space Navigation State**: `docs/design/states/space_navigation.md` - Parent state implementation

## Future Enhancements

- **Variable pause duration**: Longer pause for larger/more important planets?
- **Visual proximity indicator**: Circular ring, flashing border, approach vector
- **Proximity warning**: Audio cue or visual hint before full pause triggers
- **Configurable proximity radius**: Different radius per planet type or size class
- **Assisted orbit entry**: Auto-slow when approaching planets (toggle-able setting)
- **Momentum preservation**: Slingshot carries ship's velocity vector through
