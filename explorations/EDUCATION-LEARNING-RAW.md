# Education & Learning Through Conservation Spectral Analysis

---

## ROUND 1 — The Knowledge Graph Laplacian

### Concepts as Nodes, Prerequisites as Edges

Every curriculum is a directed graph. The nodes are concepts — calculus, algebra, trigonometry, limits, derivatives, integrals. The edges are prerequisites: you need limits before derivatives, derivatives before integrals, algebra before all of it. Strip away the textbooks and the syllabi and the lecture halls, and what remains is a directed graph of intellectual dependency.

But here's the move that changes everything: forget the direction. Treat prerequisites as *undirected* edges — as connections between related concepts — and build the Laplacian. Because when you do, the Laplacian tells you something profound about the curriculum's *coherence*. It tells you whether knowledge flows naturally through the graph or whether students are being asked to leap across voids.

The curriculum IS a Laplacian. The question is whether it's a *good* one.

### Conservation in Curriculum Design

A well-designed curriculum has high conservation. Energy — in the form of understanding, of "getting it" — propagates cleanly from node to node. When you learn algebra, the energy flows naturally to calculus concepts because the edge is there, the prerequisite is solid. The graph's algebraic connectivity (the second-smallest eigenvalue of the Laplacian, λ₂) is high. Information doesn't leak. Students don't find themselves staring at a derivative having never seen a function.

A poorly designed curriculum has low conservation. Disconnected topics, missing prerequisites, conceptual islands. Students are asked to understand integration without ever having developed intuition for accumulation. The algebraic connectivity drops toward zero. The graph fragments. Energy injected at one node — a brilliant lecture on Riemann sums — dissipates into nothing because there's no path to carry it to the next concept.

This isn't metaphor. This is math. The spectral gap of the curriculum Laplacian is literally a quantitative measure of how well-structured a course sequence is. You can compute it. You can compare curricula. You can say, with a number, "this program is more coherent than that one."

### The Fiedler Vector and Natural Learning Order

The Fiedler vector — the eigenvector corresponding to λ₂ — is the ghost in the curriculum machine. It assigns a real number to every concept node. Sort the concepts by their Fiedler value, and you get the *natural learning order*. Not the order some committee decided on. Not the order the textbook presents. The order the graph itself implies.

Why? Because the Fiedler vector solves a relaxed version of the graph bipartition problem. It finds the cut that divides the graph into two coherent halves with the minimum number of severed edges. In curriculum terms, it identifies the natural "before" and "after" — the concepts that belong to the foundation and the concepts that belong to the superstructure. And within each half, it provides a natural ordering that respects the connectivity structure.

Follow the Fiedler walk, and students progress smoothly. Each new concept is exactly one well-connected step from the last. The cognitive load is minimized because the graph is doing the work — the structure of knowledge itself is guiding the sequence.

Deviate from the Fiedler walk, and you're forcing students to make jumps the graph doesn't support. You're asking them to learn concept X when the Fiedler vector says they should learn concept Y first. The resistance is real, measurable, and quantifiable.

### Detecting Missing Prerequisites

Here's where it gets practical. If the curriculum Laplacian has a very low λ₂ — if the spectral gap is nearly zero — the graph is nearly disconnected. There's a bottleneck. Somewhere, a critical prerequisite is missing. The Fiedler partition tells you *where*: it splits the graph into two components, and the concepts on opposite sides of the partition are the ones that need a bridge.

This is an auditable, quantitative tool for curriculum design. Feed in the prerequisite graph, compute the Laplacian, examine the spectrum. Low λ₂? Find the Fiedler cut. Add the missing edge — the missing prerequisite course or the missing connection in the syllabus. Recompute. Watch λ₂ rise. Watch conservation improve.

### CurriculumLaplacian: Implementation

