# Game Design Ideas

## Overview
Drawing inspiration Dwarf Fortress, this document aims to capture short scenes, moments, or vignettes that I want to see happen in the course of playing the game. 
A sort of Story Driven Development, where these short story snippets are what drives the development of in-game systems.

Additionally, I want to capture a sort of wishlist of game elements that I want to see implemented as the game is developed.

**What this isn't**
This is not intended to be an development bible.
This is just a collection of ideas, what ifs, and idle daydreaming for what this project might strive for.
A lot of these ideas feel achievable, but technical or practical limitations might prevent seeing them realized. 

## Design Intent
### Two game modes
I would love for there to be two game modes operating at the same time: 
    - story-mode, with hard coded mysteries and storylines
    - sandbox-mode, with emergent storytelling

The starting "Starport" equivalent for this game would act as a nexus point, giving the player access to different sectors from some central location, and thus allowing both modes to operate side-by-side.

In-game explanations can be provided as for why advanced techology can't transfer between sectors: 
    "Nexus travel using anything other than basic equipment has proven to be impossible"

This would prevent the tendency towards power-creep and provide an incentive for players to want to explore and gather resources.

### Expanded Crew Interactions
The player's crew in the original game had no opportunities to perform actions beyond ship functions.
For this remake, I would be looking for chances for specific crew members to contribute beyond their role on the ship.

**Navigators**
Navigators could provide in-game hints and knowledge about learned constellations or named planets by identifying/labelling them on the sector map.

**Engineers**
Aliens in distress could send out calls for help. On arrival, the engineer crew member could enter their ship and assist with/coordinate repairs.

Planetary ruins might have opportunities for well-trained engineers to unlock otherwise unavailable messages, secrets, or artifacts.

**Communications**
Beyond simply translating or ship-to-ship interactions, Communications could be expanded into diplomacy or cultural understanding, offering stance suggestions or communication insights to the player during alien interactions.

Planetary ruins might have texts that would become decipherable to well-trained communications officers. 

**Doctors**
A distress call from another starship could request medical assistance. A well-trained doctor could faciliate that assistance.

## Wishlist

### Expanded Skill Systems
The original games had a list of 5 skills:
- Science
- Navigation
- Engineering
- Communication
- Medicine

Each skill would range from 0 to 250 (with training). 
- High Science skill gave better planet scan information vs low Science which left the user with a bunch of unknowns, even after the scan. 
- High Communication allowed full translations of alien languages, as opposed to low Communication leaving most of the text untranslated. 
- High Navigation gave better accuracy when firing weapons, or was faster to resolve hyperspace coordinates after going through a flux jump, while low Navigation was less accurate when firing and slower to orient after a jump.
- High Enginnering would let ship repairs happen quicker
- High Medicine would heal crew members faster

It would be fascinating if Starport could raise crew skill up to some baseline cap - 150 or 200, maybe - while other facilities could be uncovered to let crew members exceed that cap, with the top-tier cap unlocking new abilities or capabilities.

Another facet might be the expansion of Skills into specialties, allowing crew members to unlock new "Classes"

Maybe 1-100 is a normal skill range, 101-200 gives access to specialized tricks or abilities, and 200-250 unlocks Skill "specialities", with crew members only being able to specialize in one skill. This would encourage a diversity of skills and crew members.

**Training and Factions**
You could pair the expanded Skill training with Faction rating, with a high enough faction rating allowing the player access to specialized facilities where a crew member could become a specialist.

**Complementary Specializations**
Complementary specializations could unlock combo abilities. For example: Navigator + Diplomat might “Stellar Envoy” missions, where you chart trade routes and negotiate treaties.

### Star Systems
**Inner/Outer orbits**
Star systems differentiate between outer and inner planetary orbits. The player could enter a star system, and see the outer planets in orbit, while the inner planets would act like a separate enterable system.
This could provide a further sense of depth and distance and increase the sense of space players felt.

**Gas Giants**
Gas giants themselves could act as their own enterable system. The gas giant would take the place of the star, while its moons would be the giant's "planets". Any planet with a moon could be handled in this way.

Gas giants, normally not landable, could provide unique signal events and provide distinct "landable" locations. These could take the form of orbiting platforms, derelict ships, or other locations that show up as specific coordinates, allowing player to select targeted points where they can "land/dock" on an otherwise inhospitable planet.

### New locations
The original games had a small number of special story-related locations. 
Starflight seemed to only have had planet-based locations. 
Starflight 2 included unique ship-based encounters like Gorzek, the abandoned Leghk ship, and the Uhl. 
Both games had a just a single space station that the player count interact with: Starport.

