# HUD Specification

## Overview

The main gameplay interface uses a single HUD (Heads-Up Display) layout divided into four fixed display slots. The content within each slot changes based on the current game state, but the slots themselves never move or resize.

## HUD Layout

The HUD consists of four distinct areas:

### 1. Main View
**Location:** Left side, large area
**Position:** (0, 0, 500, 450)
**Purpose:** Primary visual centerpiece for gameplay

**Content varies by game state:**
- **In Hyperspace:** Starfield with player ship, star systems, and other hyperspace specific celestial systems
- **In Space:** Starfield with player ship, planets, and other celestial objects
- **In Orbit:** Rotating planet view
- **During Communications:** Alien portrait/graphics
- **On Planet Surface:** Terrain vehicle and environment

**Characteristics:**
- Always displays graphics, never text menus
- Primary focus of player attention
- Can be interactive (ship movement, vehicle control), or static(rotating planet, alien portraits)

### 2. Auxiliary View
**Location:** Upper-right corner
**Position:** (500, 0, 300, 200)
**Purpose:** Supplemental information and graphics

**Content varies by game state:**
- **In Hyperspace:** Ship systems diagram
- **In Space:** Mini-map showing star system
- **In Orbit:** Terrain map with landing coordinates
- **During Scan:** Sensor scan results
- **Ship Status:** Ship systems diagram

**Characteristics:**
- Mix of graphics and data visualization
- Can be updated by crew actions (Science Officer scans)
- Provides context for Main View

### 3. Control Panel
**Location:** Right side, middle
**Position:** (500, 200, 300, 250)
**Purpose:** Navigable text-based menus

**Content varies by game state:**
- **In Hyperspace:** Crew bridge with role selection → action menus
- **In Space:** Crew bridge with role selection → action menus
- **In Orbit:** Crew bridge with role selection → action menus
- **In Landing Mode:** Landing interface (Site Select, Descend, Abort)
- **During Communications:** Dialogue choices
- **During Warnings:** Warning messages with choice options

**Characteristics:**
- **NEVER displays graphics** - text and menus only
- Player navigates with keyboard (W/S to navigate, Space/Enter to select)
- Hierarchical menu structure (roles → actions)
- Interactive/selectable, when Navigation/Maneuver is not active

### 4. Message Log
**Location:** Bottom, full width
**Position:** (0, 450, 800, 150)
**Purpose:** Scrolling log of text messages

**Content:**
- Event notifications ("Entered orbit around Mars")
- System messages ("Landing aborted")
- Communication text (alien dialogue)
- Alerts and warnings
- Action results

**Characteristics:**
- Always present across all game states utilizing the HUD interface
- Read-only display (not interactive)
- Auto-scrolls as new messages arrive
- Message history persists across state changes

## Non-HUD Screens

The following screens do NOT use the 4-slot HUD layout:
- **Main Menu:** Title screen and new game options
- **Starport:** Docking station with full-screen menus
- **Trade Screens:** Full-screen trading interfaces
- **Future:** Planet surface locations, special encounters, TBD

## Game States

The HUD slots are populated based on the current game state:

### State: IN_HYPERSPACE
- **Main View:** starfield, ship, star systems
- **Auxiliary View:** ship status
- **Control Panel:** crew roles → action menus
- **Message Log:** persistent

### State: IN_SPACE
- **Main View:** starfield, ship, planets
- **Auxiliary View:** mini-map of star system
- **Control Panel:** crew roles → action menus
- **Message Log:** persistent

### State: IN_ORBIT
- **Main View:** rotating planet
- **Auxiliary View:** terrain heightmap, coordinates
- **Control Panel:** crew roles → action menus
- **Message Log:** persistent

### State: LANDING_MODE (sub-state of IN_ORBIT)
- **Main View:** rotating planet
- **Auxiliary View:** terrain with selected site
- **Control Panel:** Site Select, Descend, Abort
- **Message Log:** persistent

### State: GAS_GIANT_WARNING (sub-state of IN_ORBIT)
- **Main View:** rotating planet
- **Auxiliary View:** terrain heightmap
- **Control Panel:** WARNING: Proceed/Abort → On Proceed: Site Select, Descend, Abort
- **Message Log:** persistent

### State: AT_STARPORT
- **Does not use HUD** - full-screen menu interface

### Future States:
- **ON_PLANET_SURFACE:** Terrain vehicle gameplay
- **IN_COMMUNICATION:** Ship-to-ship dialogue
- **IN_COMBAT:** Combat interface
- **IN_TRADE:** Trading with aliens/stations
- **IN_SPECIAL_LOCATION:** Derelict ships, ruins, etc.

## Design Principles

1. **Fixed Layout:** The four slots never change position or size
2. **State-Driven Content:** Slot content determined by game state, not by "screens"
3. **Persistent Message Log:** Message history survives state transitions
4. **Separation of Concerns:**
   - Main View: Visual/interactive gameplay
   - Auxiliary View: Supplemental information
   - Control Panel: Text menus and choices
   - Message Log: Event history
5. **One HUD Instance:** Single HUD shared across all relevant game states
6. **Panel Reuse:** Panel instances persist across state changes (preserves state like terrain generation)

## Implementation Notes

### Architecture: State-Driven Areas

The HUD uses a **reactive area-based architecture** rather than panel swapping:

**HUDManager Structure:**
- `MainViewArea` - Smart area that renders appropriate content based on game state
- `AuxiliaryViewArea` - Smart area that renders appropriate content based on game state
- `ControlPanelArea` - Smart area that renders appropriate content based on game state
- `MessageLogArea` - Always renders message log (state-independent)

**How it works:**
1. `GameState.location` changes (e.g., "space" → "orbit")
2. `HUDManager` observes the change
3. `HUDManager` notifies each area of the new state
4. Each area updates its display logic internally:
   - `MainViewArea` hears "orbit" → renders rotating planet
   - `AuxiliaryViewArea` hears "orbit" → renders terrain map
   - `ControlPanelArea` hears "orbit" → renders bridge menu
   - `MessageLogArea` doesn't care, continues rendering log

**Key Principles:**
- Screens **never manage HUD** - they only change `GameState.location`
- Areas are **smart** - they contain the rendering logic for their region
- No panel swapping - each area decides what to render based on state
- Current "panels" (SpaceViewPanel, etc.) become rendering methods within areas
- Area positions are constants defined in HUDManager
- Adding new states requires updating area render logic, not creating new panels

**Benefits:**
- Clean separation: Screens manage gameplay, HUD manages display
- Easy to extend: New states just add new conditions to area render methods
- No duplicate instantiation: Areas persist, only rendering changes
- State preserved: Each area can maintain internal state (like terrain generation)
- Centralized display logic: All HUD behavior in one place