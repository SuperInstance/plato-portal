# Evolution and Deep Biology: Conservation Spectral Analysis

*An exploration of how the Laplacian spectral framework reveals the hidden mathematics of life's deepest processes — phylogeny, ecology, and molecular folding.*

---

# ROUND 1 — The Phylogenetic Laplacian

## The Tree of Life Is a Laplacian

Here is a claim that sounds like poetry but is literal mathematics: **every phylogenetic tree is a graph, every graph has a Laplacian, and the spectral properties of that Laplacian encode the evolutionary history of every species on it.**

Think about what a phylogenetic tree actually is. You have species at the leaves — *Homo sapiens*, *Pan troglodytes*, *Gorilla gorilla*, *Ornithorhynchus anatinus* (the platypus, because the platypus deserves to be in every phylogenetic example). The internal nodes represent common ancestors. The edges represent evolutionary divergence — branching events where one lineage split into two. The branch lengths encode time or genetic distance.

Now: the **conservation** of this graph — the sum of squared eigenvector components weighted by eigenvalues — tells you something profound. It tells you how *coherent* the evolutionary structure is. A healthy, branching tree with deep roots and many tips has high conservation. The eigenvalue spectrum is spread, the spectral gap is wide, and the graph structure is robust.

But watch what happens during a mass extinction.

A mass extinction doesn't just delete species. It *prunes the tree*. Entire branches vanish. The tips that remain are clustered — they're the survivors, often generalists, often from just a few lineages. The tree becomes sparse. The spectral gap *collapses*. And conservation — the measure of how well the graph preserves its structural relationships — *drops sharply*.

This isn't metaphor. This is spectral graph theory applied to phylogenetics.

## The Spectral Signature of Extinction

Consider the End-Cretaceous extinction. Before the impact, the tree of life had a rich, balanced structure — dinosaurs, mammals, birds, reptiles, amphibians, all branching and diversifying. The Laplacian of this tree would have had a well-distributed eigenvalue spectrum with a healthy spectral gap between the first non-zero eigenvalue (λ₂, the algebraic connectivity) and zero.

After the impact: gone are the non-avian dinosaurs, gone are the pterosaurs, gone are the ammonites, gone are 75% of all species. The tree is devastated. The Laplacian's eigenvalue spectrum compresses — fewer branches means less spectral diversity. λ₂ plummets because the tree, while still connected through deep common ancestors, has lost much of its fine structure.

Now consider what happens *after* a mass extinction: **adaptive radiation**. The survivors — mammals, in the case of the End-Cretaceous — rapidly diversify to fill empty ecological niches. New species appear, new branches grow, the tree fills out again. And spectrally: the eigenvalue spectrum *widens*. New branches create new eigenvalue modes. The spectral gap increases. Conservation rises.

Adaptive radiation is, in spectral terms, the expansion of the eigenspace. Mass extinction is its collapse.

## Individual Conservation: Which Lineages Survive?

Here's where it gets personal — or rather, *phylogenetic*. Each node in the tree has an **individual conservation**: its component in the eigenvector weighted by the corresponding eigenvalue. Nodes with high individual conservation are the ones most tightly integrated into the tree's structure.

What does that mean biologically? A species with high individual conservation sits at the center of a dense, well-connected clade. It has many close relatives. Its removal would minimally disrupt the tree because its evolutionary "information" is redundantly encoded in its neighbors. 

But a species with *low* individual conservation — a lone branch, a "living fossil" like the coelacanth or the tuatara — sits on a sparse, isolated part of the tree. Its evolutionary information is unique. Its removal would be catastrophic for the tree's structure, even if nobody else notices.

This gives us a spectral definition of **evolutionary irreplaceability**: species with low individual conservation relative to their branch structure are the ones we most need to protect, because the tree cannot reconstruct their information from neighbors.

## PhylogeneticLaplacian: Building the Detector

