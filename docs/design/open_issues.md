# Open Issues

## Critical Gaps
### Tech Stack
Programming language: Python b
Rendering library: Pygame

Game loop framework
Asset management approach
File I/O strategy
This affects everything about implementation.

### Data Formats and Schemas
I know what entities exist (Species, Faction, Ship Class, Planet, etc.) but not:
File formats (JSON? YAML? Database?)
Exact data structure for each entity
Where configuration lives vs. runtime state
How seeds are generated/stored
Example: Species has "skill_modifiers: dict {skill_name: int modifier}" but:
What are the valid skill names? (Science, Navigation, Engineering, Communication, Medicine - from crew_roles.md, but not explicitly listed as a canonical set)
Are these +/- integers or multipliers?
Where is this data defined - hardcoded, loaded from files?
### Numerical Values
Lots of "TBD" which is fine for design, but blocks implementation:
Grid sizes for Outer System, Inner System, Planetary Systems (navigation_specification.md)
Fuel costs for launching from surface
Starting ship stats (fuel capacity, cargo capacity, credits)
Resource values and pricing
Upgrade costs
Crew skill ranges (0-100? 0-250 like original?)
### Procedural Generation Specifics
procedural_generation.md describes approaches but not:
Actual Perlin noise parameters (frequency, octaves, persistence)
Color palette definitions for each terrain type
Threshold values for continent vs. archipelago
Mineral/flora/fauna density numbers
How ruins/settlements are placed (rules for "seed-based, consistent" placement)
### Input Handling
You mention WASD/arrows for movement, but not:
How menu navigation works (arrow keys? Mouse? Both?)
Confirmation keys (Space for orbit entry, Y/N for prompts - but what about menu selection?)
How modal dialogs are dismissed
Keyboard shortcuts vs. menu-only actions
### Crew and Skills System
From crew_roles.md I know roles and responsibilities, but not:
Skill ranges and how they affect outcomes (e.g., "Science Officer skill affects scan quality" - but how? Linear? Thresholds? RNG modifiers?)
How crew training works mechanically
Injury/health mechanics (damage amounts, healing rates)
Death consequences beyond "role becomes vacant"
### Game Initialization
Missing:
What does "New Game" actually create? (starting location, ship configuration, crew roster, credits)
Is there ship/crew customization or fixed starting conditions?
What's the actual first state the player sees?
### Content Data
For even the MVP tutorial, you'd need:
At least one star system defined (planet types, positions, resources)
The derelict ship encounter specifications
The ruins location and what's inside
The first contact alien species/faction
Starport initial inventory/prices

## Open Questions
### Combat Specification
You've deferred this, but eventually you'll need it. The original's arcade-style combat didn't fit. You mentioned wanting something more tactical. When you're ready, this needs its own doc.

### Alien/Faction Specification
How do aliens work? Disposition, diplomacy, communication patterns, territory. For MVP you just need one alien for first contact, but the system needs thinking through.

### Procedural Generation
How are planets generated? Terrain, resources, life forms, ruins placement. The seeds, the algorithms, the distribution rules.

### Economy & Trade
Credits, pricing, what's valuable, how Starport trade works, how STV modifies prices. Deferred but will need documenting.

### Save System
What gets saved? When? How? What's the data structure?

### Audio/Visual Style Guide
Not code, but aesthetic direction. What does this game look like? What does it sound like?

### Lore
What exactly is the lore of this setting? Alien/Faction specifications matter for how systems get implemented, but what's the story?