"""
Bluegrass Terrain — the high lonesome ridge.

The landscape: major pentatonic plus a flat 7, played at breakneck
speed on fretted instruments (mandolin, banjo, guitar, fiddle, bass).
Bill Monroe's "high lonesome sound" lives here: high-register vocals
with tight two- and three-part harmonies, instrumental breaks that
are as virtuosic as any jazz solo, and a rhythmic engine built on
the banjo's rolling arpeggios.

The funnel pulls hard toward I-IV-V. Bluegrass songs are typically
simple harmonically — the complexity lives in the arrangement and
the solo breaks. Each instrument takes a turn through the same
chord progression, and the soloist must find a new path through
the well-worn I-IV-V terrain every time.

The G run (on guitar) and the Scruggs roll (on banjo) are
characteristic gestures — short, recognizable patterns that function
like words in a language. Bluegrass vocabulary is built from these
shared licks, and the art is in combining them in novel ways.

Rigidity is MEDIUM. The chord progression is simple but fixed.
The rhythm is driving and continuous (no stops, no breaks in the
time). Solos must outline the chords clearly. Crosspicking,
alternate picking, and three-finger rolls are the technical substrate.
"""

from ..terrain import ScaleDegree, RhythmicSkeleton, Terrain

BLUEGRASS = Terrain(
    name="bluegrass",
    description=(
        "The high lonesome ridge. Major pentatonic plus flat 7, played at "
        "breakneck speed on fretted instruments. I-IV-V gravitational "
        "pull with tight vocal harmonies and virtuosic instrumental breaks. "
        "The banjo roll is the rhythmic engine. Every instrument takes a "
        "solo through the same chord progression — the art is finding "
        "a new path every time."
    ),
    scale_degrees=[
        ScaleDegree(0, 1.0, "root"),
        ScaleDegree(2, 0.88, "major 2nd"),
        ScaleDegree(4, 0.92, "major 3rd"),
        ScaleDegree(5, 0.85, "perfect 4th"),
        ScaleDegree(7, 0.95, "perfect 5th"),
        ScaleDegree(9, 0.8, "major 6th"),
        # The flat 7 — crucial bluegrass color (borrowed from Mixolydian)
        ScaleDegree(10, 0.82, "flat 7th"),
    ],
    characteristic_intervals=[
        2,   # major second — scalar runs
        4,   # major third — the "major" in major pentatonic
        5,   # perfect fourth — crosspicking patterns
        7,   # perfect fifth — double stops, chop chords
        9,   # major sixth — the "country" sound
        3,   # minor third — less common, used in bluesy inflection
        10,  # minor seventh interval — flat 7 to root resolution
    ],
    rhythmic_skeletons=[
        RhythmicSkeleton(
            name="scruggs_roll",
            # 3-finger banjo roll: T-I-M-T-I-M-T-I (thumb-index-middle)
            subdivisions=[0.125] * 8,
            accents=[0, 2, 4, 6],  # even eighths, driving
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="guitarboom_chuck",
            # Bass note on 1 and 3, strum on 2 and 4
            subdivisions=[0.33, 0.17, 0.33, 0.17],
            accents=[0, 2],
            swing=0.1,
        ),
        RhythmicSkeleton(
            name="mandolin_chop",
            # Off-beat "chop" chords — the backbeat
            subdivisions=[0.25, 0.25, 0.25, 0.25],
            accents=[1, 3],  # backbeat emphasis
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="fiddle_breakdown",
            # Fast fiddle tune — 16th note runs with bowing patterns
            subdivisions=[0.125] * 8,
            accents=[0, 2, 4, 6],
            swing=0.05,
        ),
    ],
    register_tendency=(48, 84),  # C3 to C5 (instruments + high vocals above)
    chromatic_density=0.1,
    typical_tempo=(120, 180),
)

# ── The Funnel ──
# I-IV-V is the primary gravitational engine:
#   I (weight 1.0) → IV (weight 0.8) → V (weight 0.85) → I
#   The V chord has strong pull back to I (dominant-tonic gravity).
#   IV provides contrast and variety — a different basin to explore.
#
# Common additions:
#   ii → V (secondary dominant preparation)
#   VI (relative minor) — used as bridge contrast
#   I → V/ii → ii → V → I (circle-of-fifths segment)
#
# The flat 7 (degree 10) is a secondary gravitational attractor:
#   It creates Mixolydian color and connects to the V chord's 7th.
#   Resolves down to 5th or up to root.
#
# ── The Holonomy ──
# Standard song forms:
#   AABA (32-bar): verse-verse-bridge-verse, each 8 bars
#   Verse-chorus: simpler, 16-24 bars
#   Fiddle tunes: AABB, 16 bars each (32 bars total)
#
# Instrumental break protocol:
#   Verse 1 (vocals) → Break (instrument) → Verse 2 → Break → Verse 3 → Outro
#   Each break covers the entire chord progression.
#   The loop returns to the vocal after each instrumental cycle.
#
# ── The Rigidity ──
# MEDIUM:
#   - Chord progression must be clearly outlined in solos
#   - Rhythm is continuous and driving — no stops
#   - Solos must be melodic (not textural or abstract)
#   - Instrumental technique is prescribed (3-finger rolls, crosspicking)
# LOOSE:
#   - Ornamentation style varies by player
#   - Harmony singing can use different voicings
#   - Solo vocabulary is personal
#
# ── The Metronome ──
# Fast and driving. 120-180 BPM. Straight eighth notes (no swing).
# The banjo roll creates continuous momentum.
# Off-beat accents (mandolin chop) reinforce the backbeat.
# No rubato, no tempo changes within a tune. The train don't stop.
#
# ── Depth Soundings ──
# - Bill Monroe, "Blue Moon of Kentucky" — the birth of bluegrass
# - Flatt & Scruggs, "Foggy Mountain Breakdown" — the banjo anthem
# - The Stanley Brothers, "Rank Stranger" — high lonesome harmony
# - Tony Rice, "Church Street Blues" — guitar virtuosity
# - David Grisman Quintet, "Dawggy Mountain Breakdown" — newgrass
# - Alison Krauss, "Every Time You Say Goodbye" — modern bluegrass
