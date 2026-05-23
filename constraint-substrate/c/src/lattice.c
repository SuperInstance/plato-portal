#include "constraint_substrate.h"
#include <math.h>

CsSnapResult cs_snap(double x, double y, uint32_t group_order) {
    (void)group_order;
    CsSnapResult result;
    double sqrt3 = sqrt(3.0);

    /* Approximate axial coordinates:
       x = a - b/2, y = b*sqrt3/2
       => b ≈ 2y/sqrt3, a ≈ x + y/sqrt3 */
    double b_approx = 2.0 * y / sqrt3;
    double a_approx = x + y / sqrt3;

    long b_lo = (long)floor(b_approx);
    long a_lo = (long)floor(a_approx);

    double best_dist_sq = 1e300;
    long best_a = 0;
    long best_b = 0;

    /* Check candidate lattice points in a small neighborhood */
    for (long da = -1; da <= 1; da++) {
        for (long db = -1; db <= 1; db++) {
            long a = a_lo + da;
            long b = b_lo + db;
            /* Cartesian coordinates of lattice point (a, b) */
            double px = (double)a - (double)b / 2.0;
            double py = (double)b * sqrt3 / 2.0;
            double dx = px - x;
            double dy = py - y;
            double dist_sq = dx * dx + dy * dy;
            if (dist_sq < best_dist_sq) {
                best_dist_sq = dist_sq;
                best_a = a;
                best_b = b;
            }
        }
    }

    result.a = (double)best_a - (double)best_b / 2.0;
    result.b = (double)best_b * sqrt3 / 2.0;
    result.error = sqrt(best_dist_sq);

    return result;
}
