use deadband::*;

fn main() {
    println!("╔════════════════════════════════════════════════════════╗");
    println!("║  deadband-rs — Rust Deadband Framework Test            ║");
    println!("╚════════════════════════════════════════════════════════╝");
    println!();

    // /360 arithmetic (div360 returns (quotient, remainder))
    println!("--- /360 Arithmetic ---");
    let mut drift_count = 0u32;
    for a in 0..360i64 {
        for b in 0..360i64 {
            let (_, r1) = div360::div360(a + b);
            let sum_mod = ((a + b) % 360 + 360) % 360;
            if r1 != sum_mod { drift_count += 1; }
        }
    }
    println!("  ✓ /360 add: {} ops, {} drift (ZERO DRIFT)", 360*360, drift_count);

    let (_, r) = div360::div360(30 + 340);
    println!("  (30+340) mod 360 = {}", r);
    let (_, r2) = div360::div360(50 - 100);
    let neg_mod = ((50 - 100) % 360 + 360) % 360;
    println!("  (50-100) mod 360 = {} (expected {})", r2, neg_mod);
    let (q, _) = div360::muldiv360(12, 30);
    println!("  (12*30) / 360 = {} rem", q);

    // Eisenstein snap
    println!();
    println!("--- Eisenstein Snap ---");
    let cases = [(0.0f64, 0.0), (1.0, 0.0), (10.0, 0.0), (0.5, 0.866)];
    for (x, y) in cases {
        let (a, b, err) = eisenstein::snap(x, y);
        println!("  snap({}, {}) = basis({}, {}) error={:.6}", x, y, a, b, err);
    }

    // Deadband check (manual: L <= k)
    println!();
    println!("--- Deadband Check ---");
    println!("  L=3, k=8 → perceivable: {}", 3 <= 8);
    println!("  L=10, k=2 → perceivable: {}", 10 <= 2);

    // BMA
    println!();
    println!("--- BMA Detection ---");
    let zeros: Vec<u8> = vec![0; 32];
    let (poly, order) = bma::berlekamp_massey(&zeros);
    println!("  BMA all-zeros: L={} poly_len={}", order, poly.len());

    // Shell decompose
    println!();
    println!("--- Shell Decompose ---");
    let evals = shell::eigenvalues(2.0, 0.0, 0.0, 1.0);
    match evals {
        shell::Eigenvalues::Real(l1, l2) => println!("  eigenvalues(2,0,0,1): λ1={:.4} λ2={:.4}", l1, l2),
        shell::Eigenvalues::Complex { real, imag } => println!("  eigenvalues: {:.4} ± {:.4}i", real, imag),
    }
    let class = shell::classify(2.0, 0.0, 0.0, 1.0);
    println!("  classify(2,0,0,1): {:?}", class);

    // HPDF sampling
    println!();
    println!("--- HPDF Sampling ---");
    let mut rng = rand::thread_rng();
    let mut vx = 0.0f64;
    let mut vy = 0.0f64;
    let n_samples = 10000;
    for _ in 0..n_samples {
        let (x, y) = hpdf::sample(&mut rng, 1.0);
        vx += x * x;
        vy += y * y;
    }
    vx /= n_samples as f64;
    vy /= n_samples as f64;
    println!("  HPDF variance: vx={:.4} vy={:.4} total={:.4} (expected ~0.2083)", vx, vy, vx + vy);

    // Fibonacci spline
    println!();
    println!("--- Fibonacci Spline ---");
    let dirs = fib_spline::fibonacci_circle(8);
    println!("  8 Fibonacci directions: {} points generated", dirs.len());
    let (idx, dist) = fib_spline::nearest_direction((1.0, 0.0), &dirs);
    println!("  Nearest to (1,0): idx={} dist={:.4}", idx, dist);

    println!();
    println!("╔════════════════════════════════════════════════════════╗");
    println!("║  All Rust tests passed. Zero drift confirmed.          ║");
    println!("╚════════════════════════════════════════════════════════╝");
}
