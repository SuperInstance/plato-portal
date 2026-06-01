/* tests/test_basic.c — TDD: written before implementation */
#include <stdio.h>
#include <math.h>
#include "../include/lau_conservation.h"

static int tests_run    = 0;
static int tests_passed = 0;

#define TEST(name, cond) do { \
    tests_run++; \
    if (cond) { tests_passed++; printf("  PASS: %s\n", (name)); } \
    else       { printf("  FAIL: %s (line %d)\n", (name), __LINE__); } \
} while (0)

#define NEAR(a, b, eps) (fabs((double)(a) - (double)(b)) < (eps))

int main(void) {
    printf("=== lau-conservation-c tests ===\n\n");

    /* ---- conservation_check ---- */
    printf("conservation_check:\n");
    {
        double v[] = {1.0, 2.0, 3.0};
        TEST("exact conservation returns 0.0",
             NEAR(conservation_check(v, 3, 6.0), 0.0, 1e-12));
    }
    {
        double v[] = {1.0, 2.0, 3.0};
        /* sum=6, baseline=10 → |6-10|/10 = 0.4 */
        TEST("known 40% error",
             NEAR(conservation_check(v, 3, 10.0), 0.4, 1e-12));
    }
    {
        double v[] = {-1.0, -2.0, -3.0};
        TEST("negative values exact conservation",
             NEAR(conservation_check(v, 3, -6.0), 0.0, 1e-12));
    }
    {
        double v[] = {5.0};
        TEST("single element exact",
             NEAR(conservation_check(v, 1, 5.0), 0.0, 1e-12));
    }
    {
        double v[] = {5.0};
        /* sum=5, baseline=10 → 0.5 */
        TEST("single element 50%% error",
             NEAR(conservation_check(v, 1, 10.0), 0.5, 1e-12));
    }
    {
        double v[] = {0.25, 0.25, 0.25, 0.25};
        TEST("four quarters sum to 1.0",
             NEAR(conservation_check(v, 4, 1.0), 0.0, 1e-12));
    }

    /* ---- conservation_verify ---- */
    printf("\nconservation_verify:\n");
    {
        double v[] = {1.0, 2.0, 3.0};
        TEST("exact match verifies",
             conservation_verify(v, 3, 6.0, 1e-9) == 1);
    }
    {
        double v[] = {1.0, 2.0, 3.0};
        /* error=0.4 < epsilon=0.5 → 1 */
        TEST("error within epsilon returns 1",
             conservation_verify(v, 3, 10.0, 0.5) == 1);
    }
    {
        double v[] = {1.0, 2.0, 3.0};
        /* error=0.4 > epsilon=0.1 → 0 */
        TEST("error exceeds epsilon returns 0",
             conservation_verify(v, 3, 10.0, 0.1) == 0);
    }
    {
        double v[] = {1.0, 2.0, 4.0};
        /* sum=7, baseline=10, error=0.3, epsilon=0.3 → strict < so 0 */
        TEST("error equal to epsilon returns 0 (strict <)",
             conservation_verify(v, 3, 10.0, 0.3) == 0);
    }

    /* ---- conservation_balance ---- */
    printf("\nconservation_balance:\n");
    {
        double v[] = {1.0, 2.0, 3.0};
        conservation_balance(v, 3, 10.0);
        TEST("balance makes sum equal baseline",
             NEAR(v[0] + v[1] + v[2], 10.0, 1e-12));
    }
    {
        double v[] = {1.0, 5.0, 2.0};
        /* largest=v[1]=5, sum=8, need +2 → v[1] becomes 7 */
        conservation_balance(v, 3, 10.0);
        TEST("balance adjusts the largest element",
             NEAR(v[1], 7.0, 1e-12));
    }
    {
        double v[] = {1.0, 2.0, 3.0};
        conservation_balance(v, 3, 6.0);
        TEST("already balanced leaves sum unchanged",
             NEAR(v[0] + v[1] + v[2], 6.0, 1e-12));
    }
    {
        double v[] = {5.0};
        conservation_balance(v, 1, 10.0);
        TEST("single element balance sets element to baseline",
             NEAR(v[0], 10.0, 1e-12));
    }
    {
        double v[] = {3.0, 1.0, 2.0};
        /* largest=v[0]=3; sum=6, need -1 → v[0] becomes 2 */
        conservation_balance(v, 3, 5.0);
        TEST("balance works when largest is first element",
             NEAR(v[0], 2.0, 1e-12));
    }

    /* ---- running_sum ---- */
    printf("\nrunning_sum:\n");
    {
        RunningSum rs;
        running_sum_init(&rs);
        TEST("initial sum is 0.0",
             NEAR(running_sum_get(&rs), 0.0, 1e-12));
    }
    {
        RunningSum rs;
        running_sum_init(&rs);
        running_sum_add(&rs, 1.0);
        running_sum_add(&rs, 2.0);
        running_sum_add(&rs, 3.0);
        TEST("accumulates three values correctly",
             NEAR(running_sum_get(&rs), 6.0, 1e-12));
    }
    {
        RunningSum rs;
        running_sum_init(&rs);
        running_sum_add(&rs, 1.0);
        running_sum_add(&rs, 2.0);
        running_sum_add(&rs, 3.0);
        TEST("count tracks number of additions", rs.count == 3);
    }
    {
        RunningSum rs;
        running_sum_init(&rs);
        running_sum_add(&rs, 1e308);
        running_sum_add(&rs, 1e308); /* sum overflows to +inf */
        TEST("overflow flag set on infinity", rs.overflow == 1);
    }
    {
        RunningSum rs;
        running_sum_init(&rs);
        running_sum_add(&rs, 1e308);
        running_sum_add(&rs, 1e308);
        int ret = running_sum_add(&rs, 1.0);
        TEST("add returns 0 when already overflowed", ret == 0);
    }

    /* ---- batch_check ---- */
    printf("\nbatch_check:\n");
    {
        double a1[] = {1.0, 2.0, 3.0};  /* sum=6, exact */
        double a2[] = {2.0, 4.0, 4.0};  /* sum=10, error=4/6 */
        double *arrays[] = {a1, a2};
        int sizes[] = {3, 3};
        double errors[2];
        batch_check(arrays, sizes, 2, 6.0, errors);
        TEST("batch first array: exact conservation",
             NEAR(errors[0], 0.0, 1e-12));
        TEST("batch second array: correct relative error",
             NEAR(errors[1], 4.0 / 6.0, 1e-12));
    }
    {
        double a1[] = {6.0};
        double *arrays[] = {a1};
        int sizes[] = {1};
        double errors[1];
        batch_check(arrays, sizes, 1, 6.0, errors);
        TEST("batch single array exact", NEAR(errors[0], 0.0, 1e-12));
    }
    {
        double a1[] = {10.0, 20.0};  /* sum=30 */
        double a2[] = {5.0,  5.0};  /* sum=10 */
        double a3[] = {15.0, 5.0};  /* sum=20 */
        double *arrays[] = {a1, a2, a3};
        int sizes[] = {2, 2, 2};
        double errors[3];
        batch_check(arrays, sizes, 3, 20.0, errors);
        /* a1: |30-20|/20=0.5, a2: |10-20|/20=0.5, a3: exact=0 */
        TEST("batch three arrays: first has 50%% error",
             NEAR(errors[0], 0.5, 1e-12));
        TEST("batch three arrays: third is exact",
             NEAR(errors[2], 0.0, 1e-12));
    }

    printf("\n=== Results: %d/%d passed ===\n", tests_passed, tests_run);
    return (tests_passed == tests_run) ? 0 : 1;
}
