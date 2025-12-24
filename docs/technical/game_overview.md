# Game Overview
This game is intended to be a re-imagining of the classic computer games Starflight and Starflight 2. It will be created with an eye towards modern developments in technology and rendering.

## Tech Stack
The game will be written in Python, leveraging Pygame.

## Display & Rendering
### Display
The game screen will be 800x600, but will be dynamically adjustable by the player to any size they want.

### Framerate
The game will run at 60FPS

### Scaling strategy
**What happens if someone has a different resolution? Letterboxing? Stretching? Fixed window?**
The game window will be allowed to stretch to match monitor size.

### HUD
**How you're handling the HUD layout - are those pixel positions hardcoded or calculated from screen dimensions?**
For the HUD positions are locked, but the size of each window will be dynamically scalable, and calculated according to the playable game window.
- Main View is locked to the upper left corner
- Auxiliary View is locked to the upper right corner
- Message Log is locked to the bottom part of the screen
- Command View is locked to the right side of the screen, balanced between the Auxiliary View and the Message Log

### Asset format decisions
**PNG for sprites?**
Eventually, pixel art will be used. Art will use PNG format.

**What about the procedural stuff?**
Procedural stuff will be rendered in a similar pixelated way.

### Coordinate System
In hyperspace, the coordinate system origin will be bottom left, and will only cover quadrant 1.
In local space, the coordinate system origin will be the center of the system, and will run like standard coordinates.

On a celestial body map, the coordinate system origin will be the center of the map, designated as (0,0) with the planetary prime meridian extending vertically and the equator horizontally from that location. Coordinates will extend with respect to that centerpoint. 
- From the Prime Meridian, quadrants 1 and 4 will be East, while quadrants 2 and 3 will be west.
- From the equator, quadrants 1 and 2 will be North, while quadrants 3 and 4 will be South.

## Architecture & Patterns
Game loop structure (fixed timestep? Variable with delta time?)
State management approach - you've designed a context stack conceptually, but what's the actual implementation pattern? A state machine class? Stack of state objects?
Event/messaging system - how do components communicate? Direct calls? Event bus? Your docs talk about "commands flow up" from the Control Panel, but what does that look like in code?
Entity management - how are ships, planets, crew members tracked and updated? ECS? Simple lists? Dictionary lookups?

## Data & Persistence
File formats for static data (JSON seems implied in places, but confirm it)
Directory structure for assets and data files
Save file format and what gets serialized
How seeds are generated, stored, and used
Config file approach (settings, key bindings)

## Input Handling
Key binding definitions (hardcoded vs configurable?)
Input routing logic - how does the game decide where keypresses go based on current state/mode?
Mouse support? Your docs mention keyboard exclusively but worth being explicit

## Audio
Sound system approach
Music handling (if any)
File formats

TBD. For now, the game won't have any audio.

## Code Organization
Module/package structure
Naming conventions
Where does game logic live vs rendering vs data?

## Dependencies
Python version
Pygame version
Any other libraries (noise generation for Perlin? JSON schema validation?)

## Development & Tooling
How to run the game
How to run tests (if any)
Debug modes or cheats for testing
Logging approach