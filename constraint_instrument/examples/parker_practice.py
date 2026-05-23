"""Parker Mode — Practice and Internalize"""

from constraint_instrument import Instrument

# Create the instrument
inst = Instrument(mode="parker", voice="sax", terrain="bebop")

# Practice specific vocabulary
sessions = inst.practice(
    focus="chromatic_enclosure",
    tempo=220,
    sessions=5,
)

print("=== Practice Sessions ===")
for s in sessions:
    print(f"  {s.focus}: accuracy={s.accuracy:.2f}, "
          f"internalization={s.internalization:.2f}, "
          f"reps={s.repetitions}")

# Feel a trajectory through pitch space
traj = inst.feel_trajectory("ii-V-I", voiceleading="smooth", register="tenor")
print(f"\n=== Trajectory: ii-V-I ===")
print(f"  Path: {traj.path}")
print(f"  Curvature: {[round(c, 2) for c in traj.curvature]}")

# Perform a solo
solo = inst.perform(changes="rhythm", minutes=1)
print(f"\n=== Solo Performance ===")
print(f"  Notes: {len(solo['notes'])}")
print(f"  Tempo: {solo['tempo']} BPM")
print(f"  Internalization: {solo['internalization']:.2f}")

# Render to audio
inst.render("parker_solo.wav")
print("\n  Saved: parker_solo.wav")
