"""Goodman Mode — Diagnose What's Missing"""

from constraint_instrument import Instrument

# First, create a performance to analyze (using Parker mode)
parker = Instrument(mode="parker", voice="sax", terrain="blues")
solo = parker.perform(changes="blues_12", minutes=1)

# Now switch to Goodman for diagnosis
inst = Instrument(mode="goodman", voice="sax", terrain="blues")

# Diagnose the solo
report = inst.diagnose(solo["notes"])

print("=== Diagnostic Report ===")
print(f"\n  0th order (POSITION):     {report.stars['POSITION']}  {report.details['POSITION']}")
print(f"  1st order (DIRECTION):    {report.stars['DIRECTION']}  {report.details['DIRECTION']}")
print(f"  2nd order (CURVATURE):    {report.stars['CURVATURE']}  {report.details['CURVATURE']}")
print(f"  3rd order (STRUCTURE):    {report.stars['STRUCTURE']}  {report.details['STRUCTURE']}")
print(f"\n  Weakest: order {report.weakest_order}")
print(f"\n  RECOMMENDATION:")
print(f"    {report.recommendation}")

# Get a prescription for the weakest order
rx = inst.prescribe(missing_order=report.weakest_order)
print(f"\n=== Prescription for Order {rx.order} ({rx.focus}) ===")
print(f"  {rx.description}")
print(f"  Exercises: {', '.join(rx.exercises)}")
