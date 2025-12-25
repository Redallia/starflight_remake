# Open Issues

## ✅ Resolved Issues
Issues that have been addressed through implementation:

### Tech Stack ✅
- **Programming language**: Python
- **Rendering library**: Pygame
- **Game loop framework**: State-based architecture implemented (see `src/core/state_manager.py`)
- **Asset management**: DataLoader class implemented (see `src/core/data_loader.py`)
- **File I/O strategy**: JSON for static data, located in `src/data/static/`

### Data Formats and Schemas ✅
- **File format**: JSON (confirmed and implemented)
- **Data locations**:
  - Static game data: `src/data/static/` (species, factions, ships, equipment, minerals, skills)
  - Star system data: `src/data/star_systems.json`
  - Menu configurations: `src/data/static/menu/`
- **Skills defined**: Science, Navigation, Engineering, Communication, Medicine (see `src/data/static/skills.json`)
- **Species data**: Starting and maximum skill values defined per species (see `src/data/static/species.json`)

### Numerical Values - Partially Resolved ✅
**Resolved:**
- ✅ Crew skill ranges: 0-250 (species-specific maximums defined in `species.json`)
- ✅ Resource values and pricing: 21 minerals defined, ranging 40-500 credits (see `src/data/static/minerals.json`)
- ✅ Upgrade costs: Equipment classes 1-5 defined with costs (engines: 1k-100k, weapons: 8k-200k, etc.)
- ✅ Ship cargo capacity: Defined per ship class (`available_cargo_bays` in `ships.json`)

**Still needed:**
- Grid sizes for Outer System, Inner System, Planetary Systems
- Fuel costs for launching from surface
- Starting ship stats (fuel capacity, starting credits)
- Fuel/power capacity and consumption units clarification
### Input Handling - Partially Resolved ✅
**Resolved:**
- ✅ Menu navigation: Keyboard-based (W/S, arrows, numpad 8/2) - implemented in InputManager
- ✅ Confirmation keys: Space and Enter for selection - implemented
- ✅ Input system: Centralized in `src/core/input_manager.py`

**Still needed:**
- Modal dialog dismissal patterns (standardize Escape/Backspace behavior)
- Complete keyboard shortcuts documentation

## Critical Gaps - Still Open

### Procedural Generation Specifics
procedural_generation.md describes approaches but not:
- Actual Perlin noise parameters (frequency, octaves, persistence)
- Color palette definitions for each terrain type
- Threshold values for continent vs. archipelago
- Mineral/flora/fauna density numbers
- How ruins/settlements are placed (rules for "seed-based, consistent" placement)

**Note**: Planet types and atmosphere types are defined in `src/data/static/planetary_info/planet_types.json`, but generation algorithms need implementation.

### Crew and Skills System - Partially Resolved
**Resolved:**
- ✅ Skill ranges: 0-250 with species-specific maximums (see `species.json`)
- ✅ Skill definitions: Effects documented in `skills.json`

**Still needed:**
- Skill effect formulas (how does Science skill 150 vs 50 affect scan quality? Linear? Thresholds? RNG modifiers?)
- Crew training mechanics (cost, time, skill gain rates)
- Injury/health mechanics (damage amounts, healing rates, max health values)
- Death consequences beyond "role becomes vacant"
- Crew member roster templates (names, starting skills, species distribution)

### Game Initialization
**Partially defined:**
- ✅ Star system exists: "Home System" with Starport, Aqua (water world), Typhon (gas giant) in `star_systems.json`
- ✅ Factions defined: Citadel (human) and Ov'al Collective with starting standings

**Still needed:**
- Starting credits amount
- Starting fuel and fuel capacity
- Starting crew roster (names, species, roles, initial skills)
- Starting equipment loadout (which engine class, weapons, shields?)
- Starting location (Starport in Home System - confirm)
- Fixed start vs. customization options
- First state player sees after "New Game" (Starport menu? Ship bridge? Intro cutscene?)

