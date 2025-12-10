# HUD Specification

## Overview

The main gameplay interface uses a HUD (Heads-Up Display) that acts as a canvas for rendering game information. While the most common configuration divides this canvas into four fixed display areas, the architecture supports different layouts as needed by different game states.

The core principle: **Game state determines what gets painted on the canvas.** The HUD manager receives state changes and instructs each area what to display.

## Standard Four-Area Layout

The default HUD configuration used for most gameplay consists of four distinct areas:

### 1. Main View
**Location:** Left side, large area  
**Position:** (0, 0, 500, 450)  
**Purpose:** Primary visual centerpiece for gameplay

**Content by game state:**
- **Hyperspace:** Starfield with player ship and visible star systems
- **In System Space:** Starfield with player ship, planets, and celestial objects
- **In Orbit:** Rotating planet view
- **On Planet Surface:** Terrain vehicle and environment
- **In Communications:** Alien portrait/graphics (or derelict ship visual)

**Characteristics:**
- Always displays graphics, never text menus
- Primary focus of player attention
- Can be interactive (ship movement, vehicle control) or static (rotating planet, alien portraits)
- Purely reactive to game state; no internal state beyond rendering/animation needs

### 2. Auxiliary View
**Location:** Upper-right corner  
**Position:** (500, 0, 300, 200)  
**Purpose:** Supplemental information and graphics

**Default content by game state:**
- **Hyperspace:** Ship status diagram (shows fuel, system health)
- **In System Space:** Mini-map showing star system (planets, orbits, ship position)
- **In Orbit:** Static terrain heightmap of planet surface
- **On Planet Surface:** Terrain vehicle statistics (fuel/energy remaining)
- **In Communications:** Retains previous display (mini-map, ship status, or scan results)

**Override displays (triggered by crew actions):**
- **Science Officer → Sensors:** Scanning animation (dither effect on target silhouette), then scan results. Detailed analysis appears in Message Log.
- **Science Officer → Analysis:** Extended details in Message Log; Auxiliary View may retain scan results.
- **Engineer → Damage/Repair:** Ship systems diagram showing damage state.
- **Doctor → Examine:** Crew member silhouette (based on species) with scanning dither, then health status display. (Note: Role needs design attention to increase usefulness.)

**Characteristics:**
- Display-only; no direct player interaction
- Default display determined by game state
- Crew actions can temporarily override the display
- Override clears when action completes or player backs out of menu
- HUD manager tracks active override (or game state includes `auxiliary_override`)

### 3. Control Panel
**Location:** Right side, middle  
**Position:** (500, 200, 300, 250)  
**Purpose:** Navigable text-based menus and player input

**Content by game state:**
- **Most states:** Crew bridge with role selection → action menus
- **Landing Mode:** Landing interface (Site Select, Descend, Abort)
- **Communications:** Dialogue choices
- **Warnings/Prompts:** Modal messages with choice options (e.g., gas giant landing warning)

**Characteristics:**
- Text and menus only; never displays graphics
- Player navigates with keyboard (W/S to navigate, Space/Enter to select)
- Hierarchical menu structure (roles → actions → sub-options)
- Has internal menu navigation state (current position in hierarchy, active modals)
- Menu navigation is internal; executing actions emits commands that affect game state
- Primary input point for player intent

### 4. Message Log
**Location:** Bottom, full width  
**Position:** (0, 450, 800, 150)  
**Purpose:** Scrolling log of text messages

**Content:**
- Event notifications ("Entered orbit around Mars")
- System messages ("Landing aborted")
- Communication text (alien dialogue)
- Scan analysis details
- Alerts and warnings
- Action results

**Characteristics:**
- Always present across all game states using the HUD
- Read-only display (not interactive)
- Auto-scrolls as new messages arrive
- Message history persists across state changes, unless otherwise specified
- Append-only; no display logic beyond rendering accumulated messages

## Layout Variations

### Planet Surface Layout
When on the planet surface, the HUD maintains the four-area structure but with adjustments:
- Auxiliary View shows terrain vehicle statistics (fuel/energy)
- Specific layout changes TBD (original game made minor adjustments)

### Special-Case Screens (Non-HUD or Alternate Layout)
Some interactions use full-screen interfaces outside the standard HUD:
- **Main Menu:** Title screen and game options
- **Starport:** Full-screen hub interface
- **Captain → Cargo:** Full-screen cargo manifest, message review, artifact examination
- **Navigator → Starmap:** Full-screen starmap interface (when not in hyperspace?)
- **Trade Screens:** Full-screen trading interfaces
- **Future:** Explorable locations (ruins, derelicts) may use alternate layouts

Note: The boundary between "HUD with different content" and "separate full-screen interface" needs clarification for some of these cases.

## Game States

The HUD displays are driven by game state, which consists of:
- **Location:** Where the player is (Hyperspace, System Space, Orbit, Planet Surface, etc.)
- **Sub-state:** Modifier to current location (Landing Mode, Communications, Scanning, etc.)
- **Auxiliary Override:** Temporary override for Auxiliary View display (or None)

### State: HYPERSPACE
- **Main View:** Starfield, ship, star systems
- **Auxiliary View:** Ship status (fuel, systems)
- **Control Panel:** Crew roles → action menus
- **Message Log:** Persistent

