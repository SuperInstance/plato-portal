#include <stdio.h>
#include <math.h>
#include <assert.h>
#include <string.h>
#include "constraint_substrate.h"

#define TOLERANCE 1e-9

static int tests_passed = 0;
static int tests_failed = 0;

#define ASSERT_APPROX(a, b, tol, msg) do { \
    if (fabs((a) - (b)) < (tol)) { \
        tests_passed++; \
    } else { \
        tests_failed++; \
        printf("FAIL: %s: expected %f, got %f\n", msg, (double)(b), (double)(a)); \
    } \
} while(0)

#define ASSERT_TRUE(cond, msg) do { \
    if (cond) { tests_passed++; } \
    else { tests_failed++; printf("FAIL: %s\n", msg); } \
} while(0)

/* --- Lattice --- */

void test_lattice_snap_origin(void) {
    CsSnapResult r = cs_snap(0.0, 0.0, 3);
    ASSERT_APPROX(r.error, 0.0, 1e-12, "lattice origin error");
    ASSERT_APPROX(r.a, 0.0, 1e-12, "lattice origin x");
    ASSERT_APPROX(r.b, 0.0, 1e-12, "lattice origin y");
}

void test_lattice_snap_known(void) {
    CsSnapResult r = cs_snap(0.01, 0.99, 3);
    ASSERT_TRUE(r.error < 0.6, "lattice known error < covering radius");
}

void test_lattice_batch(void) {
    double xs[] = {0.0, 1.0, 0.0};
    double ys[] = {0.0, 0.0, 1.0};
    for (int i = 0; i < 3; i++) {
        CsSnapResult r = cs_snap(xs[i], ys[i], 3);
        ASSERT_TRUE(r.error < 1.0, "batch snap error");
    }
}

void test_lattice_hex_rounding(void) {
    CsSnapResult r = cs_snap(0.4, 0.2, 3);
    double d_origin = sqrt(0.4*0.4 + 0.2*0.2);
    ASSERT_TRUE(r.error <= d_origin + 1e-9, "hex rounding nearest");
}

void test_lattice_point_unchanged(void) {
    /* (1, 0) → lattice point (a=1, b=0) */
    CsSnapResult r1 = cs_snap(1.0, 0.0, 3);
    ASSERT_TRUE(r1.error < 1e-12, "lattice point (1,0) unchanged");

    /* (-0.5, sqrt3/2) → lattice point (a=0, b=1) */
    double sqrt3 = sqrt(3.0);
    CsSnapResult r2 = cs_snap(-0.5, sqrt3/2.0, 3);
    ASSERT_TRUE(r2.error < 1e-12, "lattice point (0,1) unchanged");

    /* (0.5, sqrt3/2) → lattice point (a=1, b=1) */
    CsSnapResult r3 = cs_snap(0.5, sqrt3/2.0, 3);
    ASSERT_TRUE(r3.error < 1e-12, "lattice point (1,1) unchanged");
}

/* --- Funnel --- */

void test_funnel_exponential_decay(void) {
    CsFunnelResult r = cs_funnel_step(1.0, 2.0, 1.0, 0.1);
    ASSERT_APPROX(r.epsilon, exp(-0.1), TOLERANCE, "funnel exponential decay");
}

void test_funnel_converges(void) {
    double current = 0.0;
    double target = 5.0;
    double eps = 1.0;
    for (int i = 0; i < 1000; i++) {
        CsFunnelResult r = cs_funnel_step(current, target, eps, 0.1);
        current = r.value;
        eps = r.epsilon;
    }
    ASSERT_TRUE(fabs(current - target) < 0.5, "funnel convergence");
}

void test_funnel_within_deadband(void) {
    CsFunnelResult r = cs_funnel_step(1.0, 1.05, 0.2, 0.1);
    ASSERT_APPROX(r.epsilon, 0.2 * exp(-0.1), TOLERANCE, "funnel within deadband epsilon");
    ASSERT_TRUE(r.value > 1.0, "funnel within deadband moves toward target");
}

void test_funnel_outside_deadband(void) {
    CsFunnelResult r = cs_funnel_step(0.0, 5.0, 1.0, 0.1);
    ASSERT_APPROX(r.value, 1.0, TOLERANCE, "funnel outside deadband step");
    ASSERT_APPROX(r.epsilon, exp(-0.1), TOLERANCE, "funnel outside deadband epsilon");
}

void test_funnel_epsilon_stays_positive(void) {
    double eps = 1.0;
    for (int i = 0; i < 10000; i++) {
        CsFunnelResult r = cs_funnel_step(0.0, 1.0, eps, 0.5);
        eps = r.epsilon;
    }
    ASSERT_TRUE(eps > 0.0, "exponential decay never reaches zero");
}

/* --- Holonomy --- */

void test_holonomy_zero_winding(void) {
    double vals[] = {1.0, 2.0, 3.0, 4.0};
    double w = cs_holonomy(vals, 4, 10.0);
    ASSERT_APPROX(w, 0.3, TOLERANCE, "holonomy zero winding");
}

void test_holonomy_full_wind(void) {
    double vals[] = {1.0, 3.0, 5.0, 7.0, 9.0, 1.0};
    double w = cs_holonomy(vals, 6, 10.0);
    ASSERT_APPROX(w, 1.0, TOLERANCE, "holonomy full winding");
}

void test_holonomy_empty(void) {
    double w = cs_holonomy(NULL, 0, 10.0);
    ASSERT_APPROX(w, 0.0, TOLERANCE, "holonomy empty");
}

/* --- Rigidity --- */

