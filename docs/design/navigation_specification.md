# Navigation Specification

## Overview
This document defines how movement works across all spatial contexts: hyperspace, local space (star systems), and the transitions between them. Navigation is the core verb of the game. Everything else depends on how moving through space actually feels and functions.
Coordinate Systems

## Hyperspace
Hyperspace uses a tile-based coordinate system. The sector grid is 125 x 110 tiles, with each tile being 10 x 10 units. This gives a total navigable space of 1250 x 1100 units.

Ship position is tracked at the unit level for smooth movement and visual rendering. A ship might be at position (473, 891) within the 1250x1100 space.
Tile position is derived from unit position and determines what feature (if any) the ship is interacting with. Position (473, 891) means the ship is in tile (47, 89).

Each tile can contain at most one feature. Features are positioned at the center of their tile, but their visual and collision radii vary. A ship can fly around the edges of a tile without necessarily colliding with its feature.

### Hyperspace Objects
Three object types can occupy hyperspace tiles:
#### Stars (System Entry Points)
Stars are entry points into local space. Visual size varies by stellar spectral class:
Spectral Class | Relative Size | Notes
O, B (Blue giants) | Large | Dominates tile
A, F (White/Yellow-white) | Medium-large | 
G (Yellow, Sol-like) | Medium |
K (Orange) | Medium-small | 
M (Red dwarf) | Small |

**Interaction**: Collision with the star's boundary triggers automatic system entry. No confirmation prompt. Approach angle is preserved; entering from galactic north places the ship at the northern edge of the Outer System map.

#### Nebulae
Nebulae are fixed regions that change the visual background (from black to a colored field) and impose a mechanical effect: shields cannot be raised while inside a nebula.
**Interaction**: Fully passable. The ship flies through freely. The nebula effect applies to any tile marked as nebula territory, which may span multiple tiles.

#### Flux Points
Flux points are fast-travel nodes connecting distant parts of the sector. Visually rendered as a small cluster of stars that shift between configurations, suggesting spatial instability.
**Interaction**: Collision triggers the jump to the linked destination. Flux points are paired or networked; each point has a defined destination. Whether the destination is known before first use or must be discovered through exploration is TBD.

## Local Space (Star Systems)
Local space also uses a tile-based coordinate system, but at a smaller scale than hyperspace. The exact grid size varies depending on what's being represented:

**Outer System**: Contains gas giants, ice giants, and an enterable Inner System at the center. Grid size TBD based on system scale.
**Inner System**: Contains rocky planets (and potentially hot Jupiters) with the star at the center. Grid size TBD.
**Planetary Systems**: Any planet with satellites becomes its own enterable local space, with the planet at the center and moons in orbit. Grid size scales based on the extent of the moon system. Limited to four moons maximum per planet.

Ship position tracking works the same as hyperspace: unit-level for rendering, tile-level for interactions.

### Orbital Paths
Planets and moons are positioned along visible orbital paths rendered as circles or ellipses around their parent body. For MVP, celestial bodies occupy fixed positions on these paths. Actual orbital movement is deferred to post-MVP development.

The orbital path serves as visual context, communicating "this is where this planet travels" even without active motion.

### Local Space Objects
#### Star (Central Body)
The star sits at the center of the Inner System. It is non-interactive. Ships can fly through or over the star with no collision or penalty. The star is a visual centerpiece only.

#### Planets
Planets exist in both Outer and Inner Systems. Each planet has:

- A position on its orbital path
- A visual radius (how large it appears)
- A collision radius (when approach is detected)

**Interaction**: When the ship collides with a planet's boundary, a prompt appears in the Message Log: "Approaching [Planet Name]. Press Space to enter orbit." The player must confirm to transition to the ORBIT state. This allows ships to fly past planets without accidentally entering orbit.

#### Inner System Entry Point
The center of the Outer System contains an entry point to the Inner System. This functions like a star in hyperspace: collision triggers automatic transition inward. The ship appears at the edge of the Inner System map, with approach angle preserved.

**Exiting the Inner System**: Flying to the outer edge of the Inner System grid pops the context and returns the ship to the Outer System.

#### Planetary System Entry
Any planet with moons can be entered as its own local space context. Collision with such a planet still prompts for orbit, but an additional option may be presented (TBD) or entering the planetary system may require entering orbit first and then selecting a "View Moons" option.

**Alternative approach**: Planetary systems could be entered automatically on collision (like Inner System entry), with orbit being a separate action once inside. This needs design consideration.

#### Moons
Moons orbit within planetary systems. Interaction works identically to planets: collision prompts orbit entry via Message Log.

#### Starport/Space Station
Starport and Space Stations within planetary systems. Interaction works identically to planets: collision prompts dock entry via Message Log.

