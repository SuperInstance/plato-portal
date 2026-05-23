"""
Modal Jazz Terrain — wide open water, few landmarks.

The landscape: a deliberately sparse lattice. Miles Davis's "So What"
uses only 7 notes in D Dorian — no raised leading tone, no dominant
chord to create a V→I pull. The gravitational field is nearly flat;
any note can move to any other note without "wrong" resolution.

John Coltrane's "Impressions" and "My Favorite Things" extend this:
sustained pedal points create drone-like gravity, and the improviser
builds tension through register, rhythm, and density rather than
harmonic motion. The freedom is genuine — you can play the same note
for 8 bars and it's a valid artistic choice, or you can run through
all 12 chromatic degrees over a pedal and it's also valid.

The funnel is WIDE: the root and fifth have slightly more gravity,
but the real constraint is maintaining the MODE (Dorian, Mixolydian,
etc.) — staying in the scalar field even as you explore it.

Rigidity is LOW. There is no prescribed chord sequence, no required
resolution pattern. The only constraint is aesthetic: you must create
coherence through motivic development, rhythmic invention, or
registeral architecture. The mode is the territory.

Time is slow and spacious. Long tones, pregnant silences, and
rhythmic elasticity. The rhythm section (typically piano, bass,
drums in post-bop configuration) provides a flexible pulse.
"""

from ..terrain import ScaleDegree, RhythmicSkeleton, Terrain

MODAL_JAZZ = Terrain(
    name="modal_jazz",
    description=(
        "Wide open water with few landmarks. A deliberately sparse lattice "
        "where the mode (Dorian, Mixolydian, etc.) is the primary constraint. "
        "Nearly flat gravitational field — any note can move to any other "
        "within the mode. Tension is built through register, rhythm, and "
        "density rather than harmonic motion. The space IS the music."
    ),
    scale_degrees=[
        # D Dorian as canonical example — the mode can shift but the
        # SPARSINESS of the lattice is the point
        ScaleDegree(0, 1.0, "root / final"),
        ScaleDegree(2, 0.85, "major 2nd"),
        ScaleDegree(3, 0.78, "minor 3rd"),    # Dorian characteristic
        ScaleDegree(5, 0.8, "perfect 4th"),
        ScaleDegree(7, 0.88, "perfect 5th"),
        ScaleDegree(9, 0.75, "major 6th"),     # Dorian — not minor 6th
        ScaleDegree(10, 0.65, "minor 7th"),
    ],
    characteristic_intervals=[
        2,   # stepwise — motivic development within mode
        5,   # perfect fourth — pentatonic subset
        7,   # perfect fifth — the pedal anchor
        3,   # minor third — Dorian color
        9,   # major sixth — Dorian signature interval (from root)
        4,   # major third — available but less idiomatic
    ],
    rhythmic_skeletons=[
        RhythmicSkeleton(
            name="long_phrases",
            # Extended phrases with space between — think Miles's pacing
            subdivisions=[2.0, 1.0, 1.0, 0.5, 0.5],
            accents=[0],
            swing=0.3,
        ),
        RhythmicSkeleton(
            name="rubato_opening",
            subdivisions=[1.5, 0.5, 2.0, 1.0],
            accents=[0],
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="pedal_point_pulse",
            # Sustained drone with rhythmic activity above
            subdivisions=[1.0, 1.0, 1.0, 1.0],
            accents=[0],
            swing=0.2,
        ),
        RhythmicSkeleton(
            name="coltrane_sheets_of_sound",
            # Rapid sequential patterns — Coltrane's modal approach
            subdivisions=[0.25] * 16,
            accents=[0, 4, 8, 12],
            swing=0.4,
        ),
    ],
    register_tendency=(43, 89),   # wide range — G2 to F5
    chromatic_density=0.1,
    typical_tempo=(50, 140),
)

# ── The Funnel ──
# Nearly flat. Root and fifth are slightly deeper basins, but the mode
# itself is the constraint surface:
#
#   Dorian: the major 6th (degree 9) is the characteristic color note
#   It distinguishes Dorian from natural minor. Playing the minor 6th
#   (degree 8) would break the mode.
#
#   The pedal point (sustained root or fifth in bass) creates a
#   non-directive gravity — everything is heard AGAINST the pedal,
#   not RESOLVING toward it.
#
#   Moving between modes (parallel or relative) creates sudden
#   shifts in the gravitational field — the entire landscape changes.
#
# ── The Holonomy ──
# AABA form is common (So What, Impressions) but the A sections are
# all the same mode — there's no harmonic bridge, just a step up
# (D- to Eb- in So What) and back. The loop is more about energy
# arc than harmonic return.
#
# Coltrane's "My Favorite Things" approach: single mode for extended
# improvisation (sometimes 20+ minutes). The "return" is the head.
#
# ── The Rigidity ──
# VERY LOW formally:
#   - No prescribed chord sequence
#   - No required resolution patterns
#   - Register and rhythmic choices are free
# MEDIUM modally:
#   - You should stay in the mode (with occasional chromaticism)
#   - Motivic development is the primary structural tool
#   - Space and silence are as valid as notes
#
# ── The Metronome ──
# Slow to medium. The pulse is present but flexible. Think of it as
# a lake, not a river — there's movement but no current.
# Bass walks or pedals, drums play time but with color and texture.
# Rubato passages are welcome, especially in ballads.
#
# ── Depth Soundings ──
# - Miles Davis, "So What" (Kind of Blue, 1959) — THE modal statement
# - Miles Davis, "Flamenco Sketches" — five modes, no form
# - John Coltrane, "Impressions" — modal fury
# - John Coltrane, "My Favorite Things" — soprano sax + mode
# - Wayne Shorter, "Footprints" — 6/4 modal minor
# - McCoy Tyner, "Passion Dance" — pentatonic modal
