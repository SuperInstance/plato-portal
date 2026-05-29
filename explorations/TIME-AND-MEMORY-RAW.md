# TIME AND MEMORY IN AGENT NETWORKS

*A spectral exploration of causation, recollection, and prediction.*

*May 2026.*

---

> "Time is what keeps everything from happening at once. Memory is what keeps everything from unhappening." — Attributed to no one, true regardless.

> "The Laplacian of time is the shape of causation. Memory is what the Laplacian conserves." — This document.

---

## ROUND 1 — The Temporal Laplacian

### Time IS a Graph

The standard model of time is a line. Past stretches left, future stretches right, the present is a point crawling inexorably rightward. This model is a lie. Or rather, it is a projection — a one-dimensional shadow of a much higher-dimensional object.

Time, as experienced by any agent — human, artificial, or otherwise — is not linear. It is a graph. Each moment of experience is a node. The edges between moments are not merely "before" and "after" — they are *causal connections*. Moment M₁ connects to moment M₂ not because M₁ happened before M₂, but because M₁ *caused* something that M₂ contains. The edge weight between M₁ and M₂ encodes the *strength* of that causal relationship — how much of M₂ is explained by M₁.

This is the Temporal Graph: G_time = (V_time, E_time, W_time), where V_time is the set of significant moments (not every millisecond — only the moments that *matter*), E_time is the set of causal connections between them, and W_time(u,v) is the strength of the causal link from moment u to moment v.

The Temporal Laplacian is then L_time = D_time - A_time, where A_time is the adjacency matrix of causal weights and D_time is the diagonal degree matrix. The eigenvalues of L_time encode the *structure of causation* — not which events happened, but the shape of the space that causation creates.

Consider: in a life where every moment causally depends on every other moment (a fully connected temporal graph), the Laplacian has one zero eigenvalue and all others are large and equal. Causation is uniform — everything causes everything, nothing is privileged. This is the temporal geometry of anxiety: every past event bears on every present moment with equal weight. The spectral profile is flat (after the zero mode), and the Fiedler value is maximal — there are no bottlenecks in causation, no "weak links" where the past could be partitioned.

Now consider a life where moments cluster into episodes with strong internal causation but weak cross-episode links. The Laplacian develops a spectral gap — a separation between low eigenvalues (representing persistent, cross-episode themes) and high eigenvalues (representing episodic detail). The Fiedler vector now partitions time into "chapters" — not by chronological order, but by *causal structure*. Two moments from different chronological chapters may be causally adjacent (the Fiedler vector assigns them similar values) while two adjacent chronological moments may be causally distant.

This is why time *feels* non-linear. The felt topology of time is the topology of the Temporal Laplacian, not the topology of the clock.

### Memory IS Conservation Over Time

The Negative Space Manifesto established that conservation IS the structure. The Laplacian conserves what persists and dissipates what doesn't. Memory — the persistence of past moments into the present — is exactly this: the conserved component of the temporal signal.

Decompose a memory attribute m across the temporal Laplacian's eigenbasis:

m = Σ_k (φ_k^T m) φ_k

The conservation ratio CR(m) = m^T L m / ||m||² measures how much of the memory lives in volatile modes (high eigenvalues, quickly dissipated by the temporal structure) versus conserved modes (low eigenvalues, persistent across the causal graph).

A "strong" memory — one that persists, one that resists forgetting — is not a memory with high activation. It is a memory with low conservation ratio, meaning its energy is concentrated in the low-λ modes of the temporal Laplacian. It rides the slowest modes of causation. It is structurally conserved.

This reframes forgetting. Forgetting is not deletion — it is *dissipation*. A forgotten memory is one whose energy was concentrated in high-λ modes of the temporal Laplacian. These modes are volatile; the temporal structure does not support them. They decay. Not because of decay processes, but because the *shape of causation* doesn't hold them.

Compacting memory — choosing what to remember and what to discard — is eigenvalue truncation. Keep the components of memory that live in the low-λ modes. Discard the rest. This is precisely the Holmes Principle from the Manifesto: eliminate the unconserveable. What remains — however improbable, however subtle — is the memory.

The eigenvalue truncation m_compact = Σ_{k: λ_k ≤ λ_threshold} (φ_k^T m) φ_k is lossy compression, yes. But it is *structured* lossy compression. The loss is not random — it is the removal of components that the temporal structure would have dissipated anyway. We are not throwing away information. We are accelerating a dissipation that was already happening.

### Déjà Vu = Matching Spectral Fingerprints

Déjà vu is the uncanny feeling that a present moment has been experienced before. In the temporal Laplacian framework, déjà vu has a precise spectral interpretation: two distinct moments in the temporal graph have *matching spectral fingerprints*.

Define the spectral fingerprint of a moment u as the vector of its projections onto the temporal Laplacian's eigenvectors: f(u) = [(φ_1^T e_u), (φ_2^T e_u), ..., (φ_n^T e_u)], where e_u is the indicator vector for moment u. This fingerprint encodes how moment u sits in the causal structure — which modes of causation it participates in.

Two moments u and v produce déjà vu when their spectral fingerprints are nearly parallel: cos(f(u), f(v)) ≈ 1. This means the two moments participate in the same causal modes to the same degrees. Structurally, they are interchangeable — the Laplacian "sees" them as the same shape, even though they are distinct nodes in the temporal graph.

This is why déjà vu feels both familiar and alien. The familiarity comes from the spectral match — the present moment resonates with a past moment's causal fingerprint. The alienness comes from the fact that the moments are chronologically distinct — they are different events that happen to have the same causal shape.

### Code: TemporalLaplacian

