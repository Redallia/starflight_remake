# Minimum Viable Product (MVP) Definition

## Core Question
What's the smallest version of this game that still feels like Starflight?

## MVP Goal
Create a playable loop where you can:
1. Launch from starport
2. Navigate to a planet
3. Land and gather resources
4. Return and sell resources
5. Use credits to improve your ship
6. Repeat with better capabilities

## Essential Systems (Must Have)

### 1. Basic Starport Interface
- Simple menu system
- View/manage ship status
- Purchase fuel and basic upgrades
- Save/load game
- Launch into space

### 1.5. Game Flow & Starport
- New game initialization
- Basic ship/game state (fuel, cargo capacity, credits, location)
- Simple starport screen with menu
  - View Ship Status
  - Launch to Space
  - Exit to Main Menu
- Placeholder space screen (proves transitions work)
  - Display basic status
  - Return to Starport option
- Screen transitions (menu → starport → space → starport)
- Wire up "New Game" button to create game state and go to starport

**Scope Limits:**
- No actual fuel purchases (deferred to Phase 5)
- No upgrades (deferred to Phase 5)
- No actual space movement (deferred to Phase 2)
- No save/load (deferred to Phase 5)
- No planets visible yet (deferred to Phase 2)
- Basic text menus only
- Focus on screen flow and basic state management only

### 2. Space Navigation
- Grid-based movement in a single star system
- WASD controls
- Simple starfield background
- Fuel consumption
- Planet proximity detection
- Return to starport

**Scope Limits:**
- Single star system only
- No hyperspace
- No other ships/encounters
- Simple collision detection
- No complex navigation aids

### 3. Planetary Orbit
- Enter orbit around planets
- Basic scan (shows if resources present)
- Landing option
- Exit orbit

**Scope Limits:**
- Simple scan data (yes/no for resources)
- No detailed analysis
- No orbital hazards
- Basic text display

### 4. Planet Exploration
- Deploy to surface
- Grid-based vehicle movement
- Terrain types (easy/medium/hard)
- Resource detection and collection
- Fuel management
- Return to orbit

**Scope Limits:**
- Small planet grid (maybe 20x20)
- 2-3 terrain types
- 2-3 resource types
- No weather or hazards (yet)
- Simple visual representation

### 5. Resource System
- Fuel (consumed by travel)
- Credits (for purchasing)
- 2-3 mineable resources with different values
- Cargo capacity
- Basic pricing

**Scope Limits:**
- No market fluctuations
- Fixed prices
- Simple value system
- No special/rare items

### 6. Basic Ship Systems
- Fuel tank (capacity and current level)
- Cargo hold (capacity and contents)
- Simple damage (optional for MVP)
- One upgradeable system (cargo or fuel capacity)

**Scope Limits:**
- No weapons or shields
- No complex systems
- Minimal upgrade paths

## Explicitly NOT in MVP

### Deferred to Later Phases
- Crew management and training
- Multiple star systems
- Hyperspace travel
- Alien interactions
- Combat system
- Trading between locations
- Complex ship systems
- Weather and hazards
- Multiple ship types
- Story elements
- Multiple starports
- Advanced scanning
- Diplomatic relations

## Success Criteria
The MVP is successful if a player can:
1. Understand the basic controls within 5 minutes
2. Complete a full loop (launch → explore → return) successfully
3. Feel progression (better equipment, more resources)
4. Want to explore "just one more planet"
5. Experience the core risk/reward (fuel vs. exploration distance)

## Technical MVP Requirements

### Core Classes Needed
- Game (main game loop)
- GameState (manages overall state)
- Ship (player's vessel)
- Planet (planet data and generation)
- Terrain (planet surface)
- Resource (collectible items)
- StarportScreen
- SpaceNavigationScreen
- OrbitScreen
- ExplorationScreen

### Data Files Needed
- Game configuration (settings)
- Planet generation parameters
- Resource definitions
- Ship definitions
- Price data

### UI Screens Needed
1. Main Menu (new/load/quit)
2. Starport (menu-based)
3. Space Navigation (grid view)
4. Planetary Orbit (status screen)
5. Surface Exploration (grid view)

## Development Order

### Phase 1: Foundation (Week 1-2)
- Project setup
- Basic game loop
- Input handling
- Screen management system
- Simple rendering framework
- Working main menu

### Phase 1.5: Game Flow & Starport (Week 2)
- New game initialization
- Basic ship/game state
- Simple starport screen with menu
- Launch button to transition to space
- Return to starport functionality
- Screen transitions (menu → starport → space → starport)

### Phase 2: Space Navigation (Week 3)
- Grid-based movement
- Starfield rendering
- Fuel consumption
- Planet objects in space
- Basic collision

### Phase 3: Planetary System (Week 4-5)
- Planet generation
- Orbit interface
- Landing mechanics
- Surface grid
- Terrain system

### Phase 4: Resource Loop (Week 6)
- Resource placement
- Collection mechanics
- Cargo system
- Return to orbit

### Phase 5: Starport & Economy (Week 7)
- Starport menus
- Buy/sell resources
- Purchase upgrades
- Save/load

### Phase 6: Polish & Balance (Week 8)
- Bug fixes
- Balance fuel/distance/rewards
- UI improvements
- Playtesting

## Testing Milestones

### Milestone 1: "I Can Move"
- Can move ship in space
- Fuel decreases
- Can reach planets

### Milestone 2: "I Can Land"
- Can enter orbit
- Can scan planet
- Can land on surface
- Can move vehicle
- Can return to orbit

### Milestone 3: "I Can Profit"
- Can collect resources
- Can return to starport
- Can sell resources
- Can buy fuel

### Milestone 4: "I Can Progress"
- Can purchase upgrades
- Upgrades have meaningful impact
- Risk/reward balance feels right

## MVP Philosophy
- Get it working, not perfect
- Simple placeholder graphics
- Focus on mechanics
- Test constantly
- Document everything
- Keep scope tight

## Post-MVP Priorities
Once MVP is complete and tested:
1. Add multiple star systems
2. Implement crew system
3. Add alien encounters
4. Introduce combat
5. Expand ship systems
6. Add story elements

## Notes
- This is meant to be achievable in 6-8 weeks of part-time work
- Every feature should support the core loop
- If in doubt, cut it and add it later
- The goal is "playable" not "complete"
- We can always add more later, but we need the foundation first