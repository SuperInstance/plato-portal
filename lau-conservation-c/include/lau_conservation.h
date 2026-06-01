#ifndef LAU_CONSERVATION_H
#define LAU_CONSERVATION_H

/* Relative error: |sum(values) - baseline| / |baseline| */
double conservation_check(double *values, int n, double baseline);

/* 1 if conservation_check < epsilon, 0 otherwise */
int conservation_verify(double *values, int n, double baseline, double epsilon);

/* Adjust the largest element so sum(values) == baseline */
void conservation_balance(double *values, int n, double baseline);

/* Cumulative sum tracker with overflow detection */
typedef struct {
    double sum;
    int    count;
    int    overflow;
} RunningSum;

void   running_sum_init(RunningSum *rs);
int    running_sum_add(RunningSum *rs, double value); /* returns 0 on overflow */
double running_sum_get(const RunningSum *rs);

/* Compute conservation_check for each array; store results in errors_out */
void batch_check(double **arrays, int *sizes, int num_arrays,
                 double baseline, double *errors_out);

#endif /* LAU_CONSERVATION_H */
