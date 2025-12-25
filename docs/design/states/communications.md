# Communications State

## Overview
Dialogue interface for communicating with alien ships or interacting with derelict vessels. Player selects statements, questions, and postures to navigate conversations.

## State Information
- **State Name**: `communications`
- **Implementation**: (Not yet created)
- **Uses HUD**: Yes (standard 4-area HUD with modifications)
- **Status**: ❌ Not implemented

## HUD Layout

### Main View (Left, Large)
- **Alien Encounter**: Alien portrait representing the species
  - Generic species portrait initially
  - (Future) Specific character portraits
- **Derelict Ship**: Visual of the derelict vessel
- Static image during conversation

### Auxiliary View (Upper-Right)
Retains previous display from before communications started:
- Mini-map (if coming from system space)
- Ship status (if coming from hyperspace)
- Prior scan results

**Rationale**: Provides context - player can see where they are, ship status while talking.

### Control Panel (Right, Middle)
Communications menu (replaces crew bridge):

**Top-level options:**
- **Statement** → Sends posture-flavored statement to alien; they respond in Message Log
- **Question** → Opens question sub-menu
- **Posture** → Opens posture sub-menu
- **Terminate** → Ends communication, returns to prior state

**Question Sub-menu:**
Replaces top-level menu when selected:
- Themselves (ask about their species, culture, history)
- Other Beings (ask about other aliens they know)
- The Past (ask about ancient civilizations, history, ruins)
- Trade (ask about trade goods, economic info)
- General Info (ask about locations, coordinates, rumors)

Navigation: W/S to select, Enter to ask, Backspace/ESC to return to top-level.

**Posture Sub-menu:**
Replaces top-level menu when selected:
- Hostile (aggressive, threatening tone)
- Friendly (default at conversation start; cooperative, respectful)
- Obsequious (submissive, flattering, deferential)

Selection persists for duration of conversation until changed.
Navigation: W/S to select, Enter to confirm, Backspace/ESC to cancel.

### Message Log (Bottom, Full-Width)
All dialogue appears here:
- Player's statements (what you say, influenced by posture)
- Alien responses
- Conversation history scrolls up as new messages arrive
- System messages ("Connection terminated")

**Example flow:**
```
> You: "Greetings. We come in peace." [Friendly posture]
  Alien: "Welcome, travelers. What do you seek?"
> You: "Tell us about yourselves."
  Alien: "We are the Ov'al. We have journeyed far..."
```

## Conversation Mechanics

### Posture Effects
Posture affects:
- Tone of player statements
- Alien disposition changes (how they react to you)
- Unlock different dialogue branches

**Hostile**: May intimidate weaker species, anger equals, provoke attacks
**Friendly**: Builds trust, more likely to share information
**Obsequious**: May flatter some species, be seen as weak by others

### Questions
Each question category has sub-topics that expand based on:
- What the alien knows
- Their willingness to share (affected by posture, faction standing)
- Player's Communication Officer skill (better translations, more detail)

### Statements
Simple one-liner based on current posture:
- Friendly: "We wish to establish peaceful relations."
- Hostile: "Stand down or face destruction."
- Obsequious: "Your wisdom and power are renowned throughout the stars."

### Alien Responses
- Vary based on species personality, faction standing, posture
- May provide coordinates, trade offers, warnings, lore
- May terminate communication if angered
- May attack if severely provoked

## Derelict Interactions
Same interface but adapted for automated systems or ship logs:
- Statements may not work (no one to talk to)
- Questions become log queries:
  - Ship Logs (instead of "Themselves")
  - Coordinates (navigation data)
  - System Status (what happened to the ship)
  - (Future) May have limited AI responses

## Communication Officer Skill
Affects:
- Translation quality (low skill = partial garbled text, high skill = full clear translation)
- Diplomatic insight (suggestions during conversation? Future feature)
- Unlocking additional dialogue options

## Input Handling
- **W/S**: Navigate menu options
- **Space/Enter**: Select option, send statement/question
- **Backspace/ESC**: Back out of sub-menus

## State Transitions
- **To Space Navigation**: When "Terminate" is selected or alien ends communication
- **From Space Navigation**: When hailing another ship or being hailed (encounter context)

## Data Requirements
- Alien species data (portrait, dialogue trees, personality)
- Faction standing (affects alien disposition)
- Conversation state (what has been asked, current posture)
- Communication Officer skill level

## Game State Requirements
```python
{
    "communications": {
        "with": "oval_ship_alpha",  # ship ID or derelict ID
        "species": "ov'al",
        "faction": "oval_collective",
        "posture": "friendly",
        "disposition": 50,  # how they currently feel about you
        "topics_discussed": ["themselves", "other_beings"],
        "conversation_history": [
            {"speaker": "player", "text": "Greetings..."},
            {"speaker": "alien", "text": "Welcome..."}
        ]
    },
    "faction_standings": {
        "oval_collective": 35  # overall standing, may affect disposition
    }
}
```

## Dialogue Tree Structure
Needs design for how dialogue content is authored:
- JSON files per species/faction?
- Dynamic response generation based on keywords?
- Scripted conversations for story encounters?

**Example structure (TBD):**
```json
{
  "species": "ov'al",
  "topics": {
    "themselves": {
      "friendly": "We are the Ov'al. We value knowledge and exploration.",
      "hostile": "You dare question us? We owe you no explanations.",
      "obsequious": "We are honored by your interest..."
    }
  }
}
```

## Implementation Phases

### Phase 1 (Basic Interface)
- Communications HUD layout
- Menu navigation working
- Posture selection functional
- Message Log displays dialogue
- Terminate returns to space

### Phase 2 (Simple Dialogue)
- Hardcoded test conversation
- Question categories implemented
- Statement sends posture-based text
- Alien gives canned responses

### Phase 3 (Dialogue Content)
- Load dialogue from data files
- Species-specific responses
- Faction standing affects disposition
- Posture affects responses

### Phase 4 (Advanced Features)
- Communication Officer skill affects translation
- Unlock coordinates, trade offers from dialogue
- Disposition tracking (can improve/worsen during conversation)
- Consequences (attacking if too hostile, gifts if very friendly)

### Phase 5 (Derelict Support)
- Adapted interface for derelicts
- Ship log queries
- Coordinate retrieval from nav computers

## Notes
- Critical for story progression and exploration
- Should feel like actual conversation, not just clicking options
- Faction standing creates long-term consequences
- Posture adds strategy - when to flatter, when to threaten
- Translation quality (skill-based) adds progression feeling
- Consider: Voice indicators (alien "language" symbols/sounds)?
- Consider: Emotion indicators (alien portrait changes expression)?
- Consider: Reputation system (word spreads about how you treat species)?
