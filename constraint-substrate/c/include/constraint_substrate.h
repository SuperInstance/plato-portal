#ifndef CONSTRAINT_SUBSTRATE_H
#define CONSTRAINT_SUBSTRATE_H

#include <stdint.h>
#include <math.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Lattice snap */
typedef struct { double a; double b; double error; } CsSnapResult;
CsSnapResult cs_snap(double x, double y, uint32_t group_order);

/* Funnel step */
typedef struct { double value; double epsilon; } CsFunnelResult;
CsFunnelResult cs_funnel_step(double current, double target, double epsilon, double decay);

/* Holonomy */
double cs_holonomy(const double* values, uint32_t count, double modulus);

/* Rigidity */
typedef struct { uint32_t a; uint32_t b; } CsEdge;
int cs_is_laman(uint32_t n, const CsEdge* edges, uint32_t edge_count);

/* Consensus */
typedef struct { double* values; int converged; } CsConsensusResult;
CsConsensusResult cs_consensus(const double* values, uint32_t count, double epsilon);
CsConsensusResult cs_consensus_mod(const double* values, uint32_t count, double epsilon, double modulus);

/* Helper to free consensus result */
void cs_consensus_free(CsConsensusResult result);

#ifdef __cplusplus
}
#endif

#endif /* CONSTRAINT_SUBSTRATE_H */
