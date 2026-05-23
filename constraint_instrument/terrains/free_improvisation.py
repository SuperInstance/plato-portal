"""
Free Improvisation Terrain — the ocean with no floor.

The landscape: a fully chromatic lattice with all 12 notes available
and equal weighting. There is no key, no mode, no scale — every
pitch is equally valid (or equally invalid). The gravitational field
is ZERO or generated entirely by the performers in real-time.

This is Derek Bailey's world: "non-idiomatic improvisation" where
the constraints are created moment-to-moment by the musicians.
The only "rules" are listening, responding, and making choices
that create coherence — but the definition of coherence is itself
improvised. A performance can be dense and frenetic (Peter Brötzmann)
or sparse and contemplative (Pauline Oliveros's deep listening).

The funnel doesn't exist — or rather, the performers CREATE the
funnel in real-time through:
- Register choices (staying in a range creates a temporary lattice)
- Dynamic choices (loudness creates temporary gravity)
- Textural choices (density implies importance)
- Intervallic choices (repetition creates temporary structure)
The art is in CREATING constraints, not operating within them.

Rigidity is ZERO. There are no prescribed notes, rhythms, forms,
or techniques. The only constraint is that the music is made in
real-time by listening musicians. The performer IS the composer
IS the instrument. Every choice is free; the only discipline is
the discipline of attention.
"""

from ..terrain import ScaleDegree, RhythmicSkeleton, Terrain

FREE_IMPROVISATION = Terrain(
    name="free_improvisation",
    description=(
        "The ocean with no floor. Fully chromatic lattice with equal "
        "weighting — no key, no mode, no scale. The gravitational field "
        "is zero or generated entirely by performers in real-time. "
        "Constraints are created moment-to-moment through register, "
        "dynamics, texture, and intervallic choices. The performer IS "
        "the constraint surface."
    ),
    scale_degrees=[
        # All 12 notes, equal weight — no hierarchy
        ScaleDegree(0, 0.5, "C / any root"),
        ScaleDegree(1, 0.5, "C# / Db"),
        ScaleDegree(2, 0.5, "D"),
        ScaleDegree(3, 0.5, "D# / Eb"),
        ScaleDegree(4, 0.5, "E"),
        ScaleDegree(5, 0.5, "F"),
        ScaleDegree(6, 0.5, "F# / Gb"),
        ScaleDegree(7, 0.5, "G"),
        ScaleDegree(8, 0.5, "G# / Ab"),
        ScaleDegree(9, 0.5, "A"),
        ScaleDegree(10, 0.5, "A# / Bb"),
        ScaleDegree(11, 0.5, "B"),
        # Plus: quarter tones, multiphonics, noise, silence
        # The lattice extends BEYOND 12-TET into continuous sound space
    ],
    characteristic_intervals=[
        # All intervals equally available — but some are more commonly
        # chosen as structural tools in the moment:
        1,    # semitone — close dissonance, micro-motion
        2,    # whole tone — neutral motion
        3,    # minor third — close enough for consonance, far enough for color
        6,    # tritone — maximum chromatic tension
        7,    # perfect fifth — the most "neutral" interval (if chosen)
        11,   # major seventh — close dissonance
        0,    # unison — extreme consonance as radical choice
        # Non-12-TET: quarter tones, microtonal intervals, noise bands
    ],
    rhythmic_skeletons=[
        RhythmicSkeleton(
            name="free_pulse",
            # No regular pulse — durations are improvised
            subdivisions=[1.0],
            accents=[],
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="pointillist",
            # Isolated attacks with silences — Webern-like spatial distribution
            subdivisions=[0.2, 0.4, 0.1, 0.8, 0.3, 0.2],
            accents=[],
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="density_swarm",
            # Rapid activity — Evan Parker's circular breathing saxophone
            subdivisions=[0.0625] * 32,
            accents=[],
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="silence",
            # John Cage 4'33" territory — the sound IS the environment
            subdivisions=[4.0],
            accents=[],
            swing=0.0,
        ),
    ],
    register_tendency=(0, 127),    # FULL RANGE — no restrictions
    chromatic_density=1.0,         # fully chromatic + beyond
    typical_tempo=(0, 300),        # silence to maximum speed
)

# ── The Funnel ──
# THERE IS NO PRE-EXISTING FUNNEL. Gravity is created in real-time:
#
# Temporary funnel creation strategies:
#   Register: staying in a narrow range for a time creates a "key"
#   Repetition: repeating a note or interval creates a temporary tonic
#   Dynamics: louder notes become gravitational centers
#   Duration: longer notes become anchors
#   Texture: dense passages create gravity; sparse ones create space
#   Intervallic focus: using primarily minor thirds creates a "mode"
#
# The art of free improvisation is creating a gravitational field
# convincing enough to generate musical structure, then either
# maintaining or destroying it at the right moment.
#
# ── The Holonomy ──
# THERE IS NO PRESCRIBED LOOP. The form is discovered, not imposed.
#
# Emergent structures:
#   - Dialogue: musician A states, musician B responds
#   - Architecture: slow → dense → sparse → dense → resolution
#   - Timbral narrative: dark → bright → dark
#   - Textural: solo → duo → trio → full ensemble → solo
#
# The "return" in free improvisation is:
#   - A timbral callback (returning to an earlier sound)
#   - A register callback (returning to an earlier pitch area)
#   - A textural callback (returning to an earlier density)
#   - Silence (the ultimate return — to the state before music)
#
# ── The Rigidity ──
# ZERO formal rigidity:
#   - No prescribed notes, scales, or modes
#   - No required rhythmic patterns or time signatures
#   - No song form, no chord progression
#   - No required techniques or approaches
#   - No minimum or maximum duration
#
# The ONLY constraints:
#   - Listen to the other musicians (attentive constraint)
#   - Make choices (creative constraint)
#   - Accept responsibility for those choices (ethical constraint)
#   - The performance happens in real-time (temporal constraint)
#
# Paradox: the most "free" music requires the most discipline.
# The discipline is not of technique but of ATTENTION.
#
# ── The Metronome ──
# THERE IS NO METRONOME. The performer IS the metronome.
# Time is elastic, personal, and negotiated in real-time.
# A performance can move from no pulse → steady pulse → no pulse.
# The pulse, when it emerges, is created by the musicians together.
# It can be felt without being stated (implied pulse).
# It can be stated and then abandoned.
# Silence is a valid tempo (0 BPM).
# Maximum speed is whatever the body can produce (~300 BPM sustained).
#
# ── Depth Soundings ──
# - Derek Bailey, "Lot 74" — non-idiomatic guitar improvisation
# - Peter Brötzmann, "Machine Gun" — European free jazz fury
# - Evan Parker, "Topography of the Lungs" — circular breathing sax
# - AMM, "AMMMusic" — electro-acoustic free improvisation
# - Cecil Taylor, "Unit Structures" — piano as percussive architecture
# - Pauline Oliveros, "Deep Listening" — meditative improvisation
# - Evan Parker + Derek Bailey + Han Bennink, "The Topography of the Lungs"
# - Ornette Coleman, "Free Jazz" — the album that named the genre
