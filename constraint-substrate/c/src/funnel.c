#include "constraint_substrate.h"

CsFunnelResult cs_funnel_step(double current, double target, double epsilon, double decay) {
    CsFunnelResult result;
    double diff = target - current;
    double exp_decay = exp(-decay);
    double new_eps = epsilon * exp_decay;

    if (fabs(diff) < epsilon) {
        /* Within deadband — snap toward target */
        double correction = diff * (1.0 - exp_decay);
        result.value = current + correction;
    } else {
        /* Outside deadband — pull toward target */
        double step_size = (diff > 0 ? 1.0 : -1.0) * epsilon;
        result.value = current + step_size;
    }
    result.epsilon = new_eps;
    return result;
}