### Content Data for MVP Tutorial
**Partially defined:**
- ✅ Star system with landable planets exists
- ✅ Two factions exist for first contact scenario (Citadel, Ov'al Collective)
- ✅ Ship classes defined for player and aliens

**Still needed:**
- Derelict ship encounter specifications (location, defenses, rewards, dialogue/logs)
- Ruins location and contents (coordinates, artifacts, breadcrumbs)
- First contact scenario details (which faction? scripted dialogue? trigger conditions?)
- Starport initial inventory (which equipment classes available at start?)
- Starport pricing (base prices vs. STV modifications)
- Tutorial trigger system (how do scripted events fire?)

## Open Questions - Deferred Post-MVP

### Combat Specification
Deferred but eventually needed. The original's arcade-style combat didn't fit. You mentioned wanting something more tactical. When you're ready, this needs its own doc.

**Current state**: Weapons defined with damage values in `src/data/static/ship_equipment/weapons.json`, but combat mechanics undefined.

### Alien/Faction Specification - Partially Resolved
**Resolved:**
- ✅ Faction data structure: territories, relationships, standings defined in `factions.json`
- ✅ Species communication styles defined in `species.json`
- ✅ Inter-faction relationships and player standings defined

**Still needed:**
- Disposition calculation (how do actions affect standing?)
- Communication pattern implementation (friendly vs. neutral vs. hostile dialogue trees)
- Territory enforcement (what happens when you enter protected space?)
- Dialogue content and conversation trees

### Procedural Generation - Partially Resolved
**Resolved:**
- ✅ Seed-based planet generation framework (seeds in `star_systems.json`)
- ✅ Planet types defined (7 types in `planet_types.json`)
- ✅ Atmosphere and hydrosphere types defined

**Still needed:**
- Terrain generation algorithms (Perlin noise implementation and parameters)
- Resource distribution algorithms (mineral/flora/fauna placement)
- Color palette mapping (terrain type → visual colors)
- Ruins/settlement placement rules

### Economy & Trade - Partially Resolved
**Resolved:**
- ✅ Base mineral values defined (40-500 credits in `minerals.json`)
- ✅ Equipment costs defined (all classes 1-5 with prices)
- ✅ Rarity system for minerals (common/uncommon/rare)

**Still needed:**
- STV (Standard Trade Value) calculation and per-faction modifiers
- Starport pricing rules (markup/markdown percentages)
- Planetary trade outpost pricing
- Supply/demand mechanics (if any)
- Sell-back values (percentage of purchase price)

### Save System
What gets saved? When? How? What's the data structure?

**Needs definition:**
- Save file format (JSON recommended for consistency)
- What game state needs serialization (ship, crew, inventory, location, faction standings, discovered systems, etc.)
- Auto-save vs. manual save
- Save slots or single save file
- What doesn't need saving (can be regenerated from seeds)

### Audio/Visual Style Guide
Not code, but aesthetic direction. What does this game look like? What does it sound like?

**Current state**: Colors defined in `src/core/colors.py` for UI consistency. No sprite assets or audio yet.

**Still needed:**
- Pixel art style guide (resolution, palette constraints, animation principles)
- Sprite specifications (ship sizes, planet rendering approach, UI elements)
- Audio plan (deferred - no audio in initial MVP per game_overview.md)

### Lore
What exactly is the lore of this setting?

**Current state**:
- Two factions exist (Citadel - human, Ov'al Collective)
- Species have affinities (humans and Ov'al have -20 mutual affinity)
- Factions have relationships (Citadel and Ov'al Collective: -30 and -10)

**Still needed:**
- Backstory (why the tension between Citadel and Ov'al?)
- First contact scenario narrative
- Ancient civilization lore (for ruins, artifacts, mysteries)
- Tutorial intro story (humanity's first expedition narrative)
- Broader universe context

## Recommended Next Steps

Based on remaining gaps, prioritize:

1. **Game Constants File**: Create `src/data/static/game_constants.json` with:
   - Grid sizes (hyperspace, system space, planetary grids)
   - Starting game values (credits, fuel, capacity)
   - Fuel costs (launch, maneuver, hyperspace)
   - Power/fuel consumption units clarification

2. **New Game Configuration**: Create `src/data/static/new_game_defaults.json` with:
   - Starting ship configuration
   - Starting crew roster template
   - Starting equipment loadout
   - Starting location

3. **Tutorial Scenario Data**: Create `src/data/scenarios/intro_tutorial.json` with:
   - Scripted events and triggers
   - Derelict ship details
   - Ruins coordinates and contents
   - First contact encounter

4. **Data Schema Documentation**: Create `docs/technical/data_schemas.md` documenting:
   - All JSON file structures
   - Field definitions and valid values
   - Examples for each entity type
   - Relationships between data files