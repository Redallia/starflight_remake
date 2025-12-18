# Entity Specifications
Different game entities and details about each one.


## Species
Defines a type of sentient being. Template for crew members and NPCs.
Not a spatial entity - a data structure referenced by other entities.

Contains:
- Name (e.g., "Thrynn", "Human", "Velox")
- Physical characteristics (portrait set, crew silhouette, physical scale)
- Skill modifiers (e.g., Thrynn get +10 Navigation, -5 Medicine)
* Communication style (dialogue patterns, translation difficulty baseline)
- Homeworld reference (origin system/planet)
- Default faction (for MVP: assumed faction when spawning this species)

Data Structure:
- name: string
- portrait_set: string (path or identifier)
- silhouette: string (path or identifier)
- scale: enum (small, medium, large) or float
- skill_modifiers: dict {skill_name: int modifier}
- communication_style: string (identifier referencing dialogue patterns)
- translation_difficulty: int (baseline difficulty for comms officer)
- homeworld: string (system/planet reference)
- default_faction: string (faction identifier)

## Faction
A political, organizational, or cultural entity that the player can have standing with.
Not a spatial entity - a data structure that affects encounters, access, and NPC behavior.

Contains:
- Name (e.g., "Thrynn Empire", "Tandelou Eshvey", "Tandelou Eshvara")
- Associated species (list - which species are members; often one, sometimes multiple)
- Faction portraits (optional overrides for species portraits when representing this faction)
- Player standing (hostile/unfriendly/neutral/friendly/allied, or numeric scale)
- Territory (which systems/regions they claim - list of system references)
- Relationships (attitudes toward other factions)
- Encounter behavior (how ships of this faction act - aggressive, mercantile, evasive, etc.)

Data Structure:
- name: string
- species: list[string] (species identifiers)
- portraits: dict {species_id: portrait_path} (optional overrides)
- player_standing: int or enum
- territory: list[string] (system/region references)
- relationships: dict {faction_id: stance}
- default_behavior: string (behavior pattern identifier)

## Ship Entity
A space-faring vessel capable of hyperspace and local space travel. Both player ship and alien ships share this base definition.
Contains:
Name
- Ship class/type (determines base stats, visual representation)
- Crew roster (for player ship; alien ships have implied crew)
- Faction/species affiliation
- Equipment (weapons, armor, shields, engines, special technology or artifacts)
- Coordinate location (in hyperspace or local space context)
- Cargo (minerals, lifeforms, artifacts, messages)
- Fuel level (current and maximum)
- Hull integrity (current and maximum)

Player ship is the vessel the player commands. Equipment can be upgraded at Starport. Cargo is managed via Captain → Cargo. Fuel and hull are critical resources that constrain exploration.

Alien ships are encountered in hyperspace and local space. They have faction affiliations that determine behavior (hostile, neutral, friendly). Their equipment loadout affects encounter difficulty. Defeated alien ships may drop cargo or debris.

## Crew Entity
A sentient being capable of serving aboard a starship. Both player crew and alien crew share this base definition.
Contains:
- Name
- Species (determines available skill bonuses, visual representation)
- Assigned ship role (Captain, Science Officer, Navigator, Engineer, Communications, Doctor, or none)
- Skills and training levels (Science, Navigation, Engineering, Communication, Medicine)
- Health (current and maximum)

Player crew are assigned to the player's ship and controlled via bridge commands. They're created or recruited at Starport and can be trained to improve skills.

Alien crew exist aboard alien vessels. Their skill levels affect how well their ship performs in encounters (accuracy, scan resistance, communication clarity). The player doesn't interact with them directly, but their presence is implied by ship behavior.

**Death**: When a crew member dies, their role becomes vacant. For player crew, the crew member with the next highest rating fills in until a replacement is assigned at Starport. Deceased player crew appear as a memorial at Starport.

## Celestial Entities
Bodies that exist in space, forming the structure of star systems.

### Star
The central body of a star system. Exists at two levels: as an entry point in hyperspace, and as the non-interactive center of an Inner System.
Contains:

- Name
- Spectral class (O, B, A, F, G, K, M - determines size, color, visual representation)
- Hyperspace coordinates (tile position in sector)
- System reference (links to the Local Space it contains)

**In hyperspace**: Collision with the star's boundary triggers entry into the Outer System. Visual size varies by spectral class.
**In Inner System**: The star sits at the center, non-interactive. Ships can pass through it freely. It's a visual landmark only.

### Planet
A body orbiting a star (in Inner or Outer System) or a gas giant (as a moon in a Planetary System). The primary destination for exploration.
Contains:
Name
- Planetary type (rocky, gas giant, ice giant, molten, frozen, etc.)
- Size (affects visual radius, surface grid scale if landable)
- Atmosphere (composition, density - affects surface conditions and landing feasibility)
- Surface conditions (temperature range, gravity, hazard level)
- Orbital radius (distance from parent body)
- Orbital angle (current position on orbital path, fixed for MVP)
- Moons (references to satellite bodies, if any; max 4)
- Landable (boolean - gas giants are not landable unless special conditions apply)
- Surface seed (for procedural generation of terrain, resources, life)
- Ruins/settlements (seed-based locations, if any)
**Interaction**: Collision prompts orbit entry. From orbit, the player can scan for details and land if the planet is landable.