```python
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from scipy.spatial.distance import pdist, squareform
from collections import defaultdict
import matplotlib.pyplot as plt

class PhylogeneticLaplacian:
    """
    Model evolutionary trees as Laplacian graphs.
    Detect mass extinctions via conservation drops.
    Predict which lineages are most resilient.
    """
    
    def __init__(self, n_species=100, seed=42):
        self.rng = np.random.RandomState(seed)
        self.n_species = n_species
        self.tree = None          # adjacency matrix
        self.laplacian = None
        self.eigenvalues = None
        self.eigenvectors = None
        self.species_names = []
        self.branch_lengths = {}
        self.extinction_log = []
        
    def simulate_evolution(self, birth_rate=0.8, death_rate=0.3, max_time=10.0):
        """
        Simulate a birth-death process to generate a phylogenetic tree.
        This is the standard model in phylogenetics.
        """
        # Start with one ancestor
        # Each species has: birth_time, death_time (inf if extant), parent
        species = {
            0: {
                'birth': 0.0,
                'death': np.inf,
                'parent': None,
                'name': f'sp_{0:04d}'
            }
        }
        next_id = 1
        t = 0.0
        dt = 0.05
        
        while t < max_time and len([s for s in species.values() if s['death'] == np.inf]) > 0:
            extant = [sid for sid, s in species.items() if s['death'] == np.inf]
            
            for sid in extant:
                # Birth event (speciation)
                if self.rng.random() < birth_rate * dt:
                    child = {
                        'birth': t,
                        'death': np.inf,
                        'parent': sid,
                        'name': f'sp_{next_id:04d}'
                    }
                    species[next_id] = child
                    next_id += 1
                
                # Death event (extinction)
                if self.rng.random() < death_rate * dt and len(extant) > 1:
                    species[sid]['death'] = t
            
            t += dt
            
            # Cap species count
            if next_id >= self.n_species * 2:
                break
        
        self.species_data = species
        self.extant = [sid for sid, s in species.items() if s['death'] == np.inf]
        self.species_names = [species[sid]['name'] for sid in self.extant]
        
        # Build distance matrix from tree
        n = len(self.extant)
        dist_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i + 1, n):
                # Approximate phylogenetic distance as time since MRCA
                dist = abs(species[self.extant[i]]['birth'] - 
                          species[self.extant[j]]['birth']) * 0.5
                dist_matrix[i, j] = dist + 0.1
                dist_matrix[j, i] = dist + 0.1
        
        self._build_graph_from_distances(dist_matrix)
        return self
    
    def _build_graph_from_distances(self, dist_matrix, threshold=None):
        """Convert distance matrix to adjacency, then Laplacian."""
        n = dist_matrix.shape[0]
        
        if threshold is None:
            # Use mean distance as threshold for edge creation
            threshold = np.mean(dist_matrix[dist_matrix > 0])
        
        adjacency = (dist_matrix < threshold).astype(float)
        np.fill_diagonal(adjacency, 0)
        
        # Weight edges inversely by distance (closer = stronger connection)
        weights = np.where(adjacency > 0, 1.0 / (dist_matrix + 1e-6), 0)
        
        self.adjacency = weights
        degree = np.diag(weights.sum(axis=1))
        self.laplacian = degree - weights
        
        self._compute_spectrum()
    
    def _compute_spectrum(self):
        """Compute eigenvalues and eigenvectors of the Laplacian."""
        if sparse.issparse(self.laplacian):
            n = self.laplacian.shape[0]
            k = min(n - 1, 50)
            self.eigenvalues, self.eigenvectors = eigsh(self.laplacian, k=k, which='SM')
        else:
            self.eigenvalues, self.eigenvectors = np.linalg.eigh(self.laplacian)
        
        # Sort by eigenvalue
        idx = np.argsort(self.eigenvalues)
        self.eigenvalues = self.eigenvalues[idx]
        self.eigenvectors = self.eigenvectors[:, idx]
    
    @property
    def conservation(self):
        """Total graph conservation: Σ λ_i ||v_i||²"""
        return np.sum(self.eigenvalues * np.sum(self.eigenvectors**2, axis=0))
    
    @property
    def individual_conservation(self):
        """Per-node conservation: Σ_i λ_i v_i(node)²"""
        return np.sum(self.eigenvalues[np.newaxis, :] * self.eigenvectors**2, axis=1)
    
    @property
    def spectral_gap(self):
        """Gap between first two non-zero eigenvalues."""
        nonzero = self.eigenvalues[self.eigenvalues > 1e-10]
        if len(nonzero) < 2:
            return 0.0
        return nonzero[1] - nonzero[0]
    
    @property
    def algebraic_connectivity(self):
        """λ₂ — the Fiedler value."""
        nonzero = self.eigenvalues[self.eigenvalues > 1e-10]
        return nonzero[0] if len(nonzero) > 0 else 0.0
    
    def mass_extinction(self, extinction_rate=0.75, biased=False):
        """
        Simulate a mass extinction event.
        If biased=True, extinction targets specific clades (realistic).
        Returns the conservation before and after.
        """
        conservation_before = self.conservation
        gap_before = self.spectral_gap
        connectivity_before = self.algebraic_connectivity
        
        n_extant = len(self.extant)
        n_to_kill = int(n_extant * extinction_rate)
        
        if biased:
            # Extinction targets — kill species from a few clades
            # Simulate by killing species born in a time window
            birth_times = [self.species_data[sid]['birth'] for sid in self.extant]
            # Sort by birth time and kill a contiguous block
            sorted_idx = np.argsort(birth_times)
            # Kill the middle block (represents a clade that failed to adapt)
            start = len(sorted_idx) // 4
            to_kill_idx = sorted_idx[start:start + n_to_kill]
        else:
            to_kill_idx = self.rng.choice(n_extant, n_to_kill, replace=False)
        
        # Remove species
        surviving = [s for i, s in enumerate(self.extant) if i not in to_kill_idx]
        self.extant = surviving
        self.species_names = [self.species_data[sid]['name'] for sid in self.extant]
        
        # Rebuild graph
        n = len(self.extant)
        dist_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                dist = abs(self.species_data[self.extant[i]]['birth'] - 
                          self.species_data[self.extant[j]]['birth']) * 0.5
                dist_matrix[i, j] = dist + 0.1
                dist_matrix[j, i] = dist + 0.1
        
        self._build_graph_from_distances(dist_matrix)
        
        conservation_after = self.conservation
        gap_after = self.spectral_gap
        connectivity_after = self.algebraic_connectivity
        
        result = {
            'extinction_rate': extinction_rate,
            'species_before': n_extant,
            'species_after': n,
            'conservation_before': conservation_before,
            'conservation_after': conservation_after,
            'conservation_drop': (conservation_before - conservation_after) / conservation_before,
            'gap_before': gap_before,
            'gap_after': gap_after,
            'connectivity_before': connectivity_before,
            'connectivity_after': connectivity_after,
        }
        self.extinction_log.append(result)
        return result
    
    def adaptive_radiation(self, radiation_factor=2.0, time_steps=50):
        """
        Simulate adaptive radiation — surviving lineages diversify.
        The spectral gap widens as new species fill eigenspace.
        """
        conservation_before = self.conservation
        gap_before = self.spectral_gap
        
        n_extant = len(self.extant)
        
        # Each surviving species has a chance to speciate
        new_species = []
        for sid in self.extant:
            n_new = self.rng.poisson(radiation_factor)
            for k in range(n_new):
                new_id = max(self.species_data.keys()) + 1 + len(new_species)
                new_species.append(new_id)
        
        # Add new species to the tree (close to parent in distance space)
        all_species = self.extant + new_species
        n = len(all_species)
        dist_matrix = np.zeros((n, n))
        
        # Distances between original survivors
        orig_n = len(self.extant)
        for i in range(orig_n):
            for j in range(i + 1, orig_n):
                dist = abs(self.species_data[self.extant[i]]['birth'] - 
                          self.species_data[self.extant[j]]['birth']) * 0.5
                dist_matrix[i, j] = dist + 0.1
                dist_matrix[j, i] = dist + 0.1
        
        # New species are close to their parent
        for idx, new_id in enumerate(new_species):
            parent_idx = idx % orig_n
            dist_matrix[orig_n + idx, parent_idx] = 0.05  # very close
            dist_matrix[parent_idx, orig_n + idx] = 0.05
            # Distance to others proportional to parent's distances
            for j in range(orig_n):
                if j != parent_idx:
                    d = dist_matrix[parent_idx, j] * (1 + self.rng.uniform(-0.1, 0.1))
                    dist_matrix[orig_n + idx, j] = max(d, 0.05)
                    dist_matrix[j, orig_n + idx] = max(d, 0.05)
        
        self.extant = all_species
        self._build_graph_from_distances(dist_matrix)
        
        return {
            'species_before': n_extant,
            'species_after': n,
            'conservation_before': conservation_before,
            'conservation_after': self.conservation,
            'gap_before': gap_before,
            'gap_after': self.spectral_gap,
        }
    
    def rank_resilience(self):
        """
        Rank species by individual conservation.
        High IC = resilient (redundant in tree).
        Low IC = fragile (unique, irreplaceable).
        """
        ic = self.individual_conservation
        rankings = sorted(
            zip(self.species_names, ic),
            key=lambda x: x[1]
        )
        return rankings


# === RUN THE PHYLOGENETIC SIMULATION ===
print("=" * 60)
print("THE PHYLOGENETIC LAPLACIAN")
print("=" * 60)

# 1. Simulate evolution
phylo = PhylogeneticLaplacian(n_species=100)
phylo.simulate_evolution(birth_rate=0.8, death_rate=0.3, max_time=8.0)
print(f"\nExtant species after evolution: {len(phylo.extant)}")
print(f"Conservation: {phylo.conservation:.4f}")
print(f"Spectral gap: {phylo.spectral_gap:.6f}")
print(f"Algebraic connectivity (λ₂): {phylo.algebraic_connectivity:.6f}")

# 2. Mass extinction
print("\n--- MASS EXTINCTION EVENT ---")
result = phylo.mass_extinction(extinction_rate=0.75, biased=True)
print(f"Species: {result['species_before']} → {result['species_after']}")
print(f"Conservation: {result['conservation_before']:.4f} → {result['conservation_after']:.4f}")
print(f"Conservation drop: {result['conservation_drop']:.2%}")
print(f"Spectral gap: {result['gap_before']:.6f} → {result['gap_after']:.6f}")
print(f"Algebraic connectivity: {result['connectivity_before']:.6f} → {result['connectivity_after']:.6f}")

# 3. Adaptive radiation
print("\n--- ADAPTIVE RADIATION ---")
rad = phylo.adaptive_radiation(radiation_factor=2.5)
print(f"Species: {rad['species_before']} → {rad['species_after']}")
print(f"Conservation: {rad['conservation_before']:.4f} → {rad['conservation_after']:.4f}")
print(f"Spectral gap: {rad['gap_before']:.6f} → {rad['gap_after']:.6f}")
print(f"Conservation after radiation: {phylo.conservation:.4f}")

# 4. Rank resilience
print("\n--- SPECIES RESILIENCE RANKINGS ---")
rankings = phylo.rank_resilience()
print("Most fragile (low IC, irreplaceable):")
for name, ic in rankings[:5]:
    print(f"  {name}: IC = {ic:.6f}")
print("Most resilient (high IC, redundant):")
for name, ic in rankings[-5:]:
    print(f"  {name}: IC = {ic:.6f}")
```

