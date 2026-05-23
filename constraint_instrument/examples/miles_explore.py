"""Miles Mode — Explore the Frontier"""

from constraint_instrument import Instrument

inst = Instrument(mode="miles", voice="trumpet", terrain="modal")

# See where the unexplored territory is
frontier = inst.frontier(n=5)
print("=== Frontier Regions ===")
for f in frontier:
    print(f"  {f.coordinates}: distance={f.distance:.2f}, features={f.features}")

# Perform at the edge
solo = inst.perform(
    explore=True,
    anchor="so_what",
    risk=0.8,
    minutes=2,
)
print(f"\n=== Frontier Solo ===")
print(f"  Notes: {len(solo['notes'])}")
print(f"  Frontiers explored: {solo['frontiers_explored']}")

# Check originality
orig = inst.originality(last_n=10)
print(f"\n=== Originality Check ===")
print(f"  Score: {orig['score']:.3f}")
print(f"  Unique ratio: {orig['unique_ratio']:.3f}")
print(f"  {orig['message']}")

# Second exploration
solo2 = inst.perform(explore=True, risk=0.6, minutes=2)
orig2 = inst.originality()
print(f"\n  After 2nd solo: {orig2['score']:.3f}")

inst.render("miles_explore.wav")
print("\n  Saved: miles_explore.wav")
