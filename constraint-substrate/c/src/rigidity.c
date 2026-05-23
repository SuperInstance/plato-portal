#include "constraint_substrate.h"
#include <string.h>
#include <stdlib.h>

/* Count edges where both endpoints lie in the vertex subset. */
static int edge_count_in_subgraph(const CsEdge* edges, uint32_t edge_count,
                                   const int* in_subset) {
    int count = 0;
    for (uint32_t i = 0; i < edge_count; i++) {
        if (in_subset[edges[i].a] && in_subset[edges[i].b]) {
            count++;
        }
    }
    return count;
}

/* Recursive combination generator: choose k vertices from 0..n-1.
   Calls callback for each combination. Returns 0 if callback returns 0 (early exit). */
typedef int (*combo_cb)(const int* subset, int k, void* ctx);

static int generate_combos(int start, int n, int k, int* combo, int combo_len,
                            combo_cb cb, void* ctx) {
    if (combo_len == k) {
        return cb(combo, k, ctx);
    }
    for (int i = start; i < n; i++) {
        combo[combo_len] = i;
        int ret = generate_combos(i + 1, n, k, combo, combo_len + 1, cb, ctx);
        if (ret == 0) return 0;  /* early exit */
    }
    return 1;
}

typedef struct {
    const CsEdge* edges;
    uint32_t edge_count;
    int* in_subset;
    int result;
} laman_ctx;

static int check_subset(const int* subset, int k, void* user_data) {
    laman_ctx* ctx = (laman_ctx*)user_data;

    /* Build in_subset bitmap */
    memset(ctx->in_subset, 0, sizeof(int) * 16);  /* n <= 10 */
    for (int i = 0; i < k; i++) {
        ctx->in_subset[subset[i]] = 1;
    }

    int limit = 2 * k - 3;
    int count = edge_count_in_subgraph(ctx->edges, ctx->edge_count, ctx->in_subset);
    if (count > limit) {
        ctx->result = 0;  /* too many edges in subgraph */
        return 0;  /* early exit */
    }
    return 1;
}

int cs_is_laman(uint32_t n, const CsEdge* edges, uint32_t edge_count) {
    if (n < 2) return 0;
    if (n == 2) return edge_count >= 1;
    uint32_t required = 2 * n - 3;
    if (edge_count < required) return 0;

    /* For n <= 10, check all subsets of size 2..n */
    if (n <= 10) {
        int combo[10];
        int in_subset[16];
        laman_ctx ctx;
        ctx.edges = edges;
        ctx.edge_count = edge_count;
        ctx.in_subset = in_subset;
        ctx.result = 1;

        for (uint32_t k = 2; k <= n; k++) {
            int ret = generate_combos(0, (int)n, (int)k, combo, 0, check_subset, &ctx);
            if (ret == 0) return 0;  /* early exit: found violating subgraph */
        }
    }

    return 1;
}
