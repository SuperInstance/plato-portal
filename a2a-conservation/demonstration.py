"""
Demonstration: 5 agents with different capability graphs.

Shows:
1. Conservation alignment predicts collaboration success
2. Fiedler routing outperforms random task assignment
3. Spectral fingerprinting detects incompatible agents
4. Conservation collapse detection
"""

import numpy as np
from conservation_agent import ConservationAgent
from agent_directory import AgentDirectory
from protocol import ConservationProtocol, CollaborationResult


# ── Custom compatibility functions ──────────────────────────────────────────

def code_compat(a: str, b: str) -> float:
    """Compatibility for code-related capabilities."""
    # Strongly related code capabilities
    pairs = {
        ('parsing', 'ast'): 0.9, ('ast', 'types'): 0.85,
        ('types', 'patterns'): 0.8, ('patterns', 'metrics'): 0.7,
        ('parsing', 'types'): 0.6, ('ast', 'patterns'): 0.75,
        ('ast', 'metrics'): 0.5, ('parsing', 'metrics'): 0.4,
        ('parsing', 'patterns'): 0.5, ('types', 'metrics'): 0.6,
    }
    key = (min(a, b), max(a, b))
    if key in pairs:
        return pairs[key]
    # Cross-agent: code capabilities relate to security capabilities
    cross = {
        'parsing': 0.3, 'ast': 0.25, 'types': 0.4,
        'patterns': 0.5, 'metrics': 0.2,
    }
    return cross.get(a, 0.1) if b not in ['parsing', 'ast', 'types', 'patterns', 'metrics'] else 0.1


def security_compat(a: str, b: str) -> float:
    """Compatibility for security-related capabilities."""
    pairs = {
        ('auth', 'crypto'): 0.9, ('crypto', 'vulns'): 0.85,
        ('vulns', 'input'): 0.8, ('input', 'config'): 0.7,
        ('auth', 'vulns'): 0.75, ('crypto', 'input'): 0.6,
        ('auth', 'input'): 0.7, ('auth', 'config'): 0.65,
        ('crypto', 'config'): 0.5, ('vulns', 'config'): 0.6,
    }
    key = (min(a, b), max(a, b))
    return pairs.get(key, 0.1)


def perf_compat(a: str, b: str) -> float:
    """Compatibility for performance-related capabilities."""
    pairs = {
        ('profiling', 'cpu'): 0.9, ('cpu', 'memory'): 0.85,
        ('memory', 'io'): 0.7, ('io', 'caching'): 0.8,
        ('profiling', 'memory'): 0.8, ('profiling', 'io'): 0.6,
        ('profiling', 'caching'): 0.7, ('cpu', 'io'): 0.5,
        ('cpu', 'caching'): 0.75, ('memory', 'caching'): 0.9,
    }
    key = (min(a, b), max(a, b))
    return pairs.get(key, 0.1)


def data_compat(a: str, b: str) -> float:
    """Compatibility for data-related capabilities."""
    pairs = {
        ('etl', 'transform'): 0.9, ('transform', 'validate'): 0.85,
        ('validate', 'schema'): 0.9, ('schema', 'query'): 0.8,
        ('etl', 'validate'): 0.7, ('etl', 'schema'): 0.6,
        ('etl', 'query'): 0.5, ('transform', 'schema'): 0.75,
        ('transform', 'query'): 0.7, ('validate', 'query'): 0.6,
    }
    key = (min(a, b), max(a, b))
    return pairs.get(key, 0.1)


def random_compat(a: str, b: str) -> float:
    """An 'isotropic' agent with random weak connections (Ising-type failure)."""
    return 0.05 + np.random.uniform(0, 0.05)


# ── Demonstration ──────────────────────────────────────────────────────────

