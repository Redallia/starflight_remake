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
- Message history persists across state changes
- Append-only; no display logic beyond rendering accumulated messages

## Layout Variations

### Planet Surface Layout

When on the planet surface, the HUD maintains the four-area structure but with significantly different content. The architectural pattern remains the same (game state drives display, HUD manager mediates), but the player interaction model shifts from deep crew role hierarchies to a shallower, action-focused menu.

**Main View:**
- Top-down terrain view with vehicle and icons
- Icons represent: minerals, flora/fauna, structures (ruins, alien buildings), player's landed ship
- Player moves vehicle here during Move mode
- Weapon targeting cursor appears here during Weapon/Target

**Auxiliary View:**
- Default: Vehicle statistics (cargo capacity used/remaining, fuel/energy, distance and direction to ship)
- Map mode: Toggles to show either local mini-map (nearby terrain) or regional map (wider area, structures visible from afar)
- Can overlay stats on map view or toggle between them

**Control Panel:**
- Remains interactive (unlike original game's passive crew health display)
- Uses shallow hierarchy matching ship interface pattern
- Top-level options with at most one level of sub-options

**Control Panel Menu Structure:**

- **Move** → Engages movement mode, locks menu (no sub-menu)
- **Scan** →
  - Target (move cursor to select scan target)
  - Analysis (detailed readout of scanned target, results in Message Log or modal)
  - Icons (reference modal showing what each icon type represents)
- **Cargo** → Opens cargo modal (view inventory, pick up nearby items, jettison items, examine items/messages)
- **Weapon** →
  - Mode (toggle between Stun and Attack)
  - Target (move cursor to select target, execute attack)
- **Medicine** →
  - Review (crew health status modal)
  - Treat (select crew member to heal; field treatment caps at 50-60% max health)
- **Map** → Toggles Auxiliary View between stats and map view (no sub-menu)

**Message Log:**
- Functions as normal - event notifications, scan results, descriptions, hazard warnings
- Crew injuries from creature attacks or environmental hazards reported here
- No longer gets repurposed for cargo display (cargo uses modal instead)

**Contextual Prompts:**
- Stopping adjacent to landed ship triggers "Enter Ship? Y/N" prompt
- Stopping adjacent to structure (ruins, alien building) may trigger "Enter? Y/N" prompt (future feature)

**Crew Skills on Planet Surface:**

Crew roles don't appear in the menu, but skills affect action outcomes:
- **Science Officer:** Scan detail and analysis quality
- **Navigator:** Weapon accuracy (low skill = shots miss or hit wrong target)
- **Doctor:** Healing effectiveness
- **Engineer:** Potentially vehicle repair (if vehicle damage is implemented)
- **Communications:** Potentially relevant at alien structures (future feature)

**Input Routing on Planet Surface:**

- **Move mode active:** Movement keys control vehicle, menu locked on Move option, Spacebar disengages
- **Menu navigation:** W/S navigate, Space/Enter select, Escape/Backspace backs out
- **Weapon/Target mode:** Cursor keys move targeting cursor, Space/Enter fires, Escape cancels
- **Scan/Target mode:** Cursor keys move selection cursor, Space/Enter confirms target, Escape cancels
- **Modals:** Capture input until dismissed

## Modal Specifications

Modals overlay the HUD, capturing input until dismissed. They maintain game context (the HUD remains visible beneath) while providing focused interfaces for specific tasks.

### Cargo Modal (Captain → Cargo)

Accessed via Captain → Cargo from the Control Panel (in space) or Cargo from the action menu (on planet surface). Used for inventory management on both ship and terrain vehicle.

**Layout:** Two-column design
- **Left column:** Scrollable item list organized by category
- **Right column:** Description of highlighted item, plus available actions

**Categories (with headers):**
- **Nearby** - Items within pickup range (only appears when items are present)
- **Minerals** - Sorted alphabetically, shows quantity
- **Lifeforms** - Sorted alphabetically, shows quantity
- **Artifacts** - Sorted alphabetically
- **Messages** - Sorted by discovery date

**Interaction:**
- W/S or Up/Down: Navigate item list
- Right column updates automatically to show highlighted item
- Hotkey actions shown at bottom of modal, context-sensitive:

| Item Type | Available Actions |
|-----------|-------------------|
| Nearby item | [P]ick up |
| Carried mineral/lifeform | [J]ettison |
| Carried artifact | [J]ettison |
| Carried message | [A]rchive |

- Escape: Close modal

**Behaviors:**
- **Pick up:** Transfers item from Nearby to cargo. If cargo is full, shows "Cargo hold full" - excess items remain in place.
- **Jettison:** Prompts "Jettison [item]? Y/N" - confirmed items are destroyed and cannot be recovered.
- **Archive:** Moves message to archived storage (does not consume cargo space).

**Context differences:**
- **Ship:** Nearby items are debris from destroyed vessels or items floating in proximity
- **Terrain vehicle:** Nearby items are minerals, lifeforms, artifacts on the ground within pickup range
- **Lifeforms (planet surface):** Hostile creatures must be subdued (stunned) before they appear as pickable

**Display format:**
```
┌─────────────────────────────────────────────────────────────┐
│  CARGO (23/50)                                              │
├─────────────────────────────┬───────────────────────────────┤
│                             │                               │
│  NEARBY                     │  Endurium                     │
│  ──────                     │                               │
│    Debris Fragment          │  A rare crystalline mineral   │
│                             │  with unique energy storage   │
│  MINERALS                   │  properties. Highly valued    │
│  ────────                   │  by most spacefaring          │
│  > Endurium (3)             │  civilizations.               │
│    Rhodium (7)              │                               │
│                             │  Value: ~150 credits/unit     │
│  LIFEFORMS                  │                               │
│  ─────────                  │                               │
│    Spore Sample (2)         │  [J]ettison                   │
│                             │                               │
│  ARTIFACTS                  │                               │
│  ─────────                  │                               │
│    Strange Device           │                               │
│                             │                               │
│  MESSAGES                   │                               │
│  ────────                   │                               │
│    Ruins Text (2450.7)      │                               │
│                             │                               │
├─────────────────────────────┴───────────────────────────────┤
│  [P]ick up  [J]ettison  [A]rchive           [Esc] Close     │
└─────────────────────────────────────────────────────────────┘
```

### Starmap Modal (Navigator → Starmap)

Accessed via Navigator → Starmap from the Control Panel. **Only available in Hyperspace** - option does not appear in Navigator menu when in system space.

Used for navigation planning. Purely informational - does not set course or engage autopilot. Player must manually navigate toward desired coordinates.

**Layout:**
- **Main area:** Scrolling sector map showing ~100x100 coordinate region
- **X-axis:** Along bottom edge with coordinate markers
- **Y-axis:** Along left edge with coordinate markers
- **Info bar:** Along bottom, showing Position | Destination | Distance | Fuel

**Map elements:**
- Stars (visitable systems)
- Nebulae (environmental/visual features)
- Flux/jump points (only if discovered)
- Ship marker (current location, distinct icon)
- Crosshair (destination selector, player-controlled)

**Interaction:**
- WASD or arrow keys: Move crosshair
- Map scrolls when crosshair reaches edge (rolling/continuous display)
- Info bar updates in real-time:
  - **Position:** Current ship coordinates (x, y)
  - **Destination:** Crosshair coordinates (x, y)
  - **Distance:** Straight-line distance to crosshair
  - **Fuel:** Estimated fuel consumption for journey
- Escape: Close modal

**Display format:**
```
┌─────────────────────────────────────────────────────────────┐
│  STARMAP                                                    │
├─────────────────────────────────────────────────────────────┤
│    0   10   20   30   40   50   60   70   80   90  100      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    *                                 │ 0 │
│  │        ·                      *                      │   │
│  │                  ░░░░                                │20 │
│  │    *            ░░░░░░            ⊕                  │   │
│  │                  ░░░░        +                       │40 │
│  │         *                              *             │   │
│  │                        █                             │60 │
│  │                                   *                  │   │
│  │              *                                       │80 │
│  │    *                                      *          │   │
│  └──────────────────────────────────────────────────────┘100│
│                                                             │
│  * = Star   ░ = Nebula   ⊕ = Jump Point   █ = Ship   + = Cursor │
├─────────────────────────────────────────────────────────────┤
│ Position: 47, 58  │ Destination: 62, 38 │ Dist: 24.4 │ Fuel: 12 │
├─────────────────────────────────────────────────────────────┤
│                                              [Esc] Close    │
└─────────────────────────────────────────────────────────────┘
```

**Future consideration:** When in system space (post-MVP), Navigator → Starmap could show a local system map instead, displaying planets, moons, gas giant sub-systems, and current ship position within the system.

**Related:** During hyperspace maneuvering, the Auxiliary View may cycle between Ship Status and a local hyperspace map snapshot (e.g., every 10 seconds) to provide visual interest and navigation awareness during long journeys.

### Trade Outpost Modal (Planet Surface)

Accessed by stopping terrain vehicle adjacent to a trade outpost building on a planet with sentient species settlements. Not required for MVP (intro scenario has no planetary trade encounters).

**Trigger:** Proximity to trade outpost → "Do you wish to trade? Y/N" prompt

**Layout (mini-HUD style):**
- **Top-left:** Portrait/image representing the species you're trading with
- **Top-right:** Trade info (Species name, STV percentage, player credits, current offer)
- **Middle:** Scrollable goods list (merchant inventory and player cargo)
- **Bottom:** Action bar

**Display format:**
```
┌─────────────────────────────────────────────────────────────┐
│ ┌─────────┐  SPECIES: Thrynn                                │
│ │         │  STV: 127%                                      │
│ │  [Pic]  │  Credits: 4,500                                 │
│ │         │                                                 │
│ └─────────┘  Offer: ---                                     │
├─────────────────────────────────────────────────────────────┤
│  AVAILABLE GOODS                                            │
│  ───────────────                                            │
│  > Endurium (15)         50 cr/unit                         │
│    Promethium (8)        120 cr/unit                        │
│    Medical Supplies (3)  200 cr/unit                        │
│                                                             │
│  YOUR CARGO                                                 │
│  ──────────                                                 │
│    Rhodium (7)           35 cr/unit                         │
│    Spore Sample (2)      80 cr/unit                         │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│        [B]uy          [S]ell          [Esc] Exit            │
└─────────────────────────────────────────────────────────────┘
```

**STV (Standard Trade Value):**
Percentage modifier relative to Starport base prices.
- 100% = standard prices
- Above 100% = merchant charges more (buying) / pays less (selling)
- Below 100% = better deals for player

**Interaction - Browse Mode:**
- W/S or Up/Down: Navigate goods list
- B: Initiate buy of highlighted item → Transaction mode
- S: Initiate sell of highlighted cargo item → Transaction mode
- Escape: Exit trade screen

**Interaction - Transaction Mode:**
Info area updates to show merchant's offer price. Action bar changes:

```
├─────────────────────────────────────────────────────────────┤
│       [A]gree         [H]aggle        [C]ancel              │
└─────────────────────────────────────────────────────────────┘
```

- Agree: Complete transaction at offered price, return to browse mode
- Haggle: (Post-MVP) Initiate haggling mini-game to negotiate better price
- Cancel: Abort transaction, return to browse mode

**Quantity selection:**
For items with quantity > 1, transaction mode may include quantity selector (TBD):
- Left/Right or A/D: Adjust quantity
- Offer price updates based on quantity

### Special-Case Screens (Non-HUD or Alternate Layout)
Some interactions use full-screen interfaces outside the standard HUD:
- **Main Menu:** Title screen and game options
- **Starport:** Full-screen hub interface. MVP uses simple text menu; future versions will use side-scroller exploration mode. See separate Starport specification document.
- **Captain → Cargo:** Modal over HUD (not full-screen takeover)
- **Navigator → Starmap:** Modal over HUD, or Auxiliary View override (TBD)
- **Trade Screens:** Modal interfaces where needed
- **Future:** Explorable locations (ruins, derelicts) may use side-scroller mode similar to Starport

Note: Most "special" interfaces are now planned as modals over the HUD rather than full-screen takeovers, maintaining context and simplifying implementation.

## Game States

The HUD displays are driven by game state, which consists of:
- **Location:** Where the player is (Hyperspace, System Space, Orbit, Planet Surface, etc.)
- **Sub-state:** Modifier to current location (Landing Mode, Communications, Scanning, etc.)
- **Auxiliary Override:** Temporary override for Auxiliary View display (or None)
- **Active Encounter:** Reference to ships in current encounter, if any (context modifier, not a location)

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

### Encounters (Context Modifier)

Encounters are not a separate location state. They are a **context modifier** that can occur during IN_SYSTEM_SPACE or HYPERSPACE. When an encounter is active, the game tracks `active_encounter` referencing the involved ships.

**What changes during an encounter:**
- **Main View:** Renders encounter mode - player ship and all other ships in the encounter (may be multiple hostile vessels)
- **Auxiliary View:** No change from base state (mini-map in system space, ship status in hyperspace)
- **Control Panel:** No change - full crew role access remains available
- **Message Log:** Encounter events reported ("Captain, they've armed their weapons!")

**What stays the same:**
- All crew functions remain accessible
- Navigator → Maneuver still works (you can fly around within the encounter)
- Science Officer can scan alien vessels (reveals composition, size, shield status, weapons armed)

**Encounter triggers:**
- Another ship closes to interaction range
- Attempting to orbit a protected planet (forced encounter with defenders)

**Encounter resolution:**
- Flee successfully → encounter ends, return to normal space/hyperspace
- Hail/Respond → transitions to IN_COMMUNICATIONS
- Combat (post-MVP) → transitions to combat state
- Alien flees/destroyed → encounter ends

**Protected planet flow:**
1. Player attempts to enter orbit around protected planet
2. Defender encounter triggers; player remains in IN_SYSTEM_SPACE with active_encounter
3. Player resolves encounter (negotiate, fight, flee)
4. If resolved peacefully or defenders defeated → orbit becomes available
5. If player flees → back to normal IN_SYSTEM_SPACE, planet still protected

Note: Encounters can occur in IN_SYSTEM_SPACE and HYPERSPACE, but never during IN_ORBIT. Once in orbit, the player is in a "safe" state.

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
- **Main View:** Top-down terrain with vehicle and icons (minerals, flora/fauna, structures, landed ship)
- **Auxiliary View:** Vehicle statistics (cargo, fuel, distance to ship); toggles to map view
- **Control Panel:** Shallow action-focused menu (Move, Scan, Cargo, Weapon, Medicine, Map)
- **Message Log:** Persistent; receives scan results, hazard warnings, injury reports

This state uses a significantly different interaction model. See **Layout Variations > Planet Surface Layout** for full details on menu structure, input routing, and how crew skills apply.

### State: IN_COMMUNICATIONS
- **Main View:** Alien portrait (generic by species; specific character portraits are a future enhancement) or derelict ship visual
- **Auxiliary View:** Retains previous display (mini-map, ship status, or prior scan results)
- **Control Panel:** Communications menu (see below)
- **Message Log:** All dialogue appears here - player statements, alien responses, conversation record

**Communications Control Panel Menu:**

Top-level options:
- **Statement** → Sends a posture-flavored statement to the alien; they respond in Message Log
- **Question** → Opens sub-menu (replaces top-level menu):
  - Themselves
  - Other Beings
  - The Past
  - Trade
  - General Info
- **Posture** → Opens sub-menu (replaces top-level menu):
  - Hostile
  - Friendly (default at conversation start)
  - Obsequious
  - Selection persists for duration of conversation until changed
- **Terminate** → Ends communication, returns to prior game state

Posture affects the tone of Statements and Questions, and may influence alien responses and disposition.

Note: Derelict interactions use the same Communications interface for MVP. Future versions may differentiate (e.g., limited options for automated systems, different question categories like Ship Logs, Coordinates, System Status).

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

**During Maneuvering (Navigator → Maneuver active):**
- Movement keys control ship/vehicle
- Control Panel is locked on Navigator/Maneuver option (highlighted)
- Spacebar behavior depends on location:
  - In space/hyperspace: Disengages maneuver mode, unlocks Control Panel, returns to Bridge menu
  - Approaching a planet: Can transition to IN_ORBIT state and reset Control Panel to Bridge
- Other crew functions inaccessible until maneuver mode disengaged

**In Menus (maneuver mode not active):**
- W/S navigate menu options
- Space/Enter select highlighted option
- Movement keys may be ignored or could re-engage maneuver mode (TBD)
- Backspace/Escape backs out of sub-menus

**During Communications:**
- W/S navigate dialogue options
- Space/Enter select option
- Sub-menus (Question, Posture) replace top-level menu; backing out returns to top level

**Modals/Prompts:**
- Modal captures all input until dismissed
- Typically Y/N or selection from limited options

The input handler checks game state to determine where to route input. The Control Panel receives input only when it's the active interaction context (i.e., not during maneuvering).

## Open Questions

1. **Captain → Cargo and Navigator → Starmap:** Are these full-screen takeovers, or HUD with alternate content? Leaning toward modals over the HUD rather than full-screen takeovers. Need to finalize and document.

2. **Doctor role redesign:** Current design makes the role feel superfluous in space. On planet surface, Medicine/Treat is useful but limited. Consider tying to exploration (examining alien life, assessing biosphere safety, diagnosing environmental hazards) rather than just reactive healing.

3. **Landing site selection interface:** Modal with "blow up lines" to terrain map? Needs design work.

4. **Derelict/ruin exploration:** MVP uses Communications state. Future versions may need dedicated exploration interface (side-scroller mode?).

5. **Planet Surface - structure interaction:** What happens when player enters ruins or alien buildings? Modal interaction? Separate game state? Side-scroller mode (future)?

6. **Starport interface:** Full-screen hub, but what's the actual layout and flow? Needs detailed specification.