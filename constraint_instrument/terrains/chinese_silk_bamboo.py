"""
Chinese Silk and Bamboo Terrain — five-element waters.

The landscape: a pentatonic lattice with five notes corresponding to
the wuxing (five elements: wood, fire, earth, metal, water). Each
degree has an elemental character and a specific gravitational
relationship to the others. The lattice is SPARSE — only 5 notes —
but the space between them is filled with ornamental nuance:
grace notes, slides, pitch bends, and vibrato create a continuous
surface over the discrete lattice.

The silk-and-bamboo (sizhu) ensemble: erhu (2-string fiddle), pipa
(lute), dizi (bamboo flute), yangqin (hammered dulcimer), ruan
(moon lute), and percussion. The texture is heterophonic — everyone
plays the SAME melody but with individual ornamentation and timing.
There are no chords, no harmony; the depth comes from the layered
individuality on a shared melodic skeleton.

The funnel follows the wuxing cycle:
- Gong (root/earth) → central, grounding
- Shang (2nd/metal) → clear, bright
- Jiao (3rd/wood) → sprouting, rising
- Zhi (5th/fire) → brilliant, energetic
- Yu (6th/water) → flowing, yielding
Each generates the next in the sheng (generating) cycle and
can be overcome in the ke (overcoming) cycle.

Rigidity is MEDIUM. The pentatonic lattice is fixed, but ornamentation
style is personal. The melody is shared but interpretation is free.
"""

from ..terrain import ScaleDegree, RhythmicSkeleton, Terrain

CHINESE_SILK_BAMBOO = Terrain(
    name="chinese_silk_bamboo",
    description=(
        "Five-element waters. A pentatonic lattice where five scale degrees "
        "correspond to the wuxing (wood, fire, earth, metal, water). "
        "Heterophonic texture — all instruments play the same melody with "
        "individual ornamentation. No harmony, no chords — depth comes from "
        "nuance, vibrato, and timing. The funnel follows the elemental "
        "generation cycle."
    ),
    scale_degrees=[
        # Gong mode (C pentatonic) as canonical example
        # Five notes = five elements
        ScaleDegree(0, 1.0, "Gong (earth/root)"),       # central, grounding
        ScaleDegree(2, 0.82, "Shang (metal/2nd)"),       # clear, resonant
        ScaleDegree(4, 0.78, "Jiao (wood/3rd)"),         # sprouting, rising
        ScaleDegree(7, 0.85, "Zhi (fire/5th)"),          # brilliant, energetic
        ScaleDegree(9, 0.8, "Yu (water/6th)"),           # flowing, yielding
    ],
    characteristic_intervals=[
        2,   # major second — Shang from Gong (earth→metal)
        4,   # major third — Jiao from Gong (earth→wood)
        3,   # minor third — Jiao from Shang (metal→wood)
        5,   # perfect fourth — Zhi from Jiao (wood→fire)
        7,   # perfect fifth — Zhi from Gong (earth→fire)
        9,   # major sixth — Yu from Gong (earth→water)
        2,   # major second — Yu from Zhi (fire→water, completing cycle)
    ],
    rhythmic_skeletons=[
        RhythmicSkeleton(
            name="sanban_free",
            # "Scattered beat" — free rhythm, rubato, ad-libitum
            # The traditional opening of many pieces
            subdivisions=[1.5, 0.5, 2.0, 1.0, 0.5, 1.5],
            accents=[0, 2],
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="manban_slow",
            # Slow section — 4/4 at slow tempo, beat 1 and 3 emphasized
            subdivisions=[0.25] * 4,
            accents=[0, 2],
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="zhongban_medium",
            # Medium tempo — flowing, the main body of the piece
            subdivisions=[0.25] * 4,
            accents=[0],
            swing=0.0,
        ),
        RhythmicSkeleton(
            name="kuaiban_fast",
            # Fast section — driving to climax
            subdivisions=[0.125] * 8,
            accents=[0, 4],
            swing=0.0,
        ),
    ],
    register_tendency=(55, 84),  # G3 to C5 — erhu and dizi core range
    chromatic_density=0.0,       # STRICTLY pentatonic
    typical_tempo=(40, 120),
)

# ── The Funnel ──
# The wuxing (five-element) cycle creates a circular gravitational field:
#
# Sheng (generating) cycle:
#   Wood (Jiao) → Fire (Zhi) → Earth (Gong) → Metal (Shang) → Water (Yu) → Wood
#   Each element generates/nourishes the next.
#   Musically: phrases tend to follow this directional flow.
#
# Ke (overcoming) cycle:
#   Wood (Jiao) → Earth (Gong) → Water (Yu) → Fire (Zhi) → Metal (Shang) → Wood
#   Each element controls/restrains the next.
#   Musically: deliberate jumps against the generating cycle create tension.
#
# Primary gravity wells:
#   Gong (root) is the center — phrases begin and end here
#   Zhi (5th) is the secondary center — important cadential arrival
#   Yu (6th) provides the "flow" — descending to Gong is the cadence
#
# ── The Holonomy ──
# The melodic form is the loop. Traditional forms:
#   Bada (Eight Great Pieces) — each has a fixed melodic skeleton
#   Sections: sanban (free) → manban (slow) → zhongban (medium) → kuaiban (fast)
#   The melody returns to Gong at the end of each phrase.
#   The overall arc is from free/slow to fast/dense, always returning to Gong.
#
# Heterophony as holonomy:
#   All instruments navigate the same melodic path but with different timing.
#   The "return" is hearing the same melody through a different instrument's
#   ornamentation — it's the same landscape seen from different angles.
#
# ── The Rigidity ──
# MEDIUM:
#   - Pentatonic lattice is fixed (no outside notes)
#   - Melodic skeleton of traditional pieces is prescribed
#   - Phrases must end on the correct degree (usually Gong or Zhi)
#   - Tempo progression (slow→fast) follows convention
# FLEXIBLE:
#   - Ornamentation is personal (vibrato, slides, grace notes)
#   - Timing within the phrase can be individual
#   - Heterophonic layering creates freedom within unity
#   - Improvisation happens through ornamentation, not new notes
#
# ── The Metronome ──
# Slow and flowing. 40-120 BPM. The pulse is steady but not rigid.
# The sanban (free rhythm) opening has NO metronome.
# As tempo increases through sections, the pulse becomes more defined.
# Percussion (ban/gong) provides timekeeping but gently.
# The feel is water-like — continuous, unforced, naturally flowing.
# No swing — the rhythm is even and circular.
#
# ── Depth Soundings ──
# - "Erquan Yingyue" (Moon Reflected on Second Spring) — erhu masterpiece
# - "Gaoshan Liushui" (High Mountains, Flowing Water) — guqin classic
# - "Zhonghua Liuban" — silk-and-bamboo ensemble standard
# - "Huanxisha" — pipa traditional
# - Jiangnan sizhu tradition — Shanghai tea-house music
# - "Yuzhou Changwan" (Boats in the Evening) — dizi showcase