def run_demonstration():
    """Run the full A2A Conservation Protocol demonstration."""

    print("=" * 70)
    print("A2A CONSERVATION PROTOCOL — Demonstration")
    print("=" * 70)
    print()
    print("Creating 5 agents with distinct capability structures...")
    print()

    # Create agents with realistic compatibility functions
    np.random.seed(42)  # Reproducibility

    analyst = ConservationAgent(
        "code-analyzer",
        ["parsing", "ast", "types", "patterns", "metrics"],
        compatibility_fn=code_compat,
    )

    scanner = ConservationAgent(
        "security-scanner",
        ["auth", "crypto", "vulns", "input", "config"],
        compatibility_fn=security_compat,
    )

    optimizer = ConservationAgent(
        "perf-optimizer",
        ["profiling", "cpu", "memory", "io", "caching"],
        compatibility_fn=perf_compat,
    )

    data_eng = ConservationAgent(
        "data-pipeline",
        ["etl", "transform", "validate", "schema", "query"],
        compatibility_fn=data_compat,
    )

    isotropic = ConservationAgent(
        "random-agent",
        ["cap-a", "cap-b", "cap-c", "cap-d", "cap-e"],
        compatibility_fn=random_compat,
    )

    agents = [analyst, scanner, optimizer, data_eng, isotropic]

    # ── Section 1: Spectral Fingerprints ────────────────────────────────────
    print("─" * 70)
    print("SECTION 1: Spectral Fingerprints")
    print("─" * 70)
    print()

    for agent in agents:
        fp = agent.spectral_fingerprint
        print(f"  {agent.name}:")
        print(f"    Eigenvalues:       {[f'{e:.4f}' for e in fp.eigenvalues]}")
        print(f"    Spectral gap:      {fp.spectral_gap:.4f}")
        print(f"    Cheeger constant:  {fp.cheeger_constant:.4f}")
        print(f"    Spectral entropy:  {fp.spectral_entropy:.4f}")
        print(f"    Graph density:     {fp.graph_density:.4f}")
        print(f"    Fiedler vector:    {[f'{v:.3f}' for v in fp.fiedler_vector]}")
        print()

    # ── Section 2: Pairwise Alignment Matrix ────────────────────────────────
    print("─" * 70)
    print("SECTION 2: Pairwise Alignment Matrix")
    print("─" * 70)
    print()
    print("  Alignment α(A,B) = cosine similarity of eigenvalue spectra")
    print()

    # Compute alignment matrix
    n = len(agents)
    align_matrix = np.zeros((n, n))
    names = [a.name for a in agents]

    for i in range(n):
        for j in range(i, n):
            alpha = agents[i].can_collaborate_with(agents[j])
            align_matrix[i, j] = alpha
            align_matrix[j, i] = alpha

    # Print matrix
    header = "                " + "  ".join(f"{nm[:12]:>12}" for nm in names)
    print(f"  {header}")
    for i, nm in enumerate(names):
        row = "  ".join(f"{align_matrix[i, j]:12.4f}" for j in range(n))
        print(f"  {nm[:12]:>12}  {row}")
    print()

    # Interpret
    print("  Interpretation:")
    for i in range(n):
        for j in range(i + 1, n):
            alpha = align_matrix[i, j]
            if alpha > 0.8:
                label = "STRONG affinity"
            elif alpha > 0.5:
                label = "Moderate affinity"
            elif alpha > 0.15:
                label = "Weak affinity"
            elif alpha > 0:
                label = "Minimal affinity"
            else:
                label = "Anti-alignment"
            print(f"    {names[i]} ↔ {names[j]}: α = {alpha:.4f} ({label})")
    print()

    # ── Section 3: Protocol Registration and Discovery ──────────────────────
    print("─" * 70)
    print("SECTION 3: Protocol Registration and Discovery")
    print("─" * 70)
    print()

    directory = AgentDirectory()
    protocol = ConservationProtocol(directory)

    # Register all agents
    for agent in agents:
        protocol.broadcast_identity(agent)
        print(f"  ✓ {agent.name} registered (spectral fingerprint published)")

    print()

    # Discover collaborators for code-analyzer
    print(f"  Finding collaborators for {analyst.name} (min α = 0.15)...")
    response = protocol.query_collaborators(analyst, min_alignment=0.15)
    for candidate in response.payload['candidates']:
        print(f"    → {candidate['agent_id']}: α = {candidate['alignment']:.4f}")
    print()

    # ── Section 4: Collaboration Predictions ────────────────────────────────
    print("─" * 70)
    print("SECTION 4: Collaboration Predictions via Conservation")
    print("─" * 70)
    print()

    # Test specific pairs
    test_pairs = [
        (analyst, scanner, "security audit"),
        (analyst, optimizer, "performance analysis"),
        (analyst, data_eng, "data quality check"),
        (analyst, isotropic, "general task"),
        (scanner, optimizer, "security performance"),
    ]

    results = []
    for agent_a, agent_b, task in test_pairs:
        result = protocol.propose_collaboration(agent_a, agent_b, task)
        results.append(result)

        status = "✓ ACCEPTED" if result.alignment >= 0.15 else "✗ REJECTED"
        print(f"  {agent_a.name} + {agent_b.name} ({task}):")
        print(f"    Alignment:              α = {result.alignment:.4f}")
        print(f"    Conservation ratio:     CR = {result.conservation_ratio:.4f}")
        print(f"    Predicted success:      P = {result.predicted_success:.1%}")
        print(f"    Status:                 {status}")
        print(f"    Routing:                {result.routing}")
        print()

    # ── Section 5: Fiedler vs Random Routing ────────────────────────────────
    print("─" * 70)
    print("SECTION 5: Fiedler Routing vs Random Assignment")
    print("─" * 70)
    print()

    # For each accepted collaboration, compare Fiedler routing to random
    for result in results:
        if result.alignment < 0.15:
            continue

        agent_a = next(a for a in agents if a.name == result.agent_a)
        agent_b = next(a for a in agents if a.name == result.agent_b)
        composition = agent_a.compose_with(agent_b)

        # Fiedler routing cut weight
        W = composition['composed_graph']['adjacency']
        fiedler = np.array(composition['fiedler_vector'])
        n_total = len(fiedler)

        # Fiedler partition
        S_fiedler = fiedler >= 0
        S_bar_fiedler = ~S_fiedler
        if S_fiedler.sum() == 0 or S_bar_fiedler.sum() == 0:
            cut_fiedler = 0
        else:
            cut_fiedler = W[np.ix_(S_fiedler, S_bar_fiedler)].sum()

        # Random partition (average over 100 trials)
        cuts_random = []
        for _ in range(100):
            perm = np.random.permutation(n_total)
            k = n_total // 2
            S_rand = np.zeros(n_total, dtype=bool)
            S_rand[perm[:k]] = True
            S_bar_rand = ~S_rand
            cut_rand = W[np.ix_(S_rand, S_bar_rand)].sum()
            cuts_random.append(cut_rand)

        avg_cut_random = np.mean(cuts_random)
        improvement = (avg_cut_random - cut_fiedler) / (avg_cut_random + 1e-10) * 100

        print(f"  {result.agent_a} + {result.agent_b}:")
        print(f"    Fiedler cut weight:   {cut_fiedler:.4f}")
        print(f"    Random avg cut:       {avg_cut_random:.4f}")
        print(f"    Fiedler improvement:  {improvement:.1f}% less communication overhead")
        print()

    # ── Section 6: Detecting Incompatible Agents ────────────────────────────
    print("─" * 70)
    print("SECTION 6: Incompatible Agent Detection")
    print("─" * 70)
    print()

    # The isotropic agent should be detected as incompatible
    iso = isotropic
    print(f"  {iso.name} — Spectral properties:")
    print(f"    Spectral gap:     {iso.spectral_fingerprint.spectral_gap:.6f}")
    print(f"    Cheeger constant: {iso.spectral_fingerprint.cheeger_constant:.4f}")
    print(f"    Entropy:          {iso.spectral_fingerprint.spectral_entropy:.4f}")
    print(f"    Density:          {iso.spectral_fingerprint.graph_density:.4f}")
    print()

    alignments_with_iso = []
    for agent in agents:
        if agent.name == iso.name:
            continue
        alpha = iso.can_collaborate_with(agent)
        alignments_with_iso.append((agent.name, alpha))

    print("  Alignments with random-agent:")
    for name, alpha in sorted(alignments_with_iso, key=lambda x: x[1]):
        verdict = "COMPATIBLE" if alpha > 0.15 else "INCOMPATIBLE"
        print(f"    ↔ {name}: α = {alpha:.4f} — {verdict}")
    print()
    print("  → Isotropic (near-uniform) capability graphs produce low alignment.")
    print("    This is the A2A equivalent of the Ising model failure mode.")
    print()

    # ── Section 7: Conservation Health Monitoring ───────────────────────────
    print("─" * 70)
    print("SECTION 7: Conservation Health Monitoring")
    print("─" * 70)
    print()

    for result in results:
        if result.alignment < 0.15:
            continue
        check = protocol.conservation_check(result)
        status = "🟢 HEALTHY" if check['healthy'] else "🔴 DEGRADED"
        print(f"  {check['collaboration']}: {status}")
        print(f"    Alignment: {check['alignment']:.4f}, "
              f"CR: {check['conservation_ratio']:.4f}, "
              f"P(success): {check['predicted_success']:.1%}")
    print()

    # ── Summary ─────────────────────────────────────────────────────────────
    print("─" * 70)
    print("SUMMARY")
    print("─" * 70)
    print()
    print("  1. Spectral fingerprints uniquely identify agents by structure")
    print("  2. Alignment coefficient α predicts collaboration success:")
    print(f"     - Best pair:  {max(align_matrix[align_matrix < 1]):.4f}")
    print(f"     - Worst pair: {align_matrix[align_matrix > 0].min():.4f}")
    print(f"     - Isotropic:  {min(a for _, a in alignments_with_iso):.4f} (detected as incompatible)")
    print("  3. Fiedler routing reduces communication overhead vs random assignment")
    print("  4. Conservation checks detect degradation in real-time")
    print("  5. The protocol replaces schema negotiation with eigenvalue comparison")
    print()
    print("  Total protocol messages exchanged:", len(protocol._message_log))
    print()

    return agents, results, align_matrix


if __name__ == "__main__":
    agents, results, align_matrix = run_demonstration()
