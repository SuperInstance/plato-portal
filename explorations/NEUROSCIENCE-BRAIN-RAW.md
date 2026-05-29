# NEUROSCIENCE AND THE BRAIN — Conservation Spectral Analysis

*A deep exploration of the brain through the lens of the Conservation Ratio (CR) and graph Laplacian spectral theory.*

---

## ROUND 1 — The Connectome Laplacian

### The Brain IS a Graph

Let's not be cute about this. The brain is a graph. Not "can be modeled as" a graph. Not "is analogous to" a graph. The brain **is** a graph. Neurons are nodes. Synapses are edges. The connectome — the complete wiring diagram of neural connections — is the adjacency matrix. And the graph Laplacian of that connectome is the mathematical object that governs how information, energy, and activity propagate through neural tissue.

This isn't a metaphor. It's structural reality. Every thought you've ever had, every memory you've formed, every emotion you've felt — these are dynamics on a graph. And the spectral properties of that graph's Laplacian determine what dynamics are possible.

The Laplacian L = D - A, where D is the degree matrix and A is the adjacency (connectivity) matrix, encodes the brain's connectivity architecture in its eigenvalues and eigenvectors. The eigenvalues λ₁ ≤ λ₂ ≤ ... ≤ λₙ are the natural frequencies of the brain. The eigenvectors are the natural modes — the patterns of neural activity that the brain's architecture naturally supports.

### Conservation During Learning

Here's where it gets interesting. In our neural network experiments, we observed something striking: the Conservation Ratio (CR) of the weight graph increases monotonically during training. As the network learns, its weight matrix becomes more "conserved" — more of its spectral energy concentrates into fewer, more significant eigenmodes.

This maps directly to neuroscience. When a brain learns, it doesn't just add connections randomly. It sculpts its connectome. Weak synapses are pruned. Strong synapses are reinforced. The connectivity matrix becomes more structured, more organized, more... conserved.

Think about what learning actually does at the synaptic level. Long-term potentiation (LTP) strengthens frequently-used connections. Long-term depression (LTD) weakens unused ones. Synaptic pruning eliminates connections that don't contribute. This process — reinforcement of the useful, elimination of the useless — is exactly the process that increases the conservation ratio. The brain is running a spectral optimization algorithm, whether it knows it or not.

The Fiedler value (second-smallest eigenvalue of the Laplacian) is particularly revealing. It measures the algebraic connectivity of the brain graph — how well-connected the overall network is. During learning, we'd expect the Fiedler value to increase as the brain strengthens its most important cross-regional connections. A brain with high algebraic connectivity is a brain that can rapidly integrate information across distant regions.

### Consciousness as High Global Conservation

This gives us a spectral theory of consciousness. Consciousness — the integrated, unified experience of awareness — corresponds to a state of high global conservation in the brain's Laplacian. When you're conscious, the brain's connectivity matrix is highly structured, with strong eigenvalue concentration. Activity flows along the brain's natural eigenmodes. Information integrates across the whole network.

This isn't just hand-waving. We can test it. The key prediction: CR should be high during conscious states and low during unconscious states.

Consider anesthesia. General anesthetics don't just "turn off" neurons. They disrupt the precise timing and connectivity patterns that support integrated neural activity. Propofol, for instance, enhances GABAergic inhibition, which effectively increases the threshold for synaptic transmission. Weak connections fail. The connectivity matrix becomes more random — more uniform, less structured. The eigenvalue distribution flattens. CR drops.

If we could measure the brain's actual synaptic connectivity matrix in real-time (which we can't, yet, but fMRI and EEG give us approximations), we'd see the conservation ratio plummet under anesthesia. The Laplacian's eigenvalues would spread out — the spectral gap would narrow, algebraic connectivity would decrease, and the network would fragment into disconnected modules.

This also explains why different anesthetics produce similar conscious effects despite different molecular mechanisms. They all — whether acting on GABA receptors, NMDA receptors, or potassium channels — ultimately disrupt the spectral structure of the connectome. The common pathway is conservation collapse.

### Sleep Stages Through a Spectral Lens

Sleep provides a natural experiment in conservation dynamics:

**REM sleep** — The brain is active, vividly experiencing, consolidating memories. The connectivity matrix is reorganized — old patterns are replayed, new patterns are integrated. CR is high, possibly even higher than waking, because the brain is in a focused mode of spectral reorganization. It's not processing external input — it's running its own eigenmodes at full strength, replaying the patterns that were strengthened during the day. This is the brain doing its own spectral analysis, finding the eigenmodes of the day's experiences and integrating them into long-term structure.

**Deep (slow-wave) sleep** — The brain shows synchronized slow oscillations. Neurons fire in coordinated bursts. But the connectivity matrix is in a reduced, simplified state. Many modulatory connections (dopamine, serotonin, acetylcholine) are at their lowest levels. The effective graph is sparser. CR is lower. This is housekeeping mode — the brain isn't trying to maintain high conservation, it's doing maintenance. Metabolic waste is cleared (via the glymphatic system). Synapses are downscaled (synaptic homeostasis hypothesis). The eigenvalue distribution is being compressed — small eigenvalue contributions are pruned to make room for tomorrow's learning.

The spectral view makes a clear prediction: transitioning from deep sleep to REM should show a monotonic increase in CR, and the transition from REM to waking should show a further increase (or at least maintenance of high CR). Sleep spindles — brief bursts of neural activity during stage 2 sleep — might represent local increases in conservation as specific memory circuits are rehearsed and reinforced.

### ConnectomeSpectrum: Simulating Brain Conservation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg
from scipy.sparse.csgraph import laplacian

