"""
Bebop Terrain — the lattice at speed.

The landscape: a fully chromatic lattice where seven diatonic notes are
"home" and five chromatic notes are "passing" — but at 200+ BPM the
distinction blurs. Every scale degree is available; the art is in the
sequencing. The ii-V-I progression is the gravitational engine: it creates
a dense network of local funnels that chain together into long arcs.

Charlie Parker's vocabulary lives here: enclosures (approach from above
and below), chromatic passing tones on weak beats, and rhythm changes as
a harmonic obstacle course. Dizzy Gillespie's Afro-Cuban extensions add
polyrhythmic cross-currents.

The rigidity is HIGH for resolution: you must land on a chord tone on
strong beats, and your lines must imply the harmony even when playing
"out." But the path between chord tones is wild — any chromatic route
is valid as long as you resolve correctly.

Time is fast and relentless. The eighth-note stream is the default
surface — constant motion, with accents creating the illusion of space.
"""

from ..terrain import ScaleDegree, RhythmicSkeleton, Terrain

BEBOP = Terrain(
    name="bebop",
    description=(
        "The lattice at speed. Fully chromatic surface where seven diatonic "
        "degrees are home and five are passing — but at 200+ BPM the "
        "distinction blurs into flow. The ii-V-I progression is the "
        "gravitational engine creating a dense network of local funnels. "
        "You must land on chord tones on downbeats; how you get there is "
        "the art."
    ),
    scale_degrees=[
        ScaleDegree(0, 1.0, "root"),
        ScaleDegree(1, 0.4, "flat 2 / sharp 1", blues_note=False),   # passing
        ScaleDegree(2, 0.85, "major 2nd (9th)"),
        ScaleDegree(3, 0.7, "minor 3rd"),
        ScaleDegree(4, 0.9, "major 3rd"),
        ScaleDegree(5, 0.8, "perfect 4th (11th)"),
        ScaleDegree(6, 0.55, "tritone"),                               # the pivot
        ScaleDegree(7, 0.92, "perfect 5th"),
        ScaleDegree(8, 0.45, "flat 6 / sharp 5", blues_note=False),  # passing / altered
        ScaleDegree(9, 0.8, "major 6th (13th)"),
        ScaleDegree(10, 0.85, "minor 7th"),
        ScaleDegree(11, 0.65, "major 7th"),                            # leading tone
    ],
    characteristic_intervals=[
        2,   # diatonic step — default motion
        3,   # minor third — blues inflection + triadic
        4,   # major third — chord tone approach
        5,   # perfect fourth — enclosures
        6,   # tritone — V7 b9 → I resolution engine
        7,   # perfect fifth — root motion
        1,   # chromatic approach — the bebop signature
    ],
    rhythmic_skeletons=[
        RhythmicSkeleton(
            name="eighth_note_stream",
            subdivisions=[0.5] * 8,
            accents=[0, 3, 4, 7],  # syncopated accents
            swing=0.6,
        ),
        RhythmicSkeleton(
            name="triplet_run",
            subdivisions=[1.0 / 3] * 12,
            accents=[0, 3, 6, 9],
            swing=0.5,
        ),
        RhythmicSkeleton(
            name="bebob_head_rhythm",
            # typical AABA head rhythm — mix of durations
            subdivisions=[0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.5, 0.5,
                          0.5, 0.25, 0.25, 1.0],
            accents=[0, 4, 8],
            swing=0.55,
        ),
        RhythmicSkeleton(
            name="doubled_time_feel",
            subdivisions=[0.25] * 16,
            accents=[0, 4, 8, 12],
            swing=0.65,
        ),
    ],
    register_tendency=(55, 91),  # G3 to G5 — horn range
    chromatic_density=0.7,
    typical_tempo=(180, 320),
)

# ── The Funnel ──
# The ii-V-I is the primary gravitational engine:
#   ii (weight 0.6) → V (weight 0.85) → I (weight 1.0)
# Each chord creates a local funnel:
#   On ii:  root, 4, 10 are chord tones (landing points)
#   On V:   root, 4, 7, 10 are chord tones; 6 is the characteristic tension
#   On I:   root, 4, 7, 11 are chord tones — home
#
# Enclosure pattern (the bebop funnel within a funnel):
#   target-1 semitone above → target-1 semitone below → target
#   This creates a micro-gravity well around every chord tone.
#
# Tritone substitution creates parallel funnels:
#   V → I is also bII → I (same tritone, different root)
#
# ── The Holonomy ──
# AABA form (rhythm changes): the loop must return to the tonic
# after the bridge's III-VI-II-V cycle. The bridge is a different
# gravitational field; returning to A must feel like re-entry.
#
# Blues form: 12 bars with ii-V substitutions turning every bar
# into a local funnel. The final ii-V-I turnaround is mandatory.
#
# ── The Rigidity ──
# HIGH for resolution rules:
#   - Strong beats must land on chord tones
#   - Lines must clearly imply the underlying harmony
#   - The last note of a phrase must resolve (7→1, 4→3, or root)
# LOW for the path between resolutions:
#   - Any chromatic route is valid
#   - Enclosures, approach notes, side-slipping all allowed
#   - Odd groupings (3 over 4, 5 over 4) create polyrhythmic tension
#
# ── The Metronome ──
# Fast, relentless, swinging. Eighth notes are the surface texture.
# At 200-320 BPM, the eighth-note pulse is constant.
# Swing ratio ~0.55-0.65 — not as loose as blues, not straight.
# The ride cymbal IS the metronome; the bass walks quarters.
#
# ── Depth Soundings ──
# - Charlie Parker, "Ko-Ko" (1945) — the opening statement
# - Charlie Parker, "Donna Lee" — speed + chromaticism
# - Dizzy Gillespie, "Salt Peanuts" — rhythm + humor
# - Bud Powell, "Un Poco Loco" — piano bebop at full tilt
# - Thelonious Monk, "Straight No Chaser" — the angular side
# - Clifford Brown & Max Roach, "Joy Spring" — hard bop extension
