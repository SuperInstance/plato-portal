! spin_statistics_f90.f90 — Spin Statistics Consonance (Fortran 90)
!
! Physics Analogy:
!   Fermions obey Pauli exclusion: two particles cannot occupy the same state.
!   We model harmonic partial proximity as a Fermi-Dirac distribution:
!     w = 1 / (exp((|f_i - f_j| - delta) / sigma) + 1)
!   Close partials → high weight (excluded, rough, dissonant).
!   Far partials → low weight (allowed, smooth, consonant).
!
! Compile: gfortran -O2 -o spin_statistics_f90 spin_statistics_f90.f90

program spin_statistics
  implicit none
  integer, parameter :: N_HARM = 8
  integer, parameter :: N_INT = 13
  double precision, parameter :: DELTA = 100.0d0
  double precision, parameter :: SIGMA = 50.0d0
  double precision, parameter :: F0 = 440.0d0

  character(len=10) :: names(N_INT)
  double precision :: ratios(N_INT)
  double precision :: r, f1, f2, fi, fj, df, w, roughness, tenney, cents_val
  integer :: i, j, k, n_pairs

  ! Interval names and ratios (chromatic scale)
  names = (/ "Unison ", "m2     ", "M2     ", "m3     ", "M3     ", &
             "P4     ", "TT     ", "P5     ", "m6     ", "M6     ", &
             "m7     ", "M7     ", "Octave " /)
  ratios = (/ 1.0d0, 16.0d0/15.0d0, 9.0d0/8.0d0, 6.0d0/5.0d0, 5.0d0/4.0d0, &
              4.0d0/3.0d0, 45.0d0/32.0d0, 3.0d0/2.0d0, 8.0d0/5.0d0, &
              5.0d0/3.0d0, 9.0d0/5.0d0, 15.0d0/8.0d0, 2.0d0 /)

  write(*, '(A)') '{"experiment": "spin_statistics_consonance",'
  write(*, '(A)') ' "language": "Fortran 90",'
  write(*, '(A,I2,A,F5.1,A,F5.1,A,F6.1,A)') &
    ' "parameters": {"N_harmonics":', N_HARM, ', "delta_Hz":', DELTA, &
    ', "sigma_Hz":', SIGMA, ', "f0_Hz":', F0, '},'
  write(*, '(A)') ' "intervals": ['

  do k = 1, N_INT
    r = ratios(k)
    f1 = F0
    f2 = F0 * r

    roughness = 0.0d0
    n_pairs = 0

    do i = 1, N_HARM
      do j = 1, N_HARM
        fi = f1 * dble(i)
        fj = f2 * dble(j)
        df = abs(fi - fj)
        w = 1.0d0 / (exp((df - DELTA) / SIGMA) + 1.0d0)
        roughness = roughness + w
        n_pairs = n_pairs + 1
      end do
    end do

    roughness = roughness / dble(n_pairs)
    tenney = log(r) / log(2.0d0)
    if (r < 1.0d0) tenney = -tenney
    cents_val = 1200.0d0 * log(r) / log(2.0d0)

    if (k < N_INT) then
      write(*, '(A,A10,A,F10.8,A,F10.4,A,F12.8,A,F8.6,A)') &
        '  {"name": "', trim(names(k)), '", "ratio_decimal":', r, &
        ', "cents":', cents_val, ', "roughness":', roughness, &
        ', "tenney_height":', tenney, '},'
    else
      write(*, '(A,A10,A,F10.8,A,F10.4,A,F12.8,A,F8.6,A)') &
        '  {"name": "', trim(names(k)), '", "ratio_decimal":', r, &
        ', "cents":', cents_val, ', "roughness":', roughness, &
        ', "tenney_height":', tenney, '}'
    end if
  end do

  write(*, '(A)') ' ],'
  write(*, '(A)') ' "physics_interpretation": "Consonant intervals have low Fermi-Dirac roughness (partial exclusion principle)."'
  write(*, '(A)') '}'

end program spin_statistics
