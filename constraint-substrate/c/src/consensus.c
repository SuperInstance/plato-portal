#include "constraint_substrate.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

static double circular_mean(const double* values, uint32_t count, double modulus) {
    if (count == 0) return 0.0;
    if (modulus <= 0.0) {
        double sum = 0.0;
        for (uint32_t i = 0; i < count; i++) sum += values[i];
        return sum / (double)count;
    }

    double two_pi = 2.0 * M_PI;
    double sin_sum = 0.0;
    double cos_sum = 0.0;
    for (uint32_t i = 0; i < count; i++) {
        double angle = (values[i] / modulus) * two_pi;
        sin_sum += sin(angle);
        cos_sum += cos(angle);
    }
    double mean_angle = atan2(sin_sum / (double)count, cos_sum / (double)count);
    if (mean_angle < 0.0) mean_angle += two_pi;
    return (mean_angle / two_pi) * modulus;
}

CsConsensusResult cs_consensus(const double* values, uint32_t count, double epsilon) {
    /* Default: arithmetic mean (no circular) */
    return cs_consensus_mod(values, count, epsilon, -1.0);
}

CsConsensusResult cs_consensus_mod(const double* values, uint32_t count, double epsilon, double modulus) {
    CsConsensusResult result;
    result.converged = 1;

    if (count == 0) {
        result.values = NULL;
        return result;
    }

    double use_modulus = modulus;
    int use_circular = (modulus > 0.0);

    double mean = circular_mean(values, count, use_circular ? use_modulus : -1.0);

    result.values = (double*)malloc(count * sizeof(double));
    for (uint32_t i = 0; i < count; i++) {
        double diff = mean - values[i];
        /* For cyclic values, take shortest path around the circle */
        /* Use proper Euclidean modulo (always non-negative for positive divisor) */
        if (use_circular) {
            double shifted = diff + use_modulus / 2.0;
            double rem = shifted - floor(shifted / use_modulus) * use_modulus;
            diff = rem - use_modulus / 2.0;
        }
        if (fabs(diff) > epsilon) {
            result.converged = 0;
            double sign = (diff > 0) ? 1.0 : -1.0;
            result.values[i] = values[i] + sign * epsilon * 0.5;
        } else {
            result.values[i] = mean;
        }
    }
    return result;
}

void cs_consensus_free(CsConsensusResult result) {
    free(result.values);
}