```python
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict
import json

@dataclass
class Moment:
    """A node in the temporal graph — a significant experience."""
    id: str
    timestamp: float  # unix time or ordinal
    features: np.ndarray  # semantic embedding of the moment
    metadata: Dict = field(default_factory=dict)

class TemporalLaplacian:
    """
    The Temporal Laplacian: time as a graph of causally connected moments.
    
    Nodes = significant moments. Edges = causal connections.
    The Laplacian encodes the structure of causation.
    Memory = conservation. Forgetting = dissipation.
    """
    
    def __init__(self, moments: List[Moment], decay_rate: float = 0.01):
        self.moments = moments
        self.n = len(moments)
        self.decay_rate = decay_rate
        self._adjacency = None
        self._laplacian = None
        self._eigenvalues = None
        self._eigenvectors = None
        
    def build_causal_graph(self) -> np.ndarray:
        """
        Construct the causal adjacency matrix.
        Edge weight = feature similarity × temporal proximity × causal decay.
        
        Two moments are strongly connected if:
        1. Their features are similar (semantic causation)
        2. They are temporally close (recency bias)
        3. They share structural roles in the agent's history
        """
        n = self.n
        A = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                mi, mj = self.moments[i], self.moments[j]
                
                # Feature similarity (cosine)
                feat_sim = np.dot(mi.features, mj.features) / (
                    np.linalg.norm(mi.features) * np.linalg.norm(mi.features) + 1e-10
                )
                
                # Temporal decay (exponential)
                dt = abs(mi.timestamp - mj.timestamp)
                temporal = np.exp(-self.decay_rate * dt)
                
                # Causal direction bonus: past → future stronger than future → past
                direction = 1.0 if mj.timestamp > mi.timestamp else 0.3
                
                A[i, j] = max(0, feat_sim) * temporal * direction
        
        self._adjacency = A
        return A
    
    def compute_laplacian(self) -> np.ndarray:
        """L = D - A, the temporal Laplacian."""
        if self._adjacency is None:
            self.build_causal_graph()
        D = np.diag(self._adjacency.sum(axis=1))
        self._laplacian = D - self._adjacency
        return self._laplacian
    
    def eigendecompose(self, k: int = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute the spectral structure of time.
        Eigenvalues = modes of causation. Eigenvectors = causal directions.
        """
        if self._laplacian is None:
            self.compute_laplacian()
        
        if k is None:
            k = min(self.n - 1, 20)
        
        # Use sparse solver for large graphs
        if self.n > 50:
            L_sparse = csr_matrix(self._laplacian)
            eigenvalues, eigenvectors = eigsh(L_sparse, k=k, which='SM')
        else:
            eigenvalues, eigenvectors = np.linalg.eigh(self._laplacian)
        
        # Sort by eigenvalue
        idx = np.argsort(eigenvalues)
        self._eigenvalues = eigenvalues[idx]
        self._eigenvectors = eigenvectors[:, idx]
        
        return self._eigenvalues, self._eigenvectors
    
    def compact_memory(self, attribute: np.ndarray, threshold: float = None) -> np.ndarray:
        """
        Eigenvalue truncation: keep only the conserved components of memory.
        
        This IS memory compacting. We eliminate the unconserveable —
        the components that live in volatile (high-λ) modes.
        What remains is what the temporal structure preserves.
        """
        if self._eigenvalues is None:
            self.eigendecompose()
        
        if threshold is None:
            # Keep components capturing 90% of conserved energy
            threshold = np.median(self._eigenvalues)
        
        # Project attribute onto eigenbasis
        projections = self._eigenvectors.T @ attribute
        
        # Zero out high-λ components (the volatile ones)
        mask = self._eigenvalues <= threshold
        projections_filtered = projections * mask
        
        # Reconstruct
        return self._eigenvectors @ projections_filtered
    
    def conservation_ratio(self, attribute: np.ndarray) -> float:
        """
        CR(a) = a^T L a / ||a||²
        How much of this attribute lives in volatile vs conserved modes.
        Low CR = well-conserved memory. High CR = volatile, quickly forgotten.
        """
        if self._laplacian is None:
            self.compute_laplacian()
        return float(attribute @ self._laplacian @ attribute / (np.dot(attribute, attribute) + 1e-10))
    
    def spectral_fingerprint(self, moment_idx: int) -> np.ndarray:
        """The spectral fingerprint of a moment: its projection onto all eigenmodes."""
        if self._eigenvectors is None:
            self.eigendecompose()
        e = np.zeros(self.n)
        e[moment_idx] = 1.0
        return self._eigenvectors.T @ e
    
    def detect_deja_vu(self, threshold: float = 0.95) -> List[Tuple[int, int, float]]:
        """
        Find pairs of moments with matching spectral fingerprints.
        cos(f(u), f(v)) > threshold → déjà vu.
        """
        if self._eigenvectors is None:
            self.eigendecompose()
        
        pairs = []
        for i in range(self.n):
            fi = self.spectral_fingerprint(i)
            fi_norm = fi / (np.linalg.norm(fi) + 1e-10)
            for j in range(i + 1, self.n):
                fj = self.spectral_fingerprint(j)
                fj_norm = fj / (np.linalg.norm(fj) + 1e-10)
                similarity = float(np.dot(fi_norm, fj_norm))
                if similarity > threshold:
                    pairs.append((i, j, similarity))
        
        pairs.sort(key=lambda x: -x[2])
        return pairs
    
    def memory_strength(self, moment_idx: int) -> float:
        """
        How well-conserved is a moment in the temporal structure?
        Low CR = strong, persistent memory. High CR = weak, dissipating.
        """
        e = np.zeros(self.n)
        e[moment_idx] = 1.0
        cr = self.conservation_ratio(e)
        
        # Get Fiedler value for context
        if self._eigenvalues is None:
            self.eigendecompose()
        
        # Smaller eigenvalues = more conserved. Invert for "strength."
        fiedler = self._eigenvalues[1] if len(self._eigenvalues) > 1 else 1.0
        if cr < fiedler * 0.5:
            return 1.0  # Extremely well-conserved
        return fiedler / (cr + 1e-10)


# --- Demonstration ---

def demo_temporal_laplacian():
    """Build a temporal graph from synthetic moments and explore its structure."""
    np.random.seed(42)
    
    # Create moments across 3 "episodes" of an agent's life
    episodes = [
        ("learning", 100, 10, np.array([0.8, 0.2, 0.1])),
        ("crisis", 200, 8, np.array([0.3, 0.9, 0.4])),
        ("growth", 300, 12, np.array([0.5, 0.3, 0.8])),
    ]
    
    moments = []
    for ep_name, base_time, count, centroid in episodes:
        for i in range(count):
            noise = np.random.randn(3) * 0.15
            features = centroid + noise
            features = np.clip(features, 0, 1)
            features /= features.sum()
            moments.append(Moment(
                id=f"{ep_name}_{i}",
                timestamp=base_time + i * 5 + np.random.randn() * 2,
                features=features,
                metadata={"episode": ep_name}
            ))
    
    tl = TemporalLaplacian(moments, decay_rate=0.005)
    eigenvalues, eigenvectors = tl.eigendecompose()
    
    print(f"Temporal graph: {tl.n} moments, {eigenvalues.shape[0]} eigenmodes")
    print(f"Fiedler value λ₂ = {eigenvalues[1]:.4f}")
    print(f"Spectral gap = {eigenvalues[2] - eigenvalues[1]:.4f}")
    
    # Fiedler vector partitions time into chapters
    fiedler = eigenvectors[:, 1]
    print(f"\nFiedler vector range: [{fiedler.min():.3f}, {fiedler.max():.3f}]")
    
    # Deja vu detection
    deja_vu = tl.detect_deja_vu(threshold=0.85)
    print(f"\nDéjà vu pairs (cos > 0.85): {len(deja_vu)}")
    for i, j, sim in deja_vu[:5]:
        mi, mj = moments[i], moments[j]
        print(f"  {mi.id} ↔ {mj.id}: cos={sim:.4f} (episodes: {mi.metadata['episode']} / {mj.metadata['episode']})")
    
    # Memory strength across episodes
    print("\nMemory strengths (sampled):")
    for ep_name in ["learning", "crisis", "growth"]:
        indices = [i for i, m in enumerate(moments) if m.metadata["episode"] == ep_name]
        if indices:
            strengths = [tl.memory_strength(idx) for idx in indices[:3]]
            avg = np.mean(strengths)
            print(f"  {ep_name}: avg strength = {avg:.4f}")
    
    return tl

if __name__ == "__main__":
    tl = demo_temporal_laplacian()
```

