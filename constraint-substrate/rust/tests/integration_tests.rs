//! Integration tests for constraint-substrate (Rust).

use constraint_substrate::{consensus, funnel, holonomy, lattice, rigidity};

const TOLERANCE: f64 = 1e-9;

// --- Lattice ---

#[test]
fn lattice_snap_origin() {
    let (sx, sy, err) = lattice::snap(0.0, 0.0, 3);
    assert!(err < 1e-12, "Origin should snap to itself, got err={err}");
    assert!((sx).abs() < 1e-12);
    assert!((sy).abs() < 1e-12);
}

#[test]
fn lattice_snap_known_1() {
    let (sx, sy, err) = lattice::snap(0.01, 0.99, 3);
    assert!(err < lattice::COVERING_RADIUS + 0.01, "Error should be small, got {err}");
}

#[test]
fn lattice_snap_known_2() {
    let x = (3.0_f64.sqrt()) / 2.0 + 0.01;
    let (sx, sy, err) = lattice::snap(x, 0.02, 3);
    assert!(err < lattice::COVERING_RADIUS + 0.01, "Error should be small, got {err}");
}

#[test]
fn lattice_batch() {
    let vals = vec![(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)];
    let results = lattice::snap_batch(&vals, 3);
    assert_eq!(results.len(), 3);
    for (sx, sy, err) in &results {
        assert!(err < &1.0, "Batch snap error too large: {err}");
    }
}

#[test]
fn covering_radius() {
    let cr = lattice::COVERING_RADIUS;
    assert!((cr - 1.0 / 3.0_f64.sqrt()).abs() < TOLERANCE);
}

#[test]
fn lattice_hex_rounding_nearest() {
    // Point (0.4, 0.2) — should snap to nearest lattice point
    let (sx, sy, err) = lattice::snap(0.4, 0.2, 3);
    let d_origin = (0.4_f64 * 0.4 + 0.2_f64 * 0.2).sqrt();
    assert!(err <= d_origin + 1e-9, "Should find nearest lattice point, got err={err}");
}

#[test]
fn lattice_point_unchanged() {
    let sqrt3 = 3.0_f64.sqrt();
    // (1, 0) → lattice point (a=1, b=0)
    let (sx, sy, err) = lattice::snap(1.0, 0.0, 3);
    assert!(err < 1e-12, "Lattice point (1,0) should snap to itself");
    // (-0.5, √3/2) → lattice point (a=0, b=1)
    let (sx, sy, err) = lattice::snap(-0.5, sqrt3 / 2.0, 3);
    assert!(err < 1e-12, "Lattice point (0,1) should snap to itself");
    // (0.5, √3/2) → lattice point (a=1, b=1)
    let (sx, sy, err) = lattice::snap(0.5, sqrt3 / 2.0, 3);
    assert!(err < 1e-12, "Lattice point (1,1) should snap to itself");
}

// --- Funnel ---

#[test]
fn funnel_exponential_decay() {
    // exp(-0.1) ≈ 0.9048, NOT 0.9 (linear)
    let (_, eps) = funnel::step(1.0, 2.0, 1.0, 0.1);
    assert!((eps - (-0.1_f64).exp()).abs() < TOLERANCE, "Epsilon must decay exponentially");
}

#[test]
fn funnel_step_converges() {
    let mut current = 0.0;
    let target = 5.0;
    let mut eps = 1.0;
    for _ in 0..1000 {
        let (c, e) = funnel::step(current, target, eps, 0.1);
        current = c;
        eps = e;
    }
    assert!(
        (current - target).abs() < 0.5,
        "Funnel should converge toward target, got {current}"
    );
}

#[test]
fn funnel_within_deadband() {
    let (val, new_eps) = funnel::step(1.0, 1.05, 0.2, 0.1);
    // new_eps = 0.2 * exp(-0.1) ≈ 0.1810
    assert!((new_eps - 0.2 * (-0.1_f64).exp()).abs() < TOLERANCE, "Epsilon should decay exponentially");
    assert!(val > 1.0, "Value should move toward target");
}

#[test]
fn funnel_outside_deadband() {
    let (val, new_eps) = funnel::step(0.0, 5.0, 1.0, 0.1);
    assert!((val - 1.0).abs() < TOLERANCE, "Should step by epsilon");
    assert!((new_eps - (-0.1_f64).exp()).abs() < TOLERANCE, "Epsilon should decay exponentially");
}

#[test]
fn funnel_batch() {
    let currents = &[0.0, 10.0];
    let targets = &[5.0, 5.0];
    let epsilons = &[1.0, 1.0];
    let (vals, eps) = funnel::step_batch(currents, targets, epsilons, 0.1);
    assert_eq!(vals.len(), 2);
    assert_eq!(eps.len(), 2);
    for e in &eps {
        assert!((e - (-0.1_f64).exp()).abs() < TOLERANCE);
    }
}

#[test]
fn funnel_epsilon_stays_positive() {
    let mut eps = 1.0;
    for _ in 0..10000 {
        (_, eps) = funnel::step(0.0, 1.0, eps, 0.5);
    }
    assert!(eps > 0.0, "Exponential decay never reaches zero");
}

// --- Holonomy ---

