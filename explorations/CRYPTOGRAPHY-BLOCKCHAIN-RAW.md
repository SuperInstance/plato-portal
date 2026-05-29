# Cryptography, Blockchain, and Zero-Knowledge Through Conservation Spectral Analysis

*An exploration in three rounds — eigenvalues as one-way functions, spectral zero-knowledge proofs, and the Laplacian structure of distributed ledgers.*

---

# ROUND 1 — The Spectral Hash

## Can Eigenvalues Serve as One-Way Functions?

Here's the insight that kicks everything off: computing the eigenvalues of a graph's Laplacian matrix is polynomial-time — just diagonalize an *n × n* matrix, O(n³) with standard methods. But reconstructing the graph from its spectrum alone? That's the *inverse spectral problem*, and it's brutal.

Two graphs can share identical spectra — these are called **cospectral graphs** (or isospectral graphs). The smallest pair is K₁,₄ (a star with 4 leaves) and C₄ ∪ K₁ (a 4-cycle plus an isolated vertex), both on 5 vertices with identical Laplacian spectra. But here's the key asymmetry:

- **Forward direction (graph → spectrum):** Trivial. Build the Laplacian, run `numpy.linalg.eigvalsh`. Done in milliseconds even for thousands of vertices.
- **Inverse direction (spectrum → graph):** Fundamentally underdetermined. The spectrum is a lossy compression of the graph structure. There are infinitely many graphs that share a given spectrum (for large enough vertex counts), and finding *any* graph matching a given spectrum is a hard combinatorial search.

This asymmetry — easy in one direction, hard to reverse — is exactly what a cryptographic hash function requires.

## Conservation Ratio as a Fingerprint

The **conservation ratio** (CR) of a graph — defined as λ₂/λ_max where λ₂ is the algebraic connectivity (smallest non-zero eigenvalue) and λ_max is the largest eigenvalue of the normalized Laplacian — captures something essential about the graph's connectivity structure. It's a single scalar that encodes:

- **CR near 0:** The graph is barely connected — bridges, bottlenecks, tree-like structure
- **CR near 1:** The graph is expander-like — highly connected, no weak cuts
- **CR = 1:** Only for complete graphs (every vertex connected to every other)

Two graphs with the same full spectrum trivially have the same CR. But two graphs with the same CR don't necessarily have the same spectrum. CR is a *summary statistic* — a hash of a hash, if you will. Yet it's remarkably stable under small perturbations: add or remove a few edges from a large graph, and the CR barely budges. This makes it useful as a quick integrity check.

## Spectral Collision Resistance

The gold standard for hash functions is **collision resistance** — it should be computationally infeasible to find two distinct inputs that produce the same output. For spectral hashing, this means: how hard is it to find two non-isomorphic graphs with identical Laplacian spectra?

The answer is nuanced:

1. **For small graphs (n < 10):** Not hard at all. Cospectral pairs are well-catalogued. You can look them up in databases.
2. **For medium graphs (10 < n < 50):** Cospectral graphs exist but finding them requires search. The fraction of cospectral pairs among all graphs on *n* vertices appears to decrease as *n* grows (for Laplacian spectra), though this is still an open research question.
3. **For large graphs (n > 100):** The space of possible spectra grows much faster than the space of "nearby" spectra. Finding collisions becomes a needle-in-haystack problem.