void test_rigidity_triangle(void) {
    CsEdge edges[] = {{0,1}, {1,2}, {0,2}};
    ASSERT_TRUE(cs_is_laman(3, edges, 3), "triangle is Laman");
}

void test_rigidity_not_laman(void) {
    CsEdge edges[] = {{0,1}};
    ASSERT_TRUE(!cs_is_laman(3, edges, 1), "single edge not Laman for n=3");
}

void test_rigidity_two_vertices(void) {
    CsEdge edges[] = {{0,1}};
    ASSERT_TRUE(cs_is_laman(2, edges, 1), "2 vertices + 1 edge is rigid");
}

void test_rigidity_single(void) {
    ASSERT_TRUE(!cs_is_laman(1, NULL, 0), "single vertex not rigid");
}

void test_rigidity_k4(void) {
    /* K4: 6 edges on 4 vertices, 2*4-3=5, too many for Laman */
    CsEdge edges[] = {{0,1},{0,2},{0,3},{1,2},{1,3},{2,3}};
    ASSERT_TRUE(!cs_is_laman(4, edges, 6), "K4 not Laman (redundantly rigid)");
}

void test_rigidity_minimally_rigid_4(void) {
    /* 4 vertices, 5 edges (2*4-3=5), properly distributed */
    CsEdge edges[] = {{0,1},{1,2},{2,3},{0,3},{0,2}};
    ASSERT_TRUE(cs_is_laman(4, edges, 5), "minimally rigid 4 vertices");
}

void test_rigidity_dense_subgraph(void) {
    /* K4 on 0-3 (6 edges > 2*4-3=5) plus edge to vertex 4 */
    CsEdge edges[] = {{0,1},{0,2},{0,3},{1,2},{1,3},{2,3},{3,4}};
    ASSERT_TRUE(!cs_is_laman(5, edges, 7), "dense subgraph fails Laman");
}

void test_rigidity_hinge(void) {
    /* Two triangles sharing vertex: 5 vertices, 6 edges, need 7 */
    CsEdge edges[] = {{0,1},{1,2},{0,2},{2,3},{3,4},{2,4}};
    ASSERT_TRUE(!cs_is_laman(5, edges, 6), "hinge not rigid");
}

/* --- Consensus --- */

void test_consensus_converges(void) {
    double vals[] = {1.0, 2.0, 3.0};
    double current[3];
    memcpy(current, vals, sizeof(vals));
    int converged = 0;
    for (int iter = 0; iter < 100; iter++) {
        CsConsensusResult r = cs_consensus(current, 3, 0.5);
        memcpy(current, r.values, sizeof(current));
        converged = r.converged;
        cs_consensus_free(r);
        if (converged) break;
    }
    ASSERT_TRUE(converged, "consensus converges");
    for (int i = 0; i < 3; i++) {
        ASSERT_APPROX(current[i], 2.0, 0.5, "consensus near mean");
    }
}

void test_consensus_already_converged(void) {
    double vals[] = {2.0, 2.0, 2.0};
    CsConsensusResult r = cs_consensus(vals, 3, 0.5);
    ASSERT_TRUE(r.converged, "identical values converged");
    for (int i = 0; i < 3; i++) {
        ASSERT_APPROX(r.values[i], 2.0, 1e-12, "consensus identity");
    }
    cs_consensus_free(r);
}

void test_consensus_empty(void) {
    CsConsensusResult r = cs_consensus(NULL, 0, 0.5);
    ASSERT_TRUE(r.converged, "empty consensus converged");
    ASSERT_TRUE(r.values == NULL, "empty consensus null values");
}

void test_consensus_circular_wraparound(void) {
    /* 0.1 and 9.9 with modulus 10: circular mean ~0.0, NOT 5.0 */
    double vals[] = {0.1, 9.9};
    CsConsensusResult r = cs_consensus_mod(vals, 2, 0.5, 10.0);
    double mean = (r.values[0] + r.values[1]) / 2.0;
    ASSERT_TRUE(mean < 2.0 || mean > 8.0, "circular mean near 0 mod 10, not 5");
    cs_consensus_free(r);
}

void test_consensus_circular_no_wrap(void) {
    double vals[] = {2.0, 3.0};
    CsConsensusResult r = cs_consensus_mod(vals, 2, 0.5, 10.0);
    double mean = (r.values[0] + r.values[1]) / 2.0;
    ASSERT_APPROX(mean, 2.5, 0.5, "circular no wrap like arithmetic");
    cs_consensus_free(r);
}

int main(void) {
    printf("Running constraint-substrate C tests...\n\n");

    /* Lattice */
    test_lattice_snap_origin();
    test_lattice_snap_known();
    test_lattice_batch();
    test_lattice_hex_rounding();
    test_lattice_point_unchanged();

    /* Funnel */
    test_funnel_exponential_decay();
    test_funnel_converges();
    test_funnel_within_deadband();
    test_funnel_outside_deadband();
    test_funnel_epsilon_stays_positive();

    /* Holonomy */
    test_holonomy_zero_winding();
    test_holonomy_full_wind();
    test_holonomy_empty();

    /* Rigidity */
    test_rigidity_triangle();
    test_rigidity_not_laman();
    test_rigidity_two_vertices();
    test_rigidity_single();
    test_rigidity_k4();
    test_rigidity_minimally_rigid_4();
    test_rigidity_dense_subgraph();
    test_rigidity_hinge();

    /* Consensus */
    test_consensus_converges();
    test_consensus_already_converged();
    test_consensus_empty();
    test_consensus_circular_wraparound();
    test_consensus_circular_no_wrap();

    printf("\n%d passed, %d failed\n", tests_passed, tests_failed);
    return tests_failed > 0 ? 1 : 0;
}
