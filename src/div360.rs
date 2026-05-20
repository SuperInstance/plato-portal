/// Exact integer arithmetic for division by 360.
///
/// Computes `n / 360` with exact rational remainder using 128-bit intermediates,
/// returning (quotient, numerator_of_remainder) where remainder = rem/360.
/// This is useful for angle normalization without floating-point error.

/// Divide `n` by 360, returning (quotient, remainder) with `0 <= remainder < 360`.
/// Uses Euclidean division (remainder is always non-negative).
pub fn div360(n: i64) -> (i64, i64) {
    let q = n.div_euclid(360);
    let r = n.rem_euclid(360);
    (q, r)
}

/// Multiply `a * b` then divide by 360, returning (quotient, remainder).
/// Uses i128 to avoid overflow.
pub fn muldiv360(a: i64, b: i64) -> (i64, i64) {
    let product = (a as i128) * (b as i128);
    let q = product.div_euclid(360) as i64;
    let r = product.rem_euclid(360) as i64;
    (q, r)
}

/// Sum multiple angles (in integer degrees), return result mod 360.
pub fn sum_mod360(angles: &[i64]) -> i64 {
    let total: i128 = angles.iter().map(|&a| a as i128).sum();
    total.rem_euclid(360) as i64
}

/// Scale an angle `a` by rational `p/q` and return result mod 360, exact.
/// Returns None if q == 0.
pub fn scale_mod360(a: i64, p: i64, q: i64) -> Option<i64> {
    if q == 0 {
        return None;
    }
    // a * p / q mod 360 — exact if a*p divisible by q
    let numerator = (a as i128) * (p as i128);
    if numerator % (q as i128) != 0 {
        // Not exactly divisible; return floor mod 360
        let scaled = numerator / (q as i128);
        Some(scaled.rem_euclid(360) as i64)
    } else {
        let scaled = numerator / (q as i128);
        Some(scaled.rem_euclid(360) as i64)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn basic_division() {
        assert_eq!(div360(720), (2, 0));
        assert_eq!(div360(361), (1, 1));
        assert_eq!(div360(0), (0, 0));
        assert_eq!(div360(-1), (-1, 359)); // Euclidean: remainder >= 0
        assert_eq!(div360(359), (0, 359));
        assert_eq!(div360(360), (1, 0));
    }

    #[test]
    fn muldiv_no_overflow() {
        // 10^9 * 10^9 = 10^18, fits in i128 but not i64
        let (q, r) = muldiv360(1_000_000_000, 1_000_000_000);
        let product = 1_000_000_000_i128 * 1_000_000_000_i128;
        assert_eq!(q as i128, product / 360);
        assert_eq!(r as i128, product % 360);
    }

    #[test]
    fn sum_mod360_wraps_correctly() {
        assert_eq!(sum_mod360(&[90, 180, 90]), 0);
        assert_eq!(sum_mod360(&[350, 20]), 10);
        assert_eq!(sum_mod360(&[-10, 5]), 355);
    }

    #[test]
    fn scale_exact() {
        // 360 * 1/2 = 180
        assert_eq!(scale_mod360(360, 1, 2), Some(180));
        // 270 * 4/3 = 360 mod 360 = 0
        assert_eq!(scale_mod360(270, 4, 3), Some(0));
        // divide by zero
        assert_eq!(scale_mod360(90, 1, 0), None);
    }
}
