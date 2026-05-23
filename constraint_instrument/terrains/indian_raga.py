"""
Indian Raga Terrain — the sruti landscape.

The landscape: a 22-sruti (microtonal) lattice that is FAR more detailed
than the 12-tone equal-tempered grid. Each raga selects a specific subset
of these srutis (typically 5-7, occasionally more) and assigns them
hierarchical roles: vadi (most important), samvadi (second), anuvadi
(assenting), and vivadi (dissonant, avoided). The result is a terrain
where every note has a specific gravitational weight AND a specific
directional behavior.

The funnel is ASYMMETRIC and DIRECTION-DEPENDENT:
- Arohana (ascending): one set of allowed notes and their order
- Avarohana (descending): potentially a DIFFERENT set and order
- Some ragas have "vakra" (zigzag) paths — the scale is non-linear
- Some notes are approached only from above, others only from below
- The vadi and samvadi are the two deepest basins; everything flows
  toward or away from them

This is NOT a scale — it's a grammar. A raga specifies:
- Which notes to use (the lattice)
- How to move between them (the funnel)
- Which notes to emphasize (the gravity centers)
- How to begin and end phrases (syntax)
- The emotional rasa (aesthetic frame)
- The time of day/season for performance

The tala (rhythmic cycle) provides the metronome — but it's
non-isochronous: cycles of 7, 8, 10, 14, 16 beats with internal
groupings that are NOT uniform. The most common is teental (16 beats
in 4+4+4+4), but the variety is enormous.
"""

from ..terrain import ScaleDegree, RhythmicSkeleton, Terrain

INDIAN_RAGA = Terrain(
    name="indian_raga",
    description=(
        "The sruti landscape. A 22-sruti microtonal lattice where each raga "
        "selects a subset and assigns hierarchical roles. Direction-dependent "
        "funnel: ascending (arohana) and descending (avarohana) may use "
        "different notes and paths. The vadi is the primary gravity center. "
        "Tala provides non-isochronous rhythmic cycles. Maximum rigidity — "
        "the raga grammar is the tradition."
    ),
    scale_degrees=[
        # Bhairavi (morning raga) as canonical example — one of the most
        # popular ragas, uses all 12 notes in different combinations
        ScaleDegree(0, 1.0, "Sa (shadja)"),          # root — constant drone
        ScaleDegree(1, 0.45, "Komal Re (flat 2)"),   # used in descent
        ScaleDegree(2, 0.7, "Shuddha Re (natural 2)"),  # used in ascent
        ScaleDegree(3, 0.85, "Komal Ga (flat 3)"),    # vadi — primary gravity
        ScaleDegree(4, 0.5, "Shuddha Ga (natural 3)"),  # ascent only
        ScaleDegree(5, 0.8, "Ma (perfect 4th)"),
        ScaleDegree(6, 0.4, "Tivra Ma (sharp 4th)"), # occasional
        ScaleDegree(7, 0.82, "Pa (perfect 5th)"),     # samvadi
        ScaleDegree(8, 0.5, "Komal Dha (flat 6)"),    # descent emphasis
        ScaleDegree(9, 0.65, "Shuddha Dha (natural 6)"),
        ScaleDegree(10, 0.75, "Komal Ni (flat 7)"),   # important in descent
        ScaleDegree(11, 0.4, "Shuddha Ni (natural 7)"),  # ascent
    ],
    characteristic_intervals=[
        # Microtonal shades not capturable in 12-TET, but characteristic
        # intervals between the selected srutis:
        3,   # minor third — Sa to Komal Ga
        5,   # perfect fourth — Sa to Ma
        7,   # perfect fifth — Sa to Pa
        4,   # major third — Sa to Shuddha Ga (ascent)
        2,   # major second — Sa to Re
        10,  # minor seventh — Sa to Komal Ni
        # Characteristic phrases (pakad) are more important than intervals:
        # Ga Ma Dha Ni Sa (ascent) vs Sa Ni Dha Pa Ma Ga Re Sa (descent)
    ],
    rhythmic_skeletons=[
        RhythmicSkeleton(
            name="teental",
            # 16 beats in 4+4+4+4 grouping
            subdivisions=[0.25] * 16,
            accents=[0, 4, 8, 12],  # sam on beat 1 (accented), khali on 9
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="jhaptal",
            # 10 beats in 2+3+2+3 grouping
            subdivisions=[0.2] * 10,
            accents=[0, 2, 5, 7],
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="ektal",
            # 12 beats in 2+2+2+2+2+2 grouping (felt as 6+6)
            subdivisions=[1.0 / 6] * 12,
            accents=[0, 6],
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="alaap_free",
            # Pre-compositional free rhythm — no tala
            subdivisions=[1.0],
            accents=[0],
            swing=0.0,
        ),
    ],
    register_tendency=(43, 79),   # Sa around C#3 to G#4 (sitar/vocal range)
    chromatic_density=0.3,        # notes available but selection is strict
    typical_tempo=(30, 200),      # very slow alaap to fast gat
)