### State: IN_SYSTEM_SPACE
- **Main View:** Starfield, ship, planets
- **Auxiliary View:** System mini-map (planets, orbits, ship position)
- **Control Panel:** Crew roles → action menus
- **Message Log:** Persistent

### State: IN_ORBIT
- **Main View:** Rotating planet
- **Auxiliary View:** Terrain heightmap
- **Control Panel:** Crew roles → action menus
- **Message Log:** Persistent

### Sub-state: LANDING_MODE (during IN_ORBIT)
- **Main View:** Rotating planet
- **Auxiliary View:** Terrain heightmap (possibly with modal overlay for site selection)
- **Control Panel:** Landing interface (Site Select, Descend, Abort)
- **Message Log:** Persistent

Note: Landing site selection may use a modal interface with "blow up lines" connecting to the terrain map, rather than direct interaction with the Auxiliary View.

### Sub-state: GAS_GIANT_WARNING (during IN_ORBIT)
- **Main View:** Rotating planet
- **Auxiliary View:** Terrain heightmap
- **Control Panel:** Warning prompt (Proceed/Abort) → on Proceed: Landing interface
- **Message Log:** Persistent

### State: ON_PLANET_SURFACE
- **Main View:** Terrain vehicle and environment
- **Auxiliary View:** Vehicle statistics (fuel/energy)
- **Control Panel:** Crew roles → action menus (adjusted for surface context)
- **Message Log:** Persistent

### State: IN_COMMUNICATIONS
- **Main View:** Alien portrait, derelict ship visual, or other communication source
- **Auxiliary View:** Retains previous display (mini-map, ship status, or prior scan results)
- **Control Panel:** Dialogue choices
- **Message Log:** Communication text and responses

Note: Derelict interactions (automated responses, log playback, coordinate retrieval) use the Communications state for MVP.

### State: STARPORT
- Does not use standard HUD
- Full-screen hub interface

### State: MAIN_MENU
- Does not use HUD
- Title screen and game options

## Architecture

### Core Principles

1. **HUD is a Canvas:** The HUD is a rendering surface. Game state determines what gets painted on it.

2. **Game State is Source of Truth:** All display decisions flow from game state (location + sub-state + auxiliary override). Areas don't decide what to show; they're told what to show.

3. **HUD Manager as Mediator:** The HUD manager listens to game state changes and translates them into specific instructions for each area. Areas expose methods like `show_planet(planet)` or `show_terrain_map(planet)` and render what they're told.

4. **Areas are Renderers:** Areas don't subscribe to events or track game state themselves. They receive instructions from the HUD manager and render accordingly. This keeps them simple and testable.

5. **Control Panel Owns Menu State:** The Control Panel has internal state for menu navigation (current position in hierarchy, active modals). This is the one exception to "areas don't have state." Menu navigation doesn't change game state; executing a selected action does.

6. **Commands Flow Up:** Player interacts with Control Panel → selects action → action emits a command → command execution may change game state → HUD manager hears state change → areas update.

### Communication Flow

```
Game State changes (location, sub-state, auxiliary_override)
       ↓
HUD Manager receives state change event
       ↓
HUD Manager determines what each area should display
       ↓
HUD Manager calls area methods:
  - main_view.show_orbiting_planet(planet)
  - auxiliary_view.show_terrain_map(planet)
  - control_panel.set_context(location=ORBIT)
  - message_log.add("Entering orbit around {planet.name}")
       ↓
Areas render their assigned content
```

```
Player navigates Control Panel menus (internal to Control Panel)
       ↓
Player selects an action
       ↓
Control Panel emits a Command
       ↓
Command executes, potentially changing game state
       ↓
(Back to top of first flow)
```

### Benefits

- **Clean separation:** Game logic manages state, HUD manages display
- **Testable areas:** Can call `main_view.show_planet(fake_planet)` without full game state
- **Flexible layouts:** Different states can use different area configurations
- **Centralized mapping:** "What does this state look like?" logic lives in HUD manager
- **No sync issues:** Areas don't have independent state that can drift out of sync

## Input Routing

Input handling depends on current game state and context:

- **During Maneuvering:** Movement keys go to ship/vehicle control. Control Panel is inactive or limited.
- **In Menus:** W/S navigate, Space/Enter select. Movement keys may be ignored or exit menu mode.
- **During Communications:** Input goes to dialogue selection.
- **Modals/Prompts:** Modal captures input until dismissed.

The input handler checks game state to determine where to route input. The Control Panel receives input only when it's the active interaction context.

## Open Questions

1. **Captain → Cargo and Navigator → Starmap:** Are these full-screen takeovers, or HUD with alternate content? Need to decide and document.

2. **Planet Surface layout specifics:** What exactly changes from the standard four-area layout?

3. **Doctor role redesign:** Current design makes the role feel superfluous. Consider tying to exploration (examining alien life, assessing biosphere safety, diagnosing environmental hazards) rather than just reactive healing.

4. **Landing site selection interface:** Modal with "blow up lines" to terrain map? Needs design work.

5. **Derelict/ruin exploration:** MVP uses Communications state. Future versions may need dedicated exploration interface (side-scroller mode?).
