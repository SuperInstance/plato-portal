"""
Classical Counterpoint Terrain — the engineered canal system.

The landscape: a strict diatonic lattice (7 notes, no chromatic alterations
in strict species counterpoint). The gravitational field is entirely
determined by the mode (major or minor) and the intervallic rules:
perfect consonances (unison, fifth, octave) for beginnings and endings,
imperfect consonances (thirds, sixths) for middles, and dissonances
(2nds, 4ths, 7ths, tritones) only as passing tones or prepared suspensions.

This is Fux's Gradus ad Parnassum: five species of increasingly complex
constraint surfaces, each adding a new layer of allowable motion.

The funnel is species-dependent:
  - Species 1: note-against-note, only consonances, mostly stepwise
  - Species 2: two notes against one, passing tones allowed
  - Species 3: four notes against one, more passing/neighbor tones
  - Species 4: syncopated (suspensions), dissonance on downbeat resolved
  - Species 5: florid, combines all previous species

The rigidity is MAXIMUM. Every interval is prescribed. Every motion
(conjunct or disjunct) has rules. Parallel perfect consonances are
forbidden. Direct (hidden) perfect consonances in outer voices are
forbidden. The tritone (augmented fourth / diminished fifth) must be
resolved by step in opposite directions. These are not guidelines —
they are the load-bearing walls of the structure.
"""

from ..terrain import ScaleDegree, RhythmicSkeleton, Terrain

CLASSICAL_COUNTERPOINT = Terrain(
    name="classical_counterpoint",
    description=(
        "The engineered canal system. Strict diatonic lattice with "
        "intervallic rules as load-bearing walls. Five species of "
        "increasingly complex constraint surfaces, from note-against-note "
        "to florid counterpoint. Every interval is prescribed, every motion "
        "has rules. The tritone must be resolved. Parallel fifths are "
        "forbidden. This is architecture, not improvisation."
    ),
    scale_degrees=[
        # Strict major diatonic — no chromatic alterations
        ScaleDegree(0, 1.0, "tonic / finalis"),
        ScaleDegree(2, 0.88, "supertonic"),
        ScaleDegree(4, 0.92, "mediant"),
        ScaleDegree(5, 0.9, "subdominant"),
        ScaleDegree(7, 0.95, "dominant"),
        ScaleDegree(9, 0.82, "submediant"),
        ScaleDegree(11, 0.7, "leading tone"),
    ],
    characteristic_intervals=[
        3,   # minor third — imperfect consonance
        4,   # major third — imperfect consonance
        5,   # perfect fourth — dissonant against bass, consonant in upper
        7,   # perfect fifth — perfect consonance, most restricted
        8,   # minor sixth — imperfect consonance
        9,   # major sixth — imperfect consonance
        2,   # major second — passing dissonance only
        12,  # octave — perfect consonance
    ],
    rhythmic_skeletons=[
        RhythmicSkeleton(
            name="species_1_whole_notes",
            subdivisions=[1.0],
            accents=[0],
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="species_2_half_notes",
            subdivisions=[0.5, 0.5],
            accents=[0],
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="species_3_quarter_notes",
            subdivisions=[0.25, 0.25, 0.25, 0.25],
            accents=[0],
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="species_4_syncopated",
            # Tied half+quarter creates suspension: dissonance → resolution
            subdivisions=[0.75, 0.25],
            accents=[1],  # accent on the resolution
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="species_5_florid",
            # Mixed values — the cantus firmus is still whole notes
            subdivisions=[0.5, 0.25, 0.25, 0.75, 0.25],
            accents=[0, 3],
            swing=0.0,
        ),
    ],
    register_tendency=(48, 77),  # C3 to F4 — typical two-voice range
    chromatic_density=0.0,       # STRICT: no chromaticism in species CP
    typical_tempo=(60, 80),      # MM half note = 60-80 (slow, deliberate)
)

# ── The Funnel ──
# The cantus firmus (fixed melody) IS the landscape. The counterpoint
# voice must navigate AROUND it according to intervallic rules:
#
#   Perfect consonances (P1, P5, P8): for beginnings and endings
#   Imperfect consonances (m3, M3, m6, M6): preferred for interior
#   Dissonances (m2, M2, P4, tritone, m7, M7): only as passing tones,
#     neighbor tones, or suspensions (species 4)
#
# Gravitational flow:
#   Leading tone (11) → tonic (0): STRONG pull, must resolve up
#   Subdominant (5) → mediant (4) or dominant (7): weaker pull
#   Supertonic (2) → tonic (0) or mediant (4): neighbor motion
#
# ── The Holonomy ──
# The counterpoint must begin and end on a perfect consonance
# (unison, fifth, or octave) against the cantus firmus.
# The penultimate bar must create a proper cadence:
#   Major mode: 2-3 (leading tone → tonic) in upper, 7-0 (subtonic → tonic) in lower
#   The loop is closed: the journey from consonance through controlled
#   dissonance back to consonance IS the musical form.
#
# ── The Rigidity ──
# MAXIMUM. These are not guidelines:
#   - No parallel perfect consonances (P5, P8) — ever
#   - No direct (hidden) P5 or P8 in outer voices approaching by similar motion
#   - No melodic tritone (augmented fourth) without resolution
#   - No melodic leap larger than a P5 (octave in extreme cases)
#   - Maximum two consecutive leaps; must be followed by stepwise motion
#   - Total range of any voice: one octave + rare extension
#   - Dissonances must be approached and left by step (except suspension)
#   - All parts must be singable (vocal idiom)
#
# ── The Metronome ──
# Strict, even, unwavering. No swing, no rubato, no flexibility.
# The cantus firmus moves in whole notes; the counterpoint moves in
# values determined by species. Time is ARCHITECTURAL.
# Tempo: MM half note = 60-80 (slow enough to hear every interval).
#
# ── Depth Soundings ──
# - Fux, Gradus ad Parnassum (1725) — the rulebook itself
# - Palestrina, Missa Papae Marcelli — Renaissance CP perfection
# - J.S. Bach, Two-Part Inventions — Baroque CP applied
# - J.S. Bach, Art of Fugue — maximal CP complexity
# - Mozart, Requiem — Classical-era CP in choral context