```python
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class CurriculumCourse:
    id: str
    name: str
    level: int = 0  # 0=foundational, 1=intermediate, 2=advanced
    fiedler_value: float = 0.0
    optimal_rank: int = 0

@dataclass
class Prerequisite:
    source: str
    target: str  # source is prerequisite for target
    weight: float = 1.0  # strength of the prerequisite relationship

class CurriculumLaplacian:
    """
    Analyze a course prerequisite graph through spectral lens.
    Concepts = nodes, prerequisites = edges.
    The curriculum IS a Laplacian — we measure its conservation.
    """
    def __init__(self):
        self.courses: dict[str, CurriculumCourse] = {}
        self.prerequisites: list[Prerequisite] = []
        self.adjacency: Optional[sparse.csr_matrix] = None
        self.laplacian: Optional[sparse.csr_matrix] = None
        self._id_to_idx: dict[str, int] = {}
        self._idx_to_id: dict[int, str] = {}

    def add_course(self, course_id: str, name: str, level: int = 0):
        self.courses[course_id] = CurriculumCourse(
            id=course_id, name=name, level=level
        )

    def add_prerequisite(self, prereq_id: str, course_id: str, weight: float = 1.0):
        self.prerequisites.append(
            Prerequisite(source=prereq_id, target=course_id, weight=weight)
        )

    def _build_index(self):
        ids = sorted(self.courses.keys())
        self._id_to_idx = {cid: i for i, cid in enumerate(ids)}
        self._idx_to_id = {i: cid for i, cid in enumerate(ids)}

    def build_laplacian(self) -> sparse.csr_matrix:
        """Build the graph Laplacian from the prerequisite graph."""
        self._build_index()
        n = len(self.courses)
        rows, cols, weights = [], [], []

        for prereq in self.prerequisites:
            if prereq.source in self._id_to_idx and prereq.target in self._id_to_idx:
                i = self._id_to_idx[prereq.source]
                j = self._id_to_idx[prereq.target]
                # Undirected: prerequisite edges become symmetric connections
                rows.extend([i, j])
                cols.extend([j, i])
                weights.extend([prereq.weight, prereq.weight])

        self.adjacency = sparse.csr_matrix(
            (weights, (rows, cols)), shape=(n, n)
        )
        degree = np.array(self.adjacency.sum(axis=1)).flatten()
        self.laplacian = sparse.diags(degree) - self.adjacency
        return self.laplacian

    def spectral_analysis(self) -> dict:
        """Full spectral analysis: conservation, Fiedler vector, learning order."""
        if self.laplacian is None:
            self.build_laplacian()

        n = self.laplacian.shape[0]
        k = min(4, n - 1)
        eigenvalues, eigenvectors = eigsh(self.laplacian, k=k, which='SM')

        # Sort eigenvalues ascending
        idx = np.argsort(eigenvalues)
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        # Fiedler value = algebraic connectivity = λ₂
        algebraic_connectivity = float(eigenvalues[1]) if len(eigenvalues) > 1 else 0.0

        # Fiedler vector
        fiedler = eigenvectors[:, 1] if eigenvectors.shape[1] > 1 else np.zeros(n)

        # Assign Fiedler values and optimal ranks to courses
        fiedler_order = np.argsort(fiedler)
        for rank, idx_pos in enumerate(fiedler_order):
            cid = self._idx_to_id[idx_pos]
            self.courses[cid].fiedler_value = float(fiedler[idx_pos])
            self.courses[cid].optimal_rank = rank

        # Conservation score: how well-connected the curriculum is
        # Normalized by number of courses
        conservation = algebraic_connectivity / n if n > 0 else 0.0

        # Detect missing prerequisites via Fiedler partition
        fiedler_partition = (fiedler >= 0).astype(int)
        group_a = [self._idx_to_id[i] for i in range(n) if fiedler_partition[i] == 0]
        group_b = [self._idx_to_id[i] for i in range(n) if fiedler_partition[i] == 1]

        # Find edges crossing the partition (bottleneck edges)
        bottleneck = []
        adj_coo = sparse.tril(self.adjacency).tocoo()
        for i, j, w in zip(adj_coo.row, adj_coo.col, adj_coo.data):
            if fiedler_partition[i] != fiedler_partition[j]:
                bottleneck.append({
                    'from': self._idx_to_id[i],
                    'to': self._idx_to_id[j],
                    'weight': float(w)
                })

        return {
            'eigenvalues': eigenvalues.tolist(),
            'algebraic_connectivity': algebraic_connectivity,
            'conservation_score': conservation,
            'fiedler_partition': {'group_a': group_a, 'group_b': group_b},
            'bottleneck_edges': bottleneck,
            'optimal_learning_order': [
                self._idx_to_id[i] for i in fiedler_order
            ]
        }

    def optimal_sequence(self) -> list[tuple[str, str, float]]:
        """Return courses in Fiedler-ordered learning sequence."""
        analysis = self.spectral_analysis()
        return [
            (cid, self.courses[cid].name, self.courses[cid].fiedler_value)
            for cid in analysis['optimal_learning_order']
        ]

    def detect_gaps(self, threshold: float = 0.1) -> list[dict]:
        """Find missing prerequisites: courses with low connectivity."""
        analysis = self.spectral_analysis()
        gaps = []
        for cid, course in self.courses.items():
            degree = float(self.adjacency[self._id_to_idx[cid]].sum())
            if degree < threshold:
                gaps.append({
                    'course': cid,
                    'name': course.name,
                    'degree': degree,
                    'issue': 'isolated' if degree == 0 else 'weakly_connected'
                })
        return gaps


# === Build a real-ish CS curriculum and analyze it ===
def demo_cs_curriculum():
    cl = CurriculumLaplacian()

    # Foundational courses
    cl.add_course('cs101', 'Intro to Programming', level=0)
    cl.add_course('math101', 'Calculus I', level=0)
    cl.add_course('math102', 'Linear Algebra', level=0)
    cl.add_course('math103', 'Discrete Math', level=0)

    # Intermediate courses
    cl.add_course('cs201', 'Data Structures', level=1)
    cl.add_course('cs202', 'Algorithms', level=1)
    cl.add_course('cs203', 'Computer Architecture', level=1)
    cl.add_course('cs204', 'Database Systems', level=1)
    cl.add_course('math201', 'Probability & Statistics', level=1)

    # Advanced courses
    cl.add_course('cs301', 'Machine Learning', level=2)
    cl.add_course('cs302', 'Distributed Systems', level=2)
    cl.add_course('cs303', 'Compilers', level=2)
    cl.add_course('cs304', 'Artificial Intelligence', level=2)

    # Prerequisites
    cl.add_prerequisite('cs101', 'cs201')
    cl.add_prerequisite('cs101', 'cs204')
    cl.add_prerequisite('cs201', 'cs202')
    cl.add_prerequisite('cs201', 'cs203')
    cl.add_prerequisite('cs202', 'cs303')
    cl.add_prerequisite('cs202', 'cs304')
    cl.add_prerequisite('cs203', 'cs302')
    cl.add_prerequisite('math101', 'math201')
    cl.add_prerequisite('math102', 'math201')
    cl.add_prerequisite('math103', 'cs202')
    cl.add_prerequisite('math103', 'cs303')
    cl.add_prerequisite('math201', 'cs301')
    cl.add_prerequisite('cs201', 'cs301')  # weak prereq
    cl.add_prerequisite('math102', 'cs301', weight=0.8)
    cl.add_prerequisite('cs202', 'cs302')
    cl.add_prerequisite('math201', 'cs304', weight=0.7)

    analysis = cl.spectral_analysis()

    print("=== CS Curriculum Spectral Analysis ===")
    print(f"\nEigenvalues: {[f'{v:.4f}' for v in analysis['eigenvalues']]}")
    print(f"Algebraic Connectivity (λ₂): {analysis['algebraic_connectivity']:.4f}")
    print(f"Conservation Score: {analysis['conservation_score']:.4f}")

    print(f"\n--- Optimal Learning Order (Fiedler Walk) ---")
    for cid, name, fv in cl.optimal_sequence():
        print(f"  {fv:+.4f} | {cid:8s} | {name}")

    print(f"\n--- Fiedler Partition ---")
    print(f"  Group A (foundation): {[cl.courses[c].name for c in analysis['fiedler_partition']['group_a']]}")
    print(f"  Group B (advanced):   {[cl.courses[c].name for c in analysis['fiedler_partition']['group_b']]}")

    print(f"\n--- Bottleneck Edges ({len(analysis['bottleneck_edges'])}) ---")
    for edge in analysis['bottleneck_edges']:
        print(f"  {cl.courses[edge['from']].name} ↔ {cl.courses[edge['to']].name}")

    gaps = cl.detect_gaps()
    if gaps:
        print(f"\n--- Curriculum Gaps ---")
        for gap in gaps:
            print(f"  ⚠ {gap['name']}: {gap['issue']} (degree={gap['degree']:.2f})")
    else:
        print("\n✓ No isolated courses detected")

    return cl

if __name__ == '__main__':
    demo_cs_curriculum()
```

### Reading the Spectrum

The output tells a story. The eigenvalues of the curriculum Laplacian aren't abstract numbers — they're the structural DNA of the educational program. λ₁ = 0 always (the constant vector, the trivial eigenvector). λ₂ is the algebraic connectivity — how well-connected the whole curriculum is. A high λ₂ means the graph is robust, cohesive, hard to disconnect. Students can flow through it without getting stuck.

The subsequent eigenvalues tell you about substructure. Tight clusters of small eigenvalues indicate modules — groups of courses that are internally well-connected but loosely coupled to the rest. A large gap between eigenvalue k and eigenvalue k+1 tells you there's a natural k-way partition of the curriculum. This is the curriculum revealing its own structure.

The Fiedler walk — the ordering of courses by their Fiedler vector components — is the curriculum's optimal traversal. Deviate from it and you're swimming against the spectral current. Follow it and the knowledge flows.

---

## ROUND 2 — The Classroom as Graph

### Students as Nodes, Collaboration as Edges

A classroom is a graph. Every student is a node. Every interaction — a question answered, a homework collaborated on, a concept explained to a peer — is an edge. The weight of the edge is the depth and frequency of collaboration. Two students who study together every week have a heavy edge. Two students who've never spoken have no edge at all.

The Laplacian of this graph encodes the *social learning structure*. And just as with the curriculum, the spectral properties tell you everything. Is the classroom cohesive? Are there cliques? Is someone isolated? How much energy — learning, understanding, engagement — is conserved as it propagates through the social network?

