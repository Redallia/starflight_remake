# Starflight Inspired Remake

A modern Starflight inspired remake/redesign. I loved the original games, and have fond memories of playing them.

For the longest time I've had fun thinking of all the small improvements, changes, or different approaches I might 
take to rebuilding the game myself. Stuff like moons around gas giants, or more space stations to dock at, or doing 
more with that walking interface that *only* shows up in Starport. Stuff like improving the combat system which, I 
think everybody who's played the game can agree on, has room for improvement. Or including more opportunities for
"useless" crew members to have an impact on the game. I would love to also include factions along side alien species,
to provide more interesting texture, and give opportunities for more in-depth political scenarios.

I'm planning on two different game modes. One is a straightforward approach, providing a narrative for players to
follow, mysteries to uncover, breadcrumb clues to trace, and all of the stuff that made Starflight great. For the 
other mode, I'm drawing inspiration from Dwarf Fortress and Toady One's design philosophy, inspired by interacting 
systems derived from short in-universe pieces of fiction. The idea is to get stories to tell themselves, and let 
players uncover their own unique situations. In essence, the finished game will have a Story Mode, and a Sandbox 
Mode. 

The core loop of exploring a frontier, scanning planets, and getting resources to expand your horizons will 
remain the same. Each game type will be siloed to its own sector, with some in-universe technobabble to explain why
you can't transfer powerful ships between sectors to give yourself an advantage. 

Story mode sectors will aim to play much like the original games, with messages hinting at activity or coordinates, 
named locations that the player will need to figure out, and sector-specific technology/artifacts.

Sandbox mode sectors will be procedurally generated, with randomized planets and possibly even aliens, though 
figuring out how to generate alien art on the fly will be a challenge. I don't think it's an insurmountable one though.
Worst case scenario, I'll leave it as a purely frontier exploration game that can be improved upon later.

It's all super ambitious, and I know that I'm basically describing a wishlist. But as a personal project, I think this
all should be fun to tinker with and develop. I'm making a game I'd love to play myself.

## Project Structure

```
starflight_remake/
├── src/               # Source code
│   ├── core/         # Core game systems
│   ├── ui/           # UI components
│   ├── entities/     # Game entities
│   ├── data/         # Data management
│   ├── systems/      # Game systems
│   ├── assets/       # Game assets
│   └── utils/        # Utility functions
├── docs/             # Documentation
│   ├── design/       # Design documents
│   └── technical/    # Technical documentation
└── tests/            # Test suite
```

## Development Status

After not thinking about this for ages, I've built a super simple, semi-working prototype just to get a handle on the
architecture, but the entire thing is a plate of spaghetti. It's forced me to sit down and do the hard work of actually 
designing the game, and documenting how all the pieces work together. Now I have about a eight or nine different design
spec docs, and I'm laying everything out as cleanly as I can before trying the code again.

