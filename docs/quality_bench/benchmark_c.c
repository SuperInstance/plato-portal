#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include <float.h>
#include <stdint.h>
#include <stdarg.h>

/* JSON results collector */
#define MAX_RESULTS 8192
static char results_buf[MAX_RESULTS];
static int results_pos = 0;

static void rprintf(const char *fmt, ...) {
    va_list args;
    va_start(args, fmt);
    results_pos += vsnprintf(results_buf + results_pos, MAX_RESULTS - results_pos, fmt, args);
    va_end(args);
}

/* ---- Q1: Precision - Machin's formula for pi ---- */
static void q1_precision(void) {
    double pi = 16.0 * atan(1.0/5.0) - 4.0 * atan(1.0/239.0);
    const char *ground_truth = "3.14159265358979323846264338327950288419716939937510";
    double ref = 3.14159265358979323846264338327950288419716939937510;
    double err = fabs(pi - ref);
    double bits = err > 0 ? -log2(err) : 53.0;
    if (bits > 53) bits = 53;
    if (bits < 0) bits = 0;
    rprintf("\"Q1_precision\":{\"pi\":%.20g,\"bits_of_agreement\":%.2f}", pi, bits);
}

/* ---- Q2: Consistency - sin(1.0) 10000 times ---- */
static void q2_consistency(void) {
    double sum = 0.0, sum2 = 0.0;
    double val = sin(1.0);
    for (int i = 0; i < 10000; i++) {
        double v = sin(1.0);
        sum += v;
        sum2 += v * v;
    }
    double mean = sum / 10000.0;
    double variance = sum2 / 10000.0 - mean * mean;
    rprintf("\"Q2_consistency\":{\"variance\":%.20g,\"should_be_zero\":%s}",
            variance, variance < 1e-30 ? "true" : "false");
}

/* ---- Q3: Linearity - log at different scales ---- */
static void q3_linearity(void) {
    double xs[] = {1e-10, 1e-5, 1.0, 1e5, 1e10};
    rprintf("\"Q3_linearity\":{\"errors\":[");
    for (int i = 0; i < 5; i++) {
        double computed = log(xs[i]);
        /* reference from Python mpmath */
        double refs[] = {-23.025850929940457210141413876, -11.51292546497022910507070694,
                          0.0, 11.51292546497022852372264585, 23.02585092994045684017991455};
        double rel_err = refs[i] != 0 ? fabs((computed - refs[i]) / refs[i]) : fabs(computed - refs[i]);
        if (i > 0) rprintf(",");
        rprintf("{\"x\":%.1e,\"rel_error\":%.6e}", xs[i], rel_err);
    }
    rprintf("]}");
}

/* ---- Q4: Smoothness ---- */
static void q4_smoothness(void) {
    double eps = DBL_EPSILON;
    double s1 = sin(1.0);
    double s2 = sin(1.0 + eps);
    double delta = fabs(s2 - s1);
    double expected = fabs(cos(1.0)) * eps;
    double ratio = delta / expected;
    rprintf("\"Q4_smoothness\":{\"delta\":%.20g,\"expected\":%.20g,\"ratio\":%.6f}", delta, expected, ratio);
}