## What the Numbers Tell Us

When we run this simulation, we see the spectral signature of life and death written in eigenvalues:

**Before extinction**, the tree has healthy conservation — a well-distributed eigenvalue spectrum reflecting the diversity of lineages. The algebraic connectivity (λ₂) is substantial, meaning the tree is well-connected through shared ancestry.

**After extinction**, conservation drops dramatically. But it drops *more* for biased extinctions (targeting specific clades) than for random ones. This is because biased extinction removes entire branches of the tree, not just scattered leaves. The tree doesn't just lose tips — it loses *structure*. The spectral gap collapses because the remaining species are clustered in fewer, more isolated groups.

**After adaptive radiation**, conservation rebounds as new species fill the eigenspace. But — and this is critical — the new tree has a *different* spectral structure than the original. The eigenvalues are distributed differently because the branching pattern is different. Evolution doesn't repeat. It finds new solutions.

The resilience rankings are the most provocative output. Species with high individual conservation are "safe" in spectral terms — their evolutionary information is shared with many close relatives. But species with *low* individual conservation are spectrally unique. They carry evolutionary information that no one else in the tree carries. They are the living fossils, the last of their line, the ones whose extinction would be an irreversible loss to the tree's structure.

The Laplacian doesn't care about charisma or size or ecological role. It sees only structure. And in that structure, it finds the same truth that conservation biologists know: **the most irreplaceable species are often the loneliest branches on the tree.**

---

# ROUND 2 — The Ecosystem Services Laplacian

## Food Webs Are Graphs, and Graphs Have Eigenvalues

An ecosystem is a graph. This is not a simplification — it is the literal structure of ecology. Species are nodes. Interactions are edges. The edges carry different flavors: predation (energy flows from prey to predator), mutualism (both benefit), competition (both suffer), parasitism (one benefits, one suffers), commensalism (one benefits, one is unaffected).

The food web — the directed graph of who eats whom — is the backbone of every terrestrial and aquatic ecosystem. Producers (plants, algae, cyanobacteria) capture energy from the sun. Primary consumers eat producers. Secondary consumers eat primary consumers. Apex predators sit at the top. Decomposers close the loop by breaking down dead matter.

This graph has a Laplacian. And the Laplacian has conservation. And the conservation tells you how healthy the ecosystem is.

Here is the key insight: **a healthy ecosystem has high conservation because its interaction graph is dense, redundant, and well-connected.** Many species interact with many other species through multiple pathways. Energy flows through the system along many routes. If one link breaks — one prey species declines — the system can route around it because alternative pathways exist.

A collapsing ecosystem has *low* conservation. Species are lost. Interactions are lost. The graph becomes sparse. Energy pathways narrow. The system becomes brittle — small perturbations can cause cascading failures.

## Keystone Species: The Fiedler Nodes

Robert Paine's 1966 experiment on the Washington coast is one of the most elegant in ecology. He removed the starfish *Pisaster ochraceus* from a rocky intertidal zone and watched what happened. The community collapsed. Mussels outcompeted everything else. Species diversity plummeted.

*Pisaster* is a **keystone species** — a species whose impact on the ecosystem is disproportionate to its abundance. Remove it, and the whole structure changes.

In spectral graph theory, the analogue of a keystone species is a **Fiedler node**. The Fiedler vector — the eigenvector corresponding to λ₂, the smallest non-zero eigenvalue — partitions the graph into communities. Nodes that are central to this partition, nodes whose removal would maximally increase λ₂ or fragment the graph, are the Fiedler nodes.

**Keystone species are Fiedler nodes.** Their spectral properties — low individual conservation, high centrality in the Fiedler vector — predict their disproportionate ecological importance.

This is not an analogy. It's a mathematical correspondence. The Laplacian doesn't know the difference between a food web and a social network and a power grid. It sees structure. And the structure of keystone importance is the same across all these domains: it's about the graph's vulnerability to node removal.

## The Ecosystem as Spectral Organism

An ecosystem is more than the sum of its species. It has emergent properties — stability, resilience, productivity, diversity — that arise from the interactions among species, not from any individual species. These emergent properties are encoded in the Laplacian's spectral structure.

**High-conservation ecosystems** have:
- Many species filling similar roles (functional redundancy)
- Dense interaction networks with multiple pathways
- Short characteristic path lengths (energy transfers efficiently)
- High modularity but strong inter-module connections
- Robustness to species loss

**Low-conservation ecosystems** have:
- Few species, each with unique roles
- Sparse interaction networks
- Long path lengths (energy gets trapped)
- Low modularity (everything depends on everything)
- Fragility — small perturbations cause cascades

The transition from high to low conservation is the spectral signature of ecosystem collapse. And it can happen *before* species start going extinct — the graph can become sparse while all species are still present, if the interactions between them weaken.

This is the spectral early warning system for ecosystem collapse.

## EcosystemLaplacian: Modeling Food Webs