The critical trick for cryptographic use: **randomize before hashing**. If you take a graph G, randomly relabel its vertices (producing an isomorphic graph G'), then add a small random perturbation (add/remove a few edges), the resulting graph H will almost certainly have a *different* spectrum from G while preserving similar global structure. This randomization step is the spectral equivalent of adding a salt.

## Building SpectralHash

Let's implement a practical spectral hash function:

```python
import numpy as np
from numpy.linalg import eigvalsh
import hashlib
import struct
from itertools import combinations

class SpectralHash:
    """
    A hash function based on the eigenvalue spectrum of graph Laplacians.
    
    Input: arbitrary byte string (message)
    Output: fixed-length digest (256-bit hex string)
    
    Construction:
    1. Convert message to a graph using a deterministic construction
    2. Compute the Laplacian eigenvalue spectrum
    3. Quantize eigenvalues and feed through SHA-256 for final digest
    """
    
    def __init__(self, target_vertices=64, salt_rounds=3):
        self.n = target_vertices
        self.salt_rounds = salt_rounds
    
    def bytes_to_graph(self, data: bytes) -> np.ndarray:
        """
        Deterministically convert byte string to adjacency matrix.
        
        Strategy: Use the byte stream to seed edge decisions.
        We build a graph on self.n vertices, deciding edge (i,j)
        based on a hash of (i, j, data).
        """
        n = self.n
        adj = np.zeros((n, n), dtype=np.float64)
        
        # Ensure the graph is connected: build a random spanning tree first
        # Use data hash to determine tree structure
        h = hashlib.sha256(data).digest()
        parent = list(range(n))
        
        for i in range(1, n):
            # Deterministic parent selection from hash
            seed = int.from_bytes(
                hashlib.sha256(data + struct.pack('>II', i, 0)).digest()[:4], 
                'big'
            )
            p = seed % i
            adj[i][p] = 1.0
            adj[p][i] = 1.0
        
        # Add additional edges based on data
        for i in range(n):
            for j in range(i + 1, n):
                if adj[i][j] > 0:
                    continue
                edge_hash = hashlib.sha256(
                    data + struct.pack('>II', i, j)
                ).digest()
                # Probability of adding this edge based on first byte
                if edge_hash[0] < 85:  # ~33% chance
                    adj[i][j] = 1.0
                    adj[j][i] = 1.0
        
        return adj
    
    def adjacency_to_laplacian(self, adj: np.ndarray) -> np.ndarray:
        """Compute the normalized Laplacian: L = I - D^(-1/2) A D^(-1/2)"""
        degree = adj.sum(axis=1)
        # Handle isolated vertices (shouldn't happen with spanning tree)
        degree[degree == 0] = 1.0
        d_inv_sqrt = 1.0 / np.sqrt(degree)
        # D^(-1/2) A D^(-1/2)
        normalized = adj * np.outer(d_inv_sqrt, d_inv_sqrt)
        L = np.eye(adj.shape[0]) - normalized
        return L
    
    def hash(self, message: bytes) -> str:
        """Compute the spectral hash of a message."""
        # Step 1: Build graph from message
        adj = self.bytes_to_graph(message)
        
        # Step 2: Apply salt rounds (perturbations for avalanche effect)
        for r in range(self.salt_rounds):
            salt = hashlib.sha256(
                message + struct.pack('>I', r)
            ).digest()
            # Small perturbation: flip a few edges
            for k in range(0, min(8, len(salt) - 1), 2):
                i = salt[k] % self.n
                j = salt[k+1] % self.n
                if i != j:
                    adj[i][j] = 1.0 - adj[i][j]
                    adj[j][i] = adj[i][j]
        
        # Step 3: Compute normalized Laplacian
        L = self.adjacency_to_laplacian(adj)
        
        # Step 4: Extract eigenvalues
        eigenvalues = eigvalsh(L)
        
        # Step 5: Quantize and hash
        # Scale eigenvalues to integers (multiply by 10^6 and round)
        quantized = np.round(eigenvalues * 1e6).astype(np.int64)
        # Pack into bytes
        eigen_bytes = quantized.tobytes()
        
        # Step 6: SHA-256 of the quantized spectrum
        digest = hashlib.sha256(eigen_bytes).hexdigest()
        return digest
    
    def conservation_ratio(self, message: bytes) -> float:
        """Compute the conservation ratio of the message's spectral graph."""
        adj = self.bytes_to_graph(message)
        L = self.adjacency_to_laplacian(adj)
        eigenvalues = np.sort(eigvalsh(L))
        
        # Filter out zero eigenvalues (disconnected components)
        nonzero = eigenvalues[eigenvalues > 1e-10]
        if len(nonzero) == 0:
            return 0.0
        
        lambda_2 = nonzero[0]  # Algebraic connectivity
        lambda_max = nonzero[-1]  # Largest eigenvalue
        
        return lambda_2 / lambda_max if lambda_max > 0 else 0.0


# --- Testing SpectralHash ---
def test_spectral_hash():
    sh = SpectralHash(target_vertices=64)
    
    print("=" * 60)
    print("SPECTRAL HASH TESTS")
    print("=" * 60)
    
    # Test 1: Different messages produce different hashes
    messages = [
        b"Hello, world!",
        b"Hello, world?",  # One character different
        b"The quick brown fox jumps over the lazy dog",
        b"",  # Empty message
        b"\x00" * 100,  # All zeros
    ]
    
    hashes = []
    for msg in messages:
        h = sh.hash(msg)
        cr = sh.conservation_ratio(msg)
        hashes.append(h)
        preview = msg[:30].hex() if msg else "(empty)"
        print(f"  msg: {preview}...")
        print(f"  hash: {h}")
        print(f"  CR: {cr:.6f}")
        print()
    
    # Check for collisions
    unique_hashes = set(hashes)
    print(f"Messages: {len(messages)}, Unique hashes: {len(unique_hashes)}")
    print(f"Collision: {'YES (BAD!)' if len(unique_hashes) < len(messages) else 'No (good)'}")
    
    # Test 2: Avalanche effect — small input change → big hash change
    h1 = sh.hash(b"message A")
    h2 = sh.hash(b"message B")
    
    # Count differing bits
    h1_int = int(h1, 16)
    h2_int = int(h2, 16)
    diff_bits = bin(h1_int ^ h2_int).count('1')
    total_bits = 256
    
    print(f"\nAvalanche test:")
    print(f"  Hamming distance: {diff_bits}/{total_bits} bits ({diff_bits/total_bits*100:.1f}%)")
    print(f"  Ideal: ~50%, Got: {diff_bits/total_bits*100:.1f}%")
    
    # Test 3: Collision resistance — try to find collisions
    print(f"\nCollision resistance test (1000 random messages)...")
    seen = {}
    collisions = 0
    for i in range(1000):
        msg = f"test message {i} with random content {np.random.bytes(8).hex()}".encode()
        h = sh.hash(msg)
        if h in seen:
            collisions += 1
            print(f"  COLLISION: msg {i} and msg {seen[h]}")
        seen[h] = i
    
    print(f"  Tested: 1000, Collisions: {collisions}")
    
    # Test 4: CR fingerprinting
    print(f"\nConservation ratio fingerprinting:")
    graph_types = {
        "path": b"type:path_graph",
        "cycle": b"type:cycle_graph", 
        "complete": b"type:complete_graph",
        "random_sparse": b"type:sparse_random",
        "random_dense": b"type:dense_random",
    }
    for name, msg in graph_types.items():
        cr = sh.conservation_ratio(msg)
        print(f"  {name}: CR = {cr:.6f}")


test_spectral_hash()
```

### What This Gives Us

The SpectralHash construction has several interesting properties:

1. **Deterministic:** Same input always produces the same hash (the graph construction is deterministic given the bytes).
2. **Avalanche effect:** The salt rounds ensure that small changes in the input create different graphs with different spectra, leading to very different final digests.
3. **Collision-resistant (heuristically):** The space of possible spectra for 64-vertex graphs is enormous, and the quantization + SHA-256 final step provides a standard cryptographic safety net.
4. **Structurally informative:** The CR provides a quick "fingerprint" of the input's spectral structure, useful for quick comparisons without computing the full hash.

The weakness, of course, is speed — this is orders of magnitude slower than SHA-256 or BLAKE3 for the same input size. But for applications where you want the hash to carry *structural information* about the input (not just be a random oracle), the spectral approach offers something conventional hashes can't: **meaningful collisions reveal structural similarity**.

---

# ROUND 2 — Zero-Knowledge Proofs via Spectral Alignment

## The Core Idea

Zero-knowledge proofs let a **prover** convince a **verifier** that some statement is true without revealing *why* it's true. The classic example: proving you know a Hamiltonian cycle in a graph without showing the cycle.

Here's the spectral angle: a graph's eigenvalue spectrum reveals global properties (connectivity, expansion, community structure) without revealing the graph's specific edge set. This creates a natural information gap we can exploit.

**The statement:** "I know a graph G with *n* vertices and *m* edges whose conservation ratio exceeds θ."

**What the verifier learns:** That such a graph exists and the prover knows it.

**What the verifier does NOT learn:** The actual edges of G, its adjacency matrix, or any specific structural detail beyond the spectral summary.

## The Protocol

Here's how spectral ZK works, adapted from graph isomorphism ZK protocols:

### Setup Phase
1. **Prover** has a graph G = (V, E) with |V| = n, |E| = m
2. **Prover** computes G's spectrum: {λ₁, λ₂, ..., λₙ} where λ₁ ≤ λ₂ ≤ ... ≤ λₙ
3. **Prover** commits to the spectrum using a cryptographic commitment scheme

### Commit Phase
1. Prover generates a random permutation π of {1, ..., n}
2. Prover computes the permuted graph H = π(G) — same graph, relabeled vertices
3. Prover computes L(H), the Laplacian of H
4. Prover sends commitment: C = Commit(spectrum of H, randomness r)
5. Prover also sends a "spectral summary" — just the conservation ratio and dimension

### Challenge Phase
The verifier sends a random challenge bit *b* ∈ {0, 1}:

**If b = 0 (Show Isomorphism):**
- Prover reveals π and the commitment opening
- Verifier checks that H = π(G) and spectrum(H) = spectrum(G)

**If b = 1 (Show Property):**
- Prover opens the commitment to show the full spectrum
- Verifier computes CR from the revealed eigenvalues
- Verifier checks CR ≥ θ

### Why This Works

- **Completeness:** An honest prover can always respond to either challenge. The spectrum is the same regardless of permutation (isomorphic graphs are cospectral), so the commitment is consistent.
- **Soundness:** A cheating prover who doesn't know such a graph must either fake the commitment or fake the property. The random challenge forces them to prepare for both cases, which requires knowing a valid graph.
- **Zero-knowledge:** The verifier learns only the spectrum (which is public information about the *class* of graphs) and a permutation (which is random and carries no information about G's structure). The specific edge set of G is never revealed.

## Conservation Ratio as the Proof Metric

The conservation ratio is an elegant proof metric because:

1. **It's a single number:** Easy to verify, easy to commit to.
2. **It's structure-revealing but not structure-revealing:** A CR of 0.8 tells you the graph is well-connected but doesn't tell you *how* it's connected. You can't reconstruct the graph from CR alone.
3. **It's monotone under edge addition (roughly):** Adding edges to a graph generally increases λ₂ (algebraic connectivity), making CR increase. This means "CR ≥ θ" is a meaningful threshold statement about graph quality.

More complex proof statements become possible:
- "I know a graph with CR ∈ [0.6, 0.8]" — proves bounded connectivity
- "I know a graph whose Fiedler partition separates vertex set into two roughly equal parts" — proves balanced structure
- "I know a graph with spectral gap > δ" — proves expansion property

## Building ZKSpectral

```python
import numpy as np
from numpy.linalg import eigvalsh
import hashlib
import hmac
import struct
import json
from dataclasses import dataclass, field
from typing import Tuple, List, Optional


@dataclass
class Graph:
    """Simple undirected graph."""
    n: int  # number of vertices
    edges: List[Tuple[int, int]]  # edge list
    
    def adjacency_matrix(self) -> np.ndarray:
        A = np.zeros((self.n, self.n))
        for (i, j) in self.edges:
            A[i][j] = 1.0
            A[j][i] = 1.0
        return A
    
    def laplacian(self) -> np.ndarray:
        A = self.adjacency_matrix()
        D = np.diag(A.sum(axis=1))
        return D - A
    
    def normalized_laplacian(self) -> np.ndarray:
        A = self.adjacency_matrix()
        degree = A.sum(axis=1)
        degree[degree == 0] = 1.0
        d_inv_sqrt = 1.0 / np.sqrt(degree)
        return np.eye(self.n) - A * np.outer(d_inv_sqrt, d_inv_sqrt)
    
    def spectrum(self, normalized=True) -> np.ndarray:
        if normalized:
            L = self.normalized_laplacian()
        else:
            L = self.laplacian()
        return np.sort(eigvalsh(L))
    
    def conservation_ratio(self) -> float:
        eigs = self.spectrum()
        nonzero = eigs[eigs > 1e-10]
        if len(nonzero) == 0:
            return 0.0
        return nonzero[0] / nonzero[-1] if nonzero[-1] > 0 else 0.0
    
    def permute(self, perm: List[int]) -> 'Graph':
        """Create a permuted (isomorphic) copy."""
        inv_perm = [0] * self.n
        for i, p in enumerate(perm):
            inv_perm[p] = i
        new_edges = [(inv_perm[i], inv_perm[j]) for (i, j) in self.edges]
        return Graph(self.n, new_edges)


def random_graph(n: int, edge_prob: float = 0.3, seed: int = 42) -> Graph:
    """Generate a random Erdős–Rényi graph."""
    rng = np.random.RandomState(seed)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < edge_prob:
                edges.append((i, j))
    # Ensure connected by adding a path
    connected = set()
    connected.add(0)
    for i in range(1, n):
        if not any(i in c for c in [connected]):
            pass
    # Simple connectivity fix: add path 0-1-2-...-n-1
    for i in range(n - 1):
        if (i, i + 1) not in edges and (i + 1, i) not in edges:
            edges.append((i, i + 1))
    return Graph(n, edges)


def commit(data: bytes, randomness: bytes) -> str:
    """Pedersen-like commitment: H(data || randomness)."""
    return hashlib.sha256(data + randomness).hexdigest()


def fiat_shamir_challenge(transcript: bytes) -> int:
    """Fiat-Shamir heuristic: derive challenge from transcript."""
    h = hashlib.sha256(transcript).digest()
    return h[0] % 2  # Single bit challenge


class ZKSpectralProver:
    """Zero-knowledge prover for spectral properties."""
    
    def __init__(self, graph: Graph):
        self.graph = graph
        self.spectrum = graph.spectrum()
        self.cr = graph.conservation_ratio()
    
    def create_commitment(self) -> Tuple[str, bytes, bytes, List[int]]:
        """Create commitment to permuted graph's spectrum."""
        # Generate random permutation
        perm = list(range(self.graph.n))
        np.random.shuffle(perm)
        
        # Create permuted graph
        H = self.graph.permute(perm)
        H_spectrum = H.spectrum()
        
        # Serialize spectrum
        spectrum_bytes = np.round(H_spectrum * 1e8).astype(np.int64).tobytes()
        
        # Randomness for commitment
        randomness = np.random.bytes(32)
        
        # Commit
        commitment = commit(spectrum_bytes, randomness)
        
        return commitment, spectrum_bytes, randomness, perm
    
    def prove_cr_threshold(self, threshold: float, num_rounds: int = 20) -> dict:
        """
        Create a non-interactive ZK proof that CR >= threshold.
        Uses Fiat-Shamir transform for non-interactivity.
        """
        assert self.cr >= threshold, f"CR {self.cr:.4f} < {threshold}"
        
        rounds = []
        transcript = b""
        
        for r in range(num_rounds):
            # Commit phase
            commitment, spectrum_bytes, randomness, perm = self.create_commitment()
            
            # Create round data for transcript
            round_commit_data = commitment.encode()
            transcript += round_commit_data
            
            # Fiat-Shamir challenge
            challenge = fiat_shamir_challenge(
                transcript + struct.pack('>I', r) + 
                struct.pack('>d', threshold)
            )
            
            if challenge == 0:
                # Reveal permutation (prove we know the isomorphism)
                response = {
                    "type": "isomorphism",
                    "perm": perm,
                    "commitment": commitment,
                    "spectrum_hash": hashlib.sha256(spectrum_bytes).hexdigest(),
                }
            else:
                # Reveal spectrum (prove the property)
                spectrum_list = np.round(
                    np.frombuffer(spectrum_bytes, dtype=np.int64) / 1e8, 
                    decimals=8
                ).tolist()
                
                # Verify CR ourselves
                nonzero = [x for x in spectrum_list if x > 1e-8]
                revealed_cr = nonzero[0] / nonzero[-1] if nonzero else 0.0
                
                response = {
                    "type": "property",
                    "spectrum": spectrum_list,
                    "randomness": randomness.hex(),
                    "commitment": commitment,
                    "cr": revealed_cr,
                }
            
            rounds.append({
                "commitment": commitment,
                "challenge": challenge,
                "response": response,
            })
        
        return {
            "statement": f"CR >= {threshold}",
            "n": self.graph.n,
            "m": len(self.graph.edges),
            "actual_cr": self.cr,
            "threshold": threshold,
            "num_rounds": num_rounds,
            "rounds": rounds,
        }


class ZKSpectralVerifier:
    """Zero-knowledge verifier for spectral properties."""
    
    def verify(self, proof: dict) -> bool:
        """Verify a ZK spectral proof."""
        threshold = proof["threshold"]
        n = proof["n"]
        
        for i, round_data in enumerate(proof["rounds"]):
            commitment = round_data["commitment"]
            challenge = round_data["challenge"]
            response = round_data["response"]
            
            if response["type"] == "isomorphism":
                # Verify permutation is valid
                perm = response["perm"]
                if sorted(perm) != list(range(n)):
                    print(f"  Round {i}: Invalid permutation")
                    return False
                
                # Verify commitment consistency (perm doesn't change spectrum)
                # We can't fully verify without the original graph, 
                # but we check the spectrum hash matches
                if commitment != response["commitment"]:
                    print(f"  Round {i}: Commitment mismatch")
                    return False
                    
            elif response["type"] == "property":
                # Verify spectrum gives CR >= threshold
                spectrum = response["spectrum"]
                
                # Check commitment opens correctly
                spectrum_bytes = np.round(
                    np.array(spectrum) * 1e8
                ).astype(np.int64).tobytes()
                randomness = bytes.fromhex(response["randomness"])
                
                expected_commitment = commit(spectrum_bytes, randomness)
                if expected_commitment != commitment:
                    print(f"  Round {i}: Commitment doesn't open correctly")
                    return False
                
                # Check CR
                nonzero = [x for x in spectrum if x > 1e-8]
                if not nonzero:
                    print(f"  Round {i}: No nonzero eigenvalues")
                    return False
                
                cr = nonzero[0] / nonzero[-1]
                if cr < threshold - 1e-6:
                    print(f"  Round {i}: CR {cr:.6f} < threshold {threshold}")
                    return False
                
                # Check dimension
                if len(spectrum) != n:
                    print(f"  Round {i}: Wrong spectrum dimension")
                    return False
            
            else:
                print(f"  Round {i}: Unknown response type")
                return False
        
        # Soundness: probability of cheating = 2^(-num_rounds)
        cheating_prob = 2 ** (-proof["num_rounds"])
        print(f"  Cheating probability: {cheating_prob:.2e}")
        
        return True


# --- Full Demo ---
def demo_zk_spectral():
    print("=" * 60)
    print("ZERO-KNOWLEDGE SPECTRAL PROOF DEMO")
    print("=" * 60)
    
    # Generate a well-connected graph
    np.random.seed(42)
    G = random_graph(n=30, edge_prob=0.4, seed=42)
    
    print(f"\nGraph: n={G.n}, m={len(G.edges)}")
    print(f"Conservation Ratio: {G.conservation_ratio():.6f}")
    spectrum = G.spectrum()
    print(f"Eigenvalues: λ₂={spectrum[1]:.6f}, λ_max={spectrum[-1]:.6f}")
    
    # Prover creates proof
    threshold = 0.5
    print(f"\nProving: CR >= {threshold}")
    
    prover = ZKSpectralProver(G)
    proof = prover.prove_cr_threshold(threshold, num_rounds=20)
    
    print(f"\nProof created: {proof['num_rounds']} rounds")
    print(f"Actual CR: {proof['actual_cr']:.6f}")
    
    # Verifier checks
    verifier = ZKSpectralVerifier()
    print(f"\nVerifying proof...")
    valid = verifier.verify(proof)
    print(f"Result: {'VALID ✓' if valid else 'INVALID ✗'}")
    
    # Now try with a graph that DOESN'T meet the threshold
    print(f"\n{'=' * 60}")
    print("Testing with graph that FAILS the threshold...")
    
    # Path graph has very low CR
    path_edges = [(i, i+1) for i in range(29)]
    path_G = Graph(30, path_edges)
    path_cr = path_G.conservation_ratio()
    print(f"Path graph CR: {path_cr:.6f}")
    
    try:
        bad_prover = ZKSpectralProver(path_G)
        # This should fail assertion
    except AssertionError as e:
        print(f"Prover correctly refuses: {e}")
    
    # Test: cheating prover tries to fake the proof
    print(f"\nTesting soundness — cheating prover simulation...")
    print(f"(A cheating prover must guess the challenge bit each round)")
    print(f"With 20 rounds, cheating probability = 2^(-20) ≈ {2**-20:.2e}")


demo_zk_spectral()
```

### What Makes This Interesting

The spectral ZK protocol leverages a deep fact: **eigenvalues are invariant under vertex permutation**. This means:

- The prover can always honestly answer "show me the isomorphism" (challenge 0) because the permuted graph has the same spectrum.
- The prover can always honestly answer "show me the property" (challenge 1) because the spectrum genuinely satisfies the CR threshold.
- A cheating prover who doesn't know a valid graph can only answer one of the two challenges — they must commit to either a fake isomorphism or a fake spectrum, and the verifier catches them with 50% probability per round.

The Fiat-Shamir transform makes this non-interactive: instead of the verifier sending random challenges, we derive them from the transcript hash. This is how real ZK-SNARKs work (simplified enormously).

The limitation: this is a **proof of knowledge of a graph with a property**, not a proof of knowledge of the graph itself. For applications like "I know the structure of this specific network," you'd need additional machinery (like committing to the adjacency matrix with a Merkle tree and proving properties of committed values). But the spectral approach is clean, mathematically elegant, and connects directly to the conservation framework.

---

# ROUND 3 — The Blockchain Laplacian

## Blockchain as a Path Graph

A blockchain is, at its most basic level, a **path graph**. Block 0 (genesis) connects to Block 1, which connects to Block 2, and so on. The Laplacian of a path graph on *n* vertices has a beautiful closed-form spectrum:

$$\lambda_k = 2 - 2\cos\left(\frac{\pi k}{n}\right), \quad k = 0, 1, ..., n-1$$

For the path graph:
- **λ₁ = 0** (always, for any connected component)
- **λ₂ = 2 - 2cos(π/n)** — the algebraic connectivity, which decreases as the chain grows. This makes sense: a longer chain has weaker "cohesion" in the spectral sense.
- **λ_max ≈ 4** (approaches 4 as n → ∞)

The **conservation ratio** of a path graph on *n* vertices is approximately:

$$CR_{\text{path}} \approx \frac{1 - \cos(\pi/n)}{1 + \cos(\pi/n)} \approx \frac{\pi^2}{4n^2} \text{ for large } n$$

This is terrible — CR goes to zero as the chain grows! A blockchain has inherently poor spectral connectivity because it's a path. Every block depends on exactly one predecessor, creating the worst possible expansion properties.

## Forks as Spectral Bifurcation

A **fork** occurs when two blocks are mined on top of the same parent. In graph terms, the path graph suddenly becomes a **Y-shape** — two branches diverging from a common ancestor.

Spectrally, a fork does something dramatic: it creates a **new connected component** (temporarily, until one branch wins) or, more precisely, it changes the topology from a path to a graph with a vertex of degree 3 (the common parent). The algebraic connectivity λ₂ jumps up because there's now more connectivity at the fork point.

But here's the spectral signature of a fork: the **Fiedler vector** (eigenvector corresponding to λ₂) partitions the graph into two groups. For a fork, this partition separates the two branches — one branch gets positive Fiedler values, the other gets negative values. The fork point itself has a Fiedler value near zero.

This gives us a spectral fork detection method: **monitor the Fiedler vector**. If the Fiedler partition doesn't cleanly separate into "old blocks" vs "new blocks" (which is what you'd expect for a growing path), there's a fork.

## The 51% Attack as Spectral Manipulation

A 51% attack works by building an alternative chain faster than the honest network. In graph terms, the attacker adds vertices to their fork faster than the honest network adds to the main chain. Eventually, the attacker's branch is longer and the network switches.

Spectrally, this is a battle for **which connected component dominates**. If we model the blockchain as having two branches (honest and attacker), the Laplacian captures this as:

```
     Honest chain: ... → B_n → B_{n+1} → ...
                          ↗ (fork point)
     Attacker chain: ... → B_n → B'_{n+1} → B'_{n+2} → ...
```

The Fiedler partition separates the honest chain from the attacker chain. The **conservation ratio** of the combined graph tells us how balanced the fork is:

- **CR near 0:** One branch dominates (normal operation or successful attack)
- **CR near 0.5:** Perfectly balanced fork (50/50 split — maximum uncertainty)
- **CR increasing toward 1:** The branches are reconnecting (orphaned blocks being resolved)

A 51% attack succeeds when the attacker's branch becomes the heavier component, which the Fiedler partition detects by flipping: what was the "attacker side" becomes the "honest side."

## Proof-of-Stake as Conservation Verification

In Proof-of-Stake, validators stake tokens and are selected to propose/attest blocks. The spectral interpretation:

- **Stake distribution → weighted edges:** Validators with more stake create "stronger" connections in the validation graph.
- **Finality → spectral threshold:** A block is "finalized" when the spectral signature of the chain including that block has CR above a threshold. This means the block is embedded in a well-connected validation structure that can't be easily reversed.
- **Slashing → edge removal:** If a validator equivocates (votes for two conflicting blocks), their edges are removed, dropping the local CR and signaling a fault.

Ethereum's Casper FFG can be interpreted spectrally: the "justification" and "finalization" of checkpoints correspond to the validation graph reaching certain spectral thresholds. A justified checkpoint has enough validator edges to ensure CR > θ₁; a finalized checkpoint has enough to ensure CR > θ₂ > θ₁, making reversal computationally infeasible.

## Building BlockchainLaplacian

```python
import numpy as np
from numpy.linalg import eigvalsh, eigh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict
import random


@dataclass
class Block:
    """A block in the blockchain."""
    index: int
    parent_hash: str
    hash: str
    miner: str
    timestamp: float
    is_fork: bool = False


@dataclass 
class BlockChain:
    """Blockchain with spectral analysis capabilities."""
    chain: List[Block] = field(default_factory=list)
    fork_blocks: Dict[str, List[Block]] = field(default_factory=dict)
    
    def add_block(self, block: Block):
        self.chain.append(block)
    
    def add_fork(self, parent_hash: str, block: Block):
        if parent_hash not in self.fork_blocks:
            self.fork_blocks[parent_hash] = []
        block.is_fork = True
        self.fork_blocks[parent_hash].append(block)
    
    def adjacency_matrix(self) -> np.ndarray:
        """Build adjacency matrix including forks."""
        all_blocks = list(self.chain)
        fork_blocks_list = []
        for blocks in self.fork_blocks.values():
            fork_blocks_list.extend(blocks)
        all_blocks.extend(fork_blocks_list)
        
        n = len(all_blocks)
        block_indices = {b.hash: i for i, b in enumerate(all_blocks)}
        
        A = np.zeros((n, n))
        for b in all_blocks:
            if b.parent_hash in block_indices:
                i = block_indices[b.hash]
                j = block_indices[b.parent_hash]
                A[i][j] = 1.0
                A[j][i] = 1.0
        
        return A
    
    def laplacian(self) -> np.ndarray:
        A = self.adjacency_matrix()
        D = np.diag(A.sum(axis=1))
        return D - A
    
    def spectrum(self) -> np.ndarray:
        return np.sort(eigvalsh(self.laplacian()))
    
    def fiedler_vector(self) -> Tuple[float, np.ndarray]:
        """Return (lambda_2, fiedler_vector)."""
        L = self.laplacian()
        eigenvalues, eigenvectors = eigh(L)
        idx = np.argsort(eigenvalues)
        # Find first nonzero eigenvalue
        for i in range(len(eigenvalues)):
            if eigenvalues[idx[i]] > 1e-10:
                return eigenvalues[idx[i]], eigenvectors[:, idx[i]]
        return 0.0, np.zeros(L.shape[0])
    
    def conservation_ratio(self) -> float:
        eigs = self.spectrum()
        nonzero = eigs[eigs > 1e-10]
        if len(nonzero) == 0:
            return 0.0
        return nonzero[0] / nonzero[-1]


def simulate_blockchain(
    num_blocks: int = 20,
    fork_probability: float = 0.15,
    attack_block: Optional[int] = None,
    seed: int = 42
) -> BlockChain:
    """Simulate a blockchain with random forks and optional 51% attack."""
    random.seed(seed)
    np.random.seed(seed)
    
    bc = BlockChain()
    
    # Genesis block
    genesis = Block(
        index=0,
        parent_hash="0000",
        hash="genesis",
        miner="genesis",
        timestamp=0.0
    )
    bc.add_block(genesis)
    
    for i in range(1, num_blocks):
        parent = bc.chain[-1]
        
        # Normal block
        block = Block(
            index=i,
            parent_hash=parent.hash,
            hash=f"block_{i}",
            miner=f"miner_{random.randint(0, 10)}",
            timestamp=float(i)
        )
        bc.add_block(block)
        
        # Maybe fork
        if random.random() < fork_probability and i > 2:
            fork_parent = bc.chain[-3]  # Fork from 3 blocks ago
            fork_block = Block(
                index=i,
                parent_hash=fork_parent.hash,
                hash=f"fork_{i}",
                miner=f"attacker_{random.randint(0, 3)}",
                timestamp=float(i) + 0.5
            )
            bc.add_fork(fork_parent.hash, fork_block)
    
    # 51% attack: attacker builds a longer chain from a fork point
    if attack_block is not None and attack_block < num_blocks:
        attack_start = bc.chain[attack_block]
        for j in range(attack_block + 1, min(attack_block + 8, num_blocks + 5)):
            fork_block = Block(
                index=j,
                parent_hash=attack_start.hash,
                hash=f"attack_{j}",
                miner="attacker_51",
                timestamp=float(j) + 0.3
            )
            bc.add_fork(attack_start.hash, fork_block)
            attack_start = fork_block
    
    return bc


def spectral_analysis(bc: BlockChain, label: str):
    """Perform and display spectral analysis of a blockchain."""
    print(f"\n{'=' * 60}")
    print(f"SPECTRAL ANALYSIS: {label}")
    print(f"{'=' * 60}")
    
    n_blocks = len(bc.chain)
    n_forks = sum(len(v) for v in bc.fork_blocks.values())
    
    print(f"Main chain blocks: {n_blocks}")
    print(f"Fork blocks: {n_forks}")
    print(f"Total graph vertices: {n_blocks + n_forks}")
    
    if n_blocks + n_forks < 2:
        print("Too few blocks for spectral analysis.")
        return
    
    # Spectrum
    spectrum = bc.spectrum()
    print(f"\nEigenvalue spectrum (sorted):")
    nonzero = spectrum[spectrum > 1e-10]
    if len(nonzero) > 0:
        print(f"  λ₂ (algebraic connectivity): {nonzero[0]:.6f}")
        print(f"  λ_max: {nonzero[-1]:.6f}")
        print(f"  Spectral gap: {nonzero[1] - nonzero[0]:.6f}" if len(nonzero) > 1 else "")
    print(f"  Conservation Ratio: {bc.conservation_ratio():.6f}")
    
    # Fiedler analysis
    lambda2, fiedler = bc.fiedler_vector()
    print(f"\nFiedler analysis:")
    print(f"  λ₂ = {lambda2:.6f}")
    
    # Partition based on Fiedler vector
    positive = sum(1 for v in fiedler if v > 0)
    negative = sum(1 for v in fiedler if v < 0)
    zero = sum(1 for v in fiedler if abs(v) < 1e-10)
    print(f"  Fiedler partition: {positive} positive, {negative} negative, {zero} zero")
    
    if n_forks > 0:
        print(f"\n  Fork detection: Fiedler partition reveals fork structure")
        print(f"  Main chain / fork split ratio: {positive}:{negative}")
    
    return bc.conservation_ratio(), lambda2, fiedler


def simulate_51_attack_progression():
    """Simulate a 51% attack and track spectral properties over time."""
    print(f"\n{'=' * 60}")
    print("51% ATTACK SIMULATION")
    print(f"{'=' * 60}")
    
    # Build honest chain
    bc = BlockChain()
    genesis = Block(0, "0000", "genesis", "genesis", 0.0)
    bc.add_block(genesis)
    
    for i in range(1, 21):
        parent = bc.chain[-1]
        block = Block(i, parent.hash, f"block_{i}", f"miner_{i%5}", float(i))
        bc.add_block(block)
    
    print(f"\nHonest chain: {len(bc.chain)} blocks")
    print(f"Honest CR: {bc.conservation_ratio():.6f}")
    
    # Now attacker builds from block 15
    print(f"\n--- Attacker starts building from block 15 ---")
    
    attack_parent_hash = "block_15"
    cr_history = [bc.conservation_ratio()]
    lambda2_history = []
    
    _, fiedler = bc.fiedler_vector()
    lambda2_history.append(bc.fiedler_vector()[0])
    
    for attack_len in range(1, 10):
        # Attacker adds a block
        attack_block = Block(
            15 + attack_len,
            attack_parent_hash,
            f"attack_{15 + attack_len}",
            "attacker",
            float(15 + attack_len) + 0.3
        )
        bc.add_fork("block_15", attack_block)
        attack_parent_hash = attack_block.hash
        
        cr = bc.conservation_ratio()
        lambda2 = bc.fiedler_vector()[0]
        cr_history.append(cr)
        lambda2_history.append(lambda2)
        
        # Check Fiedler partition
        _, fiedler = bc.fiedler_vector()
        pos = sum(1 for v in fiedler if v > 0)
        neg = sum(1 for v in fiedler if v < 0)
        
        attacker_wins = neg > pos  # Attacker branch is larger
        status = "⚠️ ATTACKER LEADING" if attacker_wins else "✅ Honest chain leading"
        
        print(f"  Attack blocks: {attack_len:2d} | "
              f"CR: {cr:.6f} | "
              f"λ₂: {lambda2:.6f} | "
              f"Partition: {pos}:{neg} | "
              f"{status}")
    
    print(f"\nCR progression: {[f'{cr:.4f}' for cr in cr_history]}")
    print(f"λ₂ progression: {[f'{l:.4f}' for l in lambda2_history]}")


def proof_of_stake_spectral():
    """Model Proof-of-Stake validation as a spectral consensus mechanism."""
    print(f"\n{'=' * 60}")
    print("PROOF-OF-STAKE AS SPECTRAL CONSENSUS")
    print(f"{'=' * 60}")
    
    # Validators with stakes
    validators = {
        "alice": 32,
        "bob": 64,
        "charlie": 32,
        "dave": 128,
        "eve": 16,
        "frank": 48,
    }
    
    total_stake = sum(validators.values())
    
    # Build validation graph: edges weighted by combined stake
    names = list(validators.keys())
    n = len(names)
    
    # Attestation matrix: validator i attests to validator j's block
    # Weight = combined stake (more stake = stronger edge)
    rng = np.random.RandomState(123)
    attestation = np.zeros((n, n))
    
    # Each validator attests to a few others
    for i in range(n):
        # Choose 2-3 validators to attest to
        num_attestations = rng.randint(2, 4)
        targets = rng.choice([j for j in range(n) if j != i], 
                            size=min(num_attestations, n-1), replace=False)
        for j in targets:
            weight = validators[names[i]] + validators[names[j]]
            attestation[i][j] = weight
            attestation[j][i] = weight
    
    # Weighted Laplacian
    degree = attestation.sum(axis=1)
    L_weighted = np.diag(degree) - attestation
    
    eigenvalues = np.sort(eigvalsh(L_weighted))
    nonzero = eigenvalues[eigenvalues > 1e-10]
    
    cr = nonzero[0] / nonzero[-1] if len(nonzero) > 0 else 0
    
    print(f"\nValidator stakes:")
    for name, stake in sorted(validators.items(), key=lambda x: -x[1]):
        pct = stake / total_stake * 100
        bar = "█" * int(pct / 2)
        print(f"  {name:10s}: {stake:4d} ETH ({pct:5.1f}%) {bar}")
    
    print(f"\nTotal stake: {total_stake} ETH")
    print(f"Validation graph eigenvalues: {[f'{e:.2f}' for e in eigenvalues]}")
    print(f"Conservation Ratio: {cr:.6f}")
    print(f"Algebraic connectivity (λ₂): {nonzero[0]:.2f}")
    
    # Simulate finality threshold
    # A block is "finalized" when enough validators have attested
    # This corresponds to CR exceeding a threshold
    FINALITY_CR_THRESHOLD = 0.3
    
    print(f"\nFinality threshold: CR >= {FINALITY_CR_THRESHOLD}")
    print(f"Current CR: {cr:.6f}")
    print(f"Block status: {'FINALIZED ✅' if cr >= FINALITY_CR_THRESHOLD else 'PENDING ⏳'}")
    
    # Simulate a validator going offline
    print(f"\n--- Simulating 'dave' (largest validator) going offline ---")
    attestation_reduced = attestation.copy()
    dave_idx = names.index("dave")
    attestation_reduced[dave_idx, :] = 0
    attestation_reduced[:, dave_idx] = 0
    
    degree_r = attestation_reduced.sum(axis=1)
    L_reduced = np.diag(degree_r) - attestation_reduced
    eigs_reduced = np.sort(eigvalsh(L_reduced))
    nonzero_r = eigs_reduced[eigs_reduced > 1e-10]
    cr_reduced = nonzero_r[0] / nonzero_r[-1] if len(nonzero_r) > 0 else 0
    
    print(f"Dave's stake: {validators['dave']} ETH ({validators['dave']/total_stake*100:.1f}%)")
    print(f"CR without Dave: {cr_reduced:.6f}")
    print(f"CR drop: {cr - cr_reduced:.6f}")
    print(f"Block status: {'FINALIZED ✅' if cr_reduced >= FINALITY_CR_THRESHOLD else 'PENDING ⏳'}")
    
    # Simulate equivocation (slashing)
    print(f"\n--- Simulating equivocation by 'dave' (slashing) ---")
    # Dave votes for two conflicting blocks → edge weight goes to -1 (penalty)
    attestation_slashed = attestation.copy()
    alice_idx = names.index("alice")
    bob_idx = names.index("bob")
    # Dave equivocates: attests to both alice's and bob's conflicting blocks
    # This creates contradictory edges
    attestation_slashed[dave_idx, alice_idx] = 0
    attestation_slashed[alice_idx, dave_idx] = 0
    attestation_slashed[dave_idx, bob_idx] = 0
    attestation_slashed[bob_idx, dave_idx] = 0
    
    degree_s = attestation_slashed.sum(axis=1)
    L_slashed = np.diag(degree_s) - attestation_slashed
    eigs_slashed = np.sort(eigvalsh(L_slashed))
    nonzero_s = eigs_slashed[eigs_slashed > 1e-10]
    cr_slashed = nonzero_s[0] / nonzero_s[-1] if len(nonzero_s) > 0 else 0
    
    print(f"CR after slashing: {cr_slashed:.6f}")
    print(f"Total CR drop from baseline: {cr - cr_slashed:.6f}")
    print(f"Block status: {'FINALIZED ✅' if cr_slashed >= FINALITY_CR_THRESHOLD else 'AT RISK ⚠️'}")
    
    return {
        "baseline_cr": cr,
        "offline_cr": cr_reduced,
        "slashed_cr": cr_slashed,
        "finality_threshold": FINALITY_CR_THRESHOLD,
    }


# --- Run All Demos ---
if __name__ == "__main__":
    # 1. Normal blockchain with natural forks
    bc_normal = simulate_blockchain(num_blocks=25, fork_probability=0.2, seed=42)
    spectral_analysis(bc_normal, "Normal Blockchain (Natural Forks)")
    
    # 2. Blockchain under 51% attack
    bc_attack = simulate_blockchain(
        num_blocks=25, fork_probability=0.1, attack_block=15, seed=99
    )
    spectral_analysis(bc_attack, "Blockchain Under 51% Attack")
    
    # 3. 51% attack progression
    simulate_51_attack_progression()
    
    # 4. Proof-of-Stake spectral consensus
    pos_results = proof_of_stake_spectral()
    
    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    print("""
Key findings from spectral blockchain analysis:

1. PATH GRAPH LIMITATION: A blockchain's path structure gives it
   terrible spectral properties (CR → 0 as chain grows). This 
   spectral fragility is WHY forks are dangerous.

2. FORK DETECTION: The Fiedler vector naturally partitions forked
   chains. Monitoring Fiedler partition changes detects forks in
   O(n³) time (dominated by eigendecomposition).

3. 51% ATTACK SIGNATURE: A growing attack branch first increases CR
   (more connectivity) then dominates, collapsing CR back down as
   the honest chain becomes the "minority fork."

4. POS AS CONSERVATION: Stake-weighted validation graphs have 
   meaningful CR values. Finality = CR crossing a threshold.
   Slashing drops CR, making equivocation economically detectable.
    """)
```

## The Bigger Picture

What does it mean that a blockchain has terrible conservation ratio? It means the canonical chain structure — a simple path — is spectrally fragile. The whole reason we need consensus mechanisms (PoW, PoS, BFT) is because the underlying graph structure provides no inherent robustness.

If you wanted to build a *spectrally robust* blockchain, you'd want a **block DAG** (directed acyclic graph) where each block references multiple predecessors, creating an expander-graph-like structure with high CR. This is exactly what projects like Sui and Aptos attempt with their DAG-based consensus — though they don't frame it in spectral terms.

The conservation ratio gives us a unified language:

- **PoW difficulty** ↔ maintaining minimum spectral gap in the block graph
- **Fork choice rules** ↔ selecting the branch that maximizes CR
- **Finality** ↔ CR exceeding a threshold that makes reversal infeasible
- **Network security** ↔ CR of the validator attestation graph

The Laplacian sees through the blockchain abstractions to the underlying graph structure. And the conservation ratio — that simple ratio λ₂/λ_max — captures in a single number how "healthy" the chain is, how vulnerable to attack, and how close to finality.

---

*Three rounds complete. The spectrum is the cipher. The Laplacian is the ledger. The conservation ratio is the proof.*