For my remake, I'd like to expand the number of locations as well as more varied opportunities for interacting with them.
The trade-off is that with more locations like this, there's less telegraphing to the player this "THIS IS IMPORTANT! PAY ATTENTION!". 
This might necessitate making story-relevant locations or events more obvious.

**Location-based Scenarios**
Different locations could provide miniature scenarios requiring different crew member skills to accomplish and/or fully explore.

    - Derelict ships could require scanning (Science Officer), repairs (Engineer), translation of logs (Navigator, Communications), forensics (Doctor).
    - Ruins could require in-orbit locating and scanning (Science Officer), gaining access (Engineer), translation services

Locations could utilize an expanded side-scroller game interface, allowing player to play in a simple "away team" game loop.

Location-based scenarios would also help to break up the repetitive gameplay loops present in the regular game, and provide a more varied and improved visual experience.

### Planets
**Weather Systems**
While the original games had simulated weather, the weather was planetary in scale with no visual effects. It would be fascinating to aim for ongoing, Perlin-noise generated weather effects for different simulated environment types. Hurricanes or storm fronts for temperate Earth-like planets, to Mars-like planet-wide sandstorms, to simulations of Jupiter-like red spots and similar. Weather might then depend on the local effects of high-level simulation, procedurally derived from whatever the weather layer of the Perlin was.

Might be necessary to leverage a GPU to handle all that high-level rendering though, which would take the game significantly outside the scope of what the original games were able to provide. However, the immersive quality might be worth it.

**Moons and Craters**
I want to look into how to generate craters and similar effects during planet surface generation. A celestial body without an atmosphere should be pock-marked by craters to sell the effect, rather than simply rendering like any other planet.

### Including modern gameplay loops
#### Colony building
In the original games, the player could find and recommend habitable planets for colonization. But beyond simply logging them and receiving a monetary reward, these had no other effect on gameplay, and were utilized as quick way to accumulate credits for ship improvement.

In the new game, as the player finds and recommends planets for colonization, these recommendations could be the source for further gameplay in the form of:
    - finding good colonization sites on the recommended planet
    - escorting colony ships to the site
    - providing colony resources and materials through trade
    - giving players investment opportunities and returns in the form of making resources available, providing a return on invested credits
    - colony growth could be directed by the player. Specialized buildings, unique structures
    - colonies could require defending, whether from native creatures, raiding bandits, or invading aliens

This obviously represents a radical departure from the original game designs, which were focused on exploration, mystery uncovering, and storytelling. As such, this sort of interaction would be more appropriate for a sandbox-mode sector, rather than a story focused one.

#### Sidescroller game
The original Starflight games had simple interfaces that allowed the player to walk around as a character, instead of flying around in a starship. 
The only place this sort of interaction showed up was in the Starport area.
I would love to see that system expanded into something more.
Explorable ruins, explorable space stations or derelict starships. More and varied options for interacting with the game world.
Locations might have events or interactable objects that might require crews to coordinate efforts:
    - Science Officers could scan environments
    - Engineers could repair broken equipment
    - Communicaton Officers could translate ancient or alien languages. 
    - Navigators could interpret location coordinates
    - Doctors could interact with injured individuals in locations, or handle interactions with other living beings/creatures

The aim would be to give the player more options for interaction that felt interesting, and provide more usefulness for crew members beyond their ship roles. Doctors and Engineers especially felt almost superfluous in the original game outside of specific conditions.

#### The Race 
In the original games, the player was the only character that was going around surveying planets. Aside from discovering habitable worlds and uncovering more of the mystery that was dropped as breadcrumbs, there was little reason to visit every planet.

In The Race, the player starts in a fresh, unexplored sector. Player should be able to decide how many other "racers" they're competing against. The **Player's Organization** then tasks all racers to conduct a full survey of the sector.  

All star systems, all planets, moons, celestial bodies are counted. **Flux jumps** might not be considered as necessary for a full survey, but each flux found could be added to a player's point count. The same flux could count multiple times, but only once per player.

Each body is scored, individually, with bonuses for fully surveyed systems. Systems with more bodies are worth more in terms of body count, and in terms of system value.

A "winner" is declared when all systems and other celestial phenomenon have been surveyed, the "players" return back to **Starport**, and the final totals are tallied.

Different AI algorithms can be developed with different survey styles. If this is opened to the public, PvP surveying could be done, including the capacity for PvP ship engagement, though this should act as a reset rather than a full ship destruction.

