program benchmark_fortran
    use iso_fortran_env
    implicit none
    
    call run_all_benchmarks()
    
contains

    subroutine run_all_benchmarks()
        print *, "=== Fortran Quality Benchmark ==="
        call q1_precision()
        call q2_consistency()
        call q3_linearity()
        call q4_smoothness()
        call q5_spectral()
        call q6_temporal_drift()
        call q7_accumulation()
        call q8_edge_cases()
        call q9_cross_config()
        call q10_error_entropy()
    end subroutine

    subroutine q1_precision()
        real(real64) :: pi
        pi = 16.0d0 * atan(1.0d0/5.0d0) - 4.0d0 * atan(1.0d0/239.0d0)
        print *, "  Q1: pi =", pi
    end subroutine

    subroutine q2_consistency()
        real(real64) :: val, sm, sm2, mean, variance
        integer :: i
        sm = 0.0d0; sm2 = 0.0d0
        do i = 1, 10000
            val = sin(1.0d0)
            sm = sm + val
            sm2 = sm2 + val*val
        end do
        mean = sm / 10000.0d0
        variance = sm2 / 10000.0d0 - mean*mean
        print *, "  Q2: variance =", variance
    end subroutine

    subroutine q3_linearity()
        real(real64) :: xs(5), computed
        integer :: i
        xs = [1.0d-10, 1.0d-5, 1.0d0, 1.0d5, 1.0d10]
        print *, "  Q3: Log linearity:"
        do i = 1, 5
            computed = log(xs(i))
            print *, "    log(", xs(i), ") =", computed
        end do
    end subroutine

    subroutine q4_smoothness()
        real(real64) :: eps, s1, s2, delta, expected, ratio
        eps = epsilon(1.0d0)
        s1 = sin(1.0d0)
        s2 = sin(1.0d0 + eps)
        delta = abs(s2 - s1)
        expected = abs(cos(1.0d0)) * eps
        ratio = delta / expected
        print *, "  Q4: smoothness ratio =", ratio
    end subroutine

    subroutine q5_spectral()
        integer, parameter :: sr = 44100, n = 44100
        real(real64) :: sig(n), t
        integer :: i
        do i = 1, n
            t = real(i-1, real64) / real(sr, real64)
            sig(i) = sin(2.0d0 * 4.0d0 * atan(1.0d0) * 440.0d0 * t)
        end do
        print *, "  Q5: Generated 440Hz sine"
        print *, "      Max amplitude =", maxval(sig), "Min =", minval(sig)
    end subroutine

    subroutine q6_temporal_drift()
        real(real32) :: x_f
        real(real64) :: x_d, r
        integer :: i, first_diverge
        x_f = 0.4; x_d = 0.4d0; r = 3.9d0; first_diverge = -1
        do i = 1, 1000000
            x_f = real(r, real32) * x_f * (1.0 - x_f)
            x_d = r * x_d * (1.0d0 - x_d)
            if (first_diverge == -1 .and. real(x_f, real64) /= x_d) then
                first_diverge = i
            end if
        end do
        print *, "  Q6: float vs double first diverge at iteration", first_diverge
    end subroutine

    subroutine q7_accumulation()
        real(real64) :: naive, kahan, c, y, t, diff
        real :: rn
        integer :: i, n
        real(real64), allocatable :: nums(:)
        n = 1000000
        allocate(nums(n))
        do i = 1, n
            call random_number(rn)
            nums(i) = 2.0d0 * rn - 1.0d0
        end do
        naive = 0.0d0
        do i = 1, n
            naive = naive + nums(i)
        end do
        kahan = 0.0d0; c = 0.0d0
        do i = 1, n
            y = nums(i) - c
            t = kahan + y
            c = (t - kahan) - y
            kahan = t
        end do
        diff = abs(naive - kahan) / max(abs(kahan), 1.0d-30)
        print *, "  Q7: naive =", naive, "kahan =", kahan, "rel_diff =", diff
        deallocate(nums)
    end subroutine

    subroutine q8_edge_cases()
        ! Fortran doesn't easily allow 0/0 etc at compile time
        ! We test what we can
        integer :: score
        real(real64) :: neg_zero, pos_zero, r3, r6
        score = 0
        ! -0 == 0
        neg_zero = -0.0d0; pos_zero = 0.0d0
        if (neg_zero == pos_zero) score = score + 1
        ! Use transfer to create NaN and Inf
        ! NaN = 7FF8000000000000 hex
        ! Inf = 7FF0000000000000 hex
        block
            integer(int64), parameter :: nan_bits = int(z'7FF8000000000000', int64)
            integer(int64), parameter :: inf_bits = int(z'7FF0000000000000', int64)
            real(real64) :: nan_val, inf_val
            nan_val = transfer(nan_bits, 1.0d0)
            inf_val = transfer(inf_bits, 1.0d0)
            ! NaN == NaN should be false
            if (.not. (nan_val == nan_val)) score = score + 1
            ! NaN check
            if (nan_val /= nan_val) score = score + 1  ! another way to check NaN
            ! inf - inf = NaN
            r6 = inf_val - inf_val
            if (r6 /= r6) score = score + 1  ! NaN check
        end block
        print *, "  Q8: IEEE score =", score, "/6 (partial: Fortran traps 0/0, sqrt(-1))"
    end subroutine

    subroutine q9_cross_config()
        real(real64) :: val
        val = sin(1.0d0) + cos(1.0d0) + log(2.0d0) + exp(1.0d0)
        print *, "  Q9: reference value =", val
    end subroutine

    subroutine q10_error_entropy()
        integer, parameter :: N = 10000
        real(real64) :: errors(N), x, entropy, bin_width, p
        real(real32) :: sf
        integer :: i, b, counts(100)
        real(real64) :: max_err
        counts = 0
        max_err = 0.0d0
        do i = 1, N
            x = 2.0d0 * 4.0d0 * atan(1.0d0) * real(i-1, real64) / real(N, real64)
            sf = sin(real(x, real32))
            errors(i) = sin(x) - real(sf, real64)
            if (abs(errors(i)) > max_err) max_err = abs(errors(i))
        end do
        bin_width = 2.0d0 * max_err / 100.0d0
        do i = 1, N
            b = int((errors(i) + max_err) / bin_width) + 1
            if (b > 100) b = 100
            if (b < 1) b = 1
            counts(b) = counts(b) + 1
        end do
        entropy = 0.0d0
        do i = 1, 100
            if (counts(i) > 0) then
                p = real(counts(i), real64) / real(N, real64)
                entropy = entropy - p * log(p) / log(2.0d0)
            end if
        end do
        print *, "  Q10: Shannon entropy =", entropy, "bits"
    end subroutine

end program benchmark_fortran
