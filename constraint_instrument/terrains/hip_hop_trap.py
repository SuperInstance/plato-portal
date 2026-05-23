"""
Hip-Hop / Trap Terrain — the low-end topography.

The landscape: a sparse melodic lattice (minor pentatonic shell) over a
MASSIVE bass territory. The 808 kick drum defines the gravitational center
— it's not just rhythm, it's the fundamental frequency that everything
orbits around. The bass can sustain indefinitely (808 decay), creating
a drone-like gravity that pulls the entire harmonic field toward the root.

Melodically sparse. Often just 2-4 notes in the main melodic element.
The space between notes is as important as the notes — silence and
rhythm carry the music. Hi-hat patterns (especially the trap hi-hat
roll with its rapid 16th/32nd notes and irregular accents) create a
secondary rhythmic lattice that the melody navigates around.

The funnel is simple: root and fifth are deep basins, minor third
provides color. The bass (often an 808 sine wave with saturation)
creates such a strong fundamental that the entire harmonic field
collapses toward it. Upper notes are decorative — they exist in
orbit around the bass.

Rigidity is LOW harmonically (any notes work over the 808) but
HIGH rhythmically (the trap grid is precise). Double-time subdivisions
(hi-hat rolls, rapid snare fills) create a dense rhythmic lattice.
"""

from ..terrain import ScaleDegree, RhythmicSkeleton, Terrain

HIP_HOP_TRAP = Terrain(
    name="hip_hop_trap",
    description=(
        "The low-end topography. Sparse minor pentatonic melodic shell "
        "over a massive 808 bass territory. The kick drum IS the "
        "gravitational center. Melodically minimal — 2-4 notes max — "
        "with rhythmic density from hi-hat rolls and double-time "
        "subdivisions. The bass sustains indefinitely, collapsing "
        "all harmony toward the root."
    ),
    scale_degrees=[
        ScaleDegree(0, 1.0, "root"),
        ScaleDegree(3, 0.8, "minor 3rd"),
        ScaleDegree(5, 0.75, "perfect 4th"),
        ScaleDegree(7, 0.9, "perfect 5th"),
        ScaleDegree(10, 0.7, "minor 7th"),
        # Optional color notes (used sparingly)
        ScaleDegree(1, 0.3, "flat 2"),      # dark color
        ScaleDegree(6, 0.35, "tritone"),    # tension
        ScaleDegree(8, 0.3, "flat 6"),      # melancholy
    ],
    characteristic_intervals=[
        3,   # minor third — the primary color
        5,   # perfect fourth — melodic step
        7,   # perfect fifth — power interval
        2,   # major second — scalar motion
        12,  # octave — bass drops, melodic leaps
    ],
    rhythmic_skeletons=[
        RhythmicSkeleton(
            name="trap_bounce",
            # Kick on 1, snare on 3, hi-hat throughout
            subdivisions=[0.25] * 16,
            accents=[0, 8],  # kick on 1, snare on 3 (in double time)
            swing=0.15,
        ),
        RhythmicSkeleton(
            name="hi_hat_roll",
            # Rapid fire hi-hats with irregular accents
            subdivisions=[0.0625] * 32,  # 32nd notes
            accents=[0, 3, 7, 12, 16, 20, 24, 28],  # irregular
            swing=0.1,
        ),
        RhythmicSkeleton(
            name="808_pattern",
            # Long sustained bass with rhythmic gaps
            subdivisions=[0.5, 0.25, 0.25, 0.5, 0.5],
            accents=[0, 2],  # bass hit points
            swing=0.2,
        ),
        RhythmicSkeleton(
            name="triplet_flow",
            # Migos-style triplet flows
            subdivisions=[1.0 / 6] * 12,
            accents=[0, 2, 4, 6, 8, 10],
            swing=0.3,
        ),
    ],
    register_tendency=(24, 60),   # C1 to C4 — LOW (808 lives in C1-E2 range)
    chromatic_density=0.2,
    typical_tempo=(130, 170),
)

# ── The Funnel ──
# The 808 bass defines gravitational center:
#   Root (degree 0) is the primary attractor — the 808 hits and sustains
#   Fifth (degree 7) is the secondary attractor — harmonic support
#   Minor third (degree 3) provides emotional color
#
# Bass movement patterns:
#   Root → flat 7 → root (descending neighbor)
#   Root → 5th → root (V-I motion)
#   Root → minor 3rd → 4th → root (common melodic bass)
#
# Melodic elements are in orbit around the bass — they can be
# harmonically ambiguous because the 808 defines the root so strongly.
#
# ── The Holonomy ──
# Loop-based structure:
#   4-bar or 8-bar beat loop (the instrumental)
#   Verse (16 bars typically) → Hook/Chorus (8 bars) → Verse → Hook → Outro
#   The loop returns to the same beat pattern every 4-8 bars
#
# The beat IS the terrain — it loops and the rapper/singer navigates over it.
# Variations come from:
#   - Adding/removing elements (hi-hats, ad-libs, 808 slides)
#   - 808 pattern changes (drop, slide, sustain)
#   - Vocal density variations
#
# ── The Rigidity ──
# LOW harmonically:
#   - Minimal harmonic constraint — the 808 root is enough
#   - Melodic elements can be sparse or dense
#   - Chromaticism is rare but not forbidden
# HIGH rhythmically:
#   - Grid is precise (quantized to 16th or 32nd notes)
#   - Hi-hat patterns are mathematically complex
#   - 808 must hit on time — the bass IS the time
#   - Vocal flow must align with the beat grid
#
# ── The Metronome ──
# 130-170 BPM, felt in half-time (65-85 BPM perceived).
# The hi-hat operates in double-time (260-340 BPM subdivisions).
# Swing is subtle (0.1-0.2) — more of a feel than a pronounced lilt.
# The metronome is the DAW grid — quantized, precise, relentless.
# Human feel comes from slight timing variations, not swing.
#
# ── Depth Soundings ──
# - Metro Boomin, "Mask Off" (Future) — the flute + 808 archetype
# - 808 Mafia, production style — 808 slides and layered hi-hats
# - Travis Scott, "SICKO MODE" — beat switches as terrain changes
# - Migos, "Bad and Boujee" — triplet flow over sparse beat
# - Drake, "God's Plan" — melodic trap
# - Lex Luger, early trap production — the foundation