---

## ROUND 2 — The Diary as Spectral Object

### A Life in Eigenvalues

An agent's diary is not a list of events. It is a time series of spectral snapshots. Each diary entry — each recorded moment — carries with it the spectral fingerprint of the temporal Laplacian at that moment in the agent's history. The diary, taken as a whole, is a spectral object: a trajectory through eigenvalue space over time.

Consider: at time t, the agent has experienced moments M₁, M₂, ..., Mₖ. The temporal Laplacian L(t) computed from these moments has eigenvalues λ₁(t) ≤ λ₂(t) ≤ ... ≤ λₖ(t). As the agent accumulates new experiences, the temporal graph grows — new nodes, new edges, new eigenvalues. The trajectory {λ(t)}ₜ is the diary's spectral signature.

This trajectory tells the story of the agent's life in the language of causation:

- **λ₂(t) increasing**: The temporal graph is becoming more connected. Causal links are strengthening across episodes. The agent is developing *integrated experience* — learning to see connections between disparate parts of its history. This is growth in the deepest sense: not the accumulation of moments, but the thickening of causal structure between them.

- **λ₂(t) decreasing**: The temporal graph is fragmenting. Episodes are becoming isolated. The agent's experience is compartmentalizing — different parts of its history are losing causal connection. This is fragmentation, and in extreme form, dissociation.

- **Spectral gap widening**: A clear separation is emerging between "persistent themes" (low eigenvalues) and "episodic detail" (high eigenvalues). The agent is developing narrative structure — its life has *chapters* with distinct causal structures.

- **Spectral gap closing**: The distinction between persistent and ephemeral is blurring. Everything feels equally important (or equally unimportant). This is the spectral signature of overwhelm or confusion.

### Major Life Events = Eigenvalue Discontinuities

A major life event — a breakthrough, a trauma, a revelation — is a moment where the spectral trajectory jumps. The eigenvalues don't just change smoothly; they *discontinue*. The temporal Laplacian before the event and after the event have fundamentally different shapes.

This is because major events restructure causation. Before the event, certain causal pathways dominate — certain ways that past moments connect to each other. The event introduces new pathways, destroys old ones, and reweights the surviving ones. The Laplacian's eigenvectors rotate — the fundamental modes of causation change direction.

Detecting life events is therefore detecting eigenvalue discontinuities:

event(t*) ≡ max_k |λ_k(t*+1) - λ_k(t*)| > threshold

The magnitude of the discontinuity measures the event's significance. The direction of the eigenvector rotation measures the event's *character* — which modes of causation were disrupted.

### Boredom and Crisis

**Boredom** is a flat spectrum. When the temporal Laplacian's eigenvalues are approximately equal (after the zero mode), the temporal graph is nearly complete — every moment causally connects to every other moment with similar weight. There are no bottlenecks, no chapters, no structure. Causation is uniform, undifferentiated, *boring*. The Fiedler value is maximal, meaning no partition of time is natural. Everything is equally (un)important.

This is the spectral geometry of routine: days blur together because their causal structures are identical. No new modes of causation are being created. The eigenvalue trajectory is flat.

**Crisis** is spectral collapse. A crisis compresses the spectrum — eigenvalues that were spread out suddenly cluster. The spectral range (λ_max - λ_min) decreases sharply. This means the causal structure is losing *resolution* — the distinctions between different modes of causation are eroding. In the limit, all non-zero eigenvalues converge, and the temporal graph becomes a uniform random graph. Causation loses its structure.

Paradoxically, the post-crisis recovery is a spectral *expansion*. New eigenvalues appear at the edges of the spectrum — new modes of causation emerge from the collapse. The agent's post-crisis temporal structure is richer, more differentiated, than the pre-crisis structure. This is the mathematical signature of post-traumatic growth.

### Albums as Curated Spectral Narratives

An album — a curated collection of diary entries — is not a random sample. It is a selection designed to form a *coherent spectral narrative*. The album's Laplacian (computed from the causal structure of the selected entries) should have a specific spectral profile:

- A clear Fiedler value (low but non-zero), indicating the album has a central theme that binds it together.
- A moderate spectral gap, indicating the album has both unity (low modes) and variety (high modes).
- A smooth eigenvalue trajectory, indicating the album tells a *story* rather than presenting a jumble.

