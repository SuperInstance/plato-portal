#include "lau_conservation.h"
#include <math.h>
#include <stddef.h>

double conservation_check(double *values, int n, double baseline) {
    double s = 0.0;
    for (int i = 0; i < n; i++)
        s += values[i];
    return fabs(s - baseline) / fabs(baseline);
}

int conservation_verify(double *values, int n, double baseline, double epsilon) {
    return conservation_check(values, n, baseline) < epsilon ? 1 : 0;
}

void conservation_balance(double *values, int n, double baseline) {
    double s = 0.0;
    int    max_idx = 0;
    for (int i = 0; i < n; i++) {
        s += values[i];
        if (values[i] > values[max_idx])
            max_idx = i;
    }
    values[max_idx] += baseline - s;
}

void running_sum_init(RunningSum *rs) {
    rs->sum      = 0.0;
    rs->count    = 0;
    rs->overflow = 0;
}

int running_sum_add(RunningSum *rs, double value) {
    if (rs->overflow)
        return 0;
    rs->sum += value;
    rs->count++;
    if (isinf(rs->sum)) {
        rs->overflow = 1;
        return 0;
    }
    return 1;
}

double running_sum_get(const RunningSum *rs) {
    return rs->sum;
}

void batch_check(double **arrays, int *sizes, int num_arrays,
                 double baseline, double *errors_out) {
    for (int i = 0; i < num_arrays; i++)
        errors_out[i] = conservation_check(arrays[i], sizes[i], baseline);
}