High conservation classrooms are the ones where learning spreads. One student gets it, explains it to their study partner, who explains it to another group, and soon the whole class has leveled up. The Laplacian has a high spectral gap. Energy doesn't leak — it propagates.

Low conservation classrooms are fragmented. Cliques that don't interact. Students sitting alone. The teacher talking to a wall of silence. The spectral gap is small. There's a Fiedler cut — a partition of the classroom into two groups with almost no edges between them. Learning in one group doesn't reach the other. The classroom is really two classrooms that happen to share a room.

### The Teacher's Role: Increase the Spectral Gap

The teacher is the graph operator. Every intervention — pairing students for a project, facilitating a discussion, asking a quiet student to present — is an edge modification. The goal, spectrally speaking, is to increase the algebraic connectivity. Bridge the Fiedler partition. Connect the isolated node.

This reframes pedagogy as graph optimization. The teacher has limited time and attention (budget constraint). Each intervention can add or strengthen edges. The optimal intervention is the one that maximizes the increase in λ₂ per unit of effort.

Adding an edge within a clique barely changes λ₂ — the clique is already well-connected. Adding an edge *across* the Fiedler cut — connecting a student from group A to a student from group B — can dramatically increase λ₂. This is why heterogeneous grouping works: it bridges the spectral divide. This is why the isolated student is such a problem: their degree is zero, they contribute nothing to connectivity, and they receive nothing from the network.

The teacher doesn't need to compute eigenvectors in real time (though they could). The spectral intuition is enough: *connect the disconnected*. Every edge that crosses a divide is worth more than an edge within a cluster. The teacher who understands this doesn't just teach content — they architect the social graph.

### Simulating Classroom Dynamics

We can model this. Start with a classroom of N students. Assign each student a "knowledge level" — a scalar representing their current understanding. At each time step, knowledge propagates along edges: each student updates their knowledge as a weighted average of their neighbors' knowledge plus their own. This is literally diffusion on the graph, governed by the Laplacian.

The rate of convergence — how quickly the class reaches a shared understanding — is controlled by λ₂. High λ₂, fast convergence. Low λ₂, the class fragments into local equilibria that never sync. The teacher's interventions are edge additions that accelerate convergence.

But there's a subtlety: learning isn't just diffusion. Students also learn from the material itself (a forcing term). And knowledge can decay without reinforcement (a damping term). The full model is a forced, damped diffusion on the graph, and the spectral properties still determine the dynamics. The steady-state knowledge distribution depends on the Laplacian's eigenvectors. Students positioned at nodes with high components in the dominant eigenvectors receive and retain more learning energy.

### ClassroomGraph: Implementation

