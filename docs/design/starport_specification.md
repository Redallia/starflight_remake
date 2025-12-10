# Starport Specification

## Overview

Starport is the player's home base and operational hub. It's where the player prepares for expeditions, manages their crew and ship, receives mission communications, and handles trade.

Starport uses a **full-screen interface** separate from the four-area HUD used during space navigation and planetary exploration.

## MVP Implementation

For the MVP/introductory scenario, Starport is a **simple text menu interface**. Most functions are locked during the tutorial, with only essential options available.

### MVP Menu Structure

```
STARPORT
---------
> Launch
  Ship
  Messages
  Trade (locked)
  Crew (locked)
  Exit
```

**Launch**
- Transitions game state from STARPORT to IN_SYSTEM_SPACE
- Player's ship departs Starport and enters the local star system
- During intro: accompanied by narrative fanfare ("Humanity's first voyage...")

**Ship**
- Opens Ship modal (see below)
- View ship status and installed equipment
- Purchase and install new equipment
- MVP requirement: player must be able to buy mining laser here

**Messages**
- Opens Messages modal (see below)
- View official communications from Starport command
- Used for mission prompts and story beats during intro
- Example: "Survey the inner system" → "Investigate anomaly in outer system" → "Artifact analysis complete - hyperspace tech unlocked"

**Trade** (Locked for MVP)
- Will handle buying/selling cargo, fuel purchases
- Can display "Not available during training mission" or simply be grayed out
- If fuel management is needed for MVP, minimal implementation: just fuel purchase

**Crew** (Locked for MVP)
- Will handle crew creation, training, role assignment
- Display "Not available during training mission"
- Player uses pre-assigned default crew for intro

**Exit**
- Return to main menu
- Prompt to save game (if save system implemented)

### MVP Modals

#### Ship Modal

Displays ship information and equipment management.

```
SHIP STATUS
-----------
Hull: 100/100
Fuel: 100/100
Cargo: 0/50

EQUIPMENT
---------
Engines: Class 1
Shields: Class 1
Armor: Class 1
Weapons: None

AVAILABLE FOR PURCHASE
----------------------
> Mining Laser - 500 credits
  [additional equipment post-MVP]

[Back]
```

**MVP functionality:**
- Display current ship stats
- Display installed equipment
- List available equipment for purchase
- Purchase and install equipment (mining laser for intro scenario)
- Player starts with enough credits to afford mining laser when needed

#### Messages Modal

Displays received communications.

```
MESSAGES
--------
> [NEW] Mission Update - Stardate 2450.3
  Welcome Aboard - Stardate 2450.1

-----------------------------------
[Selected message content appears here]

[Back]
```

**MVP functionality:**
- Scrollable list of messages
- New/unread indicator
- Select message to view full content
- Messages drive tutorial progression and story beats

### Input Handling (MVP)

- W/S or Up/Down: Navigate menu options
- Space/Enter: Select option / confirm
- Escape: Back out of modals, return to menu
- Standard menu navigation, nothing complex

## Future Implementation: Side-Scroller Mode

Post-MVP, Starport will be reimplemented as a **side-scroller exploration interface**. The player controls a character who walks around the station, entering different areas through doors.

### Side-Scroller Concept

**Main View:** Side-view of Starport interior with player character
**Navigation:** WASD or arrow keys to walk left/right
**Interaction:** Spacebar to enter doors / interact with objects

**Station Areas (doors):**
- **Command Center:** Messages, mission briefings
- **Personnel Office:** Crew recruitment, training, role assignment
- **Shipyard:** Ship status, repairs, equipment installation
- **Trade Depot:** Buy/sell cargo, fuel, supplies
- **Bank/Finance:** Review transactions, account balance
- **Launch Bay:** Board ship and launch

### Why Side-Scroller?

The original Starflight games used this format, providing:
- Sense of place and physicality to the station
- Visual break from menu-heavy interfaces
- Opportunity for ambient storytelling (NPCs, environment details)
- Foundation for similar interfaces elsewhere (ruins, derelicts, alien stations)

### Shared Interface Pattern

The side-scroller mode established at Starport can be reused for:
- **Planetary ruins:** Walk through ancient structures, find artifacts
- **Derelict ships:** Explore abandoned vessels (future expansion of MVP's communication-based interaction)
- **Alien stations:** Diplomatic visits, trade negotiations
- **Other locations:** As the game expands

This creates a consistent "explorable location" interface distinct from both the space HUD and the planetary surface view.

### Design Considerations (Future)

- How much detail in the side-scroller? Simple pixel art? More elaborate?
- Are there NPCs to talk to? Or just doors to functional interfaces?
- Can events happen in Starport? (Attacked, emergency messages, etc.)
- How does this interface support the "two modes" design (story sectors vs sandbox)?
- Should crew members be visible in Starport? Walk with you?

These questions are deferred until after MVP is complete and the core game loop is proven.

## Game State

**State: STARPORT**
- Does not use the four-area HUD
- Full-screen interface (menu for MVP, side-scroller later)
- Transitions from: Landing at Starport (returning from expedition)
- Transitions to: IN_SYSTEM_SPACE (launching), MAIN_MENU (exit)

## Open Questions

1. **Fuel management in MVP:** Is fuel a constraint during the intro, or do we give the player plenty and defer the economy?

2. **Credits/economy in MVP:** Player needs credits to buy mining laser. Do they start with enough? Earn some from early scanning/surveying? Or is the mining laser just "unlocked" narratively without purchase?

3. **Save system:** Does Exit prompt for save? Is saving automatic? Deferred question.

4. **Side-scroller scope:** How elaborate should the future implementation be? This affects art requirements significantly.

5. **Starport location:** Is Starport always in the same system? Can there be multiple Starports (in different sectors)? How does this interact with the "nexus" concept from the design ideas doc?