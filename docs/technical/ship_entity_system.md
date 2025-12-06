# Ship Entity System - Architecture Design

## Overview

Ships are mobile entities in the game world. Unlike celestial bodies which are fixed in space, ships move, consume resources, and can be controlled by the player or AI.

## Current State Issues

### GameState is Bloated with Ship Data

Currently, GameState manages ship properties directly:

```python
class GameState:
    # Ship resources (should be in Ship entity)
    self.fuel = 100.0
    self.max_fuel = 100.0
    self.credits = 1000
    self.cargo_capacity = 50
    self.cargo_used = 0
    self.cargo = {}

    # Ship position (should be in Ship entity)
    self.ship_x = 0
    self.ship_y = 0
```

**Problems:**
- Ship data mixed with game session data
- Hard to add NPC ships, alien ships, or multiple ships
- Can't easily swap player ship or capture alien vessels
- No concept of ship types/classes with different capabilities

## Proposed Architecture

### Entity Hierarchy

```
entities/
├── ship.py                 # Ship entity classes
│   ├── Ship               # Base ship class (player and NPC)
│   ├── PlayerShip         # Player-controlled ship
│   ├── ShipStats          # Ship capabilities dataclass
│   ├── ShipClass          # Ship design enum
│   └── Species            # Ship builder/operator enum
```

### Core Components

#### 1. Ship Enums

```python
class ShipClass(Enum):
    """Ship classification/design"""
    TERRAN_SCOUT = "terran_scout"          # Human scout (player default)
    TERRAN_FREIGHTER = "terran_freighter"  # High cargo, slow
    TERRAN_WARSHIP = "terran_warship"      # Combat focused
    # Future: Alien ship types
    VELOXI_JAVELIN = "veloxi_javelin"      # Fast attack craft
    THRYNN_DESTROYER = "thrynn_destroyer"  # Heavy warship
    SPEMIN_SLAVER = "spemin_slaver"        # Slave hauler
    # etc.

class Species(Enum):
    """Species that build/operate ships"""
    HUMAN = "human"
    STARPORT = "starport"  # Special case for stations
    # Future aliens
    VELOXI = "veloxi"
    THRYNN = "thrynn"
    G_NOK = "g_nok"
    SPEMIN = "spemin"
    # etc.
```

#### 2. ShipStats Dataclass

```python
@dataclass
class ShipStats:
    """Ship capabilities and specifications"""
    max_fuel: float = 100.0
    max_cargo: int = 50
    max_crew: int = 6
    max_armor: int = 100
    max_shields: int = 0
    weapon_slots: int = 0
    engine_power: float = 1.0  # Movement speed multiplier
```

**Benefits:**
- Different ship classes have different strengths
- Easy to balance gameplay (freighter = high cargo, warship = high weapons)
- Clear ship progression path

#### 3. Base Ship Class

```python
@dataclass
class Ship(ABC):
    """Base class for all ships (player and NPC)"""
    name: str
    ship_class: ShipClass
    species: Species
    stats: ShipStats

    # Current state
    fuel: float = 100.0
    cargo_used: int = 0
    armor: int = 100
    shields: int = 0

    # Position (movement grid coordinates)
    x: float = 0.0
    y: float = 0.0

    # Cargo holds
    cargo: dict = field(default_factory=dict)

    def can_move(self) -> bool:
        """Check if ship has fuel"""
        return self.fuel > 0

    def get_cargo_free_space(self) -> int:
        """Get remaining cargo capacity"""
        return self.stats.max_cargo - self.cargo_used

    def add_cargo(self, resource: str, quantity: int) -> bool:
        """Add cargo (returns False if insufficient space)"""
        pass

    def consume_fuel(self, amount: float) -> bool:
        """Consume fuel (returns False if insufficient)"""
        pass

    def get_position(self) -> tuple[float, float]:
        """Get ship position"""
        return (self.x, self.y)

    def set_position(self, x: float, y: float):
        """Set ship position"""
        self.x = x
        self.y = y
```

#### 4. PlayerShip Class

```python
@dataclass
class PlayerShip(Ship):
    """Player-controlled ship with additional game state"""
    credits: int = 1000

    def can_afford(self, cost: int) -> bool:
        """Check if player can afford purchase"""
        return self.credits >= cost

    def spend_credits(self, amount: int) -> bool:
        """Spend credits (returns False if insufficient)"""
        pass

    def earn_credits(self, amount: int):
        """Add credits"""
        self.credits += amount
```