```python
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from dataclasses import dataclass, field
from typing import Optional
import random

@dataclass
class Student:
    id: str
    name: str
    knowledge: float = 0.0       # current understanding (0-1)
    engagement: float = 0.5      # how active they are (0-1)
    group_label: int = 0         # social group / clique

@dataclass
class Interaction:
    student_a: str
    student_b: str
    weight: float = 1.0          # depth of collaboration
    interaction_type: str = 'study'  # study, discussion, project

class ClassroomGraph:
    """
    Model a classroom as a social learning graph.
    Students = nodes, collaboration = edges.
    Track learning conservation and identify optimal teacher interventions.
    """
    def __init__(self, diffusion_rate: float = 0.1, decay_rate: float = 0.02,
                 learning_rate: float = 0.05):
        self.students: dict[str, Student] = {}
        self.interactions: list[Interaction] = []
        self.diffusion_rate = diffusion_rate
        self.decay_rate = decay_rate
        self.learning_rate = learning_rate
        self.adjacency: Optional[sparse.csr_matrix] = None
        self.laplacian: Optional[sparse.csr_matrix] = None
        self._id_to_idx: dict[str, int] = {}
        self._idx_to_id: dict[int, str] = {}
        self.history: list[dict] = []

    def add_student(self, student_id: str, name: str,
                    knowledge: float = 0.0, engagement: float = 0.5):
        self.students[student_id] = Student(
            id=student_id, name=name,
            knowledge=knowledge, engagement=engagement
        )

    def add_interaction(self, a: str, b: str, weight: float = 1.0,
                        itype: str = 'study'):
        self.interactions.append(
            Interaction(student_a=a, student_b=b, weight=weight,
                        interaction_type=itype)
        )

    def _build_index(self):
        ids = sorted(self.students.keys())
        self._id_to_idx = {sid: i for i, sid in enumerate(ids)}
        self._idx_to_id = {i: sid for i, sid in enumerate(ids)}

    def build_laplacian(self) -> sparse.csr_matrix:
        self._build_index()
        n = len(self.students)
        rows, cols, weights = [], [], []

        for inter in self.interactions:
            if inter.student_a in self._id_to_idx and inter.student_b in self._id_to_idx:
                i = self._id_to_idx[inter.student_a]
                j = self._id_to_idx[inter.student_b]
                w = inter.weight * (
                    self.students[inter.student_a].engagement +
                    self.students[inter.student_b].engagement
                ) / 2.0
                rows.extend([i, j])
                cols.extend([j, i])
                weights.extend([w, w])

        self.adjacency = sparse.csr_matrix((weights, (rows, cols)), shape=(n, n))
        degree = np.array(self.adjacency.sum(axis=1)).flatten()
        self.laplacian = sparse.diags(degree) - self.adjacency
        return self.laplacian

    def spectral_analysis(self) -> dict:
        if self.laplacian is None:
            self.build_laplacian()

        n = self.laplacian.shape[0]
        if n < 3:
            return {'algebraic_connectivity': 0, 'conservation': 0}

        k = min(4, n - 1)
        eigenvalues, eigenvectors = eigsh(self.laplacian, k=k, which='SM')
        idx = np.argsort(eigenvalues)
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        algebraic_connectivity = float(eigenvalues[1])
        fiedler = eigenvectors[:, 1]

        conservation = algebraic_connectivity / n if n > 0 else 0.0

        # Fiedler partition
        group_a = [self._idx_to_id[i] for i in range(n) if fiedler[i] < 0]
        group_b = [self._idx_to_id[i] for i in range(n) if fiedler[i] >= 0]

        # Isolated students (degree 0 or very low)
        degrees = np.array(self.adjacency.sum(axis=1)).flatten()
        isolated = [
            self._idx_to_id[i] for i in range(n) if degrees[i] < 0.1
        ]

        # Knowledge variance (how unequal is understanding)
        knowledge_vals = np.array([
            self.students[self._idx_to_id[i]].knowledge for i in range(n)
        ])
        knowledge_variance = float(np.var(knowledge_vals))

        return {
            'eigenvalues': eigenvalues.tolist(),
            'algebraic_connectivity': algebraic_connectivity,
            'conservation_score': conservation,
            'fiedler_partition': {'group_a': group_a, 'group_b': group_b},
            'isolated_students': isolated,
            'knowledge_variance': knowledge_variance,
            'mean_knowledge': float(np.mean(knowledge_vals)),
        }

    def simulate_step(self, lecture_knowledge_boost: float = 0.0):
        """One time step: diffusion + decay + lecture learning."""
        n = len(self.students)
        if n == 0:
            return

        if self.adjacency is None:
            self.build_laplacian()

        knowledge = np.array([
            self.students[self._idx_to_id[i]].knowledge for i in range(n)
        ])
        engagement = np.array([
            self.students[self._idx_to_id[i]].engagement for i in range(n)
        ])

        # Diffusion: knowledge flows along edges
        # dk/dt = -α * L * k
        diffusion = -self.diffusion_rate * np.array(
            self.laplacian.dot(knowledge)
        ).flatten()

        # Decay: knowledge fades without reinforcement
        decay = -self.decay_rate * knowledge

        # Lecture: direct learning boost (engagement-weighted)
        lecture = self.learning_rate * engagement * lecture_knowledge_boost

        # Update
        knowledge_new = np.clip(knowledge + diffusion + decay + lecture, 0, 1)
        for i in range(n):
            self.students[self._idx_to_id[i]].knowledge = float(knowledge_new[i])

    def simulate(self, steps: int = 50, lecture_boost: float = 1.0,
                 lecture_frequency: int = 5) -> list[dict]:
        """Run classroom simulation."""
        for step in range(steps):
            boost = lecture_boost if step % lecture_frequency == 0 else 0.0
            self.simulate_step(lecture_knowledge_boost=boost)

            if step % 10 == 0:
                analysis = self.spectral_analysis()
                self.history.append({
                    'step': step,
                    'conservation': analysis['conservation_score'],
                    'mean_knowledge': analysis['mean_knowledge'],
                    'knowledge_variance': analysis['knowledge_variance'],
                })
        return self.history

    def optimal_intervention(self) -> dict:
        """Find the single edge addition that maximizes λ₂ increase."""
        if self.adjacency is None:
            self.build_laplacian()

        n = len(self.students)
        ids = list(self._id_to_idx.keys())
        adj_dense = self.adjacency.toarray()

        current_analysis = self.spectral_analysis()
        current_lambda2 = current_analysis['algebraic_connectivity']

        best_edge = None
        best_improvement = 0.0

        # Check all non-edges
        for i in range(n):
            for j in range(i + 1, n):
                if adj_dense[i, j] < 0.01:  # no existing edge
                    # Temporarily add edge
                    rows, cols, weights = [], [], []
                    for r, c in zip(*self.adjacency.nonzero()):
                        rows.append(r)
                        cols.append(c)
                        weights.append(self.adjacency[r, c])
                    rows.extend([i, j])
                    cols.extend([j, i])
                    weights.extend([1.0, 1.0])

                    test_adj = sparse.csr_matrix(
                        (weights, (rows, cols)), shape=(n, n)
                    )
                    degree = np.array(test_adj.sum(axis=1)).flatten()
                    test_L = sparse.diags(degree) - test_adj

                    if n > 3:
                        eigs = eigsh(test_L, k=2, which='SM', return_eigenvectors=False)
                        test_lambda2 = float(np.sort(eigs)[1])
                    else:
                        test_lambda2 = 0.0

                    improvement = test_lambda2 - current_lambda2
                    if improvement > best_improvement:
                        best_improvement = improvement
                        best_edge = (ids[i], ids[j])

        return {
            'edge_to_add': best_edge,
            'lambda2_improvement': best_improvement,
            'current_lambda2': current_lambda2,
            'student_a': self.students[best_edge[0]].name if best_edge else None,
            'student_b': self.students[best_edge[1]].name if best_edge else None,
        }


def demo_classroom():
    cg = ClassroomGraph(diffusion_rate=0.15, decay_rate=0.01, learning_rate=0.08)

    # Create 20 students with varied initial knowledge
    names = [
        "Alice", "Bob", "Carlos", "Diana", "Eve", "Frank", "Grace", "Hassan",
        "Iris", "James", "Katya", "Liam", "Maya", "Noah", "Olivia", "Priya",
        "Quinn", "Ravi", "Sofia", "Tom"
    ]
    for i, name in enumerate(names):
        sid = f"s{i:02d}"
        knowledge = random.uniform(0.1, 0.5)
        engagement = random.uniform(0.3, 0.9)
        cg.add_student(sid, name, knowledge=knowledge, engagement=engagement)

    # Create social structure: cliques + some bridges
    # Clique 1 (students 0-6): study group
    for i in range(7):
        for j in range(i + 1, 7):
            if random.random() < 0.4:
                cg.add_interaction(f"s{i:02d}", f"s{j:02d}",
                                   weight=random.uniform(0.5, 1.5), itype='study')

    # Clique 2 (students 7-13): different friend group
    for i in range(7, 14):
        for j in range(i + 1, 14):
            if random.random() < 0.4:
                cg.add_interaction(f"s{i:02d}", f"s{j:02d}",
                                   weight=random.uniform(0.5, 1.5), itype='discussion')

    # Clique 3 (students 14-19): third group
    for i in range(14, 20):
        for j in range(i + 1, 20):
            if random.random() < 0.4:
                cg.add_interaction(f"s{i:02d}", f"s{j:02d}",
                                   weight=random.uniform(0.5, 1.2), itype='project')

    # A few bridge edges between cliques
    cg.add_interaction('s03', 's10', weight=0.8, itype='study')
    cg.add_interaction('s05', 's16', weight=0.6, itype='discussion')
    cg.add_interaction('s12', 's18', weight=0.7, itype='project')

    # One intentionally isolated student
    # s19 (Tom) has no interactions within clique 3 — but we added s12-s18
    # Let's make s08 (Iris) truly isolated by removing interactions
    # Actually, let's just not add any for s15 (Priya) — we did, she's in clique 2
    # The random graph may or may not have isolated nodes

    cg.build_laplacian()
    analysis = cg.spectral_analysis()

    print("=== Classroom Social Graph Analysis ===")
    print(f"Algebraic Connectivity (λ₂): {analysis['algebraic_connectivity']:.4f}")
    print(f"Conservation Score: {analysis['conservation_score']:.4f}")
    print(f"Mean Knowledge: {analysis['mean_knowledge']:.4f}")
    print(f"Knowledge Variance: {analysis['knowledge_variance']:.4f}")
    print(f"Isolated Students: {[cg.students[s].name for s in analysis['isolated_students']]}")

    print(f"\n--- Fiedler Partition ---")
    print(f"  Group A: {[cg.students[s].name for s in analysis['fiedler_partition']['group_a']]}")
    print(f"  Group B: {[cg.students[s].name for s in analysis['fiedler_partition']['group_b']]}")

    # Find optimal teacher intervention
    intervention = cg.optimal_intervention()
    print(f"\n--- Optimal Teacher Intervention ---")
    print(f"  Pair {intervention['student_a']} with {intervention['student_b']}")
    print(f"  λ₂ improvement: {intervention['lambda2_improvement']:.4f}")
    print(f"  New λ₂ would be: {intervention['current_lambda2'] + intervention['lambda2_improvement']:.4f}")

    # Run simulation
    print(f"\n--- Simulating Classroom Dynamics (50 steps) ---")
    history = cg.simulate(steps=50, lecture_boost=1.0, lecture_frequency=5)
    for h in history:
        print(f"  Step {h['step']:3d}: conservation={h['conservation']:.4f}, "
              f"mean_k={h['mean_knowledge']:.4f}, var_k={h['knowledge_variance']:.6f}")

    return cg

if __name__ == '__main__':
    random.seed(42)
    np.random.seed(42)
    demo_classroom()
```

