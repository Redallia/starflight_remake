# Starport State

## Overview
Hub location where players manage their ship, crew, and resources. Acts as the home base for the player's faction (initially Citadel).

## State Information
- **State Name**: `starport`
- **Implementation**: `src/states/starport_menu_state.py`
- **Uses HUD**: No (full-screen hub interface)
- **Status**: ✅ Basic menu implemented, will evolve

## Visual Layout
Currently implemented as a simple menu. Future versions will use side-scroller exploration mode.

**Current (MVP):**
```
┌─────────────────────────────────────┐
│      STARPORT - CITADEL             │
│                                     │
│         > Launch                    │
│           Exit to Main Menu         │
│                                     │
└─────────────────────────────────────┘
```

**Future:**
Side-scroller interface with different rooms/stations to visit.

## Available Actions (Designed)
Using the original games as a basis, Starport is where the player can access:

### Operations
- Get and review messages from The Citadel
- Mission briefings, news, updates
- (Future) Quest/story triggers

### Bank
- Review current finances
- View transaction history
- (Future) Manage investments, colony funding

### Personnel
- Create new crew members
- Train crew in skills
- Delete crew members
- View crew stats and history

### Crew Assignment
- Assign crew members to ship roles (Captain, Navigator, Science Officer, Engineer, Communications, Doctor)
- View role requirements
- Manage crew rotation

### Trade Depot
- Buy/sell minerals
- Buy/sell discovered artifacts
- View market prices (affected by STV - Standard Trade Value)
- Cargo management

### Ship Configuration
- Outfit ship with equipment (engines, weapons, shields, armor)
- Repair ship damage (requires repair materials)
- Sell ship equipment
- Rename ship
- (Future) Purchase different ship classes

### Docking Bay
- Launch to space (transitions to SpaceNavigationState)
- View ship status before launch
- Final check before departure

## Input Handling (Current MVP)
- **W/S, Up/Down**: Navigate menu
- **Space/Enter**: Select option
- **ESC**: Return to previous menu/state

## State Transitions
- **To Main Menu**: Via "Exit to Main Menu" option
- **To Space Navigation**: Via "Launch" option (or future Docking Bay)
- **From Main Menu**: When "New Game" is selected
- **From Space Navigation**: When docking at Starport

## Data Requirements
- Menu configuration: `src/data/static/menu/starport_menu.json`
- (Future) Shop inventory and pricing data
- (Future) Available crew roster templates
- (Future) Faction messages and mission data

## Game State Requirements
Requires active game state with:
- Ship information (class, equipment, damage status)
- Crew roster (names, species, skills, assignments)
- Credits (player currency)
- Current system location
- Cargo inventory (minerals, artifacts, cargo used/capacity)

## Implementation Phases

### Phase 1 (Current - MVP)
Simple menu with:
- Launch (to space)
- Exit to Main Menu

### Phase 2 (Economy)
Add:
- Trade Depot (buy/sell minerals)
- Bank (view credits, transaction log)
- Ship Configuration (buy equipment, repairs)

### Phase 3 (Crew Management)
Add:
- Personnel (create/train crew)
- Crew Assignment (assign to roles)
- Operations (messages, missions)

### Phase 4 (Visual Enhancement)
Convert to side-scroller exploration mode with distinct areas.

## Notes
- Player always starts here after "New Game"
- Acts as safe haven - no threats, no time pressure
- All major ship/crew management happens here
- Represents player's faction (Citadel for humans)
- Future: Multiple starports in different systems with different inventories, factions
- Future: Starport visual style could indicate faction (Citadel vs Ov'al Collective different aesthetics)