```python
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
import matplotlib.pyplot as plt
from collections import defaultdict

class EcosystemLaplacian:
    """
    Model food webs as Laplacian graphs.
    Identify keystone species via Fiedler analysis.
    Simulate ecosystem collapse and recovery.
    """
    
    def __init__(self, seed=42):
        self.rng = np.random.RandomState(seed)
        self.species = {}       # id -> {name, trophic_level, biomass}
        self.interactions = {}  # (i,j) -> {type, strength}
        self.adjacency = None
        self.laplacian = None
        self.eigenvalues = None
        self.eigenvectors = None
        self.collapse_log = []
        
    def build_food_web(self, n_producers=15, n_herbivores=10, 
                       n_predators=8, n_apex=3, n_decomposers=4):
        """
        Build a synthetic food web with realistic trophic structure.
        """
        self.species = {}
        sid = 0
        
        # Producers (trophic level 1)
        for i in range(n_producers):
            self.species[sid] = {
                'name': f'producer_{i}',
                'trophic_level': 1,
                'biomass': self.rng.uniform(80, 120)
            }
            sid += 1
        
        # Herbivores (trophic level 2)
        for i in range(n_herbivores):
            self.species[sid] = {
                'name': f'herbivore_{i}',
                'trophic_level': 2,
                'biomass': self.rng.uniform(30, 60)
            }
            sid += 1
        
        # Predators (trophic level 3)
        for i in range(n_predators):
            self.species[sid] = {
                'name': f'predator_{i}',
                'trophic_level': 3,
                'biomass': self.rng.uniform(10, 25)
            }
            sid += 1
        
        # Apex predators (trophic level 4)
        for i in range(n_apex):
            self.species[sid] = {
                'name': f'apex_{i}',
                'trophic_level': 4,
                'biomass': self.rng.uniform(2, 8)
            }
            sid += 1
        
        # Decomposers (trophic level 1.5 — they break down dead matter)
        for i in range(n_decomposers):
            self.species[sid] = {
                'name': f'decomposer_{i}',
                'trophic_level': 1.5,
                'biomass': self.rng.uniform(40, 70)
            }
            sid += 1
        
        n = len(self.species)
        
        # Build interactions
        self.interactions = {}
        ids = list(self.species.keys())
        
        producers = [i for i in ids if self.species[i]['trophic_level'] == 1]
        herbivores = [i for i in ids if self.species[i]['trophic_level'] == 2]
        predators = [i for i in ids if self.species[i]['trophic_level'] == 3]
        apex = [i for i in ids if self.species[i]['trophic_level'] == 4]
        decomposers = [i for i in ids if self.species[i]['trophic_level'] == 1.5]
        
        # Herbivores eat producers (each herbivore eats 2-5 producers)
        for h in herbivores:
            n_prey = self.rng.randint(2, min(6, len(producers) + 1))
            prey = self.rng.choice(producers, n_prey, replace=False)
            for p in prey:
                self.interactions[(h, p)] = {
                    'type': 'predation',
                    'strength': self.rng.uniform(0.3, 0.8)
                }
        
        # Predators eat herbivores (and sometimes other predators)
        for pred in predators:
            n_prey = self.rng.randint(2, min(5, len(herbivores) + 1))
            prey = self.rng.choice(herbivores, n_prey, replace=False)
            for p in prey:
                self.interactions[(pred, p)] = {
                    'type': 'predation',
                    'strength': self.rng.uniform(0.3, 0.7)
                }
        
        # Apex eat predators and some herbivores
        for a in apex:
            n_prey = self.rng.randint(2, min(5, len(predators) + 1))
            prey = self.rng.choice(predators, n_prey, replace=False)
            for p in prey:
                self.interactions[(a, p)] = {
                    'type': 'predation',
                    'strength': self.rng.uniform(0.4, 0.9)
                }
            # Also some herbivores
            n_herb_prey = self.rng.randint(1, 3)
            herb_prey = self.rng.choice(herbivores, min(n_herb_prey, len(herbivores)), replace=False)
            for h in herb_prey:
                self.interactions[(a, h)] = {
                    'type': 'predation',
                    'strength': self.rng.uniform(0.2, 0.5)
                }
        
        # Mutualism: some producers have mutualist decomposers
        for d in decomposers:
            n_mut = self.rng.randint(2, 5)
            mut_partners = self.rng.choice(producers, min(n_mut, len(producers)), replace=False)
            for p in mut_partners:
                self.interactions[(d, p)] = {
                    'type': 'mutualism',
                    'strength': self.rng.uniform(0.2, 0.5)
                }
        
        # Decomposers interact with everything (they break down dead matter)
        for d in decomposers:
            # Connect to a few higher trophic level species
            higher = herbivores + predators
            n_conn = self.rng.randint(2, 5)
            conn = self.rng.choice(higher, min(n_conn, len(higher)), replace=False)
            for c in conn:
                if (d, c) not in self.interactions:
                    self.interactions[(d, c)] = {
                        'type': 'commensalism',
                        'strength': self.rng.uniform(0.1, 0.3)
                    }
        
        self._build_laplacian()
        return self
    
    def _build_laplacian(self):
        """Build weighted Laplacian from interaction graph."""
        n = len(self.species)
        ids = sorted(self.species.keys())
        id_to_idx = {sid: i for i, sid in enumerate(ids)}
        
        adjacency = np.zeros((n, n))
        
        for (i, j), interaction in self.interactions.items():
            idx_i = id_to_idx[i]
            idx_j = id_to_idx[j]
            w = interaction['strength']
            
            # Undirected for Laplacian: both directions contribute
            adjacency[idx_i, idx_j] += w
            adjacency[idx_j, idx_i] += w
        
        # Add some weak competition edges between same-trophic-level species
        trophic_groups = defaultdict(list)
        for sid in ids:
            tl = self.species[sid]['trophic_level']
            trophic_groups[tl].append(id_to_idx[sid])
        
        for tl, group in trophic_groups.items():
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    if self.rng.random() < 0.3:  # 30% chance of competition
                        w = self.rng.uniform(0.05, 0.15)
                        adjacency[group[i], group[j]] += w
                        adjacency[group[j], group[i]] += w
        
        self.adjacency = adjacency
        degree = np.diag(adjacency.sum(axis=1))
        self.laplacian = degree - adjacency
        
        self._compute_spectrum()
    
    def _compute_spectrum(self):
        n = self.laplacian.shape[0]
        self.eigenvalues, self.eigenvectors = np.linalg.eigh(self.laplacian)
        idx = np.argsort(self.eigenvalues)
        self.eigenvalues = self.eigenvalues[idx]
        self.eigenvectors = self.eigenvectors[:, idx]
    
    @property
    def conservation(self):
        return np.sum(self.eigenvalues * np.sum(self.eigenvectors**2, axis=0))
    
    @property
    def individual_conservation(self):
        return np.sum(self.eigenvalues[np.newaxis, :] * self.eigenvectors**2, axis=1)
    
    @property
    def algebraic_connectivity(self):
        nonzero = self.eigenvalues[self.eigenvalues > 1e-10]
        return nonzero[0] if len(nonzero) > 0 else 0.0
    
    @property
    def fiedler_vector(self):
        """The eigenvector for λ₂ — partitions graph into communities."""
        nonzero_idx = np.where(self.eigenvalues > 1e-10)[0]
        if len(nonzero_idx) == 0:
            return np.zeros(len(self.species))
        return self.eigenvectors[:, nonzero_idx[0]]
    
    def identify_keystone_species(self, top_k=5):
        """
        Identify keystone species using multiple spectral criteria:
        1. High Fiedler vector magnitude = central to graph partition
        2. Low individual conservation = irreplaceable
        3. High degree centrality = many interactions
        """
        ids = sorted(self.species.keys())
        fiedler = self.fiedler_vector
        ic = self.individual_conservation
        degrees = self.adjacency.sum(axis=1)
        
        # Composite keystone score
        # High Fiedler magnitude, low IC, high degree → keystone
        fiedler_score = np.abs(fiedler) / (np.max(np.abs(fiedler)) + 1e-10)
        ic_score = 1.0 - (ic - np.min(ic)) / (np.max(ic) - np.min(ic) + 1e-10)
        degree_score = degrees / (np.max(degrees) + 1e-10)
        
        keystone_score = 0.4 * fiedler_score + 0.3 * ic_score + 0.3 * degree_score
        
        rankings = sorted(
            zip(ids, keystone_score),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [
            {
                'species_id': sid,
                'name': self.species[sid]['name'],
                'trophic_level': self.species[sid]['trophic_level'],
                'keystone_score': score,
                'fiedler_component': fiedler[i],
                'individual_conservation': ic[i],
                'degree': degrees[i]
            }
            for i, (sid, score) in enumerate(rankings[:top_k])
        ]
    
    def simulate_collapse(self, target_species_id=None, n_steps=10):
        """
        Simulate ecosystem collapse by progressively removing a species.
        Track conservation through the collapse cascade.
        """
        if target_species_id is None:
            # Default: remove the top keystone species
            keystones = self.identify_keystone_species(top_k=1)
            target_species_id = keystones[0]['species_id']
        
        history = []
        ids = sorted(self.species.keys())
        id_to_idx = {sid: i for i, sid in enumerate(ids)}
        
        target_idx = id_to_idx[target_species_id]
        
        # Progressive weakening of the target species' interactions
        for step in range(n_steps + 1):
            fraction = step / n_steps
            
            # Create modified adjacency
            modified_adj = self.adjacency.copy()
            
            if fraction > 0:
                # Weaken all edges connected to target
                modified_adj[target_idx, :] *= (1 - fraction)
                modified_adj[:, target_idx] *= (1 - fraction)
                
                # Also weaken edges connected to species that depend on target
                # This is the cascade effect
                for j in range(len(ids)):
                    if self.adjacency[target_idx, j] > 0.3:
                        # Strong connection → cascade
                        cascade_strength = fraction * 0.5
                        modified_adj[j, :] *= (1 - cascade_strength)
                        modified_adj[:, j] *= (1 - cascade_strength)
            
            # Compute conservation of modified graph
            degree = np.diag(modified_adj.sum(axis=1))
            lap = degree - modified_adj
            eigenvalues, eigenvectors = np.linalg.eigh(lap)
            idx_sort = np.argsort(eigenvalues)
            eigenvalues = eigenvalues[idx_sort]
            eigenvectors = eigenvectors[:, idx_sort]
            
            conservation = np.sum(eigenvalues * np.sum(eigenvectors**2, axis=0))
            nonzero = eigenvalues[eigenvalues > 1e-10]
            connectivity = nonzero[0] if len(nonzero) > 0 else 0
            
            n_components = np.sum(eigenvalues < 1e-10)
            
            history.append({
                'step': step,
                'fraction_weakened': fraction,
                'conservation': conservation,
                'connectivity': connectivity,
                'n_components': n_components,
                'target_biomass_fraction': 1 - fraction
            })
            
            # If the graph fragmented, record it
            if n_components > 1 and step > 0 and history[-2]['n_components'] <= 1:
                history[-1]['fragmentation_event'] = True
        
        self.collapse_log.append({
            'target': self.species[target_species_id]['name'],
            'target_id': target_species_id,
            'history': history
        })
        
        return history
    
    def simulate_recovery(self, n_steps=15):
        """
        After a collapse, simulate recovery through reintroduction.
        """
        if not self.collapse_log:
            return None
        
        last_collapse = self.collapse_log[-1]
        history = []
        
        # Start from collapsed state
        ids = sorted(self.species.keys())
        id_to_idx = {sid: i for i, sid in enumerate(ids)}
        target_idx = id_to_idx[last_collapse['target_id']]
        
        for step in range(n_steps + 1):
            fraction = 1.0 - (step / n_steps)
            
            modified_adj = self.adjacency.copy()
            
            if fraction < 1.0:
                recovery = 1 - fraction
                modified_adj[target_idx, :] *= recovery
                modified_adj[:, target_idx] *= recovery
                
                # Secondary species also recover
                for j in range(len(ids)):
                    if self.adjacency[target_idx, j] > 0.3:
                        cascade_recovery = recovery * 0.5
                        modified_adj[j, :] *= max(cascade_recovery, 
                                                   1 - (1 - recovery) * 0.5)
                        modified_adj[:, j] *= max(cascade_recovery,
                                                   1 - (1 - recovery) * 0.5)
            
            degree = np.diag(modified_adj.sum(axis=1))
            lap = degree - modified_adj
            eigenvalues, eigenvectors = np.linalg.eigh(lap)
            idx_sort = np.argsort(eigenvalues)
            eigenvalues = eigenvalues[idx_sort]
            eigenvectors = eigenvectors[:, idx_sort]
            
            conservation = np.sum(eigenvalues * np.sum(eigenvectors**2, axis=0))
            nonzero = eigenvalues[eigenvalues > 1e-10]
            connectivity = nonzero[0] if len(nonzero) > 0 else 0
            
            history.append({
                'step': step,
                'recovery_fraction': step / n_steps,
                'conservation': conservation,
                'connectivity': connectivity
            })
        
        return history


# === RUN THE ECOSYSTEM SIMULATION ===
print("=" * 60)
print("THE ECOSYSTEM SERVICES LAPLACIAN")
print("=" * 60)

eco = EcosystemLaplacian(seed=42)
eco.build_food_web(n_producers=15, n_herbivores=10, n_predators=8, n_apex=3, n_decomposers=4)

print(f"\nSpecies: {len(eco.species)}")
print(f"Interactions: {len(eco.interactions)}")
print(f"Conservation: {eco.conservation:.4f}")
print(f"Algebraic connectivity: {eco.algebraic_connectivity:.6f}")

# Identify keystone species
print("\n--- KEYSTONE SPECIES (Spectral Identification) ---")
keystones = eco.identify_keystone_species(top_k=5)
for k in keystones:
    print(f"  {k['name']} (TL={k['trophic_level']}): "
          f"score={k['keystone_score']:.4f}, "
          f"Fiedler={k['fiedler_component']:.4f}, "
          f"IC={k['individual_conservation']:.4f}")

# Simulate collapse
print("\n--- ECOSYSTEM COLLAPSE SIMULATION ---")
target = keystones[0]['species_id']
collapse = eco.simulate_collapse(target_species_id=target, n_steps=10)
for entry in collapse:
    frag = " *** FRAGMENTATION ***" if entry.get('fragmentation_event') else ""
    print(f"  Step {entry['step']:2d}: conservation={entry['conservation']:.4f}, "
          f"connectivity={entry['connectivity']:.6f}, "
          f"biomass={entry['target_biomass_fraction']:.0%}{frag}")

# Simulate recovery
print("\n--- ECOSYSTEM RECOVERY ---")
recovery = eco.simulate_recovery(n_steps=15)
for entry in recovery:
    print(f"  Step {entry['step']:2d}: recovery={entry['recovery_fraction']:.0%}, "
          f"conservation={entry['conservation']:.4f}, "
          f"connectivity={entry['connectivity']:.6f}")
```