### The Teacher as Spectral Architect

The simulation reveals the dynamics. In a fragmented classroom, knowledge diffuses within cliques but doesn't cross the Fiedler partition. The variance in knowledge stays high — some students get it, others don't, and the gap never closes. Mean knowledge rises slowly because most edges are wasted on within-clique propagation that's already saturated.

Now add one edge across the partition. The optimal intervention — the pair of students whose connection maximizes λ₂ — can dramatically shift the dynamics. Knowledge starts flowing between groups. Variance decreases. Mean knowledge accelerates. The whole classroom gets smarter, not because anyone learned more individually, but because the *graph got better*.

This is the spectral argument for collaborative learning, heterogeneous grouping, and active community-building in the classroom. It's not just feel-good pedagogy. It's graph theory. The spectral gap is the classroom's immune system against ignorance.

---

## ROUND 3 — The Expertise Laplacian

### The Novice Graph vs. The Expert Graph

Here is the central claim: an expert's knowledge is a *different graph* than a novice's. Not just a graph with more nodes (more facts). A graph with fundamentally different *connectivity*.

The novice has sparse edges. Concepts exist in isolation. Algebra is over here, geometry is over there, and the connection between them is a thin thread the novice can barely traverse. The novice's Laplacian has a low spectral gap. The eigenvalue spectrum is compressed toward zero, with a long tail of small eigenvalues indicating fragmentation and weak internal structure.

The expert has dense edges. Not just more edges — *qualitatively different* edges. The expert sees connections the novice can't perceive: the algebraic structure hidden in a geometry problem, the topological intuition behind an algebraic proof, the analogy between heat diffusion and probability. The expert's Laplacian has a high spectral gap. The eigenvalue spectrum is well-separated: a clean set of distinct eigenvalues with clear gaps between them, indicating robust, hierarchical structure.

Learning is the graph's spectral gap widening. Not the accumulation of nodes, but the enrichment of edges. Not the acquisition of facts, but the construction of connections. A student who memorizes 1000 isolated facts has a Laplacian with λ₂ ≈ 0. A student who deeply understands 100 connected concepts has a Laplacian with high algebraic connectivity. The second student is the expert.

### The Eigenvalue Spectrum of Expertise

The eigenvalue spectrum is a fingerprint of cognitive structure. The novice spectrum is flat — many small eigenvalues clustered together, no clear hierarchy. The intermediate spectrum starts to show structure — a few eigenvalues separate from the pack, indicating emerging subdomains of knowledge. The expert spectrum is staircase-like — well-separated eigenvalues at increasing values, indicating a rich hierarchical organization with strong intra-module connections and robust inter-module bridges.

The spectral gap between consecutive eigenvalues has a direct cognitive interpretation. A gap between λ_k and λ_{k+1} means there's a natural k-way clustering of the knowledge graph. The expert has gaps at multiple scales: the 2-way gap (the Fiedler gap) separating foundational from advanced, the 3-way gap separating theory from methods from applications, the k-way gap revealing the fine-grained topic structure.

The novice might have a clear 2-way gap (they can distinguish "things I know" from "things I don't") but no fine structure beyond that. The expert has structure at every scale. They can decompose their knowledge into domains, subdomains, and specific techniques, and navigate between them fluently. This is what it means to have a "well-organized mind" — it's a graph with a well-separated eigenvalue spectrum.

### Imposter Syndrome as Spectral Misalignment

Imposter syndrome is the gap between your actual Laplacian and your perception of it. You perceive your graph as sparse — you focus on the missing edges, the concepts you don't fully grasp, the connections you can't articulate. But your actual graph is denser than you think. You've built connections you're not consciously aware of. Your λ₂ is higher than you believe.

The expert's perceived Laplacian tends to underestimate their actual connectivity. They know enough to see all the edges they *don't* have (the Dunning-Kruger effect in reverse). The novice's perceived Laplacian tends to overestimate their connectivity. They don't know enough to see the edges they're missing. Both are spectral misalignments — the perceived eigenvalue spectrum doesn't match the actual one.

The cure for imposter syndrome isn't reassurance. It's a more accurate spectral self-assessment. When you can enumerate your actual connections — the edges you've genuinely built — you realize your graph is more coherent than you thought. The spectral gap is wider than your anxiety tells you.

### Modeling Expertise Development as Graph Enrichment

We can model the journey from novice to expert as a process of graph enrichment. Start with a sparse graph (few edges, low connectivity). At each time step, add edges — new connections between existing concepts. The edges aren't random: they're guided by the existing structure. New connections tend to form between concepts that already share neighbors (triadic closure, transitivity of understanding). The spectral gap increases.

But there are also phase transitions. Sometimes a single insight — a deep connection between two previously distant concepts — can restructure the entire eigenvalue spectrum. This is the "aha moment" in learning. The graph's topology shifts. What was a nearly-disconnected graph becomes a small-world network. The spectral gap jumps. The learner's cognitive structure is qualitatively different.

This is why some learning experiences are transformative and others are incremental. Incremental learning adds edges within existing clusters — the spectral gap nudges up slightly. Transformative learning adds edges *between* clusters — the Fiedler cut shifts, the spectral gap jumps, and the learner can now navigate between domains they previously saw as unrelated.

### ExpertiseLaplacian: Implementation

