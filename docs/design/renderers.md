# Renderers Outline

## Main View Renderers:
### Hyperspace renderer 
- starfield
- ship
- star systems as entry points
- nebulae 
- flux points

### Local space renderer 
- starfield 
- ship 
- planets/moons on orbital paths
- central body (inner system, star, gas giant)

### Orbit renderer 
- rotating planet view (probably just the planet filling most of the view)

### Surface renderer 
- top-down terrain
- vehicle 
- entity icons for minerals/flora/fauna/structures

### Communications renderer 
- alien portraits or images (possibly animated or with mood states)

## Auxiliary View Renderers:
### Ship status display
- ship outline
- fuel gauge 
- system health diagram

### System mini-map 
- planets 
- orbits 
- ship position in local space

### Terrain heightmap 
- planet surface from orbit (for landing site selection)

### Vehicle stats 
- fuel
- cargo 
- distance to ship

### Local/regional map toggle (for surface exploration)

### Scan results display (needs better definition)
- entity silhouette with dither effect, then data

## Control Panel:

### Menu renderer 
- hierarchical text menus 
- selection state

This one's probably simpler - just text layout with highlighting

## Message Log:
### Scrolling text renderer 
- append-only, auto-scroll

## Modals:
Still need to define the design specifications, as each specific modal will have its own layout structure.
### Cargo modal
### Starmap modal
### Trade modal (future)
### Various confirmation prompts

## Full-screen (non-HUD):
For now, these can be rendered as lists
- Main menu
- Starport interface