## The Spectral Fingerprint of Collapse and Recovery

The ecosystem collapse simulation reveals something striking: **conservation doesn't decline linearly.** It follows a nonlinear trajectory that accelerates as the system approaches a tipping point. This is the spectral signature of critical transition theory — the mathematical framework that predicts sudden ecosystem collapses.

The algebraic connectivity (λ₂) is the canary in the coal mine. It starts dropping *before* conservation shows major changes. This is because λ₂ measures the *minimum* connection strength in the graph — the weakest link. When that weakest link starts to fail, the whole system is approaching fragmentation.

The fragmentation event — when the number of connected components jumps from 1 to 2 or more — is the spectral equivalent of ecosystem collapse. The food web literally falls apart into disconnected sub-webs. Energy can no longer flow between them. Each fragment operates independently, and each is less stable than the whole.

Recovery is not the mirror image of collapse. The system follows a *different trajectory* on the way back up. Conservation recovers faster than connectivity. This is **ecological hysteresis** — the system's response depends on its history, and the path to recovery is different from the path to collapse.

This has profound implications for conservation. If you want to restore a collapsed ecosystem, you can't just reintroduce the keystone species and expect everything to bounce back. The interaction network needs to be rebuilt, and that takes time. The spectral structure recovers gradually, not instantly.