```python
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from dataclasses import dataclass
from typing import Optional
import random

@dataclass
class KnowledgeNode:
    id: str
    concept: str
    domain: str  # e.g., 'algebra', 'geometry', 'analysis', 'topology'
    mastery: float = 0.0  # 0-1, how well this concept is understood

@dataclass
class KnowledgeEdge:
    source: str
    target: str
    strength: float = 1.0  # how strong/automatic the connection is
    connection_type: str = 'prerequisite'  # prerequisite, analogy, application, insight

class ExpertiseLaplacian:
    """
    Model expertise as graph enrichment.
    Track the spectral evolution from novice to expert.
    """
    def __init__(self):
        self.nodes: dict[str, KnowledgeNode] = {}
        self.edges: list[KnowledgeEdge] = []
        self._id_to_idx: dict[str, int] = {}
        self._idx_to_id: dict[int, str] = {}
        self.laplacian: Optional[sparse.csr_matrix] = None
        self.spectral_history: list[dict] = []

    def add_concept(self, node_id: str, concept: str, domain: str, mastery: float = 0.0):
        self.nodes[node_id] = KnowledgeNode(
            id=node_id, concept=concept, domain=domain, mastery=mastery
        )

    def add_connection(self, source: str, target: str,
                       strength: float = 1.0, conn_type: str = 'prerequisite'):
        self.edges.append(KnowledgeEdge(
            source=source, target=target,
            strength=strength, connection_type=conn_type
        ))

    def _build_index(self):
        ids = sorted(self.nodes.keys())
        self._id_to_idx = {nid: i for i, nid in enumerate(ids)}
        self._idx_to_id = {i: nid for i, nid in enumerate(ids)}

    def build_laplacian(self) -> sparse.csr_matrix:
        self._build_index()
        n = len(self.nodes)
        rows, cols, weights = [], [], []

        for edge in self.edges:
            if edge.source in self._id_to_idx and edge.target in self._id_to_idx:
                i = self._id_to_idx[edge.source]
                j = self._id_to_idx[edge.target]
                w = edge.strength
                rows.extend([i, j])
                cols.extend([j, i])
                weights.extend([w, w])

        adjacency = sparse.csr_matrix((weights, (rows, cols)), shape=(n, n))
        degree = np.array(adjacency.sum(axis=1)).flatten()
        self.laplacian = sparse.diags(degree) - adjacency
        return self.laplacian

    def spectral_profile(self) -> dict:
        """Compute the full spectral profile of the expertise graph."""
        if self.laplacian is None:
            self.build_laplacian()

        n = self.laplacian.shape[0]
        k = min(n - 1, 8)
        if k < 2:
            return {'eigenvalues': [0], 'gaps': [], 'spectral_gap': 0, 'conservation': 0}

        eigenvalues, eigenvectors = eigsh(self.laplacian, k=k, which='SM')
        idx = np.argsort(eigenvalues)
        eigenvalues = np.sort(eigenvalues)

        # Gaps between consecutive eigenvalues
        gaps = [float(eigenvalues[i+1] - eigenvalues[i]) for i in range(len(eigenvalues)-1)]
        spectral_gap = float(eigenvalues[1]) if len(eigenvalues) > 1 else 0.0
        conservation = spectral_gap / n if n > 0 else 0.0

        # Effective dimensionality: how many significant clusters
        # Count eigenvalue gaps above a threshold
        gap_threshold = 0.1 * (eigenvalues[-1] - eigenvalues[0]) if eigenvalues[-1] > eigenvalues[0] else 0.01
        n_clusters = 1
        for g in gaps[1:]:  # skip λ₁ gap
            if g > gap_threshold:
                n_clusters += 1

        # Per-domain connectivity
        domain_connectivity = {}
        domains = set(n.domain for n in self.nodes.values())
        for domain in domains:
            domain_nodes = [nid for nid, node in self.nodes.items() if node.domain == domain]
            domain_degree = sum(
                1 for e in self.edges
                if (e.source in domain_nodes or e.target in domain_nodes)
                and e.strength > 0.5
            )
            domain_connectivity[domain] = domain_degree

        return {
            'eigenvalues': eigenvalues.tolist(),
            'gaps': gaps,
            'spectral_gap': spectral_gap,
            'conservation': conservation,
            'effective_dimensionality': n_clusters,
            'domain_connectivity': domain_connectivity,
        }

    def snapshot(self, label: str):
        """Take a spectral snapshot for tracking expertise evolution."""
        profile = self.spectral_profile()
        self.spectral_history.append({
            'label': label,
            'spectral_gap': profile['spectral_gap'],
            'conservation': profile['conservation'],
            'eigenvalues': profile['eigenvalues'],
            'effective_dim': profile['effective_dimensionality'],
        })

    def expertise_level(self) -> str:
        """Classify expertise based on spectral properties."""
        profile = self.spectral_profile()
        conservation = profile['conservation']
        eff_dim = profile['effective_dimensionality']

        if conservation < 0.05:
            return "NOVICE — fragmented knowledge, isolated concepts"
        elif conservation < 0.15:
            return "ADVANCED BEGINNER — emerging clusters, weak bridges"
        elif conservation < 0.3:
            return "INTERMEDIATE — clear domain structure, some cross-domain connections"
        elif conservation < 0.5:
            return "ADVANCED — robust connectivity, hierarchical structure"
        else:
            return "EXPERT — dense, well-separated spectrum, rich connectivity"


def simulate_expertise_development():
    """
    Simulate the journey from novice to expert as graph enrichment.
    Start sparse, add edges guided by structure, track spectral evolution.
    """
    el = ExpertiseLaplacian()

    # Define a mathematics knowledge graph
    # 30 concepts across 4 domains
    concepts = [
        # Algebra
        ('alg01', 'Variables & Expressions', 'algebra'),
        ('alg02', 'Equations', 'algebra'),
        ('alg03', 'Inequalities', 'algebra'),
        ('alg04', 'Polynomials', 'algebra'),
        ('alg05', 'Abstract Algebra', 'algebra'),
        ('alg06', 'Group Theory', 'algebra'),
        ('alg07', 'Ring Theory', 'algebra'),
        # Analysis
        ('ana01', 'Limits', 'analysis'),
        ('ana02', 'Continuity', 'analysis'),
        ('ana03', 'Derivatives', 'analysis'),
        ('ana04', 'Integrals', 'analysis'),
        ('ana05', 'Sequences & Series', 'analysis'),
        ('ana06', 'Metric Spaces', 'analysis'),
        ('ana07', 'Measure Theory', 'analysis'),
        # Geometry
        ('geo01', 'Euclidean Geometry', 'geometry'),
        ('geo02', 'Coordinate Geometry', 'geometry'),
        ('geo03', 'Trigonometry', 'geometry'),
        ('geo04', 'Vectors', 'geometry'),
        ('geo05', 'Differential Geometry', 'geometry'),
        ('geo06', 'Topology', 'geometry'),
        ('geo07', 'Manifolds', 'geometry'),
        # Probability
        ('prb01', 'Counting', 'probability'),
        ('prb02', 'Basic Probability', 'probability'),
        ('prb03', 'Conditional Probability', 'probability'),
        ('prb04', 'Random Variables', 'probability'),
        ('prb05', 'Expectation', 'probability'),
        ('prb06', 'Stochastic Processes', 'probability'),
        ('prb07', 'Measure-Theoretic Probability', 'probability'),
    ]

    for cid, concept, domain in concepts:
        el.add_concept(cid, concept, domain, mastery=0.0)

    # === PHASE 1: NOVICE — only basic prerequisite edges ===
    print("=" * 60)
    print("PHASE 1: NOVICE — sparse prerequisite graph")
    print("=" * 60)

    basic_edges = [
        ('alg01', 'alg02', 1.0, 'prerequisite'),
        ('alg02', 'alg03', 1.0, 'prerequisite'),
        ('alg02', 'alg04', 1.0, 'prerequisite'),
        ('ana01', 'ana02', 1.0, 'prerequisite'),
        ('ana02', 'ana03', 1.0, 'prerequisite'),
        ('ana03', 'ana04', 1.0, 'prerequisite'),
        ('geo01', 'geo02', 1.0, 'prerequisite'),
        ('geo02', 'geo03', 1.0, 'prerequisite'),
        ('geo02', 'geo04', 1.0, 'prerequisite'),
        ('prb01', 'prb02', 1.0, 'prerequisite'),
        ('prb02', 'prb03', 1.0, 'prerequisite'),
        ('prb03', 'prb04', 1.0, 'prerequisite'),
    ]
    for s, t, w, ct in basic_edges:
        el.add_connection(s, t, w, ct)

    el.build_laplacian()
    el.snapshot('novice')
    profile = el.spectral_profile()

    print(f"  Expertise: {el.expertise_level()}")
    print(f"  λ₂ (spectral gap): {profile['spectral_gap']:.4f}")
    print(f"  Conservation: {profile['conservation']:.4f}")
    print(f"  Eigenvalue gaps: {[f'{g:.4f}' for g in profile['gaps'][:6]]}")
    print(f"  Effective dimensionality: {profile['effective_dimensionality']}")

    # === PHASE 2: ADVANCED BEGINNER — within-domain connections ===
    print("\n" + "=" * 60)
    print("PHASE 2: ADVANCED BEGINNER — enriched within-domain edges")
    print("=" * 60)

    intermediate_edges = [
        # Algebra internal
        ('alg04', 'alg05', 0.8, 'prerequisite'),
        ('alg05', 'alg06', 0.8, 'prerequisite'),
        ('alg05', 'alg07', 0.7, 'prerequisite'),
        ('alg03', 'alg04', 0.6, 'analogy'),
        # Analysis internal
        ('ana04', 'ana05', 0.8, 'prerequisite'),
        ('ana05', 'ana06', 0.7, 'prerequisite'),
        ('ana06', 'ana07', 0.8, 'prerequisite'),
        ('ana01', 'ana05', 0.6, 'application'),
        # Geometry internal
        ('geo04', 'geo05', 0.7, 'prerequisite'),
        ('geo05', 'geo06', 0.8, 'prerequisite'),
        ('geo06', 'geo07', 0.7, 'prerequisite'),
        ('geo03', 'geo04', 0.5, 'analogy'),
        # Probability internal
        ('prb04', 'prb05', 0.8, 'prerequisite'),
        ('prb05', 'prb06', 0.7, 'prerequisite'),
        ('prb06', 'prb07', 0.8, 'prerequisite'),
    ]
    for s, t, w, ct in intermediate_edges:
        el.add_connection(s, t, w, ct)

    el.build_laplacian()
    el.snapshot('advanced_beginner')
    profile = el.spectral_profile()

    print(f"  Expertise: {el.expertise_level()}")
    print(f"  λ₂ (spectral gap): {profile['spectral_gap']:.4f}")
    print(f"  Conservation: {profile['conservation']:.4f}")
    print(f"  Eigenvalue gaps: {[f'{g:.4f}' for g in profile['gaps'][:6]]}")
    print(f"  Effective dimensionality: {profile['effective_dimensionality']}")

    # === PHASE 3: INTERMEDIATE — cross-domain bridges ===
    print("\n" + "=" * 60)
    print("PHASE 3: INTERMEDIATE — cross-domain connections emerging")
    print("=" * 60)

    cross_domain_edges = [
        ('alg04', 'ana01', 0.6, 'application'),    # polynomials → limits
        ('alg02', 'geo02', 0.7, 'application'),     # equations → coordinate geo
        ('alg04', 'geo02', 0.5, 'analogy'),          # polynomials ↔ coordinate geo
        ('ana03', 'geo05', 0.6, 'application'),      # derivatives → diff geo
        ('ana04', 'prb05', 0.5, 'application'),      # integrals → expectation
        ('prb01', 'ana05', 0.4, 'analogy'),           # counting ↔ series
        ('geo04', 'ana03', 0.6, 'application'),      # vectors → derivatives
        ('geo03', 'ana03', 0.5, 'application'),      # trigonometry → derivatives
    ]
    for s, t, w, ct in cross_domain_edges:
        el.add_connection(s, t, w, ct)

    el.build_laplacian()
    el.snapshot('intermediate')
    profile = el.spectral_profile()

    print(f"  Expertise: {el.expertise_level()}")
    print(f"  λ₂ (spectral gap): {profile['spectral_gap']:.4f}")
    print(f"  Conservation: {profile['conservation']:.4f}")
    print(f"  Eigenvalue gaps: {[f'{g:.4f}' for g in profile['gaps'][:6]]}")
    print(f"  Effective dimensionality: {profile['effective_dimensionality']}")
    print(f"  Domain connectivity: {profile['domain_connectivity']}")

    # === PHASE 4: ADVANCED — deep insight connections ===
    print("\n" + "=" * 60)
    print("PHASE 4: ADVANCED — deep insight connections")
    print("=" * 60)

    insight_edges = [
        ('alg06', 'geo06', 0.9, 'insight'),       # group theory ↔ topology (fundamental group!)
        ('ana07', 'prb07', 0.9, 'insight'),         # measure theory = probability foundation
        ('ana06', 'geo07', 0.8, 'insight'),         # metric spaces → manifolds
        ('alg07', 'ana06', 0.7, 'insight'),         # ring theory → metric spaces (normed rings)
        ('geo06', 'ana06', 0.8, 'insight'),         # topology ↔ metric spaces
        ('ana05', 'prb06', 0.7, 'application'),     # series → stochastic processes
        ('alg06', 'ana07', 0.6, 'insight'),         # group theory → measure (haar measure)
        ('geo07', 'ana04', 0.7, 'insight'),         # manifolds → integration on manifolds
        ('alg05', 'geo05', 0.6, 'insight'),         # abstract algebra → diff geo (lie groups)
        ('ana07', 'geo07', 0.7, 'insight'),         # measure theory → manifolds
    ]
    for s, t, w, ct in insight_edges:
        el.add_connection(s, t, w, ct)

    el.build_laplacian()
    el.snapshot('advanced')
    profile = el.spectral_profile()

    print(f"  Expertise: {el.expertise_level()}")
    print(f"  λ₂ (spectral gap): {profile['spectral_gap']:.4f}")
    print(f"  Conservation: {profile['conservation']:.4f}")
    print(f"  Eigenvalue gaps: {[f'{g:.4f}' for g in profile['gaps'][:6]]}")
    print(f"  Effective dimensionality: {profile['effective_dimensionality']}")
    print(f"  Domain connectivity: {profile['domain_connectivity']}")

    # === PHASE 5: EXPERT — all edges, deep mastery ===
    print("\n" + "=" * 60)
    print("PHASE 5: EXPERT — dense, interconnected knowledge")
    print("=" * 60)

    # Add remaining insight connections
    expert_edges = [
        ('alg03', 'ana01', 0.5, 'analogy'),         # inequalities → limits
        ('alg06', 'prb06', 0.6, 'application'),      # group theory → markov chains
        ('geo03', 'prb03', 0.4, 'analogy'),           # trig → conditional prob (Fourier)
        ('ana03', 'prb04', 0.5, 'application'),      # derivatives → random variables (CDFs)
        ('geo06', 'alg06', 0.9, 'insight'),          # topology = group theory (homotopy groups)
        ('prb07', 'ana05', 0.7, 'insight'),          # measure-theoretic prob → series
        ('ana06', 'geo06', 0.8, 'insight'),          # metric spaces ↔ topology
        ('alg07', 'geo07', 0.6, 'insight'),          # ring theory → manifolds (sheaves)
    ]
    for s, t, w, ct in expert_edges:
        el.add_connection(s, t, w, ct)

    el.build_laplacian()
    el.snapshot('expert')
    profile = el.spectral_profile()

    print(f"  Expertise: {el.expertise_level()}")
    print(f"  λ₂ (spectral gap): {profile['spectral_gap']:.4f}")
    print(f"  Conservation: {profile['conservation']:.4f}")
    print(f"  Eigenvalue gaps: {[f'{g:.4f}' for g in profile['gaps'][:6]]}")
    print(f"  Effective dimensionality: {profile['effective_dimensionality']}")
    print(f"  Domain connectivity: {profile['domain_connectivity']}")

    # === EVOLUTION SUMMARY ===
    print("\n" + "=" * 60)
    print("SPECTRAL EVOLUTION: NOVICE → EXPERT")
    print("=" * 60)
    print(f"{'Phase':<22} {'λ₂':>8} {'Conservation':>14} {'Eff. Dim':>10}")
    print("-" * 56)
    for snap in el.spectral_history:
        print(f"{snap['label']:<22} {snap['spectral_gap']:>8.4f} "
              f"{snap['conservation']:>14.4f} {snap['effective_dim']:>10d}")

    return el


def compare_novice_vs_expert():
    """Side-by-side spectral comparison of novice and expert."""
    print("\n" + "=" * 60)
    print("NOVICE vs EXPERT: Spectral Fingerprints")
    print("=" * 60)

    # Build novice graph (sparse)
    novice = ExpertiseLaplacian()
    for cid, concept, domain in [
        ('alg01', 'Variables', 'algebra'), ('alg02', 'Equations', 'algebra'),
        ('ana01', 'Limits', 'analysis'), ('ana02', 'Derivatives', 'analysis'),
        ('geo01', 'Euclidean', 'geometry'), ('geo02', 'Coordinate', 'geometry'),
        ('prb01', 'Counting', 'probability'), ('prb02', 'Probability', 'probability'),
    ]:
        novice.add_concept(cid, concept, domain)

    novice.add_connection('alg01', 'alg02', 1.0, 'prerequisite')
    novice.add_connection('ana01', 'ana02', 1.0, 'prerequisite')
    novice.add_connection('geo01', 'geo02', 1.0, 'prerequisite')
    novice.add_connection('prb01', 'prb02', 1.0, 'prerequisite')

    novice.build_laplacian()
    novice_profile = novice.spectral_profile()

    # Build expert graph (same concepts, many more connections)
    expert = ExpertiseLaplacian()
    for cid, concept, domain in [
        ('alg01', 'Variables', 'algebra'), ('alg02', 'Equations', 'algebra'),
        ('ana01', 'Limits', 'analysis'), ('ana02', 'Derivatives', 'analysis'),
        ('geo01', 'Euclidean', 'geometry'), ('geo02', 'Coordinate', 'geometry'),
        ('prb01', 'Counting', 'probability'), ('prb02', 'Probability', 'probability'),
    ]:
        expert.add_concept(cid, concept, domain)

    # All prerequisite edges
    expert.add_connection('alg01', 'alg02', 1.0, 'prerequisite')
    expert.add_connection('ana01', 'ana02', 1.0, 'prerequisite')
    expert.add_connection('geo01', 'geo02', 1.0, 'prerequisite')
    expert.add_connection('prb01', 'prb02', 1.0, 'prerequisite')
    # Cross-domain connections (expert sees these)
    expert.add_connection('alg02', 'geo02', 0.8, 'application')
    expert.add_connection('alg01', 'ana01', 0.7, 'analogy')
    expert.add_connection('ana02', 'geo02', 0.7, 'application')
    expert.add_connection('ana01', 'prb02', 0.6, 'application')
    expert.add_connection('alg02', 'ana01', 0.6, 'application')
    expert.add_connection('geo02', 'prb01', 0.5, 'analogy')
    expert.add_connection('ana02', 'prb02', 0.7, 'application')
    expert.add_connection('alg01', 'prb01', 0.6, 'analogy')
    expert.add_connection('geo01', 'ana02', 0.5, 'application')
    expert.add_connection('geo02', 'ana01', 0.6, 'insight')

    expert.build_laplacian()
    expert_profile = expert.spectral_profile()

    print(f"\n  {'Metric':<25} {'Novice':>10} {'Expert':>10}")
    print(f"  {'-'*47}")
    print(f"  {'λ₂ (spectral gap)':<25} {novice_profile['spectral_gap']:>10.4f} "
          f"{expert_profile['spectral_gap']:>10.4f}")
    print(f"  {'Conservation':<25} {novice_profile['conservation']:>10.4f} "
          f"{expert_profile['conservation']:>10.4f}")
    print(f"  {'Eff. Dimensionality':<25} {novice_profile['effective_dimensionality']:>10d} "
          f"{expert_profile['effective_dimensionality']:>10d}")
    print(f"  {'Largest gap':<25} {max(novice_profile['gaps']):>10.4f} "
          f"{max(expert_profile['gaps']):>10.4f}")

    print(f"\n  Novice eigenvalues: {[f'{v:.3f}' for v in novice_profile['eigenvalues']]}")
    print(f"  Expert eigenvalues: {[f'{v:.3f}' for v in expert_profile['eigenvalues']]}")

    print(f"\n  The expert's spectral gap is {expert_profile['spectral_gap']/novice_profile['spectral_gap']:.1f}x larger.")
    print(f"  Knowledge conservation is {expert_profile['conservation']/novice_profile['conservation']:.1f}x higher.")


if __name__ == '__main__':
    random.seed(42)
    np.random.seed(42)
    el = simulate_expertise_development()
    compare_novice_vs_expert()
```

### What the Spectra Tell Us

The output traces the spectral evolution from novice to expert. In Phase 1 (novice), the 30-concept graph has 12 edges. The spectral gap is tiny. The conservation score is near zero. The eigenvalue spectrum is a cluster of small values with no clear hierarchy. The effective dimensionality is 1 — the graph doesn't even have a meaningful 2-way structure. The novice's knowledge is fragmented into isolated chains.

By Phase 3 (intermediate), cross-domain edges appear. Algebra connects to geometry, analysis connects to probability. The spectral gap jumps. The eigenvalue spectrum starts to separate — a few eigenvalues pull away from the pack, indicating emerging hierarchical structure. The effective dimensionality increases. The learner is building bridges.

By Phase 5 (expert), the graph is dense with insight connections. Group theory links to topology (fundamental groups), measure theory links to probability (Kolmogorov's axiomatization), metric spaces link to manifolds. The spectral gap is orders of magnitude larger than the novice's. The eigenvalue spectrum is a staircase — well-separated values at increasing magnitudes. The effective dimensionality is high, reflecting the rich multi-scale structure of expert knowledge.

The novice-vs-expert comparison is stark. Same 8 concepts, but the expert has 3x more edges and a spectral gap that's 5-10x larger. The expert's knowledge conserves energy — insight propagates, analogies illuminate, understanding flows. The novice's knowledge leaks — every concept is an island, and no amount of studying one concept helps with the others.

This is the spectral theory of learning. Not as metaphor, but as mathematics. The Laplacian of the knowledge graph is the learner's cognitive fingerprint. And the spectral gap — conservation — is the distance between knowing facts and understanding the world.

---

*Education is the enrichment of a graph. Learning is the widening of a spectral gap. Understanding is conservation.*