## Transitions
### Transition Types
Region transitions move the ship between nested coordinate contexts. These are automatic on collision:

- Hyperspace → Outer System (collide with star)
- Outer System → Inner System (collide with central entry point)
- Inner System → Outer System (reach grid edge)
- Local Space → Planetary System (TBD, may require orbit first)
- Planetary System → Local Space (reach grid edge)
- Local Space → Hyperspace (reach Outer System grid edge)

State transitions change what the ship is doing rather than where it is. These require player confirmation:

- Local Space → Orbit (collide with planet, press Space to confirm)
- Orbit → Local Space (select Navigator → Maneuver)
- Orbit → Surface (land on planet)
- Surface → Orbit (launch from surface)

### Context Stack Behavior
Each region transition pushes a new context onto the stack. The previous context's coordinates are preserved. Exiting a region pops the context and restores the ship to its previous position.

Example navigation sequence:
- Ship at hyperspace position (473, 891)
- Collides with star → Push Outer System context, ship appears at edge based on approach angle
- Flies to Inner System entry → Push Inner System context
- Approaches planet, presses Space → Push Orbit context
- Selects Navigator → Maneuver → Pop Orbit context, ship at planet approach coordinates
- Flies to Inner System edge → Pop Inner System context, ship at Inner System entry coordinates
- Flies to Outer System edge → Pop Outer System context, ship at hyperspace (473, 891)

### Orbit Entry and Exit
**Entering orbit**:
- Ship approaches planet
- Collision detected with planet boundary
- Message Log displays: "Approaching [Planet Name]. Press Space to enter orbit."
- Player presses Space
- ORBIT context pushed onto stack
- Entry coordinates saved
- Main View transitions to rotating planet display

**Exiting orbit**:
- Player selects Navigator → Maneuver
- ORBIT context popped from stack
- Ship reappears at saved entry coordinates
- Ship has no facing direction; movement begins from stationary
- Main View transitions back to local space

## Movement
### Engaging Movement Mode
Movement is controlled through Navigator → Maneuver. Selecting this option:
- Enters maneuvering sub-state
- Locks the Control Panel on the Navigator/Maneuver option
- Enables movement input (WASD or arrow keys)
- Disables other crew actions until maneuvering ends

**Disengaging**: Press Spacebar to exit maneuvering mode. Control Panel unlocks, returns to Bridge menu.

### Movement Input
**While maneuvering**:
- WASD or Arrow Keys: Control ship direction/velocity
- Spacebar: Disengage maneuvering mode

The specific movement model (instant direction change vs. momentum/drift) is TBD. The original Starflight had a degree of drift that made piloting feel more like ship handling than direct control.

## Fuel Consumption
Fuel is consumed during hyperspace travel. The rate depends on engine class:
Engine Class | Fuel per Coordinate | Notes 
Class 1 | 1.0 | Starting engine
Class 2 | 0.75 | 
Class 3 | 0.5 |
(etc.)

Local space movement (within star systems) consumes negligible or zero fuel. The real fuel cost is getting to and from systems via hyperspace, and launching from a planetary surface into orbit.

This creates the core exploration tension: how far can I travel before I need to turn back?

## Design Decisions

**Movement model**: Instant direction changes. This is an exploration game, not a flight simulator. The ship goes where you point it.
**Flux point discovery**: Destinations must be discovered through exploration. The first time you use a flux point, you don't know where you'll end up. Additionally, an unskilled Navigator requires time after a flux jump to orient the ship and determine current position. Higher Navigator skill reduces this orientation period.
**Planetary system entry**: Automatic on collision, consistent with all other region transitions. Flying into a planet with moons enters the planetary system directly. Entering orbit around the planet (or its moons) still requires the confirmation prompt.
**Grid sizes**: To be determined through playtesting. The feel of distances and travel times needs hands-on iteration.
**Fuel display**: Ship status in Auxiliary View (matching original games) is the starting point. May iterate based on how it feels in practice, since fuel remaining is critical information.
**Nebula extent**: Nebulae are large circles, potentially massive relative to tile size, centered on a tile coordinate. Multiple nebulae can overlap. Sufficient for MVP; more sophisticated shapes or procedural generation can come later.

## Planetary Surface Navigation
### Overview
Planetary surfaces are the largest navigable spaces in the game. Players explore via terrain vehicle, collecting resources and investigating points of interest. The surface represents the payoff for all the space travel required to get there.

### Planetary Grid
Planetary surfaces use a tile-based coordinate system: 500 x 200 tiles, with each tile being 10 x 10 units. Total navigable space: 5000 x 2000 units.
Coordinates are displayed using directional notation centered on (0,0):

- East/West: 250W to 250E
- North/South: 100N to 100S

**Example**: A position might display as "127W, 43N" rather than abstract grid numbers. This reads like actual planetary navigation.