**Player-specific features:**
- Credits (money)
- Future: Quest flags, faction reputation, installed upgrades

#### 5. Factory Functions

```python
def create_terran_scout(name: str = "Starflight") -> PlayerShip:
    """Create default Terran scout ship"""
    stats = ShipStats(
        max_fuel=100.0,
        max_cargo=50,
        max_crew=6,
        max_armor=100,
        weapon_slots=2,
        engine_power=1.0
    )
    return PlayerShip(name, ShipClass.TERRAN_SCOUT, Species.HUMAN, stats)

def create_terran_freighter(name: str = "Hauler") -> Ship:
    """Create Terran freighter (high cargo, slow)"""
    stats = ShipStats(
        max_fuel=120.0,
        max_cargo=200,  # Much more cargo
        max_crew=4,
        weapon_slots=1,
        engine_power=0.7  # Slower
    )
    return Ship(name, ShipClass.TERRAN_FREIGHTER, Species.HUMAN, stats)

def create_veloxi_javelin(name: str = "Hunter") -> Ship:
    """Create Veloxi javelin (fast attack craft)"""
    stats = ShipStats(
        max_fuel=80.0,
        max_cargo=20,
        max_crew=3,
        max_armor=60,
        max_shields=50,
        weapon_slots=3,
        engine_power=1.5  # Very fast
    )
    return Ship(name, ShipClass.VELOXI_JAVELIN, Species.VELOXI, stats)
```

## GameState Refactoring

### Before (Current)

```python
class GameState:
    # Ship state scattered throughout
    self.fuel = 100.0
    self.max_fuel = 100.0
    self.credits = 1000
    self.cargo_capacity = 50
    self.cargo_used = 0
    self.cargo = {}
    self.ship_x = 0
    self.ship_y = 0
```

### After (Clean)

```python
class GameState:
    # Player ship (single entity)
    self.player_ship: PlayerShip

    # Location context
    self.location: str  # "starport", "space", "orbit", "surface"
    self.current_star_system: StarSystem
    self.orbiting_planet: Optional[Planet] = None

    # Discovery/progress
    self.scanned_planets: dict
    self.crew_roster: CrewRoster
```

**Benefits:**
- Ship data encapsulated in Ship entity
- GameState focuses on session state and context
- Easy to query ship: `game_state.player_ship.fuel`
- Ship methods handle their own logic: `player_ship.consume_fuel(10)`

## Use Cases

### 1. Ship Switching / Capturing

```python
# Player captures alien ship
captured_ship = create_veloxi_javelin("Captured Prize")
captured_ship.set_position(game_state.player_ship.x, game_state.player_ship.y)

# Transfer cargo
for resource, qty in game_state.player_ship.cargo.items():
    captured_ship.add_cargo(resource, qty)

# Switch to new ship
old_ship = game_state.player_ship
game_state.player_ship = PlayerShip.from_ship(captured_ship)
# Old ship could be sold, abandoned, or kept in reserve
```

### 2. NPC Ships in System

```python
class StarSystem:
    bodies: list[CelestialBody]
    ships: list[Ship]  # NPC ships in system

    def get_ships_near(self, x: int, y: int, radius: int) -> list[Ship]:
        """Get ships within radius of coordinates"""
        nearby = []
        for ship in self.ships:
            dx = abs(ship.x - x)
            dy = abs(ship.y - y)
            if (dx**2 + dy**2) ** 0.5 <= radius:
                nearby.append(ship)
        return nearby
```

### 3. Ship Upgrades / Progression

```python
def upgrade_cargo_hold(player_ship: PlayerShip, cost: int) -> bool:
    """Upgrade ship cargo capacity"""
    if not player_ship.can_afford(cost):
        return False

    player_ship.spend_credits(cost)
    player_ship.stats.max_cargo += 25
    return True

def install_shield_generator(player_ship: PlayerShip, cost: int) -> bool:
    """Install shields on ship"""
    if not player_ship.can_afford(cost):
        return False

    player_ship.spend_credits(cost)
    player_ship.stats.max_shields = 100
    player_ship.shields = 100
    return True
```

### 4. Ship Combat

```python
def attack_ship(attacker: Ship, target: Ship, damage: int):
    """Ship attacks another ship"""
    # Apply damage to shields first
    if target.shields > 0:
        shield_damage = min(damage, target.shields)
        target.shields -= shield_damage
        damage -= shield_damage

    # Remaining damage goes to armor
    if damage > 0:
        target.armor -= damage
        if target.armor <= 0:
            # Ship destroyed!
            target.armor = 0
```

