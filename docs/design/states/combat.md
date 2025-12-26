# Combat State

## Overview
Ship-to-ship combat. Deferred post-MVP - mechanics undefined.

## State Information
- **State Name**: `combat` (tentative)
- **Implementation**: (Not yet created)
- **Uses HUD**: TBD
- **Status**: ❌ Not implemented, not designed

## Design Notes

### From Original Games
The original Starflight had arcade-style real-time combat:
- Top-down view of all ships, player and alien
- Player fires weapons, automatically targeting the closest ship
- Dodge incoming fire, usually in the form of missiles
- Combat is largely an exercise in circling around enemy ships while occasionally pausing movement to fire weapons

**Problems**: 
- Didn't fit the exploration/strategy focus of the game.
- Combat was never particularly engaging or exciting

### Desired Direction
More tactical, less twitch-based. Possible approaches:

**Turn-based tactical:**
- XCOM-style positioning and actions
- Crew skills directly affect outcomes
- Time to think and plan
- Fits better with crew skill system

**Real-time with pause:**
- FTL-style
- Pause to issue orders, assign crew, target systems
- Unpause to execute
- Balances urgency with strategy

**Encounter-based (minimal direct control):**
- Choices during encounter ("Attack engines", "Hail", "Flee")
- Crew skills and equipment determine outcomes
- More narrative/choice-driven than mechanical
- Fastest to implement

### Crew Integration
Combat should leverage crew skills:
- **Navigator**: Weapon accuracy, evasive maneuvers
- **Engineer**: Damage repair during combat, system efficiency
    - Want to have "Scotty, more power to the shields!" moments
- **Science Officer**: Target analysis, weak point identification
- **Captain**: Combat tactics, crew coordination bonuses
- **Doctor**: Crew injury treatment during/after combat

### Equipment Integration
Ship equipment should matter:
- **Weapons**: Damage output, range, energy cost
- **Shields**: Damage absorption, recharge rate
- **Armor**: Damage reduction
- **Engines**: Evasion chance, flee success rate

## What Needs Definition

1. **Core Mechanic**: Turn-based, real-time-with-pause, or encounter-based?
2. **Win/Loss Conditions**: Ship destruction? Disable? Surrender?
3. **Damage System**: Hull HP only? Individual system damage?
4. **Targeting**: Specific ship systems or whole ship?
5. **Fleeing**: Always possible? Skill check? Equipment dependent?
6. **Consequences**: Ship damage persistence? Crew injuries? Cargo loss?
7. **Balance**: How to keep combat challenging but not overwhelming?

## Integration Points

### Entry
Combat is triggered by:
- Hostile encounter in SpaceNavigationState
- Protected planet defenders
- Attacking a peaceful ship (player-initiated)

### During Combat
- Access to crew functions (repair, heal, etc.)
- May transition to CommunicationsState mid-combat (surrender, negotiate)

### Exit
Combat ends when:
- One ship is destroyed
- One ship flees successfully
- Surrender/negotiation accepted
- Returns to SpaceNavigationState (or explosion/game over if player loses)

## Implementation Priority
**Post-MVP**. Get exploration, resource gathering, and dialogue working first. Combat can be added later as a complete system.

## Notes
- Don't rush this - bad combat is worse than no combat
- Prototype different approaches before committing
- Playtest heavily - balance is crucial
- Consider making combat avoidable for peaceful playstyle
- Should feel tense but not frustrating
- Crew injuries/death should have weight