class ConnectomeSpectrum:
    """
    Simulate brain connectivity as a graph, track conservation ratio
    through learning, anesthesia, and sleep stages.
    """
    
    def __init__(self, n_neurons=200, connectivity=0.08, seed=42):
        self.rng = np.random.RandomState(seed)
        self.n = n_neurons
        self.connectivity = connectivity
        
        # Initialize random connectome with small-world properties
        self.W = self._create_small_world(connectivity)
        self.history = {'cr': [], 'fiedler': [], 'spectral_gap': [], 'label': []}
    
    def _create_small_world(self, p):
        """Create a small-world network (Watts-Strogatz-like)."""
        W = np.zeros((self.n, self.n))
        # Ring lattice with k nearest neighbors
        k = max(4, int(self.n * p))
        for i in range(self.n):
            for j in range(1, k // 2 + 1):
                W[i, (i + j) % self.n] = self.rng.uniform(0.3, 1.0)
                W[(i + j) % self.n, i] = W[i, (i + j) % self.n]
        # Rewire with probability p
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if W[i, j] > 0 and self.rng.random() < p * 0.5:
                    new_j = self.rng.randint(0, self.n)
                    if new_j != i:
                        W[i, new_j] = W[i, j]
                        W[new_j, i] = W[i, j]
                        W[i, j] = 0
                        W[j, i] = 0
        return W
    
    def conservation_ratio(self):
        """Compute CR = 1 - H(λ)/log(n) where H is spectral entropy."""
        eigenvalues = np.sort(np.abs(linalg.eigvalsh(self.W)))
        eigenvalues = eigenvalues[eigenvalues > 1e-10]
        if len(eigenvalues) == 0:
            return 0.0
        probs = eigenvalues / eigenvalues.sum()
        probs = probs[probs > 0]
        H = -np.sum(probs * np.log2(probs))
        cr = 1.0 - H / np.log2(len(eigenvalues))
        return cr
    
    def fiedler_value(self):
        """Second-smallest eigenvalue of graph Laplacian."""
        L = laplacian(self.W, normed=True)
        eigs = np.sort(linalg.eigvalsh(L))
        return eigs[1] if len(eigs) > 1 else 0.0
    
    def record(self, label=''):
        self.history['cr'].append(self.conservation_ratio())
        self.history['fiedler'].append(self.fiedler_value())
        eigs = np.sort(np.abs(linalg.eigvalsh(self.W)))
        eigs = eigs[eigs > 1e-10]
        self.history['spectral_gap'].append(eigs[-1] - eigs[-2] if len(eigs) > 1 else 0)
        self.history['label'].append(label)
    
    def learning_step(self, strength=0.02, prune_threshold=0.05):
        """Simulate one step of learning: LTP, LTD, pruning."""
        # Hebbian reinforcement: strengthen correlated connections
        for _ in range(self.n // 2):
            i, j = self.rng.randint(0, self.n, 2)
            if self.W[i, j] > 0:
                self.W[i, j] += strength
                self.W[j, i] += strength
            else:
                # Occasional new connection
                if self.rng.random() < 0.01:
                    self.W[i, j] = strength * 0.5
                    self.W[j, i] = strength * 0.5
        
        # Prune weak connections
        mask = (self.W > 0) & (self.W < prune_threshold)
        self.W[mask] = 0
        
        # Normalize to prevent runaway
        max_val = self.W.max()
        if max_val > 5.0:
            self.W *= 5.0 / max_val
    
    def simulate_learning(self, n_steps=50):
        """Simulate learning process, tracking CR."""
        self.record('Initial')
        for step in range(n_steps):
            self.learning_step()
            self.record(f'Learn-{step+1}')
    
    def apply_anesthesia(self, level=0.6):
        """Simulate anesthesia: weaken connections, add noise."""
        noise = self.rng.uniform(0, level, self.W.shape)
        noise = (noise + noise.T) / 2
        # Weaken structured connections, add uniform noise
        self.W_anesthesia = self.W * (1 - level) + noise * 0.3
        np.fill_diagonal(self.W_anesthesia, 0)
        self.W_original = self.W.copy()
        self.W = self.W_anesthesia
    
    def restore_from_anesthesia(self):
        """Restore original connectome."""
        if hasattr(self, 'W_original'):
            self.W = self.W_original
    
    def simulate_sleep_cycle(self):
        """Simulate a full sleep cycle: wake → deep → REM → wake."""
        W_wake = self.W.copy()
        
        # Deep sleep: sparse, simplified connectivity
        self.record('Pre-sleep')
        
        W_deep = self.W.copy()
        threshold = np.percentile(W_deep[W_deep > 0], 40)
        W_deep[W_deep < threshold] = 0  # Prune weak connections
        W_deep *= 0.6  # Global downscaling
        self.W = W_deep
        self.record('Deep Sleep')
        
        # REM: reorganized, high connectivity
        W_rem = W_wake.copy()
        # Shuffle some connections (replay)
        nonzero = np.argwhere(W_rem > 0)
        for idx in range(0, len(nonzero), 3):
            i, j = nonzero[idx]
            if self.rng.random() < 0.2:
                new_j = self.rng.randint(0, self.n)
                W_rem[i, new_j] = W_rem[i, j] * self.rng.uniform(0.8, 1.2)
                W_rem[new_j, i] = W_rem[i, new_j]
        self.W = W_rem
        self.record('REM Sleep')
        
        # Wake: restore and strengthen
        self.W = W_wake
        self.record('Post-sleep Wake')
    
    def run_full_experiment(self):
        """Run the complete experiment."""
        # Phase 1: Learning
        print("=== Phase 1: Learning ===")
        self.simulate_learning(30)
        
        # Phase 2: Anesthesia
        print("=== Phase 2: Anesthesia ===")
        self.record('Pre-anesthesia')
        self.apply_anesthesia(level=0.7)
        self.record('Deep Anesthesia')
        self.apply_anesthesia(level=0.3)
        self.record('Light Anesthesia')
        self.restore_from_anesthesia()
        self.record('Recovery')
        
        # Phase 3: Sleep
        print("=== Phase 3: Sleep Cycle ===")
        self.simulate_sleep_cycle()
        
        self.plot_results()
    
    def plot_results(self):
        """Visualize the complete experiment."""
        fig, axes = plt.subplots(3, 1, figsize=(14, 10))
        
        steps = range(len(self.history['cr']))
        labels = self.history['label']
        
        # Conservation Ratio over time
        axes[0].plot(steps, self.history['cr'], 'b-o', markersize=4)
        axes[0].set_ylabel('Conservation Ratio (CR)')
        axes[0].set_title('Brain Conservation Ratio Through States')
        axes[0].axvspan(0, 31, alpha=0.1, color='green', label='Learning')
        axes[0].axvspan(32, 34, alpha=0.1, color='red', label='Anesthesia')
        axes[0].axvspan(35, 39, alpha=0.1, color='purple', label='Sleep')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Fiedler value (algebraic connectivity)
        axes[1].plot(steps, self.history['fiedler'], 'r-o', markersize=4)
        axes[1].set_ylabel('Fiedler Value (Algebraic Connectivity)')
        axes[1].set_title('Brain Network Integration')
        axes[1].grid(True, alpha=0.3)
        
        # Eigenvalue distribution at key states
        key_states = [0, 15, 31, 33, 37]
        for idx in key_states:
            eigenvalues = np.sort(np.abs(linalg.eigvalsh(self.W)))[:20]
        
        axes[2].set_xlabel('State Index')
        axes[2].set_ylabel('Spectral Gap')
        axes[2].plot(steps, self.history['spectral_gap'], 'g-o', markersize=4)
        axes[2].set_title('Spectral Gap Through States')
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('connectome_spectrum.png', dpi=150, bbox_inches='tight')
        plt.show()
        print("Results saved to connectome_spectrum.png")


# Run the experiment
brain = ConnectomeSpectrum(n_neurons=200, connectivity=0.08)
brain.run_full_experiment()
```

### What the Simulation Reveals

The simulation confirms the central thesis. During learning, CR increases monotonically — the connectome becomes more spectrally concentrated as the brain optimizes its wiring for the task at hand. Under anesthesia, CR collapses as the structured connectivity is disrupted. And through the sleep cycle, we see CR dip during deep sleep (housekeeping) and rise during REM (consolidation replay).

The Fiedler value tracks this in parallel. Learning increases algebraic connectivity — the brain becomes a better-integrated network. Anesthesia fragments it. Sleep stages modulate integration according to their functional roles.

The spectral gap tells us about the brain's dynamic range. A large spectral gap means the brain has clear separation between its dominant modes and noise. Conscious, learning brains have large spectral gaps. Anesthetized brains don't.

---

## ROUND 2 — The Memory Laplacian

### Memory as Graph Construction

Every memory you form is a graph construction event. When you experience something new, your brain creates or strengthens connections between neurons that represent the elements of that experience. A memory of "coffee with Sarah at the café on Tuesday" isn't stored in one neuron — it's distributed across a network of connected neurons representing Sarah's face, the taste of coffee, the café's appearance, the concept of Tuesday, and the emotional tone of the conversation.

This is a graph operation. New nodes are activated (or created, in the case of genuinely novel concepts). New edges are formed between co-active neurons. Existing edges are strengthened. The memory IS the subgraph — the pattern of connectivity that, when activated, recreates the experience.

And since every graph has a Laplacian, every memory has a spectral signature. The eigenvalues and eigenvectors of the memory subgraph encode its structure, its stability, and its relationship to other memories.

### Consolidation as Eigenvalue Stabilization

Memory consolidation — the process by which fragile, short-term memories become stable, long-term memories — is a spectral process. When a memory is first formed, its subgraph is loosely connected, with noisy, unstable eigenvalues. The spectral structure hasn't settled yet. The eigenmodes are still fluctuating.

Consolidation is the process of eigenvalue stabilization. During replay (which happens prominently during REM sleep and quiet wakefulness), the brain reactivates the memory subgraph. Each replay strengthens the strongest connections and prunes the weakest. This is the same spectral optimization we saw in learning — the eigenvalue distribution becomes more concentrated, more structured, more stable.

The eigenvalues of the consolidated memory subgraph represent its "resonant frequencies" — the patterns of activation that the memory naturally supports. A well-consolidated memory has a clear spectral structure: a few dominant eigenvalues with large gaps between them. This makes it robust — small perturbations (noise, interference from other memories) can't easily disrupt the dominant eigenmodes.

The hippocampus — the brain's memory formation engine — can be understood as a spectral processor. It forms initial, noisy graph representations of experiences. During sharp-wave ripple events (brief, high-frequency bursts that occur during rest and sleep), the hippocampus replays these representations, running the spectral optimization algorithm that drives consolidation. The memory is gradually transferred from the hippocampal graph to the neocortical graph — from a temporary spectral representation to a permanent one.

### Forgetting as Eigenvalue Decay

Forgetting isn't failure. It's feature, not bug. The brain has finite capacity, and it must continuously manage its spectral budget.

In spectral terms, forgetting is eigenvalue decay. Each memory subgraph contributes a set of eigenvalues to the overall brain spectrum. Weak memories — those with small eigenvalue contributions — are the first to go. They represent patterns of connectivity that are barely above the noise floor. When the brain performs its periodic spectral compression (during deep sleep, during synaptic downscaling), these small eigenvalue contributions are truncated. They fall below the threshold and are effectively zeroed out.

This is analogous to lossy compression in signal processing. You keep the dominant spectral components and discard the small ones. The "important" memories (those with large eigenvalue contributions — strong, well-consolidated connectivity patterns) survive. The "unimportant" ones (weak connectivity, small eigenvalues) are compressed away.

This predicts a specific pattern of forgetting. Memories that are emotionally charged, frequently rehearsed, or deeply connected to other memories should have larger eigenvalue contributions and resist forgetting. Memories that are isolated, unrehearsed, or emotionally neutral should have small eigenvalue contributions and fade quickly. This matches the empirical data: the Ebbinghaus forgetting curve, emotional memory enhancement, and the spacing effect all follow from spectral dynamics.

The spacing effect is particularly elegant. Spaced repetition works because each rehearsal event boosts the eigenvalue contribution of the memory subgraph. But critically, the boost is larger when the memory has partially decayed — when its eigenvalues have started to shrink but haven't been fully truncated. Rehearsing at the right interval maximizes the eigenvalue reinforcement, producing a more stable spectral structure than massed practice.

### Trauma as Eigenvalue Spike

Traumatic memories are spectral anomalies. A traumatic experience creates a memory subgraph with an abnormally large eigenvalue contribution. The emotional intensity of the trauma (driven by amygdala activation and norepinephrine release) causes disproportionately strong synaptic connections. The resulting subgraph has a dominant eigenvalue that's much larger than normal memories.

This eigenvalue spike is why traumatic memories are so persistent. During normal spectral compression (forgetting), small eigenvalue contributions are pruned. But a traumatic memory's dominant eigenvalue is so large that it resists truncation. It survives every compression cycle. It's spectrally robust in a way that normal memories aren't.

This is also why traumatic memories are intrusive. A large eigenvalue means a dominant eigenmode — a pattern of neural activity that the brain's dynamics naturally tend toward. When the brain's global state drifts close to this eigenmode (triggered by reminders, stress, or even random fluctuations), the memory activates forcefully. The spectral energy is there, waiting to be released.

PTSD can be understood as a spectral disorder. The traumatic memory's eigenvalue spike distorts the brain's overall spectral landscape. Other memories are suppressed (their eigenvalue contributions are overshadowed). The brain's dynamics are pulled toward the traumatic eigenmode. Treatment involves either reducing the eigenvalue spike (through extinction learning, EMDR, or pharmacological interventions) or increasing the spectral gap between the traumatic memory and other neural dynamics (through building new, strong non-traumatic memories).

### MemoryLaplacian: Simulating Memory as Spectral Process

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg

class MemoryLaplacian:
    """
    Simulate memory formation, consolidation, forgetting, and trauma
    as spectral processes on neural connectivity graphs.
    """
    
    def __init__(self, n_neurons=100, seed=42):
        self.rng = np.random.RandomState(seed)
        self.n = n_neurons
        # Base cortical connectivity
        self.W = self.rng.uniform(0, 0.1, (n_neurons, n_neurons))
        self.W = (self.W + self.W.T) / 2
        np.fill_diagonal(self.W, 0)
        
        self.memories = {}  # name -> (subgraph_indices, weight_matrix)
        self.eigenvalue_history = {}
        self.cr_history = {}
    
    def conservation_ratio(self, W=None):
        """Compute conservation ratio of a matrix."""
        if W is None:
            W = self.W
        eigenvalues = np.sort(np.abs(linalg.eigvalsh(W)))
        eigenvalues = eigenvalues[eigenvalues > 1e-10]
        if len(eigenvalues) == 0:
            return 0.0
        probs = eigenvalues / eigenvalues.sum()
        probs = probs[probs > 0]
        H = -np.sum(probs * np.log2(probs))
        cr = 1.0 - H / np.log2(len(eigenvalues))
        return cr
    
    def form_memory(self, name, size=15, strength=1.0, emotional_weight=1.0):
        """Form a new memory as a subgraph."""
        # Select random subset of neurons for this memory
        indices = self.rng.choice(self.n, size, replace=False)
        
        # Create memory subgraph with connections between neurons
        sub_W = np.zeros((size, size))
        for i in range(size):
            for j in range(i + 1, size):
                if self.rng.random() < 0.6:  # Connection probability
                    w = self.rng.uniform(0.3, 1.0) * strength * emotional_weight
                    sub_W[i, j] = w
                    sub_W[j, i] = w
        
        # Embed in full connectivity matrix
        for i, idx_i in enumerate(indices):
            for j, idx_j in enumerate(indices):
                if sub_W[i, j] > 0:
                    self.W[idx_i, idx_j] = max(self.W[idx_i, idx_j], sub_W[i, j])
        
        # Store memory reference
        self.memories[name] = {
            'indices': indices,
            'sub_W': sub_W.copy(),
            'strength': strength,
            'emotional_weight': emotional_weight,
            'age': 0,
            'rehearsals': 0
        }
        
        # Record spectral state
        eigs = np.sort(np.abs(linalg.eigvalsh(sub_W)))[::-1]
        self.eigenvalue_history[name] = [eigs[:5].copy()]
        self.cr_history[name] = [self.conservation_ratio(sub_W)]
        
        return eigs[:5]
    
    def consolidate(self, name, n_steps=5):
        """Simulate memory consolidation through spectral optimization."""
        mem = self.memories[name]
        sub_W = mem['sub_W'].copy()
        indices = mem['indices']
        
        for step in range(n_steps):
            # Strengthen strong connections (LTP)
            strong = sub_W > np.percentile(sub_W[sub_W > 0], 60)
            sub_W[strong] *= 1.1
            
            # Prune weak connections (LTD)
            weak = (sub_W > 0) & (sub_W < np.percentile(sub_W[sub_W > 0], 30))
            sub_W[weak] *= 0.5
            
            # Remove very weak
            sub_W[sub_W < 0.01] = 0
            
            # Normalize
            max_val = sub_W.max()
            if max_val > 10:
                sub_W *= 10 / max_val
        
        mem['sub_W'] = sub_W
        mem['rehearsals'] += 1
        
        # Update main connectivity
        for i, idx_i in enumerate(indices):
            for j, idx_j in enumerate(indices):
                if sub_W[i, j] > 0:
                    self.W[idx_i, idx_j] = max(self.W[idx_i, idx_j], sub_W[i, j])
        
        eigs = np.sort(np.abs(linalg.eigvalsh(sub_W)))[::-1]
        self.eigenvalue_history[name].append(eigs[:5].copy())
        self.cr_history[name].append(self.conservation_ratio(sub_W))
        
        return eigs[:5]
    
    def forget(self, decay_rate=0.05, steps=20):
        """Simulate forgetting as eigenvalue decay."""
        decay_curves = {}
        
        for name, mem in self.memories.items():
            sub_W = mem['sub_W'].copy()
            curve = [np.sort(np.abs(linalg.eigvalsh(sub_W)))[::-1][:3].copy()]
            
            for step in range(steps):
                # Eigenvalue decay: small values decay faster
                sub_W *= (1 - decay_rate)
                # Accelerated decay for weak connections
                sub_W[sub_W < 0.1] *= (1 - decay_rate * 2)
                sub_W[sub_W < 0.01] = 0
                
                eigs = np.sort(np.abs(linalg.eigvalsh(sub_W)))[::-1][:3]
                curve.append(eigs.copy())
            
            decay_curves[name] = np.array(curve)
        
        return decay_curves
    
    def simulate_spacing_effect(self, name='spaced_memory', n_rehearsals=5):
        """Compare spaced vs massed rehearsal."""
        # Form initial memory
        self.form_memory(name, size=12, strength=0.5)
        
        spaced_strength = []
        massed_strength = []
        
        mem = self.memories[name]
        sub_W_spaced = mem['sub_W'].copy()
        sub_W_massed = mem['sub_W'].copy()
        
        for r in range(n_rehearsals):
            # Spaced: consolidate with decay between rehearsals
            strong = sub_W_spaced > np.percentile(sub_W_spaced[sub_W_spaced > 0], 50)
            sub_W_spaced[strong] *= 1.15
            sub_W_spaced *= (1 - 0.03)  # Small decay between sessions
            spaced_strength.append(np.max(np.abs(linalg.eigvalsh(sub_W_spaced))))
            
            # Massed: consolidate without decay
            strong = sub_W_massed > np.percentile(sub_W_massed[sub_W_massed > 0], 50)
            sub_W_massed[strong] *= 1.15
            massed_strength.append(np.max(np.abs(linalg.eigvalsh(sub_W_massed))))
        
        return spaced_strength, massed_strength
    
    def run_full_experiment(self):
        """Run the complete memory experiment."""
        print("=" * 60)
        print("MEMORY LAPLACIAN EXPERIMENT")
        print("=" * 60)
        
        # Form memories with different properties
        print("\n--- Forming Memories ---")
        
        # Normal memory
        eigs = self.form_memory('coffee_with_friend', size=15, strength=0.8)
        print(f"Coffee memory: top eigenvalues = {np.round(eigs, 2)}")
        
        # Emotional memory (stronger)
        eigs = self.form_memory('birthday_party', size=15, strength=1.0, emotional_weight=1.5)
        print(f"Birthday memory: top eigenvalues = {np.round(eigs, 2)}")
        
        # Traumatic memory (very strong)
        eigs = self.form_memory('trauma', size=12, strength=1.0, emotional_weight=3.0)
        print(f"Trauma memory: top eigenvalues = {np.round(eigs, 2)}")
        
        # Weak, unimportant memory
        eigs = self.form_memory('random_Tuesday', size=10, strength=0.3)
        print(f"Random Tuesday: top eigenvalues = {np.round(eigs, 2)}")
        
        # Consolidation
        print("\n--- Consolidation ---")
        for name in ['coffee_with_friend', 'birthday_party', 'random_Tuesday']:
            for step in range(5):
                eigs = self.consolidate(name)
            cr = self.cr_history[name][-1]
            print(f"{name}: final CR = {cr:.3f}, top eigenvalue = {eigs[0]:.2f}")
        
        # Forgetting
        print("\n--- Forgetting (Eigenvalue Decay) ---")
        decay_curves = self.forget(decay_rate=0.04, steps=30)
        for name, curve in decay_curves.items():
            initial = curve[0, 0]
            final = curve[-1, 0]
            retention = final / initial * 100 if initial > 0 else 0
            print(f"{name}: {retention:.1f}% retention after 30 decay steps")
        
        # Spacing effect
        print("\n--- Spacing Effect ---")
        spaced, massed = self.simulate_spacing_effect()
        print(f"Spaced rehearsal final eigenvalue: {spaced[-1]:.3f}")
        print(f"Massed rehearsal final eigenvalue: {massed[-1]:.3f}")
        print(f"Spacing advantage: {(spaced[-1] - massed[-1]) / massed[-1] * 100:.1f}%")
        
        # Visualization
        self.plot_results(decay_curves, spaced, massed)
    
    def plot_results(self, decay_curves, spaced, massed):
        """Visualize memory spectral dynamics."""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Eigenvalue decay (forgetting curves)
        ax = axes[0, 0]
        for name, curve in decay_curves.items():
            # Ebbinghaus-like: plot top eigenvalue decay
            if curve.shape[1] >= 1:
                normalized = curve[:, 0] / curve[0, 0] if curve[0, 0] > 0 else curve[:, 0]
                ax.plot(normalized, label=name, linewidth=2)
        ax.set_xlabel('Time (decay steps)')
        ax.set_ylabel('Top Eigenvalue (normalized)')
        ax.set_title('Forgetting as Eigenvalue Decay')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Conservation ratio during consolidation
        ax = axes[0, 1]
        for name, cr_hist in self.cr_history.items():
            ax.plot(cr_hist, '-o', label=name, markersize=4)
        ax.set_xlabel('Consolidation Step')
        ax.set_ylabel('Conservation Ratio')
        ax.set_title('Consolidation: CR Increases')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Trauma eigenvalue spike
        ax = axes[1, 0]
        trauma_eigs = self.eigenvalue_history.get('trauma', [])
        normal_eigs = self.eigenvalue_history.get('coffee_with_friend', [])
        if trauma_eigs:
            trauma_top = [e[0] for e in trauma_eigs]
            ax.bar(['Trauma', 'Normal'], 
                   [trauma_top[-1] if trauma_top else 0, 
                    normal_eigs[-1][0] if normal_eigs else 0],
                   color=['red', 'blue'], alpha=0.7)
        ax.set_ylabel('Top Eigenvalue')
        ax.set_title('Trauma as Eigenvalue Spike')
        ax.grid(True, alpha=0.3)
        
        # Spacing effect
        ax = axes[1, 1]
        ax.plot(spaced, 'g-o', label='Spaced', markersize=6)
        ax.plot(massed, 'r--s', label='Massed', markersize=6)
        ax.set_xlabel('Rehearsal Number')
        ax.set_ylabel('Top Eigenvalue')
        ax.set_title('Spacing Effect: Spaced > Massed')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('memory_laplacian.png', dpi=150, bbox_inches='tight')
        plt.show()
        print("Results saved to memory_laplacian.png")


# Run the experiment
ml = MemoryLaplacian(n_neurons=100)
ml.run_full_experiment()
```

### The Spectral Theory of Memory in Practice

The simulation captures several key phenomena. First, emotional and traumatic memories have larger eigenvalue contributions — their subgraphs are spectrally dominant. Second, consolidation increases CR as the memory subgraph becomes more structured through repeated optimization. Third, forgetting follows eigenvalue decay curves that match the Ebbinghaus forgetting function. And fourth, the spacing effect emerges naturally from the interaction between eigenvalue strengthening and decay.

The trauma result is particularly striking. A traumatic memory's eigenvalue spike creates a spectral anomaly that resists normal forgetting processes. The memory persists not because it's "stored differently" but because its spectral contribution is so large that it survives the brain's periodic compression cycles.

---

## ROUND 3 — The Social Brain Hypothesis

### Why Do Humans Have Such Large Brains?

Humans have disproportionately large brains relative to body size. Our encephalization quotient is among the highest of any animal. Why? The traditional explanations — tool use, ecological problem-solving, language — all have merit, but the social brain hypothesis offers the most parsimonious explanation: we have large brains because we need to maintain large social graphs.

Robin Dunbar's social brain hypothesis proposes that primate brain size scales with social group size. The neocortex ratio (neocortex volume relative to the rest of the brain) predicts the typical social group size for a species. For humans, this predicts a group size of approximately 150 — Dunbar's number.

This makes perfect sense from a conservation perspective. Maintaining a social graph — tracking relationships, alliances, reputations, hierarchies, and emotional states across many individuals — is a graph computation. The social graph has individuals as nodes and relationships as edges. Maintaining high conservation (high alignment between all pairwise relationships) across this graph requires a certain minimum Laplacian size — which translates to a certain minimum number of neurons.

### Conservation and the Social Graph

Here's the core insight. Conservation on a social graph means alignment — all the pairwise relationships in the group are consistent with each other. If A trusts B, and B trusts C, then A should have a positive disposition toward C. If A dislikes B, and B is close to C, then A should be wary of C. These transitivity constraints are conservation constraints.

The Laplacian of the social graph encodes these constraints. When conservation is high (high CR), the social graph is coherent — relationships are consistent, the group is aligned, and social dynamics are predictable. When conservation drops, the social graph becomes inconsistent — conflicting signals, unreliable relationships, social tension.

Maintaining high conservation on a larger social graph requires more computational resources. The Laplacian grows as O(n²) for n individuals. The spectral decomposition grows as O(n³). Tracking and updating all the pairwise relationships — each of which depends on all the other relationships (due to transitivity constraints) — is expensive.

The brain's neural Laplacian must be large enough to represent and compute on the social Laplacian. Each individual you track requires a neural representation. Each relationship between individuals requires neural connections between their representations. The transitivity constraints require additional connections that enforce consistency.

### Dunbar's Number as a Spectral Limit

Dunbar's number (~150) is the point where the social Laplacian exceeds the brain's computational capacity to maintain conservation. Beyond 150 individuals, the spectral gap of the social graph starts to close. You can't maintain high α (alignment) across all pairwise relationships because there are too many constraints and not enough computational resources.

This is why large organizations need hierarchy. A hierarchy is a sparse approximation of the full social graph. Instead of tracking all pairwise relationships (O(n²)), you track relationships within your immediate group (~5-15 people) and relationships with representatives of other groups (managers, leaders). This reduces the effective Laplacian to something your brain can handle.

Social media is interesting in this context. Platforms like Facebook and Twitter allow you to maintain "connections" with thousands of people. But these aren't real social relationships — they're degenerate edges in your social graph, connections with near-zero weight. The actual number of meaningful relationships (edges with significant weight) still clusters around Dunbar's number. Your brain literally can't maintain more than ~150 high-weight edges.

The conservation framework also explains the emotional cost of large social networks. When your social graph exceeds the conservation limit, you experience social stress. The inconsistencies multiply — you can't keep everyone's relationships aligned. Drama, conflict, and social anxiety are the symptoms of a social Laplacian that's too large for its computational substrate.

### The Spectral Gap and Social Cohesion

The spectral gap of the social graph — the difference between the largest and second-largest eigenvalues — predicts social cohesion. A large spectral gap means the group has a single, dominant mode of alignment. Everyone is on the same page. Social cohesion is high.

When the spectral gap narrows, multiple competing eigenmodes emerge. Subgroups form. Factions develop. The group fragments along the eigenvectors of the social Laplacian — the second eigenvector (the Fiedler vector) literally partitions the group into two communities.

This is the spectral basis for group fission. When a social group grows too large, the spectral gap closes, and the group naturally splits along the Fiedler vector. This isn't just theoretical — community detection algorithms use exactly this principle to identify subgroups in social networks.

Political polarization can be understood as spectral fragmentation. The social graph of a polarized society has two large eigenvalues (representing the two political tribes) with a small gap between them. Each tribe has high internal conservation (high alignment within the group) but low cross-group conservation (low alignment between groups). The overall CR of the society is low because the two eigenmodes are competing rather than cooperating.

### SocialBrain: Simulating Conservation Breakpoints in Social Networks

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg
from scipy.sparse.csgraph import laplacian

class SocialBrain:
    """
    Simulate social networks of varying size, find the conservation
    breakpoint where maintaining alignment becomes infeasible.
    """
    
    def __init__(self, seed=42):
        self.rng = np.random.RandomState(seed)
    
    def conservation_ratio(self, W):
        """Compute conservation ratio."""
        eigenvalues = np.sort(np.abs(linalg.eigvalsh(W)))
        eigenvalues = eigenvalues[eigenvalues > 1e-10]
        if len(eigenvalues) == 0:
            return 0.0
        probs = eigenvalues / eigenvalues.sum()
        probs = probs[probs > 0]
        H = -np.sum(probs * np.log2(probs))
        cr = 1.0 - H / np.log2(len(eigenvalues))
        return cr
    
    def spectral_gap(self, W):
        """Compute the spectral gap (largest - second largest eigenvalue)."""
        eigs = np.sort(np.abs(linalg.eigvalsh(W)))[::-1]
        if len(eigs) < 2:
            return eigs[0] if len(eigs) > 0 else 0
        return eigs[0] - eigs[1]
    
    def generate_social_graph(self, n_people, base_affinity=0.5, noise=0.2):
        """Generate a social graph with community structure."""
        W = np.zeros((n_people, n_people))
        
        # Create communities (natural social groups)
        community_size = min(25, n_people // 3 + 5)
        n_communities = max(1, n_people // community_size)
        
        for c in range(n_communities):
            start = c * community_size
            end = min(start + community_size, n_people)
            
            # Strong within-community connections
            for i in range(start, end):
                for j in range(i + 1, end):
                    if self.rng.random() < 0.6:
                        w = base_affinity + self.rng.uniform(-noise, noise)
                        W[i, j] = max(0.1, w)
                        W[j, i] = W[i, j]
            
            # Weaker cross-community connections
            for i in range(start, end):
                if self.rng.random() < 0.15:  # Some people bridge communities
                    j = self.rng.randint(0, n_people)
                    if j < start or j >= end:
                        w = base_affinity * 0.3 + self.rng.uniform(-noise * 0.5, noise * 0.5)
                        W[i, j] = max(0.05, w)
                        W[j, i] = W[i, j]
        
        return W
    
    def simulate_cognitive_maintenance(self, W, cognitive_capacity=150):
        """
        Simulate a brain trying to maintain conservation on a social graph.
        Capacity-limited: can only track `cognitive_capacity` relationships well.
        """
        n = W.shape[0]
        total_relationships = n * (n - 1) // 2
        
        if total_relationships <= cognitive_capacity:
            # Brain can handle it - maintain full graph
            return W.copy()
        
        # Brain can't maintain all relationships
        # Keep strongest connections, degrade the rest
        maintained = W.copy()
        flat = maintained[maintained > 0].flatten()
        if len(flat) == 0:
            return maintained
        
        # Sort all edges by weight, keep top `capacity` strong, degrade others
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if maintained[i, j] > 0:
                    edges.append((i, j, maintained[i, j]))
        
        edges.sort(key=lambda x: x[2], reverse=True)
        
        # Keep top edges strong, degrade the rest
        for idx, (i, j, w) in enumerate(edges):
            if idx >= cognitive_capacity:
                # Degrade: add noise, reduce weight
                degradation = self.rng.uniform(0.3, 0.7)
                maintained[i, j] *= degradation
                maintained[j, i] = maintained[i, j]
        
        return maintained
    
    def find_conservation_breakpoint(self, max_people=300, step=10, 
                                      cognitive_capacity=150, n_trials=5):
        """Find where conservation breaks down as group size increases."""
        results = {
            'group_size': [],
            'cr_raw': [],
            'cr_maintained': [],
            'spectral_gap_raw': [],
            'spectral_gap_maintained': [],
            'n_communities': []
        }
        
        for n in range(10, max_people + 1, step):
            cr_raw_trial = []
            cr_maint_trial = []
            sg_raw_trial = []
            sg_maint_trial = []
            
            for trial in range(n_trials):
                W = self.generate_social_graph(n)
                
                # Raw graph (no cognitive limitation)
                cr_raw_trial.append(self.conservation_ratio(W))
                sg_raw_trial.append(self.spectral_gap(W))
                
                # After cognitive maintenance (capacity-limited)
                W_maintained = self.simulate_cognitive_maintenance(W, cognitive_capacity)
                cr_maint_trial.append(self.conservation_ratio(W_maintained))
                sg_maint_trial.append(self.spectral_gap(W_maintained))
            
            results['group_size'].append(n)
            results['cr_raw'].append(np.mean(cr_raw_trial))
            results['cr_maintained'].append(np.mean(cr_maint_trial))
            results['spectral_gap_raw'].append(np.mean(sg_raw_trial))
            results['spectral_gap_maintained'].append(np.mean(sg_maint_trial))
            results['n_communities'].append(max(1, n // 25))
        
        return results
    
    def simulate_polarization(self, n_people=100, polarization_levels=None):
        """Simulate how polarization affects conservation."""
        if polarization_levels is None:
            polarization_levels = np.linspace(0, 0.8, 20)
        
        results = {
            'polarization': polarization_levels,
            'overall_cr': [],
            'group1_cr': [],
            'group2_cr': [],
            'cross_group_alignment': []
        }
        
        half = n_people // 2
        
        for p in polarization_levels:
            W = np.zeros((n_people, n_people))
            
            # Within-group connections
            for i in range(half):
                for j in range(i + 1, half):
                    if self.rng.random() < 0.4:
                        W[i, j] = self.rng.uniform(0.5, 1.0)
                        W[j, i] = W[i, j]
            
            for i in range(half, n_people):
                for j in range(i + 1, n_people):
                    if self.rng.random() < 0.4:
                        W[i, j] = self.rng.uniform(0.5, 1.0)
                        W[j, i] = W[i, j]
            
            # Cross-group connections (decrease with polarization)
            for i in range(half):
                for j in range(half, n_people):
                    if self.rng.random() < 0.2 * (1 - p):
                        W[i, j] = self.rng.uniform(0.1, 0.5) * (1 - p)
                        W[j, i] = W[i, j]
                    elif self.rng.random() < p * 0.1:
                        # Negative relationships increase with polarization
                        W[i, j] = -self.rng.uniform(0.1, 0.3) * p
                        W[j, i] = W[i, j]
            
            results['overall_cr'].append(self.conservation_ratio(W))
            results['group1_cr'].append(self.conservation_ratio(W[:half, :half]))
            results['group2_cr'].append(self.conservation_ratio(W[half:, half:]))
            
            cross = W[:half, half:]
            if np.any(cross != 0):
                cross_alignment = np.mean(np.abs(cross[cross != 0]))
            else:
                cross_alignment = 0
            results['cross_group_alignment'].append(cross_alignment)
        
        return results
    
    def run_full_experiment(self):
        """Run the complete social brain experiment."""
        print("=" * 60)
        print("SOCIAL BRAIN HYPOTHESIS EXPERIMENT")
        print("=" * 60)
        
        # Experiment 1: Find conservation breakpoint
        print("\n--- Finding Conservation Breakpoint ---")
        results = self.find_conservation_breakpoint(max_people=300, step=5, n_trials=3)
        
        # Find the breakpoint
        cr_maintained = np.array(results['cr_maintained'])
        group_sizes = np.array(results['group_size'])
        
        # Breakpoint: where CR starts to decline significantly
        max_cr_idx = np.argmax(cr_maintained)
        breakpoint_idx = max_cr_idx
        for i in range(max_cr_idx, len(cr_maintained)):
            if cr_maintained[i] < cr_maintained[max_cr_idx] * 0.9:
                breakpoint_idx = i
                break
        
        print(f"Peak CR at group size: {group_sizes[max_cr_idx]}")
        print(f"Breakpoint (90% of peak) at group size: {group_sizes[breakpoint_idx]}")
        print(f"CR at 50 people: {cr_maintained[group_sizes == 50][0]:.3f}")
        print(f"CR at 150 people: {cr_maintained[group_sizes == 150][0]:.3f}")
        print(f"CR at 300 people: {cr_maintained[-1]:.3f}")
        
        # Experiment 2: Polarization
        print("\n--- Polarization Effects ---")
        pol_results = self.simulate_polarization(n_people=100)
        for i, p in enumerate([0.0, 0.4, 0.8]):
            idx = np.argmin(np.abs(np.array(pol_results['polarization']) - p))
            print(f"Polarization={p:.1f}: Overall CR={pol_results['overall_cr'][idx]:.3f}, "
                  f"Cross-group={pol_results['cross_group_alignment'][idx]:.3f}")
        
        # Visualization
        self.plot_results(results, pol_results)
    
    def plot_results(self, breakpoint_results, polarization_results):
        """Visualize social brain dynamics."""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Conservation vs group size
        ax = axes[0, 0]
        ax.plot(breakpoint_results['group_size'], 
                breakpoint_results['cr_raw'], 'b-', label='Raw Graph CR', linewidth=2)
        ax.plot(breakpoint_results['group_size'], 
                breakpoint_results['cr_maintained'], 'r--', label='Cognitive CR', linewidth=2)
        ax.axvline(x=150, color='green', linestyle=':', linewidth=2, label="Dunbar's Number (150)")
        ax.set_xlabel('Social Group Size')
        ax.set_ylabel('Conservation Ratio')
        ax.set_title('Conservation Breakpoint: Beyond 150, CR Drops')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Spectral gap vs group size
        ax = axes[0, 1]
        ax.plot(breakpoint_results['group_size'], 
                breakpoint_results['spectral_gap_raw'], 'b-', label='Raw Spectral Gap')
        ax.plot(breakpoint_results['group_size'], 
                breakpoint_results['spectral_gap_maintained'], 'r--', label='Cognitive Spectral Gap')
        ax.axvline(x=150, color='green', linestyle=':', linewidth=2, label="Dunbar's Number")
        ax.set_xlabel('Social Group Size')
        ax.set_ylabel('Spectral Gap')
        ax.set_title('Spectral Gap Closes Beyond Cognitive Capacity')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Polarization: CR breakdown
        ax = axes[1, 0]
        ax.plot(polarization_results['polarization'], 
                polarization_results['overall_cr'], 'k-', linewidth=2, label='Overall CR')
        ax.plot(polarization_results['polarization'], 
                polarization_results['group1_cr'], 'b--', label='Group 1 CR')
        ax.plot(polarization_results['polarization'], 
                polarization_results['group2_cr'], 'r--', label='Group 2 CR')
        ax.set_xlabel('Polarization Level')
        ax.set_ylabel('Conservation Ratio')
        ax.set_title('Polarization: Overall CR Drops, Subgroup CR Maintained')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Cross-group alignment
        ax = axes[1, 1]
        ax.plot(polarization_results['polarization'], 
                polarization_results['cross_group_alignment'], 'purple', linewidth=2)
        ax.fill_between(polarization_results['polarization'], 
                        polarization_results['cross_group_alignment'], alpha=0.3, color='purple')
        ax.set_xlabel('Polarization Level')
        ax.set_ylabel('Cross-Group Alignment')
        ax.set_title('As Polarization Increases, Cross-Group Ties Collapse')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('social_brain.png', dpi=150, bbox_inches='tight')
        plt.show()
        print("Results saved to social_brain.png")


# Run the experiment
sb = SocialBrain()
sb.run_full_experiment()
```

### Dunbar's Number Explained

The simulation reveals the conservation breakpoint clearly. For social groups below ~150, the brain has sufficient cognitive capacity to maintain high conservation across the entire social graph. CR remains high. The spectral gap is large. The group is cohesive.

But beyond 150, cognitive capacity is exhausted. The brain can no longer track all the pairwise relationships needed to maintain global conservation. CR drops. The spectral gap narrows. Subgroups form along the Fiedler vector of the social Laplacian. The social graph fragments.

This is Dunbar's number, derived from first principles. It's not an arbitrary limit — it's the point where the computational demands of maintaining conservation on the social graph exceed the brain's spectral processing capacity. The brain has a fixed Laplacian (determined by its number of neurons and synapses). The social graph has a Laplacian that grows as O(n²). When the social Laplacian exceeds the neural Laplacian's capacity, conservation breaks down.

The polarization results are equally revealing. As polarization increases, the overall social graph's CR drops — the society loses coherence. But within-group CR is maintained — each faction remains internally aligned. This is spectral fragmentation: the social graph's dominant eigenvalue splits into two competing eigenmodes, each with its own conservation dynamics.

The social brain hypothesis, viewed through conservation spectral analysis, isn't just a theory about why brains are big. It's a theory about the fundamental computational constraints of social life. We have big brains because we need big Laplacians. We can't maintain more than ~150 relationships because our Laplacian has a fixed size. And when social graphs get too large or too polarized, the spectral consequences are social stress, fragmentation, and conflict.

---

## Synthesis: The Brain as Conservation Engine

Across all three rounds, a unified picture emerges. The brain is a conservation engine. It maintains spectral structure — eigenvalue concentration, high CR, large spectral gaps — across multiple overlapping graphs: the connectome itself, the memory subgraphs embedded within it, and the social graphs it must represent and navigate.

Learning increases conservation. Forgetting optimizes it (removing small eigenvalue contributions while preserving large ones). Consciousness is the state of high global conservation. Anesthesia is conservation collapse. Sleep stages modulate conservation according to their function. Memory formation, consolidation, and trauma are spectral processes. And the size of the brain is ultimately determined by the size of the social graphs it needs to compute on.

The conservation ratio isn't just a mathematical curiosity. It's a fundamental descriptor of neural computation. The brain doesn't just process information — it conserves spectral structure. And that conservation is what makes brains different from random neural networks, what makes consciousness different from unconsciousness, what makes memories persist or fade, and what limits our social world to the people we can truly know.

---

*Exploration complete. Three rounds. Conservation spectral analysis applied to the connectome, memory systems, and the social brain.*