### Landing
During Captain → Land, the player selects landing coordinates via the planetary heightmap interface. The selected coordinates correspond directly to the planetary grid. The ship lands at the chosen tile and appears as an icon on the surface.

### Disembark and Movement
Selecting Captain → Disembark places the player in their terrain vehicle adjacent to the landed ship. Movement is grid-based, similar to space navigation, controlled via WASD or arrow keys while in Move mode.
**Engaging movement**: Select Move from the surface action menu. Movement controls activate, menu locks on Move option.
**Disengaging movement**: Press Spacebar to exit Move mode and return to menu navigation.

### Terrain and Fuel Efficiency
All terrain is passable. Terrain type affects fuel consumption rate rather than blocking movement:
Terrain Type | Fuel Efficiency | Visual Indication
Flat/Low-lying | High | Low elevation colors 
Elevated/Hilly | Medium | Mid elevation colors
Mountainous | Low | High elevation colors
Liquid (ocean, magma, etc.) | Very Low | Lowest elevation colors
Terrain is rendered as an elevation-based color gradient. No biome-specific graphics for MVP.

### Vehicle Fuel Depletion
When the terrain vehicle runs out of fuel:
- Vehicle is abandoned at current location
- Player automatically begins return to ship on foot
- Return path is a direct line to ship coordinates
Player is vulnerable during return: increased chance of injury from flora/fauna and weather
Terrain does not directly damage the player, even hostile environments (magma, etc.)
Upon reaching ship, player re-enters normally

This is a failure state with consequences, not game over. The player loses access their vehicle and disembarking until replaced at Starport, but otherwise survives.

### Visibility
**Local view**: Immediate tiles surrounding the vehicle are visible in the Main View.
**Radar/expanded view**: Larger area visible showing icons for points of interest. Accessible via Map toggle in surface action menu, displayed in Auxiliary View.
**Terrain visibility**: Full planetary terrain (elevation data) is always visible. Object icons appear within radar range.
No fog-of-war or hidden object mechanics. If an object is within radar range, it's visible and can be targeted.

### Points of Interest
**Procedurally generated (from planet seed)**:
- Mineral deposits
- Flora
- Fauna

**Seed-based (consistent across visits)**:
- Alien settlements
- Ruins

Procedural generation ensures variety while seed-based placement ensures story-relevant locations remain stable.

### Scanning
Scanning operates on visible objects only. To scan a surface object:
- Select Scan → Target from surface action menu
- Move cursor to select visible object
- Confirm to execute scan
- Results appear in Message Log

Science Officer skill affects the quality and detail of scan results, not what can be seen or targeted.

### Collection
Resource collection uses the Cargo modal, consistent with ship-based cargo management:
- Move terrain vehicle adjacent to collectible object
- Open Cargo modal (select Cargo from surface action menu)
- Adjacent collectibles appear under "Nearby" category
- Select item and choose [P]ick up
- Item transfers to vehicle cargo

**Lifeforms**: Hostile creatures must be subdued (stunned via Weapon → Stun mode) before they appear as collectible.
**Cargo capacity**: Terrain vehicle has limited cargo space separate from ship cargo. Collected items transfer to ship cargo upon re-entering the ship.

### Weather
Weather is global to the planet and randomly generated during surface travel. Weather changes are announced in the Message Log:
- "A storm is approaching"
- "The weather clears"
- "Seismic activity detected"

**Mechanical effect**: During inclement weather, there is a chance of crew injury. This applies whether the crew is in the vehicle or traveling on foot (during fuel depletion return). Weather does not affect movement speed, visibility, or fuel consumption.

### Return to Ship
The landed ship appears as an icon on the planetary grid at the landing coordinates. When the terrain vehicle stops adjacent to the ship icon:
- Message Log displays: "Enter ship? Y/N"
- Player confirms with Y
- Player exits terrain vehicle and enters ship
- SURFACE context remains active; player is now in ship on surface
- Player can select Captain → Launch to return to orbit

### Coordinate Display
Planetary coordinates are displayed at the top of the Main View during surface exploration, mirroring how hyperspace coordinates are displayed during space navigation. Format: "[X]W/E, [Y]N/S"

### Open Questions (Surface)
1. Vehicle fuel capacity: What's the starting range? How does this balance against planet size?
2. Vehicle loss: When abandoned due to fuel depletion, is the vehicle lost permanently? Recoverable on return? Replaced at Starport?
3. Radar range: How many tiles does the expanded view cover? Does Science Officer skill or ship equipment affect this?
4. Injury mechanics: How does weather/fauna injury work? Flat chance per time unit? Per tile moved? Does Doctor skill reduce chance or just improve treatment?
5. Terrain vehicle cargo capacity: How much can the vehicle hold versus the ship? Is this upgradeable?