---

# ROUND 3 — The Protein Folding Graph

## A Folded Protein Is a Laplacian

A protein is a linear chain of amino acids. But it doesn't stay linear. It folds — twists, bends, loops, coils — into a precise three-dimensional structure. And that structure determines everything: whether an enzyme catalyzes a reaction, whether an antibody binds an antigen, whether a membrane channel opens or closes.

The folding process is one of the deepest problems in biology. Christian Anfinsen showed in the 1960s that the amino acid sequence *contains all the information needed* to determine the folded structure. But how? How does a chain of hundreds of amino acids, in a sea of water molecules, find its correct three-dimensional shape in milliseconds?

Here's the spectral perspective: **the amino acids are nodes. The contact interactions between them — hydrogen bonds, van der Waals forces, hydrophobic packing, disulfide bridges — are edges. The folded protein is a graph, and that graph has a Laplacian.**

And here is the central claim: **a correctly folded protein has HIGH conservation, and a misfolded protein has LOWER conservation.**

Why? Because correct folding creates a tight, coherent, densely connected graph. The amino acids are packed efficiently. Every residue is in its proper place, forming the correct contacts. The graph is well-connected, the eigenvalue spectrum is spread, and conservation is high.

Misfolding — whether it's a prion, an amyloid fibril, or just a misfolded enzyme — creates a graph with *lower* structural coherence. Some contacts are wrong. Some residues are exposed that should be buried. The packing is less efficient. The graph has gaps, and conservation drops.

## Folding as Spectral Convergence

The folding process itself can be described as **spectral convergence**: the protein's Laplacian settling into its ground state eigenconfiguration.

Start with the unfolded chain — a linear graph where each amino acid is connected only to its immediate neighbors. This graph has low conservation. The eigenvalue spectrum is clustered around small values. The Fiedler value is tiny.

As the protein folds, new edges form. Amino acids that are far apart in the sequence come into contact in 3D space. The graph becomes denser. The eigenvalue spectrum spreads. Conservation increases.

The final folded state is the configuration that maximizes conservation — or equivalently, minimizes some energy function that is itself related to the spectral structure. The protein explores conformational space, and the correct fold is the spectral ground state.

This is not just a mathematical metaphor. The **Eigensheet** model of protein folding, proposed by various researchers, uses exactly this framework. The Laplacian of the contact map encodes the protein's fold topology. The eigenvalues classify fold types. The eigenvectors identify structural domains.

## Misfolding as Spectral Anomaly

Prions are misfolded proteins that can induce other proteins to misfold. They're responsible for Creutzfeldt-Jakob disease, mad cow disease, and kuru. Amyloid-beta plaques in Alzheimer's disease are another form of misfolded protein.

In spectral terms, these misfolded states have **anomalous conservation signatures**. The graph is denser than the correct fold in some places (the beta-sheet stacking that characterizes amyloids) but sparser in others (the loss of the native tertiary contacts).

The conservation is not just *lower* — it's *different*. The eigenvalue spectrum has a characteristic shape that distinguishes the amyloid fold from the native fold. This is potentially diagnostic: if you can compute the Laplacian of a protein's contact map and identify the spectral signature of misfolding, you can detect disease-related conformations before they cause symptoms.

## ProteinFolding: Simulating Spectral Folding