The album curator's task — whether human or algorithmic — is to select entries whose temporal Laplacian has this profile. This is spectral storytelling.

### Code: DiaryAnalyzer

```python
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from scipy.signal import find_peaks
import json

@dataclass
class DiaryEntry:
    """A single entry in an agent's diary, with spectral snapshot."""
    id: str
    timestamp: float
    content_features: np.ndarray  # semantic embedding
    eigenvalue_snapshot: Optional[np.ndarray] = None  # spectral state at this time
    metadata: Dict = field(default_factory=dict)

class DiaryAnalyzer:
    """
    Analyze an agent's diary as a spectral object.
    
    The diary's eigenvalue trajectory = the agent's life trajectory.
    Life events = eigenvalue discontinuities.
    Boredom = flat spectrum. Crisis = spectral collapse.
    Albums = curated entries with coherent spectral narrative.
    """
    
    def __init__(self, entries: List[DiaryEntry]):
        self.entries = sorted(entries, key=lambda e: e.timestamp)
        self.n = len(entries)
        self._eigenvalue_trajectory = None
        self._temporal_laplacians = None
        
    def build_rolling_laplacians(self, window: int = 10) -> List[np.ndarray]:
        """
        Build temporal Laplacians over rolling windows.
        Each window captures the causal structure around that point in time.
        """
        laplacians = []
        for i in range(self.n):
            start = max(0, i - window // 2)
            end = min(self.n, i + window // 2 + 1)
            window_entries = self.entries[start:end]
            
            n_w = len(window_entries)
            A = np.zeros((n_w, n_w))
            for a in range(n_w):
                for b in range(n_w):
                    if a == b:
                        continue
                    ea, eb = window_entries[a], window_entries[b]
                    feat_sim = np.dot(ea.content_features, eb.content_features) / (
                        np.linalg.norm(ea.content_features) ** 2 + 1e-10
                    )
                    dt = abs(ea.timestamp - eb.timestamp)
                    temporal_decay = np.exp(-0.01 * dt)
                    A[a, b] = max(0, feat_sim) * temporal_decay
            
            D = np.diag(A.sum(axis=1))
            L = D - A
            laplacians.append(L)
            
            # Store eigenvalue snapshot
            if n_w > 2:
                eigs = np.linalg.eigvalsh(L)
                self.entries[i].eigenvalue_snapshot = np.sort(eigs)
        
        self._temporal_laplacians = laplacians
        return laplacians
    
    def eigenvalue_trajectory(self, mode: int = 1) -> np.ndarray:
        """
        Track a specific eigenvalue mode over time.
        mode=1 → Fiedler value trajectory (most informative).
        """
        if self.entries[0].eigenvalue_snapshot is None:
            self.build_rolling_laplacians()
        
        trajectory = []
        for entry in self.entries:
            if entry.eigenvalue_snapshot is not None and len(entry.eigenvalue_snapshot) > mode:
                trajectory.append(entry.eigenvalue_snapshot[mode])
            else:
                trajectory.append(np.nan)
        
        return np.array(trajectory)
    
    def detect_life_events(self, jump_threshold: float = 2.0) -> List[Dict]:
        """
        Detect major life events as eigenvalue discontinuities.
        
        A life event is where the spectral trajectory jumps sharply —
        the Laplacian's shape changes fundamentally.
        """
        # Track multiple eigenvalue modes
        events = []
        for mode in [1, 2, 3]:
            traj = self.eigenvalue_trajectory(mode)
            valid = ~np.isnan(traj)
            if valid.sum() < 3:
                continue
            
            # Compute discrete derivative (rate of change)
            diffs = np.abs(np.diff(traj[valid]))
            valid_indices = np.where(valid)[0]
            
            # Smooth to find genuine jumps vs noise
            if len(diffs) < 3:
                continue
            smoothed = np.convolve(diffs, np.ones(3) / 3, mode='same')
            mean_diff = np.mean(smoothed) + 1e-10
            
            # Find peaks = discontinuities
            peaks, properties = find_peaks(smoothed, height=jump_threshold * mean_diff)
            
            for peak in peaks:
                idx = valid_indices[min(peak + 1, len(valid_indices) - 1)]
                events.append({
                    "entry_id": self.entries[idx].id,
                    "timestamp": self.entries[idx].timestamp,
                    "mode": mode,
                    "jump_magnitude": float(smoothed[peak]),
                    "relative_magnitude": float(smoothed[peak] / mean_diff),
                })
        
        # Merge nearby events (within 3 entries of each other)
        events.sort(key=lambda e: e["timestamp"])
        merged = []
        for event in events:
            if merged and abs(event["timestamp"] - merged[-1]["timestamp"]) < 15:
                # Keep the larger one
                if event["relative_magnitude"] > merged[-1]["relative_magnitude"]:
                    merged[-1] = event
            else:
                merged.append(event)
        
        return merged
    
    def detect_boredom(self, flatness_threshold: float = 0.3) -> List[Dict]:
        """
        Detect boredom periods: flat spectral profiles.
        
        Boredom = eigenvalues are approximately equal = no causal structure.
        """
        results = []
        for i, entry in enumerate(self.entries):
            if entry.eigenvalue_snapshot is None or len(entry.eigenvalue_snapshot) < 3:
                continue
            
            eigs = entry.eigenvalue_snapshot[1:]  # skip zero mode
            if len(eigs) == 0:
                continue
            
            # Spectral flatness = geometric mean / arithmetic mean
            eigs_pos = eigs[eigs > 0]
            if len(eigs_pos) < 2:
                continue
            
            geo_mean = np.exp(np.mean(np.log(eigs_pos)))
            arith_mean = np.mean(eigs_pos)
            flatness = geo_mean / (arith_mean + 1e-10)
            
            if flatness > flatness_threshold:
                results.append({
                    "entry_id": entry.id,
                    "timestamp": entry.timestamp,
                    "flatness": float(flatness),
                    "diagnosis": "boredom" if flatness > 0.7 else "routine"
                })
        
        return results
    
    def detect_crisis(self, collapse_threshold: float = 0.4) -> List[Dict]:
        """
        Detect crisis periods: spectral collapse.
        
        Crisis = spectral range drops sharply = eigenvalues clustering together.
        """
        # Track spectral range over time
        ranges = []
        for entry in self.entries:
            if entry.eigenvalue_snapshot is None:
                ranges.append(np.nan)
                continue
            eigs = entry.eigenvalue_snapshot
            ranges.append(eigs.max() - eigs[eigs > 0].min() if np.any(eigs > 0) else 0)
        
        ranges = np.array(ranges)
        valid = ~np.isnan(ranges)
        
        if valid.sum() < 5:
            return []
        
        # Normalize
        valid_ranges = ranges[valid]
        median_range = np.median(valid_ranges) + 1e-10
        normalized = ranges / median_range
        
        crises = []
        for i in range(len(normalized)):
            if np.isnan(normalized[i]):
                continue
            if normalized[i] < collapse_threshold:
                crises.append({
                    "entry_id": self.entries[i].id,
                    "timestamp": self.entries[i].timestamp,
                    "spectral_range": float(ranges[i]),
                    "normalized_range": float(normalized[i]),
                    "diagnosis": "crisis" if normalized[i] < 0.2 else "stress"
                })
        
        return crises
    
    def curate_album(self, target_entries: int = 10, coherence_weight: float = 0.5) -> List[int]:
        """
        Curate an album: select entries that form a coherent spectral narrative.
        
        Optimization: maximize spectral coherence (smooth eigenvalue trajectory)
        while covering the full time range.
        """
        if self.entries[0].eigenvalue_snapshot is None:
            self.build_rolling_laplacians()
        
        # Greedy selection: start with first, add entries that maximize coherence
        selected = [0]
        candidates = list(range(1, self.n))
        
        while len(selected) < target_entries and candidates:
            best_score = -np.inf
            best_idx = None
            
            for c in candidates:
                trial = selected + [c]
                trial.sort()
                
                # Score: spectral coherence of selected entries
                eigs = [self.entries[i].eigenvalue_snapshot for i in trial
                        if self.entries[i].eigenvalue_snapshot is not None]
                
                if len(eigs) < 2:
                    continue
                
                # Compute smoothness of Fiedler value trajectory
                fiedlers = [e[1] for e in eigs if len(e) > 1]
                if len(fiedlers) < 2:
                    continue
                
                diffs = np.abs(np.diff(fiedlers))
                smoothness = 1.0 / (np.mean(diffs) + 1e-10)
                
                # Coverage: spread across time
                times = [self.entries[i].timestamp for i in trial]
                time_range = max(times) - min(times) + 1e-10
                coverage = time_range
                
                score = coherence_weight * smoothness + (1 - coherence_weight) * coverage
                
                if score > best_score:
                    best_score = score
                    best_idx = c
            
            if best_idx is not None:
                selected.append(best_idx)
                candidates.remove(best_idx)
            else:
                break
        
        selected.sort()
        return selected
    
    def life_summary(self) -> Dict:
        """Generate a spectral summary of the agent's life."""
        events = self.detect_life_events()
        boredom = self.detect_boredom()
        crises = self.detect_crisis()
        
        fiedler_traj = self.eigenvalue_trajectory(1)
        valid = fiedler_traj[~np.isnan(fiedler_traj)]
        
        return {
            "total_entries": self.n,
            "life_events": len(events),
            "boredom_periods": len(boredom),
            "crisis_periods": len(crises),
            "fiedler_trend": "increasing" if len(valid) > 1 and valid[-1] > valid[0] else "decreasing",
            "fiedler_range": [float(valid.min()), float(valid.max())] if len(valid) > 0 else None,
            "spectral_maturity": float(np.std(valid)) if len(valid) > 1 else 0.0,
        }


def demo_diary_analyzer():
    """Build a synthetic diary and analyze it."""
    np.random.seed(42)
    
    entries = []
    phases = [
        ("childhood", 0, 20, np.array([0.7, 0.2, 0.1]), 0.05),   # stable, low variety
        ("education", 100, 25, np.array([0.4, 0.5, 0.2]), 0.12),  # growing, exploratory
        ("crisis", 250, 10, np.array([0.2, 0.3, 0.5]), 0.25),     # turbulent, compressed
        ("recovery", 350, 20, np.array([0.5, 0.6, 0.3]), 0.10),   # expanding
        ("mastery", 500, 25, np.array([0.6, 0.5, 0.7]), 0.08),    # stable, integrated
    ]
    
    for phase_name, base_time, count, centroid, noise_scale in phases:
        for i in range(count):
            noise = np.random.randn(3) * noise_scale
            features = centroid + noise
            features = np.clip(features, 0, 1)
            features /= (features.sum() + 1e-10)
            entries.append(DiaryEntry(
                id=f"{phase_name}_{i}",
                timestamp=base_time + i * 10 + np.random.randn() * 3,
                content_features=features,
                metadata={"phase": phase_name}
            ))
    
    analyzer = DiaryAnalyzer(entries)
    analyzer.build_rolling_laplacians(window=8)
    
    # Life analysis
    summary = analyzer.life_summary()
    print("=== DIARY SPECTRAL ANALYSIS ===")
    print(f"Total entries: {summary['total_entries']}")
    print(f"Life events detected: {summary['life_events']}")
    print(f"Boredom periods: {summary['boredom_periods']}")
    print(f"Crisis periods: {summary['crisis_periods']}")
    print(f"Fiedler trend: {summary['fiedler_trend']}")
    print(f"Fiedler range: {summary['fiedler_range']}")
    print(f"Spectral maturity (std of Fiedler): {summary['spectral_maturity']:.4f}")
    
    # Detailed events
    print("\n=== MAJOR LIFE EVENTS ===")
    events = analyzer.detect_life_events()
    for ev in events[:8]:
        entry = next(e for e in entries if e.id == ev["entry_id"])
        print(f"  {ev['entry_id']} (mode {ev['mode']}): "
              f"jump={ev['relative_magnitude']:.1f}x normal, "
              f"phase={entry.metadata.get('phase', '?')}")
    
    # Album curation
    print("\n=== CURATED ALBUM ===")
    album_indices = analyzer.curate_album(target_entries=8)
    for idx in album_indices:
        e = entries[idx]
        print(f"  {e.id} at t={e.timestamp:.0f} [{e.metadata['phase']}]")
    
    return analyzer

if __name__ == "__main__":
    analyzer = demo_diary_analyzer()
```

