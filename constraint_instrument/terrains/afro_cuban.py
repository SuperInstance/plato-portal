"""
Afro-Cuban Terrain — clave country.

The landscape: a rhythmic lattice where the clave pattern IS the
fundamental constraint surface. Everything — melody, harmony,
phrasing — is organized in relation to the clave. The 2-3 or 3-2
clave creates two distinct halves of a cycle, and musicians must
know which side they're on at all times.

The pitch lattice is mostly diatonic with characteristic tensions:
montunos (repeated piano figures) outline chord tones with
chromatic approach notes. The bass plays tumbao — anticipating
the chord change on the "and of 2" and landing on the root on
beat 3. This creates a forward-pushing gravitational field where
harmony arrives BEFORE the downbeat.

The funnel operates on multiple simultaneous rhythmic levels:
- Clave (2-bar cycle, the master clock)
- Tumbao (bass pattern, harmonic rhythm)
- Cascara (side-drum pattern, timekeeping)
- Montuno (repeated piano figure, harmonic + rhythmic)
All interlock; the funnels at each level must align.

Rigidity is MEDIUM-HIGH. You must play "in clave" — the pattern
of strong and weak beats is fixed. Playing against the clave
(cruzado) is a serious error unless done deliberately and returned
from immediately. The harmonic rhythm is also relatively fixed.
"""

from ..terrain import ScaleDegree, RhythmicSkeleton, Terrain

AFRO_CUBAN = Terrain(
    name="afro_cuban",
    description=(
        "Clave country. The clave pattern is the fundamental constraint "
        "surface — everything is organized in relation to it. Tumbao bass "
        "anticipates chord changes, montunos outline chord tones, cascara "
        "keeps time. All rhythmic levels interlock. You must play in clave; "
        "playing against it (cruzado) is a serious error."
    ),
    scale_degrees=[
        # Diatonic major with Mixolydian tendency (flat 7 common)
        ScaleDegree(0, 1.0, "root"),
        ScaleDegree(2, 0.85, "major 2nd"),
        ScaleDegree(3, 0.55, "minor 3rd"),   # color from parallel minor
        ScaleDegree(4, 0.9, "major 3rd"),
        ScaleDegree(5, 0.82, "perfect 4th"),
        ScaleDegree(7, 0.92, "perfect 5th"),
        ScaleDegree(9, 0.78, "major 6th"),
        ScaleDegree(10, 0.7, "minor 7th"),    # Mixolydian flat 7
        ScaleDegree(11, 0.5, "major 7th"),    # less common, jazzier
    ],
    characteristic_intervals=[
        4,   # major third — primary chord color
        7,   # perfect fifth — root motion
        5,   # perfect fourth — montuno patterns
        3,   # minor third — parallel minor borrowings
        2,   # major second — scalar montuno motion
        10,  # minor seventh — dominant 7th color
    ],
    rhythmic_skeletons=[
        RhythmicSkeleton(
            name="clave_2_3",
            # 2-3 son clave: X . X . . X . . X . . . (2-bar cycle)
            # Represented as one bar with clave hits
            subdivisions=[0.167, 0.167, 0.167, 0.167, 0.167, 0.167,  # beat 1-3
                          0.167, 0.167, 0.167, 0.167, 0.167, 0.167],  # beat 4
            accents=[0, 2, 5, 6, 8, 10],  # 2-3 clave strikes
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="tumbao_bass",
            # Bass anticipates chord on "and of 2", root on beat 3
            subdivisions=[0.25, 0.25, 0.25, 0.25],
            accents=[1, 2],  # anticipation + root
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="cascara",
            # Standard cascara pattern (shell pattern on timbales)
            subdivisions=[0.125] * 16,
            accents=[0, 3, 4, 6, 8, 11, 12, 14],
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="montuno_2_3",
            # Repeated piano figure — syncopated against the clave
            subdivisions=[0.125] * 16,
            accents=[1, 3, 5, 7, 9, 11, 13, 15],  # off-beat emphasis
            swing=0.0,
        ),
    ],
    register_tendency=(36, 84),  # C2 to C5 — bass to piano range
    chromatic_density=0.15,
    typical_tempo=(90, 140),
)

# ── The Funnel ──
# The clave IS the funnel. Notes fall into the clave's gravitational
# wells — accented positions in the pattern.
#
# 2-3 son clave pattern (within a 2-bar cycle):
#   Bar 1: X . X . . (strikes on beat 1, "and of 2")
#   Bar 2: . X . X . . . (strikes on beat 2, "and of 3")
#
# Harmonic funnel:
#   I → IV → I → V → I (salsa standard)
#   I → V → I (simpler son/mambo)
#   ii → V → I (jazz-influenced Latin)
# The bass tumbao anticipates the IV chord by hitting it on "and of 2"
#   before the rest of the ensemble arrives on beat 3.
#
# ── The Holonomy ──
# The 2-bar clave cycle is the primary loop. Everything must align with it.
#   Returning to the top of the clave after a mambo section, a coro (chorus),
#   or a solo is the primary structural return.
#
# Song structure:
#   Intro → Verse (canto) → Coro/Pregón (call-response) → Mambo (montuno) → Coda
#   The coro-pregón section is the improvisational space.
#   The mambo section is the peak energy, full ensemble.
#
# ── The Rigidity ──
# MEDIUM-HIGH:
#   - Must play in clave (the pattern is fixed)
#   - Tumbao bass pattern is prescribed
#   - Montuno must outline the chord tones
#   - Harmonic rhythm is relatively fixed
# ALLOWED flexibility:
#   - Soloist can play freely over the rhythm section
#   - Singer can stretch phrasing within the clave
#   - Gear changes (tempo shifts) mark structural transitions
#
# ── The Metronome ──
# 90-140 BPM. The 4/4 meter is felt in 2 (two half-note beats per bar).
# Clave divides this into a 3+2 or 2+3 pattern over two bars.
# The pulse is straight (no swing) but deeply syncopated.
# The conga march (tumbadora) provides a secondary timekeeping layer.
#
# ── Depth Soundings ──
# - Beny Moré, "Que Buena Tú Tienes" — Cuban son
# - Tito Puente, "Oye Como Va" — Latin jazz standard
# - Celia Cruz, "La Vida Es Un Carnaval" — salsa queen
# - Los Van Van, songo — modern Cuban dance music
# - Eddie Palmieri, "Azúcar" — progressive salsa
# - Mongo Santamaria, "Watermelon Man" — Latin jazz crossover
