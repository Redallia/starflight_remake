# Procedural Generation Outline
## Overview
This document captures initial thinking on procedural generation for planetary surfaces and celestial body visuals. Implementation details will be discovered through experimentation. The goal is to create varied, visually distinct worlds that feel appropriate to their type without requiring hand-crafted assets.

## Core Infrastructure
All terrain generation shares common building blocks:
Noise generation. Perlin noise as the base, with configurable frequency (feature size) and octaves (detail levels). Multiple noise layers can be combined for complexity.
Threshold system. A cutoff value that determines what counts as "liquid" versus "solid" terrain. Same heightmap can produce different results by adjusting this threshold.
Color palette mapping. Elevation values map to colors based on world type. Each terrain type has its own gradient.
Overlay systems. Additional features (craters, storms) layered on top of base terrain.
Seed-based consistency. All generation derives from a planet seed, ensuring the same planet looks the same on every visit.

## Terrain Types
Continental (Rocky/Terran Worlds)
Method: Standard Perlin heightmap with moderate sea level threshold.
Characteristics: Large landmasses, ocean basins, varied coastlines.
Parameters:
- Water coverage: ~40-60%
- Noise frequency: Medium (continental-scale features)
- Octaves: Multiple (adds coastal detail, mountain ranges)

Color mapping: Ocean depths (blues) → coastal shallows → lowlands (greens) → highlands → mountains (browns/grays) → peaks (white if cold enough)

## Archipelago (Rocky/Terran Worlds)
Method: Same as continental, higher sea level threshold.
Characteristics: Scattered islands, dominant ocean, chains and clusters.
Parameters:

Water coverage: ~70-85%
Otherwise same as continental

Color mapping: Same as continental, just more ocean visible.

## Desert (Rocky Worlds)
Method: Continental heightmap, no liquid threshold applied.
Characteristics: Dune seas in lowlands, rocky highlands, no surface water.
Parameters:

Water coverage: 0%
Noise frequency: Medium base, with additional high-frequency layer for dune texture in low elevations

Color mapping: Low elevations (sand/tan) → mid elevations (darker rock) → high elevations (bare stone/gray)

## Magma (Molten Worlds)
Method: Continental or archipelago heightmap, liquid = magma instead of water.
Characteristics: Magma lakes/oceans, volcanic terrain, harsh contrast.
Parameters:

Liquid coverage: Variable (archipelago-like or continental-like)
Noise frequency: Medium, possibly with sharper falloffs for more dramatic terrain

Color mapping: Magma (bright orange/red) → cooling rock (dark red) → solid rock (black/dark gray) → peaks (can glow or stay dark)
Future consideration: Animated magma flow in liquid areas.

## Ice (Frozen Worlds)
Method: Continental heightmap with frozen color palette.
Characteristics: Ice sheets, frozen seas, glacial features.
Parameters:

Similar to continental, threshold determines frozen ocean vs exposed rock

Color mapping: Frozen ocean (white/light blue) → ice sheets → exposed rock (gray) → peaks
Cratered (Airless Bodies - Moons, Asteroids)
Method: Low-amplitude Perlin base + procedural crater overlay.
Characteristics: Impact craters of varying sizes, relatively flat between impacts, no erosion features.
Crater generation:

Scatter crater centers across surface (random but seeded)
Assign radius to each crater (size distribution favoring small, occasional large)
For each terrain point, check proximity to crater centers
Inside crater radius: depress terrain in bowl shape
At crater edge: slight rim uplift
Craters can overlap (later impacts overwrite earlier ones partially)

Parameters:

Crater density (impacts per area)
Size distribution (min, max, falloff curve)
Rim height factor
Base terrain amplitude (should be low so craters dominate)

Color mapping: Simple grayscale or brownish monotone. Elevation affects shade but palette is minimal.
Gas Giant (Non-landable, Visual Only)
Method: Latitude-based banding with Perlin distortion.
Characteristics: Horizontal bands, turbulent edges, possible storm features.
Band generation:

Divide latitude into bands of varying width
Assign colors to bands (alternating light/dark, warm/cool depending on giant type)
Apply low-frequency Perlin to distort band edges horizontally
Creates wavy, turbulent appearance

Storm features (optional):

Place storm centers at specific coordinates (large ones can be seed-based for consistency)
Apply spiral distortion around storm center
Distinct color for storm interior (e.g., Jupiter's red spot)

Parameters:

Number of bands
Band color palette (varies by gas giant subtype: Jupiter-like, Saturn-like, ice giant)
Distortion amplitude
Storm count and placement

Surface Object Placement
Separate from terrain generation, but uses same seed for consistency.
Minerals
Method: Scatter points based on density parameter for planet type. Mineral type weighted by planet conditions (certain minerals more common on certain world types).
Clustering: Minerals should cluster somewhat rather than uniform distribution. Could use secondary noise layer to create "rich" and "poor" regions.
Flora
Method: Scatter based on habitability. Density varies by terrain elevation and proximity to liquid (if present). Desert and frozen worlds have sparse or no flora.
Clustering: Natural clustering around favorable conditions.
Fauna
Method: Scatter more sparsely than flora. Tends toward specific biome bands rather than uniform distribution.
Behavior: Hostile/passive ratio varies by planet. More hostile fauna on harsher worlds.
Ruins and Settlements
Method: Not procedural scatter. Placed based on seed at specific coordinates. These are story-relevant and need to be consistent and intentional.
Placement considerations: Ruins tend toward unusual terrain features (why did ancients build here?). Settlements near resources or favorable terrain.
Open Questions

Performance: How much can be generated on-the-fly versus pre-computed when entering orbit?
Resolution: What's the actual pixel/tile resolution of the heightmap? Does it match the 500x200 navigation grid exactly, or is it higher-res for visual display?
Caching: Do we store generated terrain, or regenerate from seed each visit?
Variation within types: How much do two "continental terran" worlds differ? Just threshold and color tweaks, or deeper parameter variation?
Transitions: Some worlds might blend types (desert with polar ice caps, for instance). Worth supporting, or out of scope?
Gas giant detail: Since you can't land, how much detail is needed? Just enough for the orbit view to look good?