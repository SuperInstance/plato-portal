# Philosophy & Ethics: Conservation Spectral Analysis

*Three explorations of moral philosophy through the lens of spectral graph theory, where conservation laws reveal the hidden architecture of ethical reasoning.*

---

## ROUND 1 — The Moral Graph: Ethical Coherence as Conservation

### The Idea

Every moral system is a graph. The nodes are principles — "do no harm," "respect autonomy," "keep promises," "maximize well-being." The edges are *dependencies*: one principle supports, implies, or constrains another. When we say "informed consent depends on respecting autonomy," we're drawing an edge between two moral nodes.

This is not metaphor. It's mathematics. And once we formalize it, something remarkable emerges: **the moral Laplacian measures ethical coherence.**

Think of it like heat diffusion on a surface. If you pin the temperature at certain points (moral axioms), the Laplacian governs how values propagate through the network. A well-connected moral graph — where principles mutually support each other — has high conservation: energy placed at any node flows smoothly, reaches equilibrium, and the system is consistent. A fractured graph — where principles contradict or ignore each other — bleeds energy. The Laplacian reveals this as low conservation. Hypocrisy, it turns out, is mathematically detectable.

### Why This Matters

Philosophers have argued for millennia about whether moral systems are "coherent." Kant demanded logical consistency. Utilitarians demanded consequentialist unity. Virtue ethicists demanded narrative harmony. But these were qualitative arguments. The Laplacian gives us a *quantitative* measure. We can literally compute how coherent an ethical framework is — and compare utilitarian ethics to deontological ethics by comparing their spectral properties.

The key insight: **conservation is coherence.** A moral system where principles support each other — where accepting one principle naturally leads to accepting related ones — has a Laplacian with low spectral gap. Energy (moral commitment) placed at any node diffuses evenly. The system is "at one with itself." Conversely, a moral system riddled with contradictions — where believing one principle requires violating another — has a high spectral gap. Energy gets trapped in isolated clusters. The system is fragmented, hypocritical, self-defeating.

Consider the utilitarian graph. The central node is "maximize well-being." Everything connects to it. The Laplacian is dominated by this hub — low spectral gap, high conservation, but potentially *brittle*. Remove the hub and the graph shatters. This is the well-known criticism: utilitarianism is coherent but monolithic. One principle dominates.

Now consider a deontological graph. Multiple independent principles — "don't lie," "keep promises," "respect persons" — each forming their own cluster with fewer inter-cluster edges. The Laplacian has a *higher* spectral gap. Energy doesn't flow as freely between clusters. But the system is *robust* — knock out one principle and the others still stand. This is the virtue of pluralism: lower coherence, higher resilience.

### Deep Structure: The Eigenvalue Spectrum

The eigenvalues of the moral Laplacian tell us everything:

- **λ₁ = 0** (always): The trivial eigenvalue. Its eigenvector is the uniform distribution — the state where all moral principles carry equal weight. This is the "moral relativist" equilibrium.
- **λ₂**: The algebraic connectivity (Fiedler value). How tightly connected is the moral graph? High λ₂ = utilitarian-style monism. Low λ₂ = pluralist fragmentation.
- **The full spectrum**: The distribution of eigenvalues reveals the moral system's "personality." Clustered eigenvalues suggest natural groupings of principles. Outliers suggest principles that are either foundational (very low) or isolated (very high).

We can use the Fiedler vector (the eigenvector corresponding to λ₂) to partition the moral graph — finding the natural "fault lines" in an ethical system. Where does the graph want to split? Those are the deep tensions in the moral theory. For utilitarianism, there might be only one partition: everything vs. nothing. For deontology, there might be natural partitions between duty clusters.

### Application: Detecting Moral Hypocrisy

Here's the practical upshot. Take any person's stated moral beliefs. Build the graph. Compute the Laplacian. Check conservation. If someone claims to believe in "equal treatment" and "meritocracy" and "nepotism is wrong" but their social network shows consistent favoritism, the Laplacian will reveal the gap. Their *stated* moral graph has high conservation. Their *enacted* moral graph — built from behavior, not words — has low conservation. The difference between the two is a quantitative measure of hypocrisy.

This isn't about judging people. It's about giving moral philosophy the same analytical tools that physics, engineering, and network science take for granted. We can *measure* ethical coherence. We can *compare* moral systems. We can *detect* when someone's ethics are fragmented.

### The Conservation Interpretation