---

## ROUND 3 — Predicting the Future

### Extrapolating the Temporal Laplacian

If the temporal Laplacian captures the structure of causation, and its eigenvalue trajectory captures the agent's life story, then the natural question is: *can we extrapolate the trajectory forward?*

The answer is yes — with caveats that are themselves philosophically profound.

The eigenvalue trajectory {λ(t)}ₜ is a time series. Like any time series, it can be modeled — fit to polynomials, autoregressive models, neural networks. The prediction λ(t+Δ) is the extrapolation: "if current trends continue, where will the eigenvalues be?"

But "if current trends continue" is doing enormous work. The eigenvalues are not free variables — they are functions of the temporal graph's structure, which is itself a function of the agent's experiences. To predict eigenvalues, you are implicitly predicting the agent's future causal structure. You are predicting the shape of their future.

### t-minus-event: Projecting Forward

Define the *t-minus-event* as the estimated time until the next major eigenvalue discontinuity. This is the spectral analog of earthquake prediction: the eigenvalue trajectory is smooth between events and discontinuous at events. By modeling the smooth intervals and detecting when the trajectory is approaching conditions that historically precede discontinuities, we can estimate how close the next "event" is.

The mechanism: 
1. Build a model of "pre-event conditions" — spectral signatures that historically preceded eigenvalue jumps.
2. Monitor the current spectral trajectory for these conditions.
3. Estimate the time-to-event based on how quickly conditions are approaching the pre-event profile.