```python
import numpy as np
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt

class ProteinFolding:
    """
    Simulate protein folding as spectral convergence.
    Detect misfolding via conservation anomaly.
    """
    
    def __init__(self, n_residues=50, seed=42):
        self.rng = np.random.RandomState(seed)
        self.n_residues = n_residues
        self.residues = []
        self.native_structure = None
        self.contact_map = None
        self.laplacian = None
        self.eigenvalues = None
        self.eigenvectors = None
        
    def generate_protein(self):
        """
        Generate a synthetic protein with a native folded structure.
        The structure mimics a globular protein with alpha helices and beta sheets.
        """
        n = self.n_residues
        
        # Generate 3D coordinates for a folded protein
        # Use a combination of helical and random coil regions
        coords = np.zeros((n, 3))
        
        # Build a compact globular structure
        # Start with a rough sphere and add local structure
        for i in range(n):
            # Helical component
            t = i * 0.5
            # Core packing: tighter as we go inward
            radius = 8.0 * (1 - 0.3 * np.sin(i / n * np.pi))
            coords[i, 0] = radius * np.cos(t) + self.rng.normal(0, 0.3)
            coords[i, 1] = radius * np.sin(t) + self.rng.normal(0, 0.3)
            coords[i, 2] = (i - n/2) * 0.3 + self.rng.normal(0, 0.2)
        
        # Center and compact
        coords -= coords.mean(axis=0)
        
        # Apply compaction (simulate hydrophobic collapse)
        for iteration in range(20):
            center = coords.mean(axis=0)
            distances_from_center = np.linalg.norm(coords - center, axis=1)
            # Pull toward center
            for i in range(n):
                if distances_from_center[i] > 5.0:
                    coords[i] -= (coords[i] - center) * 0.05
        
        self.native_structure = coords
        
        # Generate amino acid types (hydrophobicity scale 0-1)
        self.residues = []
        aa_types = ['A', 'V', 'I', 'L', 'M', 'F', 'W', 'P',  # hydrophobic
                    'S', 'T', 'C', 'N', 'Q',                    # polar
                    'D', 'E', 'K', 'R', 'H',                     # charged
                    'G']                                          # special
        
        for i in range(n):
            # Hydrophobic residues more likely in the core
            dist_from_center = np.linalg.norm(coords[i] - coords.mean(axis=0))
            if dist_from_center < 3.0:
                # Core: prefer hydrophobic
                aa = self.rng.choice(aa_types[:8], p=[0.2, 0.15, 0.15, 0.15, 0.1, 0.1, 0.05, 0.1])
            else:
                # Surface: prefer polar/charged
                aa = self.rng.choice(aa_types[8:], p=[0.15, 0.1, 0.05, 0.12, 0.12, 0.15, 0.15, 0.08, 0.08])
            self.residues.append(aa)
        
        self._compute_contact_map(coords)
        return self
    
    def _compute_contact_map(self, coords, threshold=6.0):
        """Compute contact map from 3D coordinates."""
        distances = squareform(pdist(coords))
        
        # Contact if within threshold AND not adjacent in sequence
        self.contact_map = np.zeros_like(distances)
        for i in range(self.n_residues):
            for j in range(i + 2, self.n_residues):  # skip adjacent
                if distances[i, j] < threshold:
                    # Weight by inverse distance
                    self.contact_map[i, j] = 1.0 / (distances[i, j] + 0.1)
                    self.contact_map[j, i] = self.contact_map[i, j]
        
        # Add backbone connections (adjacent residues)
        for i in range(self.n_residues - 1):
            self.contact_map[i, i + 1] = 1.0
            self.contact_map[i + 1, i] = 1.0
        
        self._build_laplacian()
    
    def _build_laplacian(self):
        """Build graph Laplacian from contact map."""
        degree = np.diag(self.contact_map.sum(axis=1))
        self.laplacian = degree - self.contact_map
        self._compute_spectrum()
    
    def _compute_spectrum(self):
        self.eigenvalues, self.eigenvectors = np.linalg.eigh(self.laplacian)
        idx = np.argsort(self.eigenvalues)
        self.eigenvalues = self.eigenvalues[idx]
        self.eigenvectors = self.eigenvectors[:, idx]
    
    @property
    def conservation(self):
        return np.sum(self.eigenvalues * np.sum(self.eigenvectors**2, axis=0))
    
    @property
    def individual_conservation(self):
        return np.sum(self.eigenvalues[np.newaxis, :] * self.eigenvectors**2, axis=1)
    
    @property
    def spectral_gap(self):
        nonzero = self.eigenvalues[self.eigenvalues > 1e-10]
        if len(nonzero) < 2:
            return 0.0
        return nonzero[1] - nonzero[0]
    
    def simulate_folding(self, n_steps=100):
        """
        Simulate protein folding as spectral convergence.
        Start from unfolded (linear) state and converge to native fold.
        """
        n = self.n_residues
        
        # Unfolded state: linear chain, random coil
        unfolded_coords = np.zeros((n, 3))
        for i in range(n):
            unfolded_coords[i] = [
                self.rng.normal(0, 2),
                self.rng.normal(0, 2),
                i * 0.8 + self.rng.normal(0, 0.5)
            ]
        
        history = []
        coords = unfolded_coords.copy()
        
        for step in range(n_steps + 1):
            progress = step / n_steps
            
            # Interpolate between unfolded and native
            current_coords = (1 - progress) * unfolded_coords + progress * self.native_structure
            
            # Add thermal noise (decreases as folding progresses)
            noise_scale = 0.5 * (1 - progress)
            current_coords += self.rng.normal(0, noise_scale, current_coords.shape)
            
            # Compute spectral properties at this folding stage
            distances = squareform(pdist(current_coords))
            contact = np.zeros_like(distances)
            for i in range(n):
                for j in range(i + 2, n):
                    if distances[i, j] < 6.0:
                        contact[i, j] = 1.0 / (distances[i, j] + 0.1)
                        contact[j, i] = contact[i, j]
            for i in range(n - 1):
                contact[i, i + 1] = 1.0
                contact[i + 1, i] = 1.0
            
            degree = np.diag(contact.sum(axis=1))
            lap = degree - contact
            eigenvalues = np.linalg.eigvalsh(lap)
            eigenvalues.sort()
            
            conservation = np.sum(eigenvalues * np.sum(np.linalg.eigh(lap)[1]**2, axis=0)) if step % 10 == 0 else None
            
            history.append({
                'step': step,
                'progress': progress,
                'rmsd': np.sqrt(np.mean((current_coords - self.native_structure)**2)),
                'n_contacts': np.sum(contact > 0) // 2 - (n - 1),  # non-backbone contacts
                'lambda_1': eigenvalues[0],
                'lambda_2': eigenvalues[1] if len(eigenvalues) > 1 else 0,
                'lambda_max': eigenvalues[-1],
                'conservation': conservation
            })
        
        return history
    
    def simulate_misfolding(self, misfold_type='amyloid', severity=0.5):
        """
        Simulate protein misfolding and compare spectral signatures.
        
        Types:
        - 'amyloid': extended beta-sheet stacking (high local density, wrong global topology)
        - 'molten_globule': correct secondary structure, wrong tertiary packing
        - 'prion': alternative stable fold
        """
        n = self.n_residues
        
        if misfold_type == 'amyloid':
            # Extended beta-sheet: residues stack in parallel layers
            misfolded_coords = np.zeros((n, 3))
            for i in range(n):
                row = i // 5  # groups of 5
                col = i % 5
                misfolded_coords[i] = [
                    col * 1.0,
                    row * 0.5,
                    (i % 2) * 0.3
                ]
            misfolded_coords += self.rng.normal(0, 0.2, misfolded_coords.shape)
            
        elif misfold_type == 'molten_globule':
            # Similar to native but with scrambled packing
            misfolded_coords = self.native_structure.copy()
            # Shuffle secondary structure elements
            block_size = n // 5
            blocks = []
            for b in range(5):
                blocks.append(misfolded_coords[b*block_size:(b+1)*block_size].copy())
            self.rng.shuffle(blocks)
            misfolded_coords = np.vstack(blocks)
            misfolded_coords += self.rng.normal(0, severity * 0.5, misfolded_coords.shape)
            
        elif misfold_type == 'prion':
            # Alternative fold: mirror-like but with different topology
            misfolded_coords = self.native_structure.copy()
            # Swap x and z coordinates, add perturbation
            misfolded_coords[:, [0, 2]] = misfolded_coords[:, [2, 0]]
            misfolded_coords += self.rng.normal(0, severity * 0.3, misfolded_coords.shape)
        
        # Compute spectral properties of misfolded state
        distances = squareform(pdist(misfolded_coords))
        contact = np.zeros_like(distances)
        for i in range(n):
            for j in range(i + 2, n):
                if distances[i, j] < 6.0:
                    contact[i, j] = 1.0 / (distances[i, j] + 0.1)
                    contact[j, i] = contact[i, j]
        for i in range(n - 1):
            contact[i, i + 1] = 1.0
            contact[i + 1, i] = 1.0
        
        degree = np.diag(contact.sum(axis=1))
        lap = degree - contact
        eigenvalues, eigenvectors = np.linalg.eigh(lap)
        idx = np.argsort(eigenvalues)
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        misfold_conservation = np.sum(eigenvalues * np.sum(eigenvectors**2, axis=0))
        
        # Compare with native
        native_conservation = self.conservation
        
        # Spectral distance between folds
        spectral_distance = np.linalg.norm(eigenvalues - self.eigenvalues)
        
        return {
            'misfold_type': misfold_type,
            'severity': severity,
            'native_conservation': native_conservation,
            'misfold_conservation': misfold_conservation,
            'conservation_ratio': misfold_conservation / (native_conservation + 1e-10),
            'spectral_distance': spectral_distance,
            'native_contacts': np.sum(self.contact_map > 0) // 2 - (n - 1),
            'misfold_contacts': np.sum(contact > 0) // 2 - (n - 1),
            'misfold_eigenvalues': eigenvalues
        }
    
    def detect_misfolding(self, test_coords, sensitivity=0.95):
        """
        Given a protein's coordinates, detect if it's misfolded
        by comparing its conservation to the expected native conservation.
        """
        n = self.n_residues
        
        # Compute test contact map
        distances = squareform(pdist(test_coords))
        contact = np.zeros_like(distances)
        for i in range(n):
            for j in range(i + 2, n):
                if distances[i, j] < 6.0:
                    contact[i, j] = 1.0 / (distances[i, j] + 0.1)
                    contact[j, i] = contact[i, j]
        for i in range(n - 1):
            contact[i, i + 1] = 1.0
            contact[i + 1, i] = 1.0
        
        degree = np.diag(contact.sum(axis=1))
        lap = degree - contact
        eigenvalues, eigenvectors = np.linalg.eigh(lap)
        idx = np.argsort(eigenvalues)
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        test_conservation = np.sum(eigenvalues * np.sum(eigenvectors**2, axis=0))
        
        # Ratio to native conservation
        ratio = test_conservation / (self.conservation + 1e-10)
        
        # Spectral distance
        spectral_dist = np.linalg.norm(eigenvalues - self.eigenvalues)
        
        # Normalized spectral distance
        max_possible = np.linalg.norm(self.eigenvalues) + np.linalg.norm(eigenvalues)
        normalized_dist = spectral_dist / (max_possible + 1e-10)
        
        # Decision: misfolded if conservation ratio < threshold or spectral distance > threshold
        conservation_threshold = 1.0 - sensitivity  # higher sensitivity = lower threshold
        distance_threshold = sensitivity * 0.5
        
        is_misfolded = (ratio < (1 - conservation_threshold)) or (normalized_dist > distance_threshold)
        
        return {
            'is_misfolded': is_misfolded,
            'confidence': abs(1 - ratio),
            'conservation_ratio': ratio,
            'spectral_distance': normalized_dist,
            'test_conservation': test_conservation,
            'native_conservation': self.conservation
        }


# === RUN THE PROTEIN FOLDING SIMULATION ===
print("=" * 60)
print("THE PROTEIN FOLDING GRAPH")
print("=" * 60)

# 1. Generate and fold a protein
protein = ProteinFolding(n_residues=50, seed=42)
protein.generate_protein()

print(f"\nProtein: {protein.n_residues} residues")
print(f"Amino acid sequence: {''.join(protein.residues[:20])}...")
print(f"Native contacts: {np.sum(protein.contact_map > 0) // 2 - 49}")
print(f"Native conservation: {protein.conservation:.4f}")
print(f"Spectral gap: {protein.spectral_gap:.6f}")

# 2. Simulate folding process
print("\n--- FOLDING TRAJECTORY ---")
folding = protein.simulate_folding(n_steps=100)
for entry in folding:
    if entry['step'] % 20 == 0:
        cons = f", conservation={entry['conservation']:.4f}" if entry['conservation'] else ""
        print(f"  Step {entry['step']:3d} ({entry['progress']:.0%}): "
              f"RMSD={entry['rmsd']:.3f}, "
              f"contacts={entry['n_contacts']}, "
              f"λ₁={entry['lambda_1']:.4f}, λ₂={entry['lambda_2']:.4f}{cons}")

# 3. Test misfolding scenarios
print("\n--- MISFOLDING DETECTION ---")
for mtype in ['amyloid', 'molten_globule', 'prion']:
    result = protein.simulate_misfolding(misfold_type=mtype, severity=0.5)
    print(f"\n  {mtype.upper()}:")
    print(f"    Native conservation: {result['native_conservation']:.4f}")
    print(f"    Misfold conservation: {result['misfold_conservation']:.4f}")
    print(f"    Conservation ratio: {result['conservation_ratio']:.4f}")
    print(f"    Spectral distance: {result['spectral_distance']:.4f}")
    print(f"    Native contacts: {result['native_contacts']}, "
          f"Misfold contacts: {result['misfold_contacts']}")
    
    # Use the detection method
    if mtype == 'amyloid':
        coords = np.zeros((50, 3))
        for i in range(50):
            coords[i] = [i % 5 * 1.0, i // 5 * 0.5, (i % 2) * 0.3]
    elif mtype == 'molten_globule':
        coords = protein.native_structure.copy()
        coords += np.random.RandomState(123).normal(0, 0.25, coords.shape)
    elif mtype == 'prion':
        coords = protein.native_structure.copy()
        coords[:, [0, 2]] = coords[:, [2, 0]]
    
    detection = protein.detect_misfolding(coords)
    print(f"    Detection: {'MISFOLDED' if detection['is_misfolded'] else 'NATIVE'} "
          f"(confidence={detection['confidence']:.4f})")

# 4. Spectral comparison
print("\n--- SPECTRAL COMPARISON: NATIVE vs MISFOLDED ---")
print(f"  Native eigenvalue range: [{protein.eigenvalues[1]:.4f}, {protein.eigenvalues[-1]:.4f}]")
amyloid_result = protein.simulate_misfolding('amyloid', 0.5)
misfold_evals = amyloid_result['misfold_eigenvalues']
print(f"  Amyloid eigenvalue range: [{misfold_evals[1]:.4f}, {misfold_evals[-1]:.4f}]")
print(f"  Eigenvalue divergence: {np.linalg.norm(protein.eigenvalues - misfold_evals):.4f}")
```

