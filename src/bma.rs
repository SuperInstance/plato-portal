/// Berlekamp-Massey algorithm over GF(2).
///
/// Given a binary sequence, finds the shortest LFSR that generates it.
/// Returns the connection polynomial C(x) as a Vec<u8> (coefficients in GF(2)),
/// where C[0] = 1 always, and the length (degree) of the LFSR.

/// Run Berlekamp-Massey on a binary sequence.
/// Returns (lfsr_polynomial, lfsr_length).
/// The polynomial is stored as a bit vector: poly[i] is the coefficient of x^i.
/// poly[0] is always 1. Length is the degree of the polynomial.
pub fn berlekamp_massey(s: &[u8]) -> (Vec<u8>, usize) {
    let n = s.len();
    // C: current connection polynomial, L: current length
    // B: previous connection polynomial at last length change
    let mut c = vec![0u8; n + 1];
    let mut b = vec![0u8; n + 1];
    c[0] = 1;
    b[0] = 1;
    let mut l = 0usize;
    let mut m = 1usize; // steps since last length change
    let mut b_coeff = 1u8; // leading coefficient of B (always 1 in GF(2))

    for n_idx in 0..n {
        // Compute discrepancy d
        let mut d: u8 = s[n_idx];
        for i in 1..=l {
            d ^= c[i] & s[n_idx - i];
        }

        if d == 0 {
            m += 1;
        } else if 2 * l <= n_idx {
            // Update length and polynomials
            let t = c.clone();
            // C(x) = C(x) - d * b_coeff^-1 * x^m * B(x)
            // In GF(2), b_coeff is always 1, d is 1, so: C(x) ^= x^m * B(x)
            let _ = b_coeff; // always 1 in GF(2)
            for i in 0..=n {
                if m + i <= n {
                    c[m + i] ^= d & b[i];
                }
            }
            l = n_idx + 1 - l;
            b = t;
            m = 1;
        } else {
            // C(x) ^= x^m * B(x) (d=1, b_coeff=1 in GF(2))
            for i in 0..=n {
                if m + i <= n {
                    c[m + i] ^= d & b[i];
                }
            }
            m += 1;
        }
    }

    c.truncate(l + 1);
    (c, l)
}

/// Generate the next bit of an LFSR given connection polynomial and current state.
/// `state` is stored oldest-first: state[0] = s[n-L], ..., state[L-1] = s[n-1].
/// The polynomial `poly` has poly[0]=1, poly[i] is the coefficient of x^i.
/// The LFSR recurrence is: s[n] = sum_{i=1}^{L} poly[i] * s[n-i].
pub fn lfsr_next(poly: &[u8], state: &[u8]) -> u8 {
    let l = poly.len() - 1;
    assert_eq!(state.len(), l);
    let mut out = 0u8;
    for i in 1..=l {
        // poly[i] multiplies s[n-i] = state[L-i]
        out ^= poly[i] & state[l - i];
    }
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn all_zeros() {
        let s = vec![0u8; 8];
        let (poly, l) = berlekamp_massey(&s);
        assert_eq!(l, 0);
        assert_eq!(poly, vec![1]);
    }

    #[test]
    fn single_bit() {
        // Sequence 1,0,0,0,... has LFSR length 1
        let s = vec![1, 0, 0, 0, 0, 0, 0, 0];
        let (poly, l) = berlekamp_massey(&s);
        assert_eq!(l, 1);
        assert_eq!(poly[0], 1);
    }

    #[test]
    fn maximal_length_lfsr_degree3() {
        // x^3 + x + 1 generates the sequence: 1,1,1,0,1,0,0 (period 7)
        // State: 1,1,1 → next = s[0]^s[2] = 1^1=0... let me just use a known sequence
        // ML sequence for x^3+x+1: 1,1,1,0,1,0,0,1,1,1,0,1,0,0,...
        let s = vec![1u8, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0];
        let (_poly, l) = berlekamp_massey(&s);
        assert_eq!(l, 3, "LFSR length should be 3 for degree-3 ML sequence");
    }

    #[test]
    fn alternating_sequence() {
        // 1,0,1,0,1,0 has LFSR: C(x) = 1 + x^2 (s[n] = s[n-2]), length 2.
        // The alternating sequence repeats every 2 positions, so the minimal
        // LFSR has length 2 with connection polynomial 1 + x^2.
        let s = vec![1u8, 0, 1, 0, 1, 0, 1, 0];
        let (poly, l) = berlekamp_massey(&s);
        assert_eq!(l, 2, "alternating sequence needs L=2: s[n] = s[n-2]");
        // verify poly generates the sequence
        // lfsr_next uses state[0..l] where poly[i] maps to state[i-1]
        // Initialize state from the first L elements of the sequence
        let mut state: Vec<u8> = s[..l].to_vec();
        for i in l..s.len() {
            let next = lfsr_next(&poly, &state);
            assert_eq!(next, s[i], "mismatch at position {i}");
            state.remove(0);
            state.push(next);
        }
    }
}
