#include "constraint_substrate.h"

double cs_holonomy(const double* values, uint32_t count, double modulus) {
    if (count == 0) return 0.0;
    double total = 0.0;
    for (uint32_t i = 1; i < count; i++) {
        double diff = values[i] - values[i - 1];
        double wrapped = diff - modulus * round(diff / modulus);
        total += wrapped;
    }
    return total / modulus;
}