### 5. Different Species Ships

```python
# Encounter different alien ships
thrynn_ship = Ship(
    name="Thrynn Destroyer",
    ship_class=ShipClass.THRYNN_DESTROYER,
    species=Species.THRYNN,
    stats=ShipStats(
        max_fuel=150.0,
        max_cargo=40,
        max_armor=200,  # Very tough
        max_shields=150,
        weapon_slots=5,  # Heavily armed
        engine_power=0.9
    )
)

# Different species could have different:
# - Ship designs
# - Technology levels
# - Combat behavior
# - Trading preferences
```

## Migration Strategy

### Phase 1: Create Ship Entity ✓ (Complete)

1. Create `entities/ship.py` with Ship, PlayerShip, ShipStats
2. Define ShipClass and Species enums
3. Create factory functions for ship types

### Phase 2: Update GameState (Next)

4. Add `player_ship: PlayerShip` to GameState
5. Initialize player ship in `__init__`: `self.player_ship = create_terran_scout()`
6. Keep old properties temporarily for backward compatibility
7. Update property access to use `self.player_ship.*`

### Phase 3: Update Dependent Code

8. Update screens to access ship via `game_state.player_ship`
9. Update status displays to show ship stats
10. Remove old ship properties from GameState

### Phase 4: Enhanced Features (Future)

11. Add NPC ships to star systems
12. Implement ship encounters/combat
13. Add ship trading/upgrading at starports
14. Support ship switching/capturing

## Design Benefits

### 1. Clean Separation of Concerns

```python
# Before: Mixed responsibilities
game_state.fuel -= 10  # GameState managing ship fuel
game_state.cargo_used += 5  # GameState managing cargo

# After: Ship handles its own state
game_state.player_ship.consume_fuel(10)  # Ship method
game_state.player_ship.add_cargo("minerals", 5)  # Ship method
```

### 2. Type Safety

```python
# Before: No type checking
fuel = game_state.fuel  # Could be anything

# After: Type-safe
fuel = game_state.player_ship.fuel  # PlayerShip.fuel is float
```

### 3. Easy Extension

```python
# Adding new ship type is simple:
class ShipClass(Enum):
    TERRAN_SCOUT = "terran_scout"
    NEW_ALIEN_SHIP = "new_alien_ship"  # Just add enum value

def create_new_alien_ship() -> Ship:
    # Create factory function with custom stats
    pass
```

### 4. Multiple Ships Support

```python
# Future: Player could own multiple ships
class GameState:
    player_ships: list[PlayerShip]  # Fleet of ships
    active_ship: PlayerShip  # Currently piloting

    def switch_ship(self, ship: PlayerShip):
        """Switch to different ship in fleet"""
        self.active_ship = ship
```

### 5. Ship Persistence / Save Games

```python
# Easy to serialize ship data
def save_ship(ship: PlayerShip) -> dict:
    return {
        'name': ship.name,
        'class': ship.ship_class.value,
        'fuel': ship.fuel,
        'cargo': ship.cargo,
        'position': ship.get_position(),
        'credits': ship.credits,
        # etc.
    }

def load_ship(data: dict) -> PlayerShip:
    # Reconstruct ship from saved data
    pass
```

## Open Questions

1. **Ship Modules/Equipment**
   - Should upgrades be properties of Ship, or separate Equipment entities?
   - Original Starflight had weapons, shields, armor, engines as purchasable items

2. **Ship Classes vs. Individual Ships**
   - Should each ship be a unique instance, or references to ship class templates?
   - How to handle ship damage persistence vs. repairs?

3. **Fleet Management**
   - Will player ever control multiple ships simultaneously?
   - If so, need fleet coordination, formation flying, etc.

4. **Ship Specialization**
   - Mining ship, exploration ship, combat ship?
   - Different modules for different roles?

5. **Alien Ship Behavior**
   - Should alien ships have AI component?
   - Different species have different behavior patterns?

## Recommendation

**Start with Phase 2**: Update GameState to use PlayerShip entity. This provides immediate benefits (clean code, encapsulation) without requiring major refactoring of game systems.

Keep the design simple initially:
- Player has one ship (PlayerShip)
- NPC ships can be added later as needed
- Ship upgrades can be simple stat modifications for now
- Advanced features (fleets, modules, AI) can be added incrementally

The entity foundation is solid and extensible for future enhancements.