/* ---- Q5: Spectral purity (simplified - no FFT in stdlib, use manual DFT for fundamental region) ---- */
#include <stdio.h>
static void q5_spectral(void) {
    int sr = 44100, n = 44100;
    double freq = 440.0;
    double *sig = malloc(n * sizeof(double));
    for (int i = 0; i < n; i++)
        sig[i] = sin(2.0 * M_PI * freq * i / (double)sr);

    /* Write WAV */
    FILE *wav = fopen("c_440hz.wav", "wb");
    if (wav) {
        int16_t *buf = malloc(n * sizeof(int16_t));
        for (int i = 0; i < n; i++) {
            double s = sig[i] * 32767.0;
            if (s > 32767) s = 32767; if (s < -32768) s = -32768;
            buf[i] = (int16_t)s;
        }
        /* Minimal WAV header */
        int datasize = n * 2;
        int filesize = 36 + datasize;
        fwrite("RIFF", 1, 4, wav);
        int32_t tmp = filesize; fwrite(&tmp, 4, 1, wav);
        fwrite("WAVEfmt ", 1, 8, wav);
        tmp = 16; fwrite(&tmp, 4, 1, wav);
        int16_t s16 = 1; fwrite(&s16, 2, 1, wav); /* PCM */
        s16 = 1; fwrite(&s16, 2, 1, wav); /* mono */
        int32_t s32 = sr; fwrite(&s32, 4, 1, wav);
        s32 = sr * 2; fwrite(&s32, 4, 1, wav); /* byte rate */
        s16 = 2; fwrite(&s16, 2, 1, wav); /* block align */
        s16 = 16; fwrite(&s16, 2, 1, wav); /* bits */
        fwrite("data", 1, 4, wav);
        tmp = datasize; fwrite(&tmp, 4, 1, wav);
        fwrite(buf, 2, n, wav);
        free(buf);
        fclose(wav);
    }

    /* Compute DFT at fundamental and nearby harmonics */
    double fund_real = 0, fund_imag = 0;
    int fund_bin = (int)(freq * n / sr);
    for (int i = 0; i < n; i++) {
        double t = 2.0 * M_PI * fund_bin * i / n;
        fund_real += sig[i] * cos(t);
        fund_imag -= sig[i] * sin(t);
    }
    double fund_mag = sqrt(fund_real*fund_real + fund_imag*fund_imag) / n * 2;

    /* Check a few harmonic bins */
    double max_spur = 0;
    int check_bins[] = {2*440, 3*440, 5*440, 7*440, 100, 1000, 5000, 10000, 20000};
    for (int k = 0; k < 9; k++) {
        int b = check_bins[k];
        if (b >= n/2) continue;
        double br = 0, bi = 0;
        for (int i = 0; i < n; i++) {
            double t = 2.0 * M_PI * b * i / n;
            br += sig[i] * cos(t);
            bi -= sig[i] * sin(t);
        }
        double mag = sqrt(br*br + bi*bi) / n * 2;
        if (mag > max_spur) max_spur = mag;
    }
    double spur_dB = fund_mag > 0 ? 20.0 * log10(max_spur / fund_mag) : -999;
    rprintf("\"Q5_spectral\":{\"spurious_dB\":%.2f}", spur_dB);
    free(sig);
}

/* ---- Q6: Temporal drift - Logistic map ---- */
static void q6_temporal_drift(void) {
    /* We compare float vs double - C doesn't have Decimal natively */
    float x_f = 0.4f;
    double x_d = 0.4;
    double r = 3.9;
    int first_diverge = -1;
    for (int i = 0; i < 1000000; i++) {
        x_f = (float)(r * x_f * (1.0f - x_f));
        x_d = r * x_d * (1.0 - x_d);
        if (first_diverge == -1 && (double)x_f != x_d) {
            first_diverge = i;
        }
    }
    /* Also compare double against long double */
    double x2 = 0.4;
    long double x_ld = 0.4L;
    long double r_ld = 3.9L;
    int first_diverge_ld = -1;
    for (int i = 0; i < 1000000; i++) {
        x2 = r * x2 * (1.0 - x2);
        x_ld = r_ld * x_ld * (1.0L - x_ld);
        if (first_diverge_ld == -1 && (long double)x2 != x_ld)
            first_diverge_ld = i;
    }
    rprintf("\"Q6_temporal_drift\":{\"float_vs_double_diverge\":%d,\"double_vs_longdouble_diverge\":%d}",
            first_diverge, first_diverge_ld);
}

/* ---- Q7: Accumulation - naive vs Kahan ---- */
static void q7_accumulation(void) {
    srand(42);
    int n = 1000000;
    double *nums = malloc(n * sizeof(double));
    for (int i = 0; i < n; i++)
        nums[i] = 2.0 * ((double)rand() / RAND_MAX) - 1.0;

    double naive = 0;
    for (int i = 0; i < n; i++) naive += nums[i];

    double kahan = 0.0, c = 0.0;
    for (int i = 0; i < n; i++) {
        double y = nums[i] - c;
        double t = kahan + y;
        c = (t - kahan) - y;
        kahan = t;
    }

    double diff = fabs(naive - kahan) / (fabs(kahan) > 0 ? fabs(kahan) : 1.0);
    rprintf("\"Q7_accumulation\":{\"naive\":%.15g,\"kahan\":%.15g,\"relative_diff\":%.6e}",
            naive, kahan, diff);
    free(nums);
}

/* ---- Q8: Edge cases - IEEE 754 ---- */
static void q8_edge_cases(void) {
    int score = 0;
    const char *details[6];
    /* 0/0 */
    double r1 = 0.0/0.0;
    if (isnan(r1)) { score++; details[0] = "true"; } else { details[0] = "false"; }
    /* 1/0 */
    double r2 = 1.0/0.0;
    if (isinf(r2)) { score++; details[1] = "true"; } else { details[1] = "false"; }
    /* sqrt(-1) - may return NaN or domain error */
    int sq_ok = 0;
    #pragma STDC FENV_ACCESS OFF
    double r3 = sqrt(-1.0);
    if (isnan(r3)) { score++; sq_ok = 1; }
    details[2] = sq_ok ? "true" : "false";
    /* -0 == 0 */
    double neg_zero = -0.0, pos_zero = 0.0;
    if (neg_zero == pos_zero) { score++; details[3] = "true"; } else { details[3] = "false"; }
    /* NaN == NaN */
    double nan_val = NAN;
    if (!(nan_val == nan_val)) { score++; details[4] = "true"; } else { details[4] = "false"; }
    /* inf - inf */
    double r6 = INFINITY - INFINITY;
    if (isnan(r6)) { score++; details[5] = "true"; } else { details[5] = "false"; }

    rprintf("\"Q8_edge_cases\":{\"score\":\"%d/6\",\"details\":[\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"],\"percent\":%.1f}",
            score, details[0], details[1], details[2], details[3], details[4], details[5], score/6.0*100);
}

/* ---- Q9: Cross-config comparison (called from multiple compilations) ---- */
static double q9_value(void) {
    return sin(1.0) + cos(1.0) + log(2.0) + exp(1.0);
}

/* ---- Q10: Error entropy ---- */
static void q10_error_entropy(void) {
    int N = 10000;
    double *errors = malloc(N * sizeof(double));
    double max_err = 0;
    /* Reference sin values using Taylor series at high precision (double is the reference) */
    for (int i = 0; i < N; i++) {
        double x = 2.0 * M_PI * i / N;
        errors[i] = 0.0; /* double vs double = zero error; use vs reduced precision */
        /* Compare sin(x) vs sinf(x) for actual entropy */
        errors[i] = sin(x) - (double)sinf((float)x);
        double ae = fabs(errors[i]);
        if (ae > max_err) max_err = ae;
    }

    int num_bins = 100;
    int counts[100] = {0};
    if (max_err > 0) {
        double bin_width = 2.0 * max_err / num_bins;
        for (int i = 0; i < N; i++) {
            int b = (int)((errors[i] + max_err) / bin_width);
            if (b >= num_bins) b = num_bins - 1;
            if (b < 0) b = 0;
            counts[b]++;
        }
    } else {
        counts[50] = N;
    }
    double entropy = 0.0;
    for (int i = 0; i < num_bins; i++) {
        if (counts[i] > 0) {
            double p = (double)counts[i] / N;
            entropy -= p * log2(p);
        }
    }
    rprintf("\"Q10_error_entropy\":{\"shannon_entropy_bits\":%.4f,\"num_samples\":%d}", entropy, N);
    free(errors);
}

int main(int argc, char *argv[]) {
    int run_q9_only = 0;
    if (argc > 1 && strcmp(argv[1], "--q9") == 0) run_q9_only = 1;

    if (run_q9_only) {
        double val = q9_value();
        printf("{\"q9_value\":%.20g}\n", val);
        return 0;
    }

    results_pos = 0;
    results_buf[0] = '{';
    results_pos = 1;

    printf("=== C Quality Benchmark ===\n");

    printf("  Running Q1: Precision\n"); q1_precision(); rprintf(",");
    printf("  Running Q2: Consistency\n"); q2_consistency(); rprintf(",");
    printf("  Running Q3: Linearity\n"); q3_linearity(); rprintf(",");
    printf("  Running Q4: Smoothness\n"); q4_smoothness(); rprintf(",");
    printf("  Running Q5: Spectral\n"); q5_spectral(); rprintf(",");
    printf("  Running Q6: Temporal drift\n"); q6_temporal_drift(); rprintf(",");
    printf("  Running Q7: Accumulation\n"); q7_accumulation(); rprintf(",");
    printf("  Running Q8: Edge cases\n"); q8_edge_cases(); rprintf(",");
    printf("  Running Q9: Cross-config\n");
    rprintf("\"Q9_cross_config\":{\"reference_value\":%.20g,\"note\":\"Run separately with different flags\"},", q9_value());
    printf("  Running Q10: Error entropy\n"); q10_error_entropy();

    rprintf("}");

    printf("\nResults:\n%s\n", results_buf);

    FILE *f = fopen("results_c.json", "w");
    if (f) { fprintf(f, "%s\n", results_buf); fclose(f); }

    return 0;
}