# ── The Funnel ──
# Direction-dependent gravity — the signature feature:
#
# Arohana (ascent): Sa Re Ga Ma Pa Dha Ni Sa↑
#   Each note pulls UPWARD toward the next. Pausing on Ga (vadi) is
#   acceptable but the overall flow is ascending. Some notes are
#   skipped in ascent (vakra).
#
# Avarohana (descent): Sa↑ Ni Dha Pa Ma Ga Re Sa
#   May include DIFFERENT notes (Bhairavi uses Komal Re in descent,
#   Shuddha Re in ascent). The descent has its own gravitational
#   character — often more ornate, more meend (slides).
#
# Vadi (sonant): The most important note — the primary gravity well.
#   Phrases tend to revolve around it, touch it frequently,
#   and use it as a resting point.
#
# Samvadi (consonant): The second most important — typically a 4th or
#   5th from the vadi. Creates a secondary gravity center.
#
# Nyasa swara: Landing note for phrases (often the vadi or samvadi).
#
# ── The Holonomy ──
# The raga is the loop. It's not a form in the Western sense — it's
# a MEANS of organizing all musical material.
#
# Performance structure:
#   Alaap (free rhythm, exploring the raga's territory)
#   → Jor (pulse introduced, still no tala)
#   → Jhala (fast, rhythmic, still no tala)
#   → Gat (composition in tala, tabla enters)
#   → Gat in faster tempi (drut)
#   The return to the gat's mukhra (opening phrase) after each
#   improvisational excursion is the primary structural return.
#
# ── The Rigidity ──
# VERY HIGH:
#   - Notes must follow the prescribed arohana/avarohana
#   - Vadi must be emphasized; vivadi must be avoided
#   - Phrase beginnings and endings follow conventions
#   - Meend (slides) must connect specific notes
#   - The rasa (emotional character) must be maintained
#   - Performance time restrictions (morning, evening, seasonal ragas)
# LOW in one dimension:
#   - Within the grammar, the improviser has enormous freedom
#   - The alaap section is entirely improvised (within raga rules)
#   - Tempo is flexible during alaap/jor/jhala
#
# ── The Metronome ──
# Non-isochronous! The tala cycles have internal groupings that are NOT
# equal. Teental (16 beats) is 4+4+4+4, but jhaptal (10) is 2+3+2+3,
# and rupak (7) is 3+2+2.
# The sam (beat 1 of the cycle) is the strongest gravitational point.
# The khali (wave/empty beat) creates a point of reduced gravity.
# The tabla player marks the tala with stroke patterns (theka).
# During alaap, there is NO metronome — time is elastic.
#
# ── Depth Soundings ──
# - Ravi Shankar, Raga Bhairavi — morning raga, deeply expressive
# - Ravi Shankar, Raga Yaman — evening raga, serene
# - Ali Akbar Khan, Raga Marwa — sunset raga, haunting
# - Shivkumar Sharma, Raga Bageshri — night raga, romantic
# - Hariprasad Chaurasia, Raga Jog — late night, sweet
# - Bhimsen Joshi, Raga Malkauns — deep night, majestic