#[test]
fn holonomy_zero_winding() {
    let vals = [1.0, 2.0, 3.0, 4.0];
    let w = holonomy::winding(&vals, 10.0);
    assert!((w - 0.3).abs() < TOLERANCE, "Expected winding 0.3, got {w}");
}

#[test]
fn holonomy_one_winding() {
    let vals = [0.5_f64, 9.5_f64];
    let w = holonomy::winding(&vals, 10.0);
    assert!((w - (-0.1)).abs() < TOLERANCE, "Expected winding -0.1, got {w}");
}

#[test]
fn holonomy_full_wind() {
    let vals = [1.0, 3.0, 5.0, 7.0, 9.0, 1.0];
    let w = holonomy::winding(&vals, 10.0);
    assert!((w - 1.0).abs() < TOLERANCE, "Should have winding 1.0, got {w}");
}

#[test]
fn holonomy_empty() {
    let w = holonomy::winding(&[], 10.0);
    assert!((w).abs() < TOLERANCE);
}

// --- Rigidity ---

#[test]
fn rigidity_laman_triangle() {
    let edges = vec![(0, 1), (1, 2), (0, 2)];
    assert!(rigidity::is_laman(3, &edges), "Triangle should be Laman-rigid");
}

#[test]
fn rigidity_not_laman() {
    let edges = vec![(0, 1)];
    assert!(!rigidity::is_laman(3, &edges), "Should not be rigid");
}

#[test]
fn rigidity_two_vertices() {
    let edges = vec![(0, 1)];
    assert!(rigidity::is_laman(2, &edges), "2 vertices + 1 edge is rigid");
}

#[test]
fn rigidity_single_vertex() {
    assert!(!rigidity::is_laman(1, &[]), "Single vertex not rigid");
}

#[test]
fn rigidity_k4_not_laman() {
    // K4 has 6 edges on 4 vertices, 2*4-3=5, too many for minimal Laman
    assert!(!rigidity::is_laman(4, &[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]));
}

#[test]
fn rigidity_minimally_rigid_4() {
    // 4 vertices, 5 edges (2*4-3=5), properly distributed
    assert!(rigidity::is_laman(4, &[(0,1),(1,2),(2,3),(0,3),(0,2)]));
}

#[test]
fn rigidity_dense_subgraph() {
    // K4 on vertices 0-3 (6 edges > 2*4-3=5), plus edge to vertex 4
    // Total 7 edges = 2*5-3, passes edge count, but subgraph is too dense
    let edges = vec![(0,1),(0,2),(0,3),(1,2),(1,3),(2,3),(3,4)];
    assert!(!rigidity::is_laman(5, &edges), "Dense subgraph should fail Laman");
}

#[test]
fn rigidity_hinge_not_rigid() {
    // Two triangles sharing one vertex: 5 vertices, 6 edges. Need 7.
    let edges = vec![(0,1),(1,2),(0,2),(2,3),(3,4),(2,4)];
    assert!(!rigidity::is_laman(5, &edges), "Hinge should not be rigid");
}

// --- Consensus ---

#[test]
fn consensus_converges() {
    let vals = [1.0, 2.0, 3.0];
    let epsilon = 0.5;
    let mut current = vals.to_vec();
    let mut converged = false;
    for _ in 0..100 {
        let (new_vals, conv) = consensus::round(&current, epsilon, None);
        current = new_vals;
        converged = conv;
        if converged {
            break;
        }
    }
    assert!(converged, "Consensus should converge");
    for v in &current {
        assert!((v - 2.0).abs() < 0.5, "Values should be near mean, got {v}");
    }
}

#[test]
fn consensus_already_converged() {
    let vals = [2.0, 2.0, 2.0];
    let (new_vals, converged) = consensus::round(&vals, 0.5, None);
    assert!(converged, "Identical values should be converged");
    for v in &new_vals {
        assert!((v - 2.0).abs() < TOLERANCE);
    }
}

#[test]
fn consensus_empty() {
    let (vals, converged) = consensus::round(&[], 0.5, None);
    assert!(converged);
    assert!(vals.is_empty());
}

#[test]
fn consensus_circular_mean_wraparound() {
    // Values near boundary: 0.1 and 9.9 with modulus 10
    // Circular mean should be ~0.0 (not 5.0 from arithmetic mean).
    // Run multiple rounds to converge.
    let mut vals = vec![0.1, 9.9];
    for _ in 0..20 {
        let (new_vals, _) = consensus::round(&vals, 0.5, Some(10.0));
        vals = new_vals;
    }
    // After convergence, both values should be near 0.0 (mod 10)
    let circular_mean = vals.iter().sum::<f64>() / vals.len() as f64;
    // Use circular distance: should be near 0 or near 10
    let dist = if circular_mean > 5.0 { 10.0 - circular_mean } else { circular_mean };
    assert!(dist < 1.0, "Circular mean should be near 0 (mod 10), got {circular_mean}, distance from 0 = {dist}");
}

#[test]
fn consensus_circular_mean_no_wrap() {
    let (vals, _) = consensus::round(&[2.0, 3.0], 0.5, Some(10.0));
    let mean = vals.iter().sum::<f64>() / vals.len() as f64;
    assert!((mean - 2.5).abs() < 0.5, "Non-wrapping values should behave like arithmetic mean");
}
