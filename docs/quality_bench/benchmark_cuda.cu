#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <float.h>
#include <stdint.h>

/* CUDA quality benchmark - runs on GPU */

#define N_DRIFT 1000000
#define N_ACCUM 1000000
#define N_ENTROPY 10000

/* Simple LCG for reproducibility */
__device__ double dev_rand(unsigned long long *state) {
    *state = *state * 6364136223846793005ULL + 1442695040888963407ULL;
    return (double)(*state >> 33) / (double)(1ULL << 31) * 2.0 - 1.0;
}

__global__ void q6_kernel(float *x_f_out, double *x_d_out) {
    float xf = 0.4f;
    double xd = 0.4;
    double r = 3.9;
    for (int i = 0; i < N_DRIFT; i++) {
        xf = (float)r * xf * (1.0f - xf);
        xd = r * xd * (1.0 - xd);
    }
    *x_f_out = xf;
    *x_d_out = xd;
}

__global__ void q7_kernel(double *naive_out, double *kahan_out) {
    double naive = 0.0;
    double kahan = 0.0, c = 0.0;
    unsigned long long state = threadIdx.x * 1000003ULL + 42;
    
    for (int i = 0; i < N_ACCUM; i++) {
        double x = dev_rand(&state);
        naive += x;
        double y = x - c;
        double t = kahan + y;
        c = (t - kahan) - y;
        kahan = t;
    }
    *naive_out = naive;
    *kahan_out = kahan;
}

int main() {
    printf("=== CUDA Quality Benchmark ===\n");
    
    /* Q1: Precision */
    double pi = 16.0 * atan(1.0/5.0) - 4.0 * atan(1.0/239.0);
    printf("  Q1: pi = %.20g\n", pi);
    
    /* Q2: Consistency */
    double s = sin(1.0);
    printf("  Q2: sin(1.0) = %.20g (always same)\n", s);
    
    /* Q3: Linearity */
    double xs[] = {1e-10, 1e-5, 1.0, 1e5, 1e10};
    printf("  Q3: log linearity:\n");
    for (int i = 0; i < 5; i++)
        printf("      log(%.1e) = %.15g\n", xs[i], log(xs[i]));
    
    /* Q4: Smoothness */
    double eps = DBL_EPSILON;
    double s1 = sin(1.0), s2 = sin(1.0 + eps);
    printf("  Q4: smoothness ratio = %.6f\n", fabs(s2-s1) / (fabs(cos(1.0)) * eps));
    
    /* Q6: Temporal drift on GPU */
    float *d_xf, *h_xf;
    double *d_xd, *h_xd;
    h_xf = (float*)malloc(sizeof(float));
    h_xd = (double*)malloc(sizeof(double));
    cudaMalloc(&d_xf, sizeof(float));
    cudaMalloc(&d_xd, sizeof(double));
    q6_kernel<<<1,1>>>(d_xf, d_xd);
    cudaMemcpy(h_xf, d_xf, sizeof(float), cudaMemcpyDeviceToHost);
    cudaMemcpy(h_xd, d_xd, sizeof(double), cudaMemcpyDeviceToHost);
    printf("  Q6: GPU float result = %.10g, double result = %.15g\n", *h_xf, *h_xd);
    
    /* Q7: Accumulation on GPU */
    double *d_naive, *d_kahan, h_naive, h_kahan;
    cudaMalloc(&d_naive, sizeof(double));
    cudaMalloc(&d_kahan, sizeof(double));
    q7_kernel<<<1,1>>>(d_naive, d_kahan);
    cudaMemcpy(&h_naive, d_naive, sizeof(double), cudaMemcpyDeviceToHost);
    cudaMemcpy(&h_kahan, d_kahan, sizeof(double), cudaMemcpyDeviceToHost);
    printf("  Q7: naive = %.15g, kahan = %.15g\n", h_naive, h_kahan);
    
    /* Q8: Edge cases on device - run on host side for CUDA */
    int score = 0;
    double r1 = 0.0/0.0; if (isnan(r1)) score++;
    double r2 = 1.0/0.0; if (isinf(r2)) score++;
    printf("  Q8: IEEE score = %d/6 (partial check)\n", score);
    
    /* Q9: Cross config */
    double val = sin(1.0) + cos(1.0) + log(2.0) + exp(1.0);
    printf("  Q9: reference value = %.20g\n", val);
    
    /* Q10: Error entropy (host-side) */
    double errors[N_ENTROPY], max_err = 0;
    for (int i = 0; i < N_ENTROPY; i++) {
        double x = 2.0 * M_PI * i / N_ENTROPY;
        errors[i] = sin(x) - sinf((float)x);
        if (fabs(errors[i]) > max_err) max_err = fabs(errors[i]);
    }
    int counts[100] = {0};
    double bw = 2.0 * max_err / 100.0;
    for (int i = 0; i < N_ENTROPY; i++) {
        int b = (int)((errors[i] + max_err) / bw);
        if (b >= 100) b = 99; if (b < 0) b = 0;
        counts[b]++;
    }
    double entropy = 0;
    for (int i = 0; i < 100; i++) {
        if (counts[i] > 0) {
            double p = (double)counts[i] / N_ENTROPY;
            entropy -= p * log2(p);
        }
    }
    printf("  Q10: entropy = %.4f bits\n", entropy);
    
    /* Cleanup */
    cudaFree(d_xf); cudaFree(d_xd);
    cudaFree(d_naive); cudaFree(d_kahan);
    free(h_xf); free(h_xd);
    
    printf("\n=== CUDA Benchmark Complete ===\n");
    return 0;
}