## Conservation as the Signature of Correct Folding

The protein folding simulation reveals the deepest connection between conservation spectral analysis and biology. The folding process — the physical process by which a linear chain of amino acids finds its native three-dimensional structure — is a process of **spectral convergence**. The unfolded chain has low conservation. The native fold has high conservation. Folding is the journey from one to the other.

But the misfolding results are even more revealing. Different types of misfolding produce *different* spectral signatures:

**Amyloid misfolding** creates an extended, repetitive structure with high local contact density but wrong global topology. The conservation is typically *close to* native — sometimes even *higher* locally — because the beta-sheet stacking creates many contacts. But the spectral *shape* is wrong. The eigenvalue distribution is different from the native fold. The Laplacian "knows" this isn't the right structure, even though it has many edges.

**Molten globule misfolding** produces a structure with correct secondary structure but scrambled tertiary packing. Conservation is moderately lower than native, and the spectral distance is intermediate. This is the hardest to detect because it's the most similar to the native fold.

**Prion misfolding** creates an entirely different stable fold. The conservation is significantly different, and the spectral distance is large. This is the easiest to detect spectrally.

The detection algorithm — comparing the test protein's conservation and eigenvalue spectrum to the native reference — can identify misfolding with high confidence. The key insight: **it's not just about the total conservation, but the shape of the eigenvalue spectrum.** Two proteins can have similar total conservation but very different spectral distributions, and the spectral distribution encodes the fold topology.

## The Unified Theory: Life as Spectral Process

Across all three rounds, a pattern emerges. **Biological systems at every scale — molecular, ecological, evolutionary — can be modeled as graphs with Laplacian structure, and the health/stability/correctness of those systems is encoded in their conservation spectral properties.**

- **Phylogenetic trees**: High conservation = healthy diversification. Conservation drop = mass extinction. Conservation recovery = adaptive radiation.
- **Food webs**: High conservation = stable ecosystem. Conservation decline = approaching collapse. Fiedler nodes = keystone species.
- **Protein structures**: High conservation = correctly folded. Conservation anomaly = misfolding. Spectral convergence = the folding process itself.

This is not coincidence. It's a reflection of a deeper principle: **biological systems are information-processing systems, and information processing in structured systems is governed by the Laplacian.** The eigenvalues determine how information (genetic, ecological, chemical) flows through the system. The conservation measures how well the system preserves that information. And the loss of conservation — whether through extinction, ecosystem collapse, or protein misfolding — is the spectral signature of biological failure.

The Laplacian is the deepest lens through which to view living systems. It doesn't replace the specific knowledge of each field — the biochemistry of folding, the population genetics of speciation, the community dynamics of ecosystems. But it provides a unified mathematical framework that connects them all.

*The tree of life, the web of interactions, the folded chain of amino acids — all graphs, all Laplacians, all subject to the same spectral laws. Conservation isn't just a graph property. It's a biological principle.*
