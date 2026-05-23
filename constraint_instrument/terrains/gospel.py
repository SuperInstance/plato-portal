"""
Gospel Terrain — the sanctuary.

The landscape: a diatonic lattice richly supplemented with chromatic
passing tones, blues inflections, and extended harmony (9ths, 11ths,
13ths). The Hammond B3 organ is the gravitational engine — its
drawbars create a thick harmonic foundation, and the Leslie speaker
adds a shimmering Doppler effect that makes every sustained note
alive with micro-movement. The piano provides rhythmic and harmonic
support, and the choir provides the melodic summit.

The funnel pulls STRONGLY toward resolution. V→I is the dominant
gravitational force, but the journey to resolution is extended and
ornamented — the delay of arrival is what creates emotional power.
Secondary dominants (V/V, V/ii, V/IV) create local gravitational
fields that chain together into extended harmonic sequences.

Call-and-response is the holonomic constraint: the preacher leads,
the congregation responds; the soloist calls, the choir answers;
the organ states, the piano comments. This creates a conversational
topology where the "return" is the response, not a harmonic cycle.

Rhythm swings — but it's a church swing, not a jazz swing. The
emphasis is on the backbeat (beats 2 and 4), and the pocket is
deep. The organist's left hand provides bass, the right hand
provides chords with characteristic "shouting" voicings (close
harmony with voice-leading that slides chromatically).
"""

from ..terrain import ScaleDegree, RhythmicSkeleton, Terrain

GOSPEL = Terrain(
    name="gospel",
    description=(
        "The sanctuary. Diatonic lattice enriched with chromatic passing "
        "tones and extended harmony. The Hammond B3 organ is the "
        "gravitational engine. V→I resolution is the dominant pull, but "
        "the journey is extended and ornamented — delaying arrival creates "
        "emotional power. Call-and-response topology. Church swing with "
        "deep backbeat pocket."
    ),
    scale_degrees=[
        # Full diatonic plus characteristic chromatic additions
        ScaleDegree(0, 1.0, "tonic"),
        ScaleDegree(1, 0.35, "flat 2"),       # passing / chromatic approach
        ScaleDegree(2, 0.82, "major 2nd"),
        ScaleDegree(3, 0.6, "minor 3rd"),     # blues inflection
        ScaleDegree(4, 0.92, "major 3rd"),    # primary chord color
        ScaleDegree(5, 0.85, "perfect 4th"),
        ScaleDegree(6, 0.4, "tritone"),       # passing / diminished
        ScaleDegree(7, 0.9, "perfect 5th"),
        ScaleDegree(8, 0.45, "flat 6"),       # secondary dominant territory
        ScaleDegree(9, 0.8, "major 6th"),
        ScaleDegree(10, 0.7, "minor 7th"),    # dominant 7th, blues color
        ScaleDegree(11, 0.6, "major 7th"),    # leading tone, IΔ7 color
    ],
    characteristic_intervals=[
        4,   # major third — the "major" in gospel's predominantly major sound
        5,   # perfect fourth — amen cadence
        7,   # perfect fifth — root motion
        2,   # major second — scalar motion, passing tones
        3,   # minor third — blues inflection
        11,  # major seventh — extended harmony color
        1,   # chromatic half-step — voice-leading slides
    ],
    rhythmic_skeletons=[
        RhythmicSkeleton(
            name="gospel_shuffle",
            # The church groove — swung 8ths with backbeat emphasis
            subdivisions=[0.67, 0.33] * 4,
            accents=[1, 3, 5, 7],  # backbeat-heavy
            swing=0.6,
        ),
        RhythmicSkeleton(
            name="hammond_b3_pulse",
            # Organ rhythmic pattern — syncopated chord stabs
            subdivisions=[0.5, 0.25, 0.25, 0.5, 0.25, 0.25],
            accents=[0, 2, 4],
            swing=0.5,
        ),
        RhythmicSkeleton(
            name="shout_chorus",
            # Full energy — driving quarter notes with anticipation
            subdivisions=[0.25] * 4,
            accents=[0, 1, 2, 3],
            swing=0.55,
        ),
        RhythmicSkeleton(
            name="devotional_slow",
            # Slow, sustained — for worship ballads
            subdivisions=[2.0, 2.0],
            accents=[0],
            swing=0.3,
        ),
    ],
    register_tendency=(36, 84),  # C2 to C5 — organ bass to soprano
    chromatic_density=0.25,      # chromaticism through passing tones
    typical_tempo=(70, 140),
)

# ── The Funnel ──
# V→I is the primary gravitational engine, but it's EXTENDED:
#   ii→V→I (standard gospel cadence)
#   iii→vi→ii→V→I (circle-of-fifths gospel run)
#   IV→V→I (plagal + authentic combined)
#
# The "shout" section is maximum gravitational acceleration:
#   Rapid harmonic rhythm, ascending chromatic bass line
#   Voice-leading slides (every chord moves by half step)
#   The entire ensemble drives toward the final V→I resolution
#
# The turnaround is a mini-funnel:
#   I → I7 → IV → iv → I → V → I
#   (I7 to IV is secondary dominant, iv is borrowed minor subdominant)
#
# ── The Holonomy ──
# Call-and-response is the primary loop:
#   Preacher (call) → Congregation (response)
#   Soloist (call) → Choir (response)
#   Organ (call) → Piano (response)
#   The "return" is always the answer — the completion of the statement.
#
# Song structure:
#   Verse → Chorus → Verse → Chorus → Bridge → Vamp (shout) → Coda
#   The vamp/shout section can extend indefinitely — it's the peak of
#   the gravitational field, and the return to the chorus is the resolution.
#
# ── The Rigidity ──
# MEDIUM:
#   - Harmonic language is prescribed (diatonic + secondary dominants)
#   - V→I resolution is expected (delaying it is the art)
#   - Call-and-response structure must be maintained
#   - The backbeat must be felt (beats 2 and 4)
# FLEXIBLE:
#   - Soloist can improvise freely within the harmonic framework
#   - Organ and piano can add personal vocabulary
#   - The vamp can extend for any length
#   - Emotional intensity guides structural decisions
#
# ── The Metronome ──
# 70-140 BPM with a deep pocket swing (0.5-0.6). Not straight,
# not fully swung — it's a "church feel" that's hard to notate.
# The backbeat (2 and 4) is STRONG. The congregation claps on it.
# The organ provides bass and harmonic rhythm. The drummer plays
# the pocket with fills at transitions. Tempo can slow for ballads
# or accelerate during the shout section.
#
# ── Depth Soundings ──
# - Thomas A. Dorsey, "Take My Hand, Precious Lord" — the father of gospel
# - Mahalia Jackson, "How I Got Over" — the voice
# - The Clark Sisters, "You Brought the Sunshine" — modern gospel
# - Kirk Franklin, "Stomp" — gospel meets hip-hop
# - Walter Hawkins, "Oh Happy Day" — gospel crossover
# - Aretha Franklin, "Amazing Grace" (live album) — the queen in church