### Moon
Functionally identical to a planet, but orbits a planet rather than a star. Exists within a Planetary System context.
Contains: Same properties as Planet, minus the Moons array (moons don't have moons, at least for MVP).
**Interaction**: Same as planets. Collision prompts orbit entry within the Planetary System context.

### Gas Giant System
Not a distinct entity, but a context created when a gas giant has moons. The gas giant itself becomes the central body (like a star in Inner System), and its moons become the orbiting bodies.
Entry: Automatic on collision with a gas giant that has moons. If a gas giant has no moons, collision prompts orbit (though landing isn't possible).

### Space Station
An artificial structure in orbit, either around a planet, moon, or at a fixed point in local space. Starport is a specific instance of this type.
Contains:
- Name
- Station type (starport, trading post, research station, alien station, etc.)
- Faction/species affiliation
- Services available (varies by type - trade, repairs, crew recruitment, fuel, missions)
- Orbital position (which body it orbits, or coordinates if free-floating)

**Interaction**: Collision prompts docking. Docking pushes a DOCKED context and presents the station interface (menu-based for MVP, potentially side-scroller later).

## Hyperspace-Only Entities
Entities that exist only at the hyperspace level.

### Nebula
A region of space with visual and mechanical effects.
Contains:
- Center coordinates (tile position)
- Radius (in tiles - can be very large)
- Color (visual effect when inside)

**Effect**: While the player ship is within the nebula's radius, shields cannot be raised. Multiple nebulae can overlap.

### Flux Point
A fast-travel node linking distant sector locations.
Contains:
- Coordinates (tile position)
- Destination (coordinates of linked flux point)
- Discovered (boolean - has the player used this before?)

**Interaction**: Collision triggers the jump. On first use, destination is unknown until arrival. Navigator skill affects post-jump orientation time.

## Surface Entities
Entities that exist on planetary surfaces, encountered during terrain vehicle exploration.
### Mineral Deposit
A collectible resource node.
Contains:
- Mineral type (determines value and rarity)
- Quantity (how much can be collected from this node)
- Coordinates (position on planetary grid)

**Interaction**: Move adjacent, open Cargo modal, pick up. Collected minerals go to terrain vehicle cargo, then transfer to ship cargo on return.

### Flora
Planetary plant life. May be collectible, may be hazardous, may be both.
Contains:
- Species (determines value, hazard type if any)
- Coordinates (position on planetary grid)
- Hazardous (boolean - does proximity risk crew injury?)

**Interaction**: If not hazardous, works like minerals. If hazardous, may injure crew on contact or proximity. Collectible regardless, but risk/reward applies.

### Fauna
Planetary animal life. Often hostile, must be subdued before collection.
Contains:
- Species (determines value, behavior, difficulty)
- Coordinates (position on planetary grid)
- Hostile (boolean - will it attack?)
- Subdued (boolean - has it been stunned?)

**Interaction**: Hostile fauna attacks the terrain vehicle or crew, risking injury. Use Weapon → Stun to subdue. Subdued fauna become collectible via Cargo modal. Some fauna may be non-hostile and directly collectible.

### Ruins
Ancient structures left by previous civilizations. Seed-based, consistent across visits.
Contains:
- Coordinates (position on planetary grid)
- Type (visual style, civilization origin)
- Contents (artifacts, messages, or nothing - determined by seed or story)
- Explored (boolean - has the player entered this ruin?)

**Interaction**: For MVP, stopping adjacent triggers an interaction (Communication-style interface or simple modal). May yield artifacts, messages, or lore. Post-MVP, could transition to side-scroller exploration mode.

### Alien Settlement
A structure belonging to a living alien civilization. Seed-based, consistent across visits.
Contains:
- Coordinates (position on planetary grid)
- Faction/species affiliation
- Settlement type (outpost, city, trading post, etc.)
- Services available (trade, information, missions)

**Interaction**: Stopping adjacent triggers interaction prompt. Entering opens communication or trade interface depending on settlement type and faction standing.

### Landed Ship
The player's ship, sitting on the surface at landing coordinates.
Contains:
- Coordinates (the landing site chosen during Captain → Land)

**Interaction**: Stopping adjacent prompts "Enter ship? Y/N". Entering returns player to ship interior. From there, Captain → Launch returns to orbit.

### Terrain Vehicle
The player's surface exploration vehicle.
Contains:
- Coordinates (current position on planetary grid)
- Fuel (current and maximum)
- Cargo (collected resources, separate from ship cargo)
- Status (operational, abandoned)

Not directly interacted with as an entity - it is the player's presence on the surface. Fuel depletion causes abandonment, triggering on-foot return to ship.

