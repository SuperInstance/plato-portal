"""
Electronic Techno Terrain — the minimal grid.

The landscape: an extremely sparse pitch lattice (often just 2-3 notes)
over a MAXIMUM-density rhythmic grid. The kick drum on every quarter note
(4/4 at 130+ BPM) is the gravitational center — not a note in the
traditional sense, but the fundamental pulse that defines the entire
constraint surface. Everything that happens must relate to this grid.

Melodic content is minimal. A single repeating pattern (riff, stab,
synth line) of 2-4 notes, cycling every 1-2 bars. The depth comes from
TIMBRE and TEXTURE: filter sweeps, resonance, reverb, delay — the
same notes sound different each repetition because the sonic surface
is continuously reshaped. This is NOT a melody-driven tradition; it's
a texture-driven tradition.

The funnel is almost entirely toward the kick drum (rhythmic downbeat)
and the root note (bass). Any melodic element must establish a pattern
and then the art is in how you DEVIATE from it — a single added or
removed note creates enormous tension because the listener has been
hypnotized by repetition.

Rigidity is HIGH for the grid: the 4/4 kick is absolute, the tempo
is locked (130-150 BPM, ±0), and the arrangement follows a prescribed
structure (build → drop → breakdown → build). But within that grid,
a single parameter change (filter opening, hi-hat addition) is the
entire musical gesture.
"""

from ..terrain import ScaleDegree, RhythmicSkeleton, Terrain

ELECTRONIC_TECHNO = Terrain(
    name="electronic_techno",
    description=(
        "The minimal grid. Extremely sparse pitch lattice (2-3 notes) over "
        "a maximum-density rhythmic grid. The 4/4 kick drum is the "
        "gravitational center — not a melody note but the fundamental pulse. "
        "Depth comes from timbre and texture, not pitch. A single added or "
        "removed element creates enormous tension against the repetition. "
        "The grid is absolute; within it, parameter changes ARE the music."
    ),
    scale_degrees=[
        # Minimal — often just root and one or two other notes
        ScaleDegree(0, 1.0, "root"),           # THE note
        ScaleDegree(7, 0.7, "perfect 5th"),    # common second note
        ScaleDegree(5, 0.5, "perfect 4th"),    # alternative
        ScaleDegree(3, 0.4, "minor 3rd"),      # darker techno
        ScaleDegree(6, 0.35, "tritone"),       # industrial/hard techno
        ScaleDegree(12, 0.6, "octave"),        # bass drop / acid squeal
    ],
    characteristic_intervals=[
        7,   # perfect fifth — the most common melodic interval
        0,   # unison — repetition IS the primary interval
        12,  # octave — bass to lead relationship
        5,   # perfect fourth — melodic step
        3,   # minor third — dark color
        6,   # tritone — acid/industrial
    ],
    rhythmic_skeletons=[
        RhythmicSkeleton(
            name="four_on_floor",
            # THE techno pattern: kick on every beat
            subdivisions=[0.25] * 4,
            accents=[0, 1, 2, 3],  # every beat
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="hi_hat_pattern",
            # Off-beat hi-hat: the perpetual tic-tic-tic
            subdivisions=[0.125] * 8,
            accents=[1, 3, 5, 7],  # off-beats only
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="synth_stab",
            # Short, rhythmic synth hit — often syncopated
            subdivisions=[0.125] * 8,
            accents=[2, 6],  # syncopated stabs
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="acid_303",
            # TB-303 pattern — repetitive 16th note pattern with accent
            subdivisions=[0.0625] * 16,
            accents=[0, 3, 6, 10, 12],
            swing=0.05,
        ),
    ],
    register_tendency=(24, 72),  # C1 to C4 — bass-heavy, treble is percussion
    chromatic_density=0.05,      # almost no chromaticism
    typical_tempo=(125, 150),
)

# ── The Funnel ──
# The kick drum IS the funnel. Every quarter note, the kick fires and
# everything resets. The gravitational center is not a pitch — it's a
# moment in time.
#
# Pitch funnel (minimal):
#   Root → Root → Root (bass drone)
#   Root → 5th → Root (melodic motif, if present)
#   The bass provides a harmonic root but it barely moves.
#
# Textural funnel (the real depth):
#   Closed filter → open filter → closed filter (build and release)
#   Dry → wet → dry (reverb/delay as tension/release)
#   Sparse → dense → sparse (element addition as crescendo)
#   The "funnel" in techno is toward MAXIMUM DENSITY at the drop,
#   then RELEASE back to minimal.
#
# ── The Holonomy ──
# The loop is the form. A techno track is built from loops:
#   Drum loop (4-8 bars) → add bass loop → add synth loop → REMOVE elements
#
# Arrangement arc (the macro-holonomy):
#   Intro (minimal) → Build (elements added) → Drop (everything hits)
#   → Breakdown (elements removed) → Build again → Drop → Outro
#   The return to the drop is the structural "home" — the place of
#   maximum gravitational satisfaction.
#
# ── The Rigidity ──
# VERY HIGH for the grid:
#   - 4/4 kick on every beat — NEVER deviates
#   - Tempo is locked (130-150 BPM, ±0)
#   - Rhythmic grid is quantized
#   - 16th note subdivision is the atomic unit
# LOW for pitch content:
#   - 2-3 notes is enough
#   - Key can be ambiguous (no V-I, no leading tone)
#   - Bass can drone on root for the entire track
# HIGH for form:
#   - Build → drop → breakdown structure is prescribed
#   - Element addition follows convention (drums → bass → lead)
#   - The DJ must be able to mix in and out (intro/outro compatibility)
#
# ── The Metronome ──
# ABSOLUTE. The grid never wavers. 125-150 BPM, locked to the DAW clock.
# The kick drum IS the metronome. Hi-hats subdivide it. There is no swing,
# no rubato, no human timing variation (in pure techno). The machine pulse
# is the aesthetic — trance-inducing, relentless, inhuman.
# The only tempo change is an intentional shift (gear change) as a
# structural marker.
#
# ── Depth Soundings ──
# - Derrick May / Rhythim Is Rhythim, "Strings of Life" — Detroit techno anthem
# - Jeff Mills, "The Bells" — minimal, driving, hypnotic
# - Robert Hood, minimal techno — the sparsest form
# - Richie Hawtin / Plastikman, "Spastik" — one-snare masterpiece
# - Underground Resistance, "Transition" — political techno
# - Carl Cox, live sets — techno as marathon, not sprint
