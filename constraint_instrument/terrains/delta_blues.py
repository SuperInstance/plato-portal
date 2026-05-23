"""
Delta Blues Terrain — the muddy water at the source.

The landscape: a pentatonic minor shell with three blue notes that don't
sit still on the lattice. The blue third (between minor and major), the
tritone (the devil's interval), and the minor seventh all exist as
*regions* more than points — you can bend into them from either direction
and the amount of bend IS the expression. Slide guitar opens every pitch
to continuous deformation; the fret hand is a suggestion, the slide is
the law.

The funnel is deep and narrow: everything pulls toward the root and fifth,
but the blue third is the gravitational anomaly — it's not quite in the
scale, not quite out of it, and every phrase orbits around resolving (or
deliberately not resolving) that tension.

Time is loose. The shuffle is a feeling, not a grid. Early delta players
(Charley Patton, Son House, Skip James) often played solo with no rhythm
section, so tempo could drift, stretch, and collapse as the story demanded.
The 12-bar form exists but it's more of a conversation than a cage.
"""

from ..terrain import ScaleDegree, RhythmicSkeleton, Terrain

DELTA_BLUES = Terrain(
    name="delta_blues",
    description=(
        "The deep muddy water. Pentatonic minor shell with three blue notes "
        "that exist as pitch-regions, not fixed points. Slide guitar opens "
        "every pitch to continuous deformation. The blue third is the "
        "gravitational anomaly — the entire tradition orbits around whether "
        "you resolve it or let it hang. Time is a feeling, not a grid."
    ),
    scale_degrees=[
        # ── The shell (pentatonic minor) ──
        ScaleDegree(0, 1.0, "root",
                    blues_note=False),
        # The minor third — bent sharp toward major in vocal and slide
        ScaleDegree(3, 0.92, "minor 3rd",
                    blues_note=True),
        # The major third — landed on occasionally, bent flat toward minor
        ScaleDegree(4, 0.6, "major 3rd",
                    blues_note=True),
        ScaleDegree(5, 0.88, "perfect 4th"),
        # ── The blue notes ──
        # The tritone: the devil in church, the soul in blues
        ScaleDegree(6, 0.82, "tritone",
                    blues_note=True),
        ScaleDegree(7, 0.95, "perfect 5th"),
        # The minor seventh — nearly as stable as root in V chord context
        ScaleDegree(10, 0.88, "minor 7th",
                    blues_note=True),
    ],
    characteristic_intervals=[
        3,   # minor third bend toward major
        4,   # major third (resolved, or bent from)
        5,   # perfect fourth — the cry
        7,   # perfect fifth — the anchor
        6,   # tritone — the trouble
        10,  # minor seventh drop — the sigh
    ],
    rhythmic_skeletons=[
        RhythmicSkeleton(
            name="shuffle",
            subdivisions=[0.67, 0.33] * 4,
            accents=[0, 2, 4, 6],
            swing=0.67,
        ),
        RhythmicSkeleton(
            name="slow_12_8",
            subdivisions=[1.0 / 3] * 12,
            accents=[0, 3, 6, 9],
            swing=0.5,
        ),
        RhythmicSkeleton(
            name="bottleneck_slide_pulse",
            # open D or open G: one bar of steady thumb, vocal fills between
            subdivisions=[0.75, 0.25, 0.5, 0.5, 0.75, 0.25, 0.5, 0.5],
            accents=[0, 4],
            swing=0.6,
        ),
        RhythmicSkeleton(
            name="skip_james_bentenian",
            # Dropped-D tuning, eerie float — almost no downbeat
            subdivisions=[1.5, 0.5, 1.0, 1.0],
            accents=[0],
            swing=0.3,
        ),
    ],
    register_tendency=(40, 72),  # E2 to C4 — guitar in open position
    chromatic_density=0.25,      # chromaticism comes from bends, not added notes
    typical_tempo=(50, 130),     # slow drag to medium walk
)

# ── The Funnel ──
# Root and fifth are the deep basins. The blue third (degree 3→4 zone) is
# a shallower basin that every phrase visits but nobody stays in.
# The tritone is a ridge — you cross it, you don't rest on it.
# The minor seventh is a secondary basin (dominant territory).
#
# Gravitational flow (typical):
#   4 → 3 → 0        (major third bends down to minor, resolves to root)
#   6 → 5 or 7       (tritone pushes to fourth or fifth)
#   10 → 0 or 7      (seventh resolves down or hangs)
#
# ── The Holonomy ──
# 12-bar blues is the primary loop:
#   I (4 bars) → IV (2 bars) → I (2 bars) → V (1) → IV (1) → I (2)
# You can truncate, extend, or blur this, but the form is the path.
# Returning to I must feel like home, even if you arrive early or late.
#
# ── The Rigidity ──
# Low to medium. The form is there but stretchable. You MUST hit the
# vocal/lead on the blue third at least once per chorus. The V→IV→I
# cadence is expected but can be replaced by a turnaround or a held V.
# Slide technique lets you treat any pitch as a bend target.
#
# ── The Metronome ──
# Tempo is felt, not counted. Shuffle swing is essential (0.6-0.7).
# Slow blues can drift ±10 BPM over the course of a performance.
# The singer/guitarist IS the timekeeper; rubato within phrases is normal.
#
# ── Depth Soundings (reference recordings) ──
# - Robert Johnson, "Cross Road Blues" (1936) — the archetype
# - Son House, "Death Letter Blues" — raw open tuning
# - Skip James, "Hard Time Killing Floor Blues" — Bentenian minor tuning
# - Charley Patton, "Pony Blues" — the deep delta pulse
# - Howlin' Wolf, "Smokestack Lightning" — one-chord vortex
# - Muddy Waters, "Rollin' Stone" — the transition to Chicago
