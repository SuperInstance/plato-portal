! berry_phase_f90.f90 — Berry Phase = Pythagorean Comma (Fortran 90)
!
! Physics Analogy:
!   The circle of fifths (repeated 3/2 multiplication) traces a path in
!   log-frequency space. After 12 steps, the path should close (12 fifths
!   = 7 octaves in flat space), but the holonomy (Berry phase) is the
!   Pythagorean comma: 3^12/2^19 = 531441/524288 ≈ 23.46 cents.
!
!   This is the musical analog of a geometric (Berry) phase: the mismatch
!   between the expected closure and actual closure of a loop in parameter
!   space reflects the curvature of the frequency manifold.
!
! Compile: gfortran -O2 -o berry_phase_f90 berry_phase_f90.f90

program berry_phase
  implicit none
  integer :: i
  double precision :: f, f_start, f_end, ratio, cents, interval
  double precision :: final_ratio, comma_cents
  double precision :: exact_comma, exact_cents, error_cents

  f_start = 440.0d0
  f_end = 880.0d0
  f = f_start
  ratio = 3.0d0 / 2.0d0

  write(*, '(A)') '{"experiment": "berry_phase_pythagorean_comma",'
  write(*, '(A)') ' "language": "Fortran 90",'
  write(*, '(A)') ' "description": "Circle of fifths holonomy = Pythagorean comma",'
  write(*, '(A)') ' "steps": ['

  do i = 1, 12
    f = f * ratio
    ! Normalize to [440, 880)
    do while (f >= f_end)
      f = f / 2.0d0
    end do

    cents = 1200.0d0 * log(f / f_start) / log(2.0d0)
    interval = f / f_start

    if (i < 12) then
      write(*, '(A,I3,A,F12.6,A,F14.10,A,F10.4,A)') &
        '  {"step":', i, ', "frequency":', f, &
        ', "interval_ratio":', interval, ', "cents":', cents, '},'
    else
      write(*, '(A,I3,A,F12.6,A,F14.10,A,F10.4,A)') &
        '  {"step":', i, ', "frequency":', f, &
        ', "interval_ratio":', interval, ', "cents":', cents, '}'
    end if
  end do

  write(*, '(A)') ' ],'

  ! Final analysis
  final_ratio = f / f_start
  comma_cents = 1200.0d0 * log(final_ratio) / log(2.0d0)
  exact_comma = 531441.0d0 / 524288.0d0
  exact_cents = 1200.0d0 * log(exact_comma) / log(2.0d0)
  error_cents = abs(comma_cents - exact_cents)

  write(*, '(A,F18.15)') ' "final_ratio":', final_ratio
  write(*, '(A)') ' "pythagorean_comma_exact": "531441/524288",'
  write(*, '(A,F18.15)') ' "pythagorean_comma_decimal":', exact_comma
  write(*, '(A,F12.6)') ' "comma_cents":', comma_cents
  write(*, '(A,F12.6)') ' "exact_comma_cents":', exact_cents
  write(*, '(A,F14.10)') ' "error_cents":', error_cents
  write(*, '(A)') ' "physics_interpretation": "The holonomy of the circle' // &
    '-of-fifths loop equals the Pythagorean comma, the musical Berry phase."'
  write(*, '(A)') '}'

end program berry_phase