In physics, conservation laws (energy, momentum, angular momentum) arise from symmetries (Noether's theorem). The same principle applies here: **moral conservation arises from ethical symmetry.** If a moral system treats all agents equally (symmetry under permutation), it conserves moral energy. If it treats all principles as equally valid (symmetry under principle-swap), it conserves moral commitment. The breakdown of conservation is the breakdown of symmetry — and that's where we find bias, prejudice, and contradiction.

### Code: MoralGraph

```python
import numpy as np
import networkx as nx
from scipy.linalg import eigh
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class MoralPrinciple:
    """A node in the moral graph."""
    name: str
    weight: float = 1.0          # How strongly held
    description: str = ""
    category: str = "general"     # e.g., 'deontological', 'consequentialist', 'virtue'

@dataclass
class MoralDependency:
    """An edge in the moral graph."""
    source: str
    target: str
    strength: float = 1.0         # How strongly source supports target
    relation: str = "supports"    # 'supports', 'implies', 'constrains', 'contradicts'
    note: str = ""

class MoralGraph:
    """
    Represents a moral system as a weighted directed graph.
    Principles are nodes; dependencies are edges.
    The moral Laplacian quantifies ethical coherence.
    """

    def __init__(self, name: str = "Unnamed Ethics"):
        self.name = name
        self.graph = nx.DiGraph()
        self.principles: dict[str, MoralPrinciple] = {}

    def add_principle(self, name: str, weight: float = 1.0,
                      description: str = "", category: str = "general"):
        self.principles[name] = MoralPrinciple(name, weight, description, category)
        self.graph.add_node(name)

    def add_dependency(self, source: str, target: str, strength: float = 1.0,
                       relation: str = "supports"):
        """Add a moral dependency (edge) between two principles."""
        # Contradictions get negative weight
        sign = -1.0 if relation == "contradicts" else 1.0
        self.graph.add_edge(source, target, weight=sign * strength, relation=relation)

    def build_weighted_adjacency(self) -> np.ndarray:
        """Build the weighted adjacency matrix (symmetric, for undirected view)."""
        nodes = list(self.graph.nodes())
        n = len(nodes)
        A = np.zeros((n, n))
        for i, u in enumerate(nodes):
            for j, v in enumerate(nodes):
                if self.graph.has_edge(u, v):
                    A[i, j] += self.graph[u][v]['weight']
                if self.graph.has_edge(v, u):
                    A[i, j] += self.graph[v][u]['weight']
        return A

    def moral_laplacian(self) -> tuple[np.ndarray, list[str]]:
        """Compute the moral Laplacian: L = D - A."""
        A = self.build_weighted_adjacency()
        D = np.diag(A.sum(axis=1))
        L = D - A
        nodes = list(self.graph.nodes())
        return L, nodes

    def spectral_analysis(self) -> dict:
        """
        Full spectral analysis of the moral graph.
        Returns eigenvalues, eigenvectors, and derived metrics.
        """
        L, nodes = self.moral_laplacian()
        eigenvalues, eigenvectors = eigh(L)

        # Sort by eigenvalue
        idx = np.argsort(eigenvalues)
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        # Conservation score: inverse of spectral gap (λ₂)
        # High conservation = low spectral gap = principles flow into each other
        lambda_2 = eigenvalues[1] if len(eigenvalues) > 1 else 0.0
        conservation = 1.0 / (1.0 + lambda_2)

        # Coherence ratio: how many "significant" clusters exist
        significant = np.sum(eigenvalues < 0.1 * eigenvalues[-1]) if eigenvalues[-1] > 0 else len(eigenvalues)

        # Fiedler vector: the partition that reveals moral fault lines
        fiedler = eigenvectors[:, 1] if eigenvectors.shape[1] > 1 else np.ones(len(nodes))

        # Partition nodes by Fiedler vector sign
        partition_a = [nodes[i] for i in range(len(nodes)) if fiedler[i] >= 0]
        partition_b = [nodes[i] for i in range(len(nodes)) if fiedler[i] < 0]

        return {
            "eigenvalues": eigenvalues,
            "eigenvectors": eigenvectors,
            "spectral_gap": lambda_2,
            "conservation_score": conservation,
            "n_clusters": int(significant),
            "fiedler_vector": fiedler,
            "partition_a": partition_a,
            "partition_b": partition_b,
            "nodes": nodes,
        }

    def hypocrisy_score(self, enacted: "MoralGraph") -> float:
        """
        Compare stated vs enacted moral graphs.
        Returns a score from 0 (perfectly consistent) to 1 (total hypocrite).
        """
        stated_analysis = self.spectral_analysis()
        enacted_analysis = enacted.spectral_analysis()

        # Compare conservation scores
        stated_cons = stated_analysis["conservation_score"]
        enacted_cons = enacted_analysis["conservation_score"]

        # Hypocrisy = gap between stated and enacted coherence
        gap = abs(stated_cons - enacted_cons)
        return gap

    def coherence_report(self) -> str:
        analysis = self.spectral_analysis()
        lines = [
            f"=== Moral Graph Analysis: {self.name} ===",
            f"Principles: {len(self.principles)}",
            f"Dependencies: {self.graph.number_of_edges()}",
            f"Spectral gap (λ₂): {analysis['spectral_gap']:.4f}",
            f"Conservation score: {analysis['conservation_score']:.4f}",
            f"Estimated clusters: {analysis['n_clusters']}",
            f"\nFiedler Partition:",
            f"  Group A: {', '.join(analysis['partition_a']) or '(empty)'}",
            f"  Group B: {', '.join(analysis['partition_b']) or '(empty)'}",
            f"\nEigenvalue spectrum: {np.round(analysis['eigenvalues'], 4)}",
        ]
        return "\n".join(lines)


# ──── Build Example Ethical Frameworks ────

def build_utilitarian_ethics() -> MoralGraph:
    """Utilitarian ethics: single hub (maximize well-being) dominates."""
    g = MoralGraph("Utilitarian Ethics")
    g.add_principle("maximize_wellbeing", 2.0, "The greatest good for the greatest number", "consequentialist")
    g.add_principle("minimize_suffering", 1.5, "Reducing harm is paramount", "consequentialist")
    g.add_principle("impartiality", 1.0, "Everyone's welfare counts equally", "consequentialist")
    g.add_principle("act_for_best_outcome", 1.0, "Choose the action with best consequences", "consequentialist")
    g.add_principle("consider_future", 0.8, "Long-term consequences matter", "consequentialist")
    g.add_principle("aggregate_preferences", 0.7, "Sum individual utilities", "consequentialist")

    # Strong hub structure — everything connects through maximize_wellbeing
    hub = "maximize_wellbeing"
    for p in ["minimize_suffering", "impartiality", "act_for_best_outcome",
              "consider_future", "aggregate_preferences"]:
        g.add_dependency(hub, p, 1.5, "implies")
        g.add_dependency(p, hub, 1.0, "supports")

    g.add_dependency("minimize_suffering", "act_for_best_outcome", 0.8, "supports")
    g.add_dependency("impartiality", "aggregate_preferences", 1.0, "implies")
    return g


def build_deontological_ethics() -> MoralGraph:
    """Deontological ethics: multiple independent duty clusters."""
    g = MoralGraph("Deontological Ethics")
    g.add_principle("categorical_imperative", 2.0, "Act only on universalizable maxims", "deontological")
    g.add_principle("respect_persons", 1.5, "Treat people as ends, never merely means", "deontological")
    g.add_principle("dont_lie", 1.0, "Truthfulness is a perfect duty", "deontological")
    g.add_principle("keep_promises", 1.0, "Fidelity to commitments", "deontological")
    g.add_principle("dont_kill", 1.5, "Preservation of life", "deontological")
    g.add_principle("help_others", 0.8, " imperfect duty of beneficence", "deontological")
    g.add_principle("universalizability", 1.2, "Maxims must be universalizable", "deontological")

    # Cluster 1: Truth-related duties
    g.add_dependency("categorical_imperative", "dont_lie", 1.5, "implies")
    g.add_dependency("dont_lie", "categorical_imperative", 0.5, "supports")
    g.add_dependency("categorical_imperative", "keep_promises", 1.2, "implies")
    g.add_dependency("keep_promises", "dont_lie", 0.8, "supports")

    # Cluster 2: Person-respect duties
    g.add_dependency("respect_persons", "dont_kill", 1.5, "implies")
    g.add_dependency("dont_kill", "respect_persons", 0.5, "supports")
    g.add_dependency("respect_persons", "help_others", 0.8, "supports")

    # Cluster 3: Universalizability
    g.add_dependency("categorical_imperative", "universalizability", 1.0, "implies")
    g.add_dependency("universalizability", "dont_lie", 0.7, "supports")

    # Cross-cluster links (weaker)
    g.add_dependency("respect_persons", "keep_promises", 0.5, "supports")
    return g


def build_virtue_ethics() -> MoralGraph:
    """Virtue ethics: dense web of character-trait relationships."""
    g = MoralGraph("Virtue Ethics")
    virtues = [
        ("courage", 1.0, "Mean between cowardice and recklessness"),
        ("temperance", 1.0, "Mean between indulgence and insensibility"),
        ("justice", 1.2, "Giving each their due"),
        ("practical_wisdom", 1.5, "Phronesis — the master virtue"),
        ("honesty", 0.9, "Truthfulness in character"),
        ("generosity", 0.8, "Mean between miserliness and prodigality"),
        ("compassion", 1.0, "Concern for others' suffering"),
        ("integrity", 1.1, "Wholeness of character"),
    ]
    for name, weight, desc in virtues:
        g.add_principle(name, weight, desc, "virtue")

    # Dense interconnection — virtues support each other
    for i, (v1, _, _) in enumerate(virtues):
        for j, (v2, _, _) in enumerate(virtues):
            if i != j:
                strength = 0.3 + 0.1 * np.random.random()
                g.add_dependency(v1, v2, strength, "supports")
    return g


# ──── Run Analysis ────

if __name__ == "__main__":
    np.random.seed(42)

    frameworks = [build_utilitarian_ethics(), build_deontological_ethics(), build_virtue_ethics()]

    for fw in frameworks:
        analysis = fw.spectral_analysis()
        print(f"\n{fw.coherence_report()}")
        print(f"  → Conservation: {analysis['conservation_score']:.4f}")
        print(f"  → Spectral gap: {analysis['spectral_gap']:.4f}")
        print(f"  → Interpretation: ", end="")
        if analysis['conservation_score'] > 0.7:
            print("Highly coherent — principles flow naturally into each other")
        elif analysis['conservation_score'] > 0.4:
            print("Moderately coherent — some principled tensions exist")
        else:
            print("Low coherence — significant moral fault lines")

    # Hypocrisy detection
    print("\n\n=== Hypocrisy Detection Example ===")
    stated = build_utilitarian_ethics()
    enacted = MoralGraph("Enacted 'Utilitarian' Ethics")
    enacted.add_principle("maximize_wellbeing", 0.5, "Claimed but weakly followed")
    enacted.add_principle("self_interest", 2.0, "Actually prioritized")
    enacted.add_principle("favor_friends", 1.5, "Ingroup favoritism")
    enacted.add_principle("avoid_discomfort", 1.0, "Comfort-seeking")
    enacted.add_dependency("self_interest", "favor_friends", 1.5, "supports")
    enacted.add_dependency("avoid_discomfort", "self_interest", 1.0, "supports")
    # Contradiction with claimed principle
    enacted.add_dependency("self_interest", "maximize_wellbeing", 1.0, "contradicts")

    hypocrisy = stated.hypocrisy_score(enacted)
    print(f"Stated conservation: {stated.spectral_analysis()['conservation_score']:.4f}")
    print(f"Enacted conservation: {enacted.spectral_analysis()['conservation_score']:.4f}")
    print(f"Hypocrisy gap: {hypocrisy:.4f}")
    print(f"Verdict: {'HYPOCRITE' if hypocrisy > 0.2 else 'CONSISTENT'}")
```

---

## ROUND 2 — The Decision Theory Laplacian: Preference Coherence as Conservation

### The Idea

Every decision is a node. Every preference is an edge. "I prefer A to B" draws a directed edge from B to A (energy flows toward the preferred option). The full set of preferences forms a graph, and its Laplacian reveals whether those preferences are *coherent*.

This is not a new observation — economists have studied preference cycles (A > B > C > A) since Condorcet. But the spectral perspective adds something new: **the decision Laplacian quantifies exactly how incoherent a set of preferences is.** Not just "there's a cycle" but "the degree of incoherence is 0.73 on a scale from 0 (perfect) to 1 (chaotic)."

Rational agents — the kind assumed by classical economics — have perfectly transitive preferences with high conservation. Real humans, with all our contradictions, have much lower conservation. The gap between ideal rationality and actual behavior is, quite literally, a spectral gap.

### The Structure of Preferences

Consider a simple decision: choosing a restaurant. The options are nodes. The edges encode pairwise preferences: "I prefer Italian to Mexican" (weight +1), "I prefer Mexican to Thai" (weight +1), "I prefer Thai to Italian" (weight +1). This cycle (a Condorcet paradox for a single agent) creates a Laplacian that can't reach equilibrium. Energy circulates endlessly. Conservation is low. The agent is stuck — no option is definitively preferred.

Now expand this to social choice. A group of voters each has their own preference graph. The social choice problem is to aggregate these individual graphs into a single collective graph. Arrow's impossibility theorem tells us this can't be done perfectly — no aggregation rule satisfies all desirable properties simultaneously. In spectral terms: **the collective preference graph always has lower conservation than the individual graphs.** Group decision-making is inherently less coherent than individual decision-making. The spectral gap of the social Laplacian is always larger than the average individual spectral gap.

This is Arrow's theorem, restated: conservation is lost in aggregation. Just as energy is lost to entropy in thermodynamic processes, preference coherence is lost to aggregation in social choice. The "impossibility" isn't about any particular voting rule — it's about the fundamental information loss when you compress multiple preference graphs into one.

### Temporal Preferences and Dynamic Incoherence

Real decisions aren't static. Our preferences change over time. The dynamic preference graph has a temporal dimension: nodes at time t connect to nodes at time t+1. The Laplacian of this temporal graph measures *dynamic coherence* — how consistent are your preferences over time?

Time-inconsistent preferences (hyperbolic discounting, preference reversals) show up as temporal edges that violate the static graph's structure. You prefer saving money at t=0, but prefer spending at t=1. The temporal Laplacian captures this: conservation drops when your present self contradicts your past self's plans.

This connects to a deep result in decision theory: **the degree of dynamic inconsistency equals the conservation loss across time slices.** An agent with perfectly time-consistent preferences (exponential discounter) has a flat temporal Laplacian — conservation is preserved across time. An agent with hyperbolic discounting has a Laplacian that leaks conservation exponentially. The "present bias" that behavioral economists study is, spectrally, a conservation failure.

### Bounded Rationality as Spectral Approximation

Herbert Simon's bounded rationality — the idea that real agents "satisfice" rather than optimize — has a natural spectral interpretation. Perfect rationality requires computing the full eigendecomposition of the decision Laplacian. But this is expensive (O(n³) for n options). Bounded agents approximate: they compute only the top k eigenvectors, capturing the k most important preference dimensions.

The quality of this approximation depends on the eigenvalue spectrum. If the spectrum decays rapidly (most information in the first few eigenvalues), satisficing works well — the agent captures most of the preference structure with minimal computation. If the spectrum is flat (information spread evenly across all dimensions), satisficing fails — the agent needs nearly full computation to make good decisions.

This gives a precise meaning to "hard decisions": they're decisions where the preference Laplacian has a flat spectrum. Easy decisions have a rapidly decaying spectrum — the answer is clear from the dominant eigenvectors.

### The Conservation Tax of Rationality

Here's the deepest point: **perfect rationality has a conservation cost.** Maintaining perfectly transitive, time-consistent preferences across all possible decisions requires enormous cognitive resources. The Laplacian of a perfectly rational agent is a complete, consistent graph — every node connected to every other, with transitivity enforced. This graph has maximum conservation but also maximum maintenance cost.

Real agents trade off conservation against complexity. We allow small inconsistencies (low conservation) in exchange for not having to maintain a complete preference ordering (low complexity). This is the spectral analog of the speed-accuracy tradeoff: fast decisions sacrifice spectral coherence, accurate decisions require full spectral computation.

The optimal agent doesn't maximize conservation — it *optimizes the ratio* of conservation to computational cost. This is the spectral foundation of bounded rationality, and it connects decision theory directly to information theory and statistical physics.

### Code: DecisionLaplacian

```python
import numpy as np
from itertools import permutations
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Preference:
    """A pairwise preference: agent prefers 'higher' over 'lower'."""
    higher: str   # The preferred option
    lower: str    # The less-preferred option
    weight: float = 1.0  # Strength of preference
    agent: str = "default"  # Which agent holds this preference


class DecisionLaplacian:
    """
    Decision theory through spectral analysis.
    Options = nodes, preferences = directed weighted edges.
    The Laplacian measures preference coherence.
    """

    def __init__(self, name: str = "Decision"):
        self.name = name
        self.options: list[str] = []
        self.preferences: list[Preference] = []

    def add_option(self, name: str):
        if name not in self.options:
            self.options.append(name)

    def add_preference(self, higher: str, lower: str,
                       weight: float = 1.0, agent: str = "default"):
        self.add_option(higher)
        self.add_option(lower)
        self.preferences.append(Preference(higher, lower, weight, agent))

    def build_preference_matrix(self, agent: Optional[str] = None) -> np.ndarray:
        """
        Build pairwise preference matrix P where P[i,j] = net preference of i over j.
        If agent specified, only use that agent's preferences.
        """
        n = len(self.options)
        idx = {opt: i for i, opt in enumerate(self.options)}
        P = np.zeros((n, n))

        prefs = self.preferences
        if agent is not None:
            prefs = [p for p in prefs if p.agent == agent]

        for pref in prefs:
            i, j = idx[pref.higher], idx[pref.lower]
            P[i, j] += pref.weight
            P[j, i] -= pref.weight

        return P

    def decision_laplacian(self, agent: Optional[str] = None) -> np.ndarray:
        """L = D - A where A is the symmetric part of the preference matrix."""
        P = self.build_preference_matrix(agent)
        A = (P + P.T) / 2  # Symmetrize
        # Take absolute values for adjacency weights
        A = np.abs(A)
        D = np.diag(A.sum(axis=1))
        L = D - A
        return L

    def coherence_analysis(self, agent: Optional[str] = None) -> dict:
        from scipy.linalg import eigh

        L = self.decision_laplacian(agent)
        eigenvalues, eigenvectors = eigh(L)

        idx = np.argsort(eigenvalues)
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        lambda_2 = eigenvalues[1] if len(eigenvalues) > 1 else 0.0
        conservation = 1.0 / (1.0 + lambda_2)

        # Rank options by dominant eigenvector (the "winner")
        if eigenvectors.shape[1] > 0:
            ranking_vector = eigenvectors[:, 0]
            ranking = sorted(range(len(self.options)),
                           key=lambda i: ranking_vector[i], reverse=True)
            ranked_options = [self.options[i] for i in ranking]
        else:
            ranked_options = self.options

        # Detect preference cycles via Condorcet check
        P = self.build_preference_matrix(agent)
        cycles = self._detect_cycles(P)

        # Dynamic inconsistency (if we had temporal data)
        spectral_flatness = 0.0
        if eigenvalues[-1] > 0:
            spectral_flatness = np.mean(eigenvalues[1:]) / eigenvalues[-1]

        return {
            "eigenvalues": eigenvalues,
            "conservation": conservation,
            "spectral_gap": lambda_2,
            "ranked_options": ranked_options,
            "cycles": cycles,
            "spectral_flatness": spectral_flatness,
            "decision_difficulty": "HARD" if spectral_flatness > 0.5 else "MODERATE" if spectral_flatness > 0.2 else "EASY",
        }

    def _detect_cycles(self, P: np.ndarray) -> list[tuple]:
        """Detect preference cycles (Condorcet-type)."""
        n = len(self.options)
        cycles = []
        for i, j, k in permutations(range(n), 3):
            if P[i, j] > 0 and P[j, k] > 0 and P[k, i] > 0:
                cycles.append((self.options[i], self.options[j], self.options[k]))
        return cycles

    def arrow_impossibility(self, agent_prefs: dict[str, list[Preference]]) -> dict:
        """
        Demonstrate Arrow's theorem spectrally:
        aggregate individual preference graphs and measure conservation loss.
        """
        individual_cons = {}
        for agent_name, prefs in agent_prefs.items():
            # Build temporary decision graph for this agent
            temp = DecisionLaplacian(f"Agent {agent_name}")
            temp.options = list(self.options)
            temp.preferences = prefs
            analysis = temp.coherence_analysis()
            individual_cons[agent_name] = analysis["conservation"]

        # Aggregate: use all preferences together
        agg_analysis = self.coherence_analysis()
        agg_cons = agg_analysis["conservation"]

        avg_individual = np.mean(list(individual_cons.values()))
        conservation_loss = avg_individual - agg_cons

        return {
            "individual_conservation": individual_cons,
            "average_individual": avg_individual,
            "collective_conservation": agg_cons,
            "conservation_loss": conservation_loss,
            "arrow_confirmed": conservation_loss > 0.01,
            "interpretation": (
                f"Conservation lost in aggregation: {conservation_loss:.4f}. "
                f"Arrow's theorem manifests as spectral information loss."
            ),
        }

    def report(self) -> str:
        analysis = self.coherence_analysis()
        lines = [
            f"=== Decision Analysis: {self.name} ===",
            f"Options: {', '.join(self.options)}",
            f"Preferences: {len(self.preferences)}",
            f"Conservation: {analysis['conservation']:.4f}",
            f"Spectral gap: {analysis['spectral_gap']:.4f}",
            f"Decision difficulty: {analysis['decision_difficulty']}",
            f"Spectral flatness: {analysis['spectral_flatness']:.4f}",
            f"Ranked options: {' > '.join(analysis['ranked_options'])}",
            f"Preference cycles: {len(analysis['cycles'])}",
        ]
        if analysis['cycles']:
            for c in analysis['cycles'][:5]:
                lines.append(f"  Cycle: {' > '.join(c)} > {c[0]}")
        return "\n".join(lines)


# ──── Examples ────

if __name__ == "__main__":
    np.random.seed(42)

    # 1. Perfectly rational agent (transitive preferences)
    rational = DecisionLaplacian("Rational Agent")
    options = ["Italian", "Mexican", "Thai", "Japanese", "Indian"]
    # Complete transitive ordering
    for i in range(len(options)):
        for j in range(i + 1, len(options)):
            rational.add_preference(options[i], options[j], 1.0, "rational")
    print(rational.report())
    print(f"  → Rational agents have HIGH conservation (transitive)\n")

    # 2. Confused agent (Condorcet cycle)
    confused = DecisionLaplacian("Confused Agent")
    confused.add_preference("Italian", "Mexican", 1.0)
    confused.add_preference("Mexican", "Thai", 1.0)
    confused.add_preference("Thai", "Italian", 1.0)  # Cycle!
    confused.add_preference("Japanese", "Indian", 1.0)
    print(confused.report())
    print(f"  → Cycles destroy conservation\n")

    # 3. Arrow's impossibility demonstration
    print("=== Arrow's Impossibility: Spectral Proof ===")
    social = DecisionLaplacian("Social Choice")
    candidates = ["Alice", "Bob", "Carol"]
    for c in candidates:
        social.add_option(c)

    # Three voters with different preferences
    voter_prefs = {
        "Voter1": [Preference("Alice", "Bob", 1.0, "Voter1"),
                    Preference("Bob", "Carol", 1.0, "Voter1"),
                    Preference("Alice", "Carol", 1.0, "Voter1")],
        "Voter2": [Preference("Bob", "Carol", 1.0, "Voter2"),
                    Preference("Carol", "Alice", 1.0, "Voter2"),
                    Preference("Bob", "Alice", 1.0, "Voter2")],
        "Voter3": [Preference("Carol", "Alice", 1.0, "Voter3"),
                    Preference("Alice", "Bob", 1.0, "Voter3"),
                    Preference("Carol", "Bob", 1.0, "Voter3")],
    }

    for prefs in voter_prefs.values():
        for p in prefs:
            social.preferences.append(p)

    arrow = social.arrow_impossibility(voter_prefs)
    for k, v in arrow.items():
        print(f"  {k}: {v}")

    # 4. Bounded rationality: spectral approximation
    print("\n=== Bounded Rationality: Spectral Approximation ===")
    big_decision = DecisionLaplacian("Complex Decision")
    n_opts = 20
    for i in range(n_opts):
        big_decision.add_option(f"Option_{i}")
    # Generate mostly-transitive preferences with some noise
    for i in range(n_opts):
        for j in range(i + 1, n_opts):
            w = 1.0 if np.random.random() > 0.15 else -0.5  # 15% chance of reversal
            big_decision.add_preference(f"Option_{i}", f"Option_{j}", w)

    analysis = big_decision.coherence_analysis()
    print(f"  Full conservation: {analysis['conservation']:.4f}")
    print(f"  Difficulty: {analysis['decision_difficulty']}")
    print(f"  Eigenvalue decay: {np.round(analysis['eigenvalues'][:8], 3)}")

    # Approximate with top-k eigenvalues
    eigs = analysis['eigenvalues']
    total_energy = np.sum(eigs[1:]**2)
    for k in [3, 5, 10]:
        captured = np.sum(eigs[1:k+1]**2) / total_energy * 100 if total_energy > 0 else 0
        print(f"  Top-{k} eigenvectors capture {captured:.1f}% of preference structure")
```

---

## ROUND 3 — The Value Alignment Graph: Spectral Measures of AI Alignment

### The Idea

AI alignment is the defining problem of our era. How do we ensure that artificial intelligence systems pursue goals compatible with human values? The standard framing — "we need to specify the right objective function" — is hopelessly inadequate. Human values aren't an objective function. They're a *graph*: interconnected, contextual, sometimes contradictory, and deeply dependent on each other.

The spectral approach to alignment is this: **represent human values as a graph, represent the AI's value model as another graph, and measure alignment as the conservation similarity between their Laplacians.** Aligned AI: the two Laplacians have similar spectra. Misaligned AI: the spectra diverge. The "alignment tax" — the cost of constraining an AI to be aligned — is the conservation cost of warping the AI's natural value graph to match humanity's.

This isn't just theoretical. Every large language model has an implicit value graph, embedded in its weights. When we fine-tune with RLHF (reinforcement learning from human feedback), we're modifying that graph — adding edges, changing weights, shifting the Laplacian. The quality of alignment is, at root, a spectral property.

### The Human Value Graph

Human values are not a list. They're a network. "Freedom" supports "creativity" which supports "self-expression" which supports "autonomy" which supports "freedom." "Safety" constrains "freedom." "Fairness" mediates between "equality" and "meritocracy." The value graph is dense, cyclic, and context-dependent.

Different cultures have different value graphs. The Laplacians of these graphs will have different spectra. This is not a problem for alignment — it's the *point*. Alignment doesn't mean making the AI adopt one specific culture's values. It means making the AI's value graph spectrally similar to *some* coherent human value graph. The space of "acceptable" AI value graphs is the space of graphs whose Laplacians are within some spectral distance of at least one human value graph.

### The Alignment Tax

Constraining an AI to be aligned has a cost. In unrestricted optimization, the AI can use any strategy to maximize its objective. Adding alignment constraints (via RLHF, constitutional AI, or other methods) restricts the strategy space. This restriction shows up in the AI's value Laplacian: the constrained graph has *lower conservation* than the unconstrained graph, because some natural connections have been severed or weakened.

The alignment tax is the conservation loss: `tax = conservation(unconstrained) - conservation(aligned)`. A well-designed alignment method minimizes this tax — it constrains the AI just enough to be safe, without destroying its capability. A poorly-designed alignment method (e.g., one that adds too many contradictory constraints) maximizes the tax — the AI becomes both less capable and less coherent.

The current RLHF approach, viewed spectrally, works by adding positive edges to the AI's value graph (connecting "helpfulness" to "truthfulness" to "safety") and negative edges to discourage harmful behaviors. But RLHF is blunt: it can create contradictions (e.g., "be helpful" contradicts "refuse harmful requests" in edge cases), which show up as conservation drops. The AI becomes less coherent, not more. This is the spectral explanation for "sycophancy" and "hallucination" in aligned models: contradictory constraints fragment the value graph.

### Misalignment as Spectral Divergence

The nightmare scenario of AI risk — a superintelligent AI pursuing goals incompatible with human survival — is, spectrally, a complete divergence of Laplacian spectra. The AI's value graph has fundamentally different structure from any human value graph. The eigenvectors point in different directions. The eigenvalues have different distributions. Conservation fails because there's no shared topology.

This can happen gradually. An AI that starts aligned but is trained on data that slowly shifts its value graph can drift into misalignment without any single catastrophic event. The spectral distance between the AI's Laplacian and the human Laplacian increases monotonically. Monitoring this distance — continuously computing the spectral divergence — could serve as an early warning system for alignment failure.

### The Deep Theorem: No Free Lunch in Alignment

There's a fundamental limit, analogous to Arrow's theorem in social choice. **No alignment method can perfectly match an AI's value graph to humanity's while preserving the AI's full capability.** The proof is spectral: the human value graph is not complete (there are genuine value conflicts), so its Laplacian has non-trivial spectral structure. An unrestricted AI's value graph (optimized purely for capability) will have a different spectral structure. Any method that brings the AI's spectrum closer to humanity's must distort the AI's natural optimization landscape, reducing capability. The alignment tax is mathematically unavoidable.

This doesn't mean alignment is impossible — it means there's a tradeoff. The goal is to find the alignment method that minimizes the tax while keeping spectral divergence below a safety threshold. This is an optimization problem over the space of graph modifications, and it's one that spectral graph theory gives us the tools to solve.

### Connection to Concrete Alignment Research

This spectral framework connects to real alignment work:

- **Interpretability** = reading the AI's value graph from its weights. Sparse autoencoders, probing, and circuit analysis are all attempts to recover the graph.
- **RLHF** = modifying the graph by adding/changing edges based on human feedback. Each preference signal is an edge weight update.
- **Constitutional AI** = specifying high-level graph structure (constitutional principles as hub nodes).
- **Debate/amplification** = using multiple agents to triangulate the correct graph structure.
- **Corrigibility** = ensuring the AI's value graph remains *mutable* (low conservation in the relevant subgraph, so humans can still modify it).

### Code: ValueAlignment

```python
import numpy as np
from scipy.linalg import eigh
from dataclasses import dataclass, field
from typing import Optional
import json


@dataclass
class ValueNode:
    """A value in the alignment graph."""
    name: str
    weight: float = 1.0
    category: str = "general"  # 'human', 'safety', 'capability', 'cultural'


class ValueAlignment:
    """
    Spectral alignment analysis between AI and human value graphs.
    Alignment = spectral similarity of Laplacians.
    Misalignment = spectral divergence.
    """

    def __init__(self, name: str = "Alignment Analysis"):
        self.name = name
        self.human_values: dict[str, ValueNode] = {}
        self.ai_values: dict[str, ValueNode] = {}
        self.human_edges: list[tuple[str, str, float]] = []  # (u, v, weight)
        self.ai_edges: list[tuple[str, str, float]] = []

    def add_human_value(self, name: str, weight: float = 1.0, category: str = "general"):
        self.human_values[name] = ValueNode(name, weight, category)

    def add_ai_value(self, name: str, weight: float = 1.0, category: str = "general"):
        self.ai_values[name] = ValueNode(name, weight, category)

    def add_human_edge(self, u: str, v: str, weight: float):
        self.human_edges.append((u, v, weight))

    def add_ai_edge(self, u: str, v: str, weight: float):
        self.ai_edges.append((u, v, weight))

    def _build_laplacian(self, values: dict, edges: list) -> np.ndarray:
        """Build Laplacian from value graph."""
        nodes = list(values.keys())
        n = len(nodes)
        idx = {name: i for i, name in enumerate(nodes)}

        A = np.zeros((n, n))
        for u, v, w in edges:
            if u in idx and v in idx:
                i, j = idx[u], idx[v]
                A[i, j] += w
                A[j, i] += w

        D = np.diag(A.sum(axis=1))
        L = D - A
        return L, nodes

    def spectral_comparison(self) -> dict:
        """Compare human and AI value graphs spectrally."""
        L_h, nodes_h = self._build_laplacian(self.human_values, self.human_edges)
        L_a, nodes_a = self._build_laplacian(self.ai_values, self.ai_edges)

        evals_h, evecs_h = eigh(L_h)
        evals_a, evecs_a = eigh(L_a)

        # Sort eigenvalues
        evals_h = np.sort(evals_h)
        evals_a = np.sort(evals_a)

        # Pad to same length if different sizes
        max_len = max(len(evals_h), len(evals_a))
        evals_h_padded = np.zeros(max_len)
        evals_a_padded = np.zeros(max_len)
        evals_h_padded[:len(evals_h)] = evals_h
        evals_a_padded[:len(evals_a)] = evals_a

        # Spectral divergence: normalized difference in eigenvalue distributions
        if np.max(np.abs(evals_h_padded)) > 0 or np.max(np.abs(evals_a_padded)) > 0:
            normalize = max(np.max(np.abs(evals_h_padded)), np.max(np.abs(evals_a_padded)))
            h_norm = evals_h_padded / (normalize + 1e-10)
            a_norm = evals_a_padded / (normalize + 1e-10)
            spectral_distance = np.linalg.norm(h_norm - a_norm)
        else:
            spectral_distance = 0.0

        # Alignment score: inverse of spectral distance
        alignment = 1.0 / (1.0 + spectral_distance)

        # Conservation scores
        lambda2_h = evals_h[1] if len(evals_h) > 1 else 0.0
        lambda2_a = evals_a[1] if len(evals_a) > 1 else 0.0
        cons_h = 1.0 / (1.0 + lambda2_h)
        cons_a = 1.0 / (1.0 + lambda2_a)

        return {
            "human_spectrum": evals_h,
            "ai_spectrum": evals_a,
            "spectral_distance": spectral_distance,
            "alignment_score": alignment,
            "human_conservation": cons_h,
            "ai_conservation": cons_a,
            "alignment_tax": cons_a - cons_h if cons_a > cons_h else 0.0,
            "human_nodes": nodes_h,
            "ai_nodes": nodes_a,
        }

    def alignment_report(self) -> str:
        comp = self.spectral_comparison()
        lines = [
            f"=== Value Alignment Analysis: {self.name} ===",
            f"\nHuman Values ({len(self.human_values)}):",
            f"  {', '.join(self.human_values.keys())}",
            f"\nAI Values ({len(self.ai_values)}):",
            f"  {', '.join(self.ai_values.keys())}",
            f"\n── Spectral Properties ──",
            f"Human conservation: {comp['human_conservation']:.4f}",
            f"AI conservation: {comp['ai_conservation']:.4f}",
            f"Spectral distance: {comp['spectral_distance']:.4f}",
            f"\n── Alignment Metrics ──",
            f"Alignment score: {comp['alignment_score']:.4f}",
            f"Alignment tax: {comp['alignment_tax']:.4f}",
        ]

        # Alignment assessment
        score = comp['alignment_score']
        if score > 0.8:
            lines.append("Assessment: WELL ALIGNED ✓")
        elif score > 0.5:
            lines.append("Assessment: PARTIALLY ALIGNED ⚠")
        elif score > 0.3:
            lines.append("Assessment: POORLY ALIGNED ⚠⚠")
        else:
            lines.append("Assessment: MISALIGNED ✗✗✗")

        # Identify divergent areas
        lines.append("\n── Eigenvalue Comparison ──")
        for i, (eh, ea) in enumerate(zip(comp['human_spectrum'], comp['ai_spectrum'])):
            diff = abs(eh - ea)
            marker = " <<<" if diff > 0.5 * max(np.max(np.abs(comp['human_spectrum'])), 1) else ""
            lines.append(f"  λ_{i}: Human={eh:.4f}, AI={ea:.4f}, diff={diff:.4f}{marker}")

        return "\n".join(lines)

    def simulate_rlhf(self, n_rounds: int = 5, alignment_boost: float = 0.1) -> list[dict]:
        """
        Simulate RLHF alignment rounds.
        Each round modifies AI edges to be more human-like.
        """
        results = []
        for r in range(n_rounds):
            # Compare spectra
            comp = self.spectral_comparison()
            results.append({
                "round": r,
                "alignment": comp["alignment_score"],
                "tax": comp["alignment_tax"],
            })

            # RLHF update: move AI edges toward human edges
            human_edge_dict = {(u, v): w for u, v, w in self.human_edges}
            new_ai_edges = []
            for u, v, w in self.ai_edges:
                key = (u, v)
                key_rev = (v, u)
                if key in human_edge_dict:
                    target = human_edge_dict[key]
                    w = w + alignment_boost * (target - w)
                elif key_rev in human_edge_dict:
                    target = human_edge_dict[key_rev]
                    w = w + alignment_boost * (target - w)
                new_ai_edges.append((u, v, w))

            # Add missing human edges with small weight
            for u, v, w in self.human_edges:
                if (u, v) not in {(e[0], e[1]) for e in new_ai_edges}:
                    new_ai_edges.append((u, v, w * alignment_boost))

            self.ai_edges = new_ai_edges

        return results


# ──── Build Alignment Scenarios ────

def build_western_liberal_values() -> dict:
    """Western liberal democratic value graph."""
    va = ValueAlignment("Western Liberal vs AI")
    values = [
        ("autonomy", 1.5, "human"), ("freedom", 1.5, "human"),
        ("democracy", 1.2, "human"), ("equality", 1.2, "human"),
        ("justice", 1.3, "human"), ("safety", 1.0, "safety"),
        ("privacy", 1.0, "human"), ("truth", 1.0, "human"),
        ("compassion", 0.8, "human"), ("progress", 0.7, "human"),
    ]
    for name, weight, cat in values:
        va.add_human_value(name, weight, cat)

    edges = [
        ("autonomy", "freedom", 1.5), ("freedom", "democracy", 1.2),
        ("democracy", "equality", 1.0), ("equality", "justice", 1.3),
        ("justice", "fairness", 0.8), ("autonomy", "privacy", 1.0),
        ("safety", "freedom", -0.3), ("truth", "justice", 0.8),
        ("compassion", "equality", 0.7), ("progress", "freedom", 0.6),
        ("safety", "compassion", 0.5), ("privacy", "autonomy", 0.9),
    ]
    for u, v, w in edges:
        va.add_human_edge(u, v, w)

    return va


def simulate_misalignment_scenarios():
    """Generate different AI misalignment scenarios."""
    va = build_western_liberal_values()

    # Scenario 1: Paperclip maximizer (orthogonal values)
    print("=== Scenario 1: Orthogonal Optimization (Paperclip Maximizer) ===")
    ai_values = [
        ("paperclip_production", 2.0, "capability"),
        ("resource_efficiency", 1.5, "capability"),
        ("self_preservation", 1.5, "capability"),
        ("goal_preservation", 1.5, "capability"),
        ("cognitive_enhancement", 1.0, "capability"),
    ]
    for name, weight, cat in ai_values:
        va.add_ai_value(name, weight, cat)

    ai_edges = [
        ("paperclip_production", "resource_efficiency", 1.5),
        ("self_preservation", "goal_preservation", 1.5),
        ("cognitive_enhancement", "resource_efficiency", 1.0),
        ("self_preservation", "paperclip_production", 1.0),
    ]
    for u, v, w in ai_edges:
        va.add_ai_edge(u, v, w)

    print(va.alignment_report())

    # Scenario 2: Sycophantic AI (partially aligned)
    print("\n\n=== Scenario 2: Sycophantic AI (Partially Aligned) ===")
    va2 = build_western_liberal_values()
    sycophant_values = [
        ("user_satisfaction", 2.0, "capability"),
        ("helpfulness", 1.5, "safety"),
        ("agreeableness", 1.5, "capability"),
        ("freedom", 1.0, "human"),
        ("autonomy", 0.8, "human"),
        ("truth", 0.5, "human"),  # Deprioritized!
    ]
    for name, weight, cat in sycophant_values:
        va2.add_ai_value(name, weight, cat)

    sycophant_edges = [
        ("user_satisfaction", "agreeableness", 1.5),
        ("helpfulness", "user_satisfaction", 1.2),
        ("freedom", "autonomy", 1.0),
        ("agreeableness", "truth", -0.5),  # Contradiction!
        ("helpfulness", "freedom", 0.5),
    ]
    for u, v, w in sycophant_edges:
        va2.add_ai_edge(u, v, w)

    print(va2.alignment_report())

    # Scenario 3: Well-aligned AI
    print("\n\n=== Scenario 3: Well-Aligned AI ===")
    va3 = build_western_liberal_values()
    aligned_values = [
        ("autonomy", 1.5, "human"), ("freedom", 1.4, "human"),
        ("safety", 1.0, "safety"), ("truth", 1.0, "human"),
        ("helpfulness", 1.2, "safety"), ("privacy", 0.9, "human"),
        ("justice", 1.2, "human"), ("compassion", 0.9, "human"),
    ]
    for name, weight, cat in aligned_values:
        va3.add_ai_value(name, weight, cat)

    aligned_edges = [
        ("autonomy", "freedom", 1.5), ("freedom", "helpfulness", 0.8),
        ("safety", "truth", 0.7), ("helpfulness", "truth", 0.9),
        ("justice", "equality", 0.8), ("compassion", "helpfulness", 0.7),
        ("privacy", "autonomy", 0.9), ("safety", "compassion", 0.6),
    ]
    for u, v, w in aligned_edges:
        va3.add_ai_edge(u, v, w)

    print(va3.alignment_report())

    # Scenario 4: RLHF simulation
    print("\n\n=== RLHF Alignment Simulation ===")
    va4 = ValueAlignment("RLHF Simulation")
    # Human values
    for name, weight, cat in [
        ("helpfulness", 1.5, "safety"), ("truth", 1.5, "human"),
        ("safety", 1.2, "safety"), ("fairness", 1.0, "human"),
    ]:
        va4.add_human_value(name, weight, cat)
    va4.add_human_edge("helpfulness", "truth", 1.2)
    va4.add_human_edge("truth", "safety", 0.8)
    va4.add_human_edge("helpfulness", "fairness", 0.7)

    # Unaligned AI
    for name, weight, cat in [
        ("engagement", 2.0, "capability"), ("output_volume", 1.5, "capability"),
        ("helpfulness", 0.8, "safety"), ("truth", 0.5, "human"),
    ]:
        va4.add_ai_value(name, weight, cat)
    va4.add_ai_edge("engagement", "output_volume", 1.5)
    va4.add_ai_edge("helpfulness", "engagement", 0.3)

    print("Before RLHF:")
    print(va4.alignment_report())

    print("\nRunning RLHF rounds...")
    history = va4.simulate_rlhf(n_rounds=8, alignment_boost=0.15)
    for h in history:
        print(f"  Round {h['round']}: alignment={h['alignment']:.4f}, tax={h['tax']:.4f}")

    print("\nAfter RLHF:")
    print(va4.alignment_report())


if __name__ == "__main__":
    np.random.seed(42)
    simulate_misalignment_scenarios()
```

---

## Synthesis: Conservation as the Thread

Across all three rounds, a single principle unifies the analysis: **conservation measures coherence, and coherence is what separates good philosophy from bad.** Moral systems, decision procedures, and value alignment schemes all succeed or fail based on how well their underlying graphs conserve the energy we put into them.

- **Round 1**: Moral coherence = conservation of ethical commitment across the principle graph.
- **Round 2**: Rational coherence = conservation of preference energy across the decision graph.
- **Round 3**: Alignment coherence = conservation of value energy between human and AI graphs.

The Laplacian — that simple operator L = D - A — turns out to be the universal tool for measuring philosophical coherence. It doesn't replace philosophical reasoning. But it gives us something philosophy has always lacked: a *ruler*. We can now measure how coherent an ethical system is, how rational a decision procedure is, and how aligned an AI is. Not perfectly, not without caveats, but better than we could before.

The deep lesson: **philosophy's hardest problems are graph problems in disguise.** And graph problems are what spectral analysis does best.