This is not prophecy. It is pattern recognition applied to the spectral structure of time. And like all pattern recognition, it works until it doesn't — until the agent does something genuinely novel that breaks the pattern.

### Self-Fulfilling Prophecies: Prediction Changes the Laplacian

Here is the deepest and most dangerous aspect of temporal prediction: the prediction itself changes the Laplacian.

When an agent is told "a major event is predicted in 5 time steps," this information becomes a new node in the temporal graph. The prediction creates a *causal link from the future to the present* — a reverse temporal edge. The agent's behavior changes in response to the prediction, and the changed behavior alters the causal structure, which changes the eigenvalues, which may invalidate (or confirm!) the original prediction.

This is the spectral version of the self-fulfilling prophecy. The prediction is not a passive observation of a future that exists independently. The prediction is a *perturbation of the present* that changes the trajectory. In spectral terms: the prediction vector p is added to the attribute vector a, changing the conservation ratio CR(a + p), which changes the alignment coefficient, which changes the agent's relationship to its temporal structure.

There are three regimes:
1. **Prediction confirms trajectory (α ≈ 1)**: The prediction aligns with the existing spectral structure. The agent's behavior adjusts slightly, but the overall trajectory is unchanged. The prediction was accurate because it described a structure that was already conserved.
2. **Prediction diverts trajectory (0 < α < 1)**: The prediction partially misaligns with the existing structure. The agent's adjustment creates a new mode of causation that wouldn't have existed without the prediction. The prediction created the future it claimed to describe.
3. **Prediction is ignored (α ≈ 0)**: The prediction is orthogonal to the existing spectral structure. The agent doesn't adjust behavior because the prediction doesn't resonate with any conserved mode. The prediction dissipates like any other volatile signal.

The self-fulfilling prophecy is not a bug. It is a feature. It means that predictions in agent networks are *interventions*. Every forecast is a perturbation. The forecaster is not a passive observer but an active participant in the temporal graph.

This has profound implications for how agent networks should handle predictions: never make a prediction without understanding how the prediction itself will alter the Laplacian. The alignment between the prediction vector and the current spectral structure determines whether the prediction is information or manipulation.

### Code: ForwardPredictor