### Factions
Introducing a faction system to the game would allow for meaningful player choice, leading to changes in alien interactions, and differentiation between internal factions within a given species, culture, or civilization.

Imagine the player encountering a pre-space flight civilization caught up in a Cold War scenario. The player taking sides in a given conflict would lead to one faction or another gaining dominance and ultimately becoming the player's point of contact for that civilization going forward.

Additionally, with a faction system, we can include the ability to secretly improve/worsen relations with hidden groups based on other trigger-based actions or behaviors.

## Stories
Each story is intended to act as the sort of event that could come about as the result of emergent gameplay. 
The idea is not to code specific stories into the game, but to allow certain stories to happen naturally as the result of game systems interacting.
Obviously, this is something that goes well beyond the intent and purpose of the original games, which had hard coded storylines and mysteries that the player would uncover.

**TO BE POPULATED AS THE STORIES COME TO ME**

### Crew is captured
The crew is captured and their ship is taken. They are abandoned on a planet near an outpost. The player must make it to the outpost, repair it, discovering a servicable terrain vehicle and starship. They must explore the local environment to find materials so the ship can be repaired, allowing them to leave the planet. While in orbit, their new ship's sensors pick up a signal from their old ship, giving them an opportunity to re-take over their original ship, and bring their captors to justice.

### Early Game/First load
Player is treated to some degree of pomp and circumstance as they launch for the first time. It's humanity's first foray out into the wider universe and player is at the helm.
Player is allowed freedom to explore the planets of the inner system, scanning, landing, etc. Planets here will be rocky and introduction-friendly.
Player will have a chance to use the different interfaces for the first time: science, navigation, communication, etc. 
A scripted event will injure one of the crew members, necessitating said crew member to visit the doctor.
A separate event might introduce them to the side-scroller game interface, as well as other interface types.

At some point, player will hit the outer boundary of the inner system and enter the outer system. Planets here will be gas giants. 
This is where they'll learn how to navigate into and out of different systems, whether inner orbits or gas giant systems. 

Eventually player will push past the outer system boundary and enter interstellar space.
Here they'll learn about flying between star systems, using the star map.
This is also where they'll have humanity's "first contact" event, and set the stage/premise for the game.

At this point, the "tutorial" will be over, and the player will be treated to a chance to customize their crew, their ship, and have a chance to experience the actual game.

### "Captain, they're lying"
The crew is engaging with a disabled Olphine frigate who sent out a distress signal. The Olphine is an alien species with a reputation for criminal activity, but your mission is to assist. They've just invited you over to their ship so you can assist with repairs, but your communications officer who's trained in alien relations surreptitiously informs you that they're lying, and that there's a good chance they're planning on hijacking your own vessel.

### Xilqik First Contact
The first meeting with the Xilqik ship is just a flash on the screen of the Xilqik portrait, following by quickly cutting off communications and an announcement from the crew that the ship has armed its weapons, but haven't raised its shields. The Xilqik are trying to figure out how to work the ship, but are inviting disaster through their ignorance.

The player is free to respond however they might, and it might end with the destruction of the ship. The player wouldn't be blamed for the outcome, since watching a ship arm its weapons is easily interpreted as a hostile act. The baseline case would assume that the player would destroy the ship (tragic, but neutral as far as the Xilqik are concerned), and the best case would be patience and seeing how the situation plays itself out 

For the good case, the player is transmitted the hyperspace coordinates of the Xilqik home system, and landing coordinates for something to progress their story. For the case of ship destruction, the player is sent a transmission of just the planetary coordinates. They'd have to find out about the Xilqik home world from the Yanooth, who don't view the Xilqik as important.

### Life Finds a Way

The player hears about a gas giant in Ov'al space that, somehow, is teeming with life. They go to investigate and find the rumor to be true, but their ship is incapable of getting close.

The player reports back about the gas giant and the unique life. A science mission is offered to go and study the life. The player is allowed to outfit their ship with special engines (Class 1 equivalent),shields designed to work in the atmosphere of a gas giant, and specially designed cargo pods for carrying these unique life forms.

Having these installed, the player is allowed to "land" on a gas giant. Instead of the terrain vehicle, the players ship is the navigable object, and fuel costs come out of the player's ship's fuel supply (so long missions are discouraged).

The terrain behaves identically, and specialty life forms are allowed to be captured. The rewards for returning with these life forms should be enough to offset the cost of fuel plus profit. Science faction standing is also increased to some set maximum.