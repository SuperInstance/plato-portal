/*
 * riscv_lattice_main.c — C wrapper for RISC-V lattice oscillator
 *
 * Compiles with: riscv64-unknown-elf-gcc -march=rv64gc -mabi=lp64d \
 *                  -static -o lattice_osc riscv_lattice_main.c riscv_lattice.S -lm
 *
 * Or cross-compile for QEMU:
 *   riscv64-linux-gnu-gcc -march=rv64gc -mabi=lp64d -o lattice_osc \
 *       riscv_lattice_main.c riscv_lattice.S -lm
 *
 * Run: ./lattice_osc 440.0 2 output.raw
 *   (generates 2 seconds of A440 as raw float32 PCM)
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define SAMPLE_RATE 44100

/* Assembly function declaration */
extern void lattice_oscillator(float *output, int num_samples,
                                float frequency, int sample_rate);

int main(int argc, char *argv[])
{
    float frequency = 440.0f;
    float duration  = 2.0f;
    const char *output_path = "output.raw";

    if (argc > 1) frequency   = strtof(argv[1], NULL);
    if (argc > 2) duration    = strtof(argv[2], NULL);
    if (argc > 3) output_path = argv[3];

    int num_samples = (int)(duration * SAMPLE_RATE);

    printf("Lattice Oscillator (RISC-V RV64GC)\n");
    printf("===================================\n");
    printf("Frequency:   %.2f Hz\n", frequency);
    printf("Duration:    %.3f s\n", duration);
    printf("Sample rate: %d Hz\n", SAMPLE_RATE);
    printf("Samples:     %d\n", num_samples);
    printf("Partials:    8 (1, 3/2, 5/4, 15/8, 2, 9/4, 5/2, 25/8)\n");
    printf("Output:      %s\n\n", output_path);

    /* Allocate output buffer */
    float *output = malloc(num_samples * sizeof(float));
    if (!output) {
        fprintf(stderr, "Error: failed to allocate %d bytes\n",
                num_samples * (int)sizeof(float));
        return 1;
    }

    /* Run the lattice oscillator */
    printf("Computing samples...\n");
    lattice_oscillator(output, num_samples, frequency, SAMPLE_RATE);
    printf("Done.\n");

    /* Write raw PCM output (float32, little-endian) */
    FILE *fp = fopen(output_path, "wb");
    if (!fp) {
        fprintf(stderr, "Error: cannot open %s for writing\n", output_path);
        free(output);
        return 1;
    }

    size_t written = fwrite(output, sizeof(float), num_samples, fp);
    fclose(fp);

    printf("Wrote %zu samples (%zu bytes) to %s\n",
           written, written * sizeof(float), output_path);

    /* Print some stats */
    float min_val = output[0], max_val = output[0], sum = 0;
    for (int i = 0; i < num_samples; i++) {
        if (output[i] < min_val) min_val = output[i];
        if (output[i] > max_val) max_val = output[i];
        sum += output[i];
    }
    printf("Sample range: [%.6f, %.6f]\n", min_val, max_val);
    printf("DC offset:    %.6f\n", sum / num_samples);

    /* Also write a WAV header for convenience */
    char wav_path[256];
    snprintf(wav_path, sizeof(wav_path), "%s.wav",
             output_path[strlen(output_path) > 5 ?
             output_path : "output");
    /* Strip .raw extension if present */
    char *dot = strrchr(wav_path, '.');
    if (dot && strcmp(dot, ".raw.wav") == 0) {
        /* Replace .raw.wav with just .wav */
        *dot = '\0';
        strcat(wav_path, ".wav");
    }

    fp = fopen(wav_path, "wb");
    if (fp) {
        /* Convert float to int16 for WAV */
        int16_t *pcm16 = malloc(num_samples * sizeof(int16_t));
        for (int i = 0; i < num_samples; i++) {
            float s = output[i];
            if (s > 1.0f) s = 1.0f;
            if (s < -1.0f) s = -1.0f;
            pcm16[i] = (int16_t)(s * 32767.0f);
        }

        uint32_t data_size = num_samples * sizeof(int16_t);
        uint32_t file_size = 36 + data_size;

        /* RIFF header */
        fwrite("RIFF", 1, 4, fp);
        fwrite(&file_size, 4, 1, fp);
        fwrite("WAVE", 1, 4, fp);

        /* fmt chunk */
        fwrite("fmt ", 1, 4, fp);
        uint32_t fmt_size = 16;
        fwrite(&fmt_size, 4, 1, fp);
        uint16_t audio_fmt = 1;  /* PCM */
        fwrite(&audio_fmt, 2, 1, fp);
        uint16_t channels = 1;
        fwrite(&channels, 2, 1, fp);
        uint32_t sr = SAMPLE_RATE;
        fwrite(&sr, 4, 1, fp);
        uint32_t byte_rate = SAMPLE_RATE * 2;
        fwrite(&byte_rate, 4, 1, fp);
        uint16_t block_align = 2;
        fwrite(&block_align, 2, 1, fp);
        uint16_t bits = 16;
        fwrite(&bits, 2, 1, fp);

        /* data chunk */
        fwrite("data", 1, 4, fp);
        fwrite(&data_size, 4, 1, fp);
        fwrite(pcm16, sizeof(int16_t), num_samples, fp);

        fclose(fp);
        free(pcm16);
        printf("Wrote WAV file: %s\n", wav_path);
    }

    free(output);
    return 0;
}