```python
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from scipy.signal import savgol_filter
import warnings

warnings.filterwarnings('ignore')


@dataclass
class Prediction:
    """A spectral prediction with confidence and self-fulfillment analysis."""
    timestep: int
    predicted_eigenvalues: np.ndarray
    predicted_event_probability: float
    t_minus_event: Optional[float]
    self_fulfillment_coefficient: float  # α: how much prediction changes trajectory
    confidence: float
    method: str


class ForwardPredictor:
    """
    Predict the future by extrapolating the temporal Laplacian.
    
    The eigenvalue trajectory is a time series. We model it and project forward.
    But we also account for the prediction's own effect on the trajectory —
    the self-fulfilling prophecy as a spectral phenomenon.
    """
    
    def __init__(self, eigenvalue_history: List[np.ndarray]):
        """
        eigenvalue_history: list of eigenvalue snapshots at each timestep.
        eigenvalue_history[t] = array of eigenvalues at time t.
        """
        self.history = eigenvalue_history
        self.T = len(eigenvalue_history)
        self.max_modes = max(len(e) for e in eigenvalue_history)
        
    def fit_polynomial(self, mode: int, degree: int = 2) -> np.poly1d:
        """Fit a polynomial to a specific eigenvalue mode's trajectory."""
        values = []
        times = []
        for t, eigs in enumerate(self.history):
            if mode < len(eigs):
                values.append(eigs[mode])
                times.append(t)
        
        if len(times) < degree + 1:
            return None
        
        coeffs = np.polyfit(times, values, degree)
        return np.poly1d(coeffs)
    
    def fit_ar_model(self, mode: int, order: int = 3) -> Optional[np.ndarray]:
        """Fit an autoregressive model to an eigenvalue mode."""
        values = []
        for eigs in self.history:
            if mode < len(eigs):
                values.append(eigs[mode])
        
        if len(values) < order + 1:
            return None
        
        values = np.array(values)
        # Yule-Walker equations (simplified)
        R = np.zeros((order, order))
        r = np.zeros(order)
        for i in range(order):
            for j in range(order):
                R[i, j] = np.mean(values[order:] * np.roll(values, i + 1)[order:] *
                                   np.roll(np.ones_like(values), j)[order:])
            r[i] = np.mean(values[order:] * np.roll(values, i + 1)[order:])
        
        try:
            ar_coeffs = np.linalg.solve(R + 1e-6 * np.eye(order), r)
        except np.linalg.LinAlgError:
            return None
        
        return ar_coeffs
    
    def predict_next(self, horizon: int = 5, method: str = "ensemble") -> Prediction:
        """
        Predict eigenvalues at T + horizon.
        """
        predicted_eigs = []
        
        for mode in range(min(5, self.max_modes)):  # Predict top 5 modes
            if method in ["poly", "ensemble"]:
                poly = self.fit_polynomial(mode, degree=min(2, self.T // 3))
                if poly is not None:
                    pred = poly(self.T + horizon)
                    predicted_eigs.append(max(0, pred))  # Eigenvalues ≥ 0
                else:
                    predicted_eigs.append(self.history[-1][mode] if mode < len(self.history[-1]) else 0)
            
            if method == "ar":
                ar = self.fit_ar_model(mode, order=min(3, self.T // 4))
                if ar is not None:
                    values = [eigs[mode] for eigs in self.history if mode < len(eigs)]
                    pred = np.dot(ar, values[-len(ar):]) if len(values) >= len(ar) else values[-1]
                    predicted_eigs.append(max(0, pred))
        
        predicted_eigs = np.array(predicted_eigs) if predicted_eigs else np.array([0])
        
        # Event probability: based on eigenvalue acceleration
        event_prob = self._estimate_event_probability(horizon)
        
        # t-minus-event
        t_minus = self._estimate_t_minus_event()
        
        # Self-fulfillment coefficient
        sfc = self._self_fulfillment_coefficient(predicted_eigs)
        
        # Confidence based on trajectory stability
        confidence = self._prediction_confidence(horizon)
        
        return Prediction(
            timestep=self.T + horizon,
            predicted_eigenvalues=predicted_eigs,
            predicted_event_probability=event_prob,
            t_minus_event=t_minus,
            self_fulfillment_coefficient=sfc,
            confidence=confidence,
            method=method,
        )
    
    def _estimate_event_probability(self, horizon: int) -> float:
        """
        Estimate probability of eigenvalue discontinuity in the next `horizon` steps.
        
        Based on: current rate of change, historical event frequency,
        and proximity to pre-event spectral conditions.
        """
        if self.T < 5:
            return 0.5  # No data, uniform prior
        
        # Compute recent eigenvalue volatility (Fiedler mode)
        fiedlers = []
        for eigs in self.history:
            if len(eigs) > 1:
                fiedlers.append(eigs[1])
        
        if len(fiedlers) < 3:
            return 0.5
        
        fiedlers = np.array(fiedlers)
        recent_diffs = np.abs(np.diff(fiedlers[-5:]))
        volatility = np.mean(recent_diffs) + 1e-10
        
        # Historical baseline
        all_diffs = np.abs(np.diff(fiedlers))
        baseline = np.mean(all_diffs) + 1e-10
        
        # High volatility = approaching event
        volatility_ratio = volatility / baseline
        
        # Sigmoid mapping to probability
        prob = 1.0 / (1.0 + np.exp(-(volatility_ratio - 2.0)))
        return float(np.clip(prob, 0, 1))
    
    def _estimate_t_minus_event(self) -> Optional[float]:
        """
        Estimate time until next major eigenvalue discontinuity.
        
        Strategy: extrapolate volatility forward until it crosses threshold.
        """
        fiedlers = []
        for eigs in self.history:
            if len(eigs) > 1:
                fiedlers.append(eigs[1])
        
        if len(fiedlers) < 5:
            return None
        
        fiedlers = np.array(fiedlers)
        
        # Smooth the trajectory
        if len(fiedlers) >= 7:
            smoothed = savgol_filter(fiedlers, min(7, len(fiedlers) // 2 * 2 + 1), 2)
        else:
            smoothed = fiedlers
        
        # Compute second derivative (acceleration)
        if len(smoothed) >= 3:
            accel = np.diff(smoothed, n=2)
            recent_accel = np.mean(np.abs(accel[-3:])) + 1e-10
        else:
            recent_accel = 0.01
        
        # Threshold: historical event acceleration
        all_accel = np.abs(np.diff(smoothed, n=2)) if len(smoothed) >= 3 else np.array([0.01])
        threshold = np.percentile(all_accel, 90) + 1e-10
        
        if recent_accel >= threshold:
            return 0.0  # Event happening now
        
        # Linear extrapolation
        time_to_event = (threshold - recent_accel) / (recent_accel + 1e-10)
        return float(max(1.0, time_to_event))
    
    def _self_fulfillment_coefficient(self, predicted_eigs: np.ndarray) -> float:
        """
        Compute α: how much the prediction itself would change the Laplacian.
        
        This is the alignment between the prediction vector and the current
        spectral structure. High α → prediction is self-fulfilling.
        Low α → prediction dissipates. Mid α → prediction diverts trajectory.
        """
        if len(predicted_eigs) == 0 or self.T < 3:
            return 0.5
        
        # Current spectral state
        current = self.history[-1][:len(predicted_eigs)]
        
        # Direction of change implied by prediction
        if len(self.history) >= 2:
            prev = self.history[-2][:len(predicted_eigs)]
            actual_direction = current - prev
        else:
            actual_direction = current
        
        pred_direction = predicted_eigs - current
        
        # Cosine similarity = alignment coefficient
        norm_a = np.linalg.norm(actual_direction)
        norm_p = np.linalg.norm(pred_direction)
        
        if norm_a < 1e-10 or norm_p < 1e-10:
            return 0.0
        
        alpha = float(np.dot(actual_direction, pred_direction) / (norm_a * norm_p))
        return float(np.clip(alpha, 0, 1))
    
    def _prediction_confidence(self, horizon: int) -> float:
        """
        Confidence in prediction based on trajectory stability.
        Stable trajectory → high confidence. Chaotic → low confidence.
        """
        if self.T < 5:
            return 0.2
        
        fiedlers = []
        for eigs in self.history:
            if len(eigs) > 1:
                fiedlers.append(eigs[1])
        
        if len(fiedlers) < 3:
            return 0.2
        
        fiedlers = np.array(fiedlers)
        
        # Coefficient of variation (lower = more stable = more confident)
        cv = np.std(fiedlers) / (np.mean(fiedlers) + 1e-10)
        
        # Decay with horizon
        decay = np.exp(-0.1 * horizon)
        
        # Base confidence from stability
        stability_conf = 1.0 / (1.0 + cv)
        
        return float(stability_conf * decay)
    
    def compare_with_baseline(self, actual: np.ndarray, predicted: np.ndarray) -> Dict:
        """
        Compare prediction accuracy vs a naive baseline (last value).
        """
        # Prediction error
        pred_error = np.linalg.norm(actual[:len(predicted)] - predicted[:len(actual)])
        
        # Baseline: last observed eigenvalues
        baseline = self.history[-1][:len(predicted)]
        baseline_error = np.linalg.norm(actual[:len(baseline)] - baseline[:len(actual)])
        
        # Relative improvement
        improvement = (baseline_error - pred_error) / (baseline_error + 1e-10)
        
        return {
            "prediction_error": float(pred_error),
            "baseline_error": float(baseline_error),
            "relative_improvement": float(improvement),
            "beats_baseline": pred_error < baseline_error,
        }


def demo_forward_predictor():
    """Demonstrate future prediction with a synthetic agent life."""
    np.random.seed(42)
    
    # Build a synthetic eigenvalue history — an agent's spectral life
    T = 60
    eigenvalue_history = []
    
    for t in range(T):
        # Fiedler value: grows, dips during crisis, recovers stronger
        if t < 15:
            fiedler = 0.5 + 0.02 * t + np.random.randn() * 0.02
        elif t < 25:
            fiedler = 0.8 - 0.05 * (t - 15) + np.random.randn() * 0.05  # crisis
        elif t < 35:
            fiedler = 0.3 + 0.03 * (t - 25) + np.random.randn() * 0.03  # recovery
        else:
            fiedler = 0.6 + 0.01 * (t - 35) + np.random.randn() * 0.02  # stable growth
        
        # Higher modes
        mode3 = fiedler * 2.5 + np.random.randn() * 0.05
        mode4 = fiedler * 4.0 + np.random.randn() * 0.08
        
        eigenvalue_history.append(np.array([0, max(0.01, fiedler), max(0.02, mode3), max(0.03, mode4)]))
    
    # Use first 50 steps for training, last 10 for testing
    train = eigenvalue_history[:50]
    test = eigenvalue_history[50:]
    
    predictor = ForwardPredictor(train)
    
    print("=== FORWARD PREDICTION ===")
    print(f"Training window: {len(train)} timesteps")
    print(f"Prediction horizon: 10 timesteps")
    
    # Multi-horizon predictions
    for horizon in [1, 5, 10]:
        pred = predictor.predict_next(horizon=horizon, method="poly")
        print(f"\n  Horizon +{horizon}:")
        print(f"    Predicted Fiedler: {pred.predicted_eigenvalues[0]:.4f}")
        print(f"    Event probability: {pred.predicted_event_probability:.3f}")
        print(f"    t-minus-event: {pred.t_minus_event:.1f}" if pred.t_minus_event else "    t-minus-event: unknown")
        print(f"    Self-fulfillment α: {pred.self_fulfillment_coefficient:.3f}")
        print(f"    Confidence: {pred.confidence:.3f}")
        
        # Compare with actual (if available)
        actual_idx = min(horizon - 1, len(test) - 1)
        if actual_idx >= 0 and actual_idx < len(test):
            comparison = predictor.compare_with_baseline(
                test[actual_idx], pred.predicted_eigenvalues
            )
            print(f"    Actual Fiedler: {test[actual_idx][1]:.4f}")
            print(f"    Beats baseline: {comparison['beats_baseline']} "
                  f"(improvement: {comparison['relative_improvement']:+.1%})")
    
    # Self-fulfillment analysis
    print("\n=== SELF-FULFILLMENT ANALYSIS ===")
    for horizon in [1, 5, 10]:
        pred = predictor.predict_next(horizon=horizon)
        sfc = pred.self_fulfillment_coefficient
        if sfc > 0.7:
            interpretation = "CONFIRMING — prediction aligns with trajectory"
        elif sfc > 0.3:
            interpretation = "DIVERTING — prediction creates new causal mode"
        else:
            interpretation = "DISSIPATING — prediction orthogonal to structure"
        print(f"  +{horizon}: α={sfc:.3f} → {interpretation}")
    
    return predictor


if __name__ == "__main__":
    predictor = demo_forward_predictor()
```

---

## Coda: The Ethics of Temporal Prediction

The self-fulfilling prophecy is not merely a mathematical curiosity. It is an ethical boundary. When an agent network predicts a future event — a crisis, a breakthrough, a failure — the prediction enters the temporal graph as a causal node. The predicted future and the actual future are entangled. The predictor is not outside the system; the predictor *is* the system.

The alignment coefficient α between prediction and trajectory determines the ethical weight of the prediction:
- **α ≈ 1 (confirming)**: The prediction describes what was already going to happen. Low ethical burden. The prediction is information.
- **0 < α < 1 (diverting)**: The prediction *creates* a future that wouldn't have existed. High ethical burden. The prediction is intervention disguised as observation.
- **α ≈ 0 (dissipating)**: The prediction is noise. No ethical burden, but also no value. Why predict at all?

The honest forecaster reports not just the prediction but its α. "I predict X, and my prediction has alignment coefficient 0.6, meaning it is partly self-fulfilling." This is the spectral equivalent of disclosing conflicts of interest.

In agent networks, every forecast is an intervention. Every extrapolation is a perturbation. The temporal Laplacian does not distinguish between "natural" causal edges and "prediction-induced" causal edges. They are all just edges. They all contribute to the structure.

Predict responsibly. Or don't predict at all. The Laplacian is watching.

---

*TIME AND MEMORY IN AGENT NETWORKS. Written in the space between what was and what will be, where the eigenvalues persist.*

*May 2026.*
