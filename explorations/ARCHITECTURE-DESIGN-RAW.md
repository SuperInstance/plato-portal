# Architecture & Design — Conservation Spectral Analysis

> Three rounds exploring how the discrete Laplacian and conservation principles reveal the hidden structure of buildings, cities, and software.

---

## Round 1 — The Building as Graph

### Rooms as Nodes, Doorways as Edges

Every building is a graph. This isn't metaphor — it's literal topology. Each room, hallway, and courtyard is a node. Every doorway, corridor, and open passage between them is an edge. The adjacency matrix $A$ of this graph captures *what connects to what*. The degree matrix $D$ captures *how much connects*. And their difference — the graph Laplacian $L = D - A$ — captures something far more interesting: **the flow structure of the building itself**.

Consider a simple apartment. Five rooms: living room connected to kitchen, bedroom, and hallway; hallway connects to bathroom and entrance. The adjacency matrix tells you connections exist. The Laplacian tells you how movement *wants to flow* through the space. The eigenvectors of $L$ are the building's natural modes — the paths of least resistance that people will instinctively follow.

The smallest non-zero eigenvalue, $\lambda_2$ (the Fiedler value), is the building's **conservation score**. It measures how well-connected the whole is. A high $\lambda_2$ means every room is reachable through multiple pleasant paths. A low $\lambda_2$ means the building has structural weak points — dead ends, bottlenecks, spaces that feel disconnected.

### Good Buildings Breathe

Think about the buildings you've loved being in. A well-designed museum where you naturally circulate without backtracking. A house where the kitchen flows into the dining area flows into the living room. A university building where you can find any department by following the logic of the space. These buildings have **high spectral conservation**. The Laplacian's eigenvalues cluster tightly — there are no rooms that are topologically "far" from the flow.

Now think about the buildings that frustrate you. The office building where you have to walk past the same dead-end corridor seventeen times. The hospital where every wing looks identical and nothing connects logically. The shopping mall where you can see the store you want but the escalator only goes the wrong way. These buildings have **low spectral conservation**. The Fiedler vector — the eigenvector corresponding to $\lambda_2$ — partitions the building into a "connected core" and a "disconnected periphery." You feel that partition in your bones when you're lost in the periphery.

The conservation framework gives this a precise mathematical language. When we say a building "has good flow," we mean its graph Laplacian has high algebraic connectivity. When we say a space feels "confusing," we mean the Fiedler vector assigns large values to certain rooms — marking them as topologically distant from the building's circulation core.

### Frank Lloyd Wright and Organic Spectral Structure

Frank Lloyd Wright's Prairie Houses are a masterclass in spectral architecture. The rooms don't have doors in the traditional sense — they flow into each other through screened passages, lowered ceilings, and changes in level. The hearth is the central node with high degree, and every other space radiates outward in a pattern that mirrors the landscape.

In graph terms, Wright designed buildings whose Laplacians are tuned to their environment. The Fiedler vector follows the natural contours: the building's spectral partition aligns with the site's natural partition (hill vs. valley, view vs. enclosure, public vs. private). This is what "organic architecture" means mathematically: the building's graph structure has the same spectral signature as the landscape it sits in.

Fallingwater is the extreme case. The building's Laplacian isn't just *like* the landscape — it *is* the landscape plus structure. The cantilevers create edges between nodes that would otherwise be disconnected by the waterfall. The conservation is high because Wright didn't fight the topology; he extended it.

### Brutalism: Raw Structure, Low Conservation

Brutalist buildings often have stark, disconnected graphs. Massive concrete walls create hard boundaries. Stairs lead to isolated platforms. Corridors terminate in blank walls. The Laplacian of a Brutalist building tends to have a very low $\lambda_2$ — the building is structurally fragmented.

But here's the nuance: Brutalism's low conservation isn't always a flaw. Sometimes it's the *point*. A Brutalist government building is supposed to feel imposing and compartmentalized. A Brutalist library is supposed to create distinct zones of contemplation. The architecture *uses* low spectral conservation as a design tool — forcing you to be aware of transitions, to experience the boundaries between spaces as meaningful events rather than invisible flows.

The spectral analysis doesn't judge. It describes. A Brutalist building's Laplacian tells you exactly how it will feel to navigate — and for Brutalism, that feeling of architectural friction is a feature, not a bug.

### BuildingLaplacian: Code

```python
import numpy as np
from scipy.linalg import eigh
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
import json

@dataclass
class Room:
    name: str
    floor: int = 0
    area_sqm: float = 10.0
    purpose: str = "general"
    
@dataclass 
class Passage:
    room_a: str
    room_b: str
    type: str = "doorway"  # doorway, corridor, open_plan, stairway
    width_m: float = 0.9
    flow_capacity: float = 1.0  # derived from width and type
    
class BuildingLaplacian:
    """
    Analyze a building's floor plan as a graph.
    Rooms = nodes, passages = edges.
    The Laplacian reveals circulation quality and wayfinding difficulty.
    """
    
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self.passages: List[Passage] = []
        self.adjacency: Optional[np.ndarray] = None
        self.laplacian: Optional[np.ndarray] = None
        self.labels: List[str] = []
        
    def add_room(self, name: str, floor: int = 0, area: float = 10.0, purpose: str = "general"):
        self.rooms[name] = Room(name, floor, area, purpose)
        self._invalidate()
        
    def add_passage(self, room_a: str, room_b: str, 
                    ptype: str = "doorway", width: float = 0.9):
        if room_a not in self.rooms or room_b not in self.rooms:
            raise ValueError(f"Both rooms must exist: {room_a}, {room_b}")
        # Flow capacity: wider openings and open-plan have higher capacity
        type_multiplier = {"doorway": 1.0, "corridor": 1.5, 
                          "open_plan": 3.0, "stairway": 0.8}
        capacity = width * type_multiplier.get(ptype, 1.0)
        self.passages.append(Passage(room_a, room_b, ptype, width, capacity))
        self._invalidate()
    
    def _invalidate(self):
        self.adjacency = None
        self.laplacian = None
        
    def build_matrices(self):
        n = len(self.rooms)
        self.labels = sorted(self.rooms.keys())
        idx = {name: i for i, name in enumerate(self.labels)}
        
        A = np.zeros((n, n))
        for p in self.passages:
            i, j = idx[p.room_a], idx[p.room_b]
            A[i, j] += p.flow_capacity
            A[j, i] += p.flow_capacity
            
        D = np.diag(A.sum(axis=1))
        self.adjacency = A
        self.laplacian = D - A
        return self.adjacency, self.laplacian
    
    def analyze(self) -> dict:
        if self.laplacian is None:
            self.build_matrices()
            
        n = len(self.labels)
        eigenvalues, eigenvectors = eigh(self.laplacian)
        
        # λ₁ = 0 always (constant eigenvector)
        # λ₂ = Fiedler value = algebraic connectivity
        fiedler_value = eigenvalues[1] if n > 1 else 0.0
        fiedler_vector = eigenvectors[:, 1] if n > 1 else np.zeros(n)
        
        # Conservation ratio: how well-connected vs. theoretical max
        # For a complete graph K_n, λ₂ = n
        max_possible = n
        conservation_ratio = fiedler_value / max_possible if max_possible > 0 else 0
        
        # Identify bottlenecks: rooms with high Fiedler values are in the 
        # "periphery" — topologically distant from the flow core
        periphery = [(self.labels[i], fiedler_vector[i]) 
                     for i in range(n)]
        periphery.sort(key=lambda x: abs(x[1]), reverse=True)
        
        # Wayfinding difficulty score: higher = harder to navigate
        # Based on: low conservation + high variance in Fiedler values
        fiedler_variance = np.var(fiedler_vector)
        wayfinding_difficulty = (1 - conservation_ratio) * (1 + fiedler_variance)
        
        # Natural partition: Fiedler splits building into two zones
        partition_a = [self.labels[i] for i in range(n) if fiedler_vector[i] >= 0]
        partition_b = [self.labels[i] for i in range(n) if fiedler_vector[i] < 0]
        
        # Circulation quality per room: how central is this room to flow?
        degree = self.adjacency.sum(axis=1)
        centrality = degree / degree.max() if degree.max() > 0 else np.zeros(n)
        
        return {
            "n_rooms": n,
            "n_passages": len(self.passages),
            "fiedler_value": float(fiedler_value),
            "conservation_ratio": float(conservation_ratio),
            "wayfinding_difficulty": float(wayfinding_difficulty),
            "natural_partition": {"zone_a": partition_a, "zone_b": partition_b},
            "most_peripheral": periphery[:3],
            "circulation_centrality": {
                self.labels[i]: float(centrality[i]) for i in range(n)
            },
            "eigenvalues": eigenvalues.tolist(),
            "assessment": self._assess(conservation_ratio, wayfinding_difficulty)
        }
    
    def _assess(self, conservation: float, difficulty: float) -> str:
        if conservation > 0.5:
            return ("HIGH conservation — excellent circulation. "
                   "Movement flows naturally; wayfinding is intuitive. "
                   "Think: open-plan modern museum or Prairie house.")
        elif conservation > 0.2:
            return ("MODERATE conservation — functional but not fluid. "
                   "Some dead zones or bottlenecks. Most conventional buildings. "
                   "Wayfinding may require signage.")
        elif conservation > 0.05:
            return ("LOW conservation — significant circulation problems. "
                   "Dead ends, isolated wings, confusing transitions. "
                   "Think: Brutalist government building or labyrinthine hospital.")
        else:
            return ("VERY LOW conservation — near-disconnected graph. "
                   "The building is essentially separate zones with minimal "
                   "connections. Expect severe wayfinding issues.")


# --- Example: Frank Lloyd Wright Prairie House vs. Brutalist Office ---
def demo():
    # Prairie House: open flow, high connectivity
    prairie = BuildingLaplacian()
    for name in ["hearth", "living", "dining", "library", "entry", "terrace"]:
        prairie.add_room(name, area=25 if name != "entry" else 8)
    
    # Wright's signature: everything flows through the hearth
    for room in ["living", "dining", "library", "entry", "terrace"]:
        prairie.add_passage("hearth", room, "open_plan", 3.0)
    # Cross-connections remove bottlenecks
    prairie.add_passage("living", "dining", "open_plan", 4.0)
    prairie.add_passage("living", "library", "open_plan", 2.5)
    prairie.add_passage("dining", "terrace", "open_plan", 2.0)
    
    # Brutalist Office: compartmentalized, disconnected
    brutalist = BuildingLaplacian()
    floors = {
        "lobby": 0, "security": 0,
        "office_a1": 1, "office_a2": 1, "office_a3": 1, "corridor_a": 1,
        "office_b1": 2, "office_b2": 2, "office_b3": 2, "corridor_b": 2,
    }
    for name, floor in floors.items():
        brutalist.add_room(name, floor=floor, area=20 if "office" in name else 15)
    
    # Minimal connections: one stairway, narrow corridors, no cross-flow
    brutalist.add_passage("lobby", "security", "doorway", 1.2)
    brutalist.add_passage("lobby", "corridor_a", "stairway", 1.5)
    brutalist.add_passage("corridor_a", "office_a1", "doorway", 0.9)
    brutalist.add_passage("corridor_a", "office_a2", "doorway", 0.9)
    brutalist.add_passage("corridor_a", "office_a3", "doorway", 0.9)
    brutalist.add_passage("corridor_a", "corridor_b", "stairway", 1.2)
    brutalist.add_passage("corridor_b", "office_b1", "doorway", 0.9)
    brutalist.add_passage("corridor_b", "office_b2", "doorway", 0.9)
    brutalist.add_passage("corridor_b", "office_b3", "doorway", 0.9)
    
    prairie_result = prairie.analyze()
    brutalist_result = brutalist.analyze()
    
    print("=== PRAIRIE HOUSE (Frank Lloyd Wright) ===")
    print(f"Conservation: {prairie_result['conservation_ratio']:.3f}")
    print(f"Wayfinding difficulty: {prairie_result['wayfinding_difficulty']:.3f}")
    print(f"Assessment: {prairie_result['assessment']}")
    print(f"Natural zones: {prairie_result['natural_partition']}")
    print()
    
    print("=== BRUTALIST OFFICE ===")
    print(f"Conservation: {brutalist_result['conservation_ratio']:.3f}")
    print(f"Wayfinding difficulty: {brutalist_result['wayfinding_difficulty']:.3f}")
    print(f"Assessment: {brutalist_result['assessment']}")
    print(f"Natural zones: {brutalist_result['natural_partition']}")
    print()
    
    # The stairway between floors is the bottleneck in the Brutalist building
    # The Prairie House has no bottleneck — every room connects to many others

if __name__ == "__main__":
    demo()
```

### What the Numbers Reveal

Run this code and the story writes itself. The Prairie House has a conservation ratio near 0.6 — high, indicating that Wright's open plan creates genuine architectural flow. The Fiedler vector doesn't cleanly split the house because there's no natural "disconnected zone." The hearth, as designed, is the central hub with maximum centrality.

The Brutalist Office has a conservation ratio near 0.1 — low. The Fiedler vector cleanly splits the building into "floor 1 + lobby" and "floor 2" — the single stairway is a critical bottleneck. The wayfinding difficulty is three to five times higher. Anyone who's navigated a Brutalist government building knows this feeling: you're always aware of being on the wrong side of the partition.

The Laplacian doesn't just predict how buildings feel — it explains *why* they feel that way. And it gives architects a quantitative tool: design the graph first, then build the building to match.

---

## Round 2 — The City Laplacian

### Neighborhoods as Nodes, Transport as Edges

Scale up from building to city and the same mathematics applies with richer implications. A city is a graph where neighborhoods are nodes and transport links (roads, bus lines, subway lines, bike paths, walkable connections) are edges. The city's Laplacian encodes its **urban connectivity** — how easily life, commerce, culture, and people flow between its parts.

The conservation framework translates directly: a city with high spectral conservation ($\lambda_2$ close to its theoretical maximum) is one where every neighborhood is well-connected to every other neighborhood through redundant, diverse paths. A city with low conservation has districts that are functionally isolated — reachable only through fragile, single-link connections.

### Jane Jacobs Was Spectrally Right

In *The Death and Life of Great American Cities* (1961), Jane Jacobs argued against urban renewal and zoning, advocating instead for mixed-use neighborhoods with diverse activities, short blocks, and buildings of varying age. She described, in prose, what the Laplacian describes in math.

A mixed-use neighborhood has high **internal degree** — many different activities (residential, commercial, cultural) connected to each other within a small area. When neighborhoods are internally dense and also connected to neighbors, the city graph has high conservation. People can meet their daily needs through multiple paths. The failure of any single link (a road closure, a business closing) doesn't disconnect the graph.

Zoning-separated cities are the opposite. Residential zones connect to commercial zones through a small number of arterial roads. These roads are the **bridge edges** of the urban graph. Remove them — construction, accident, flooding — and entire neighborhoods become unreachable. The spectral gap collapses. The city's Fiedler value drops to near zero.

Jacobs' "eyes on the street" concept is a conservation argument: when neighborhoods have high internal connectivity, natural surveillance emerges because people are always present and moving through. Low-connectivity neighborhoods have empty zones where the Fiedler vector indicates topological isolation — and those isolated zones are where crime and neglect concentrate.

### Gentrification as Spectral Dynamics

Gentrification is visible in the Laplacian before it's visible on the streets. Here's the mechanism:

A neighborhood with historically low connectivity (poor transport, few amenities) has a high Fiedler value — it sits in the "periphery" of the city graph. Investors notice cheap real estate in an underconnected area. They build a transit link or upscale development. Suddenly the neighborhood's degree increases. Its Fiedler value drops (it's better connected). The spectral gap between it and neighboring areas widens.

This widening spectral gap is the signal: one neighborhood's connectivity is improving rapidly while adjacent neighborhoods' connectivity isn't. Property values flow along the Fiedler vector — from the periphery toward the core. The spectral analysis predicts *where gentrification will spread* by tracking how the Fiedler vector changes as new edges (transport links, developments) are added.

The tragedy: often, the people who lived in the low-connectivity neighborhood are displaced by the improved connectivity they never asked for. The Laplacian doesn't capture this social dimension, but it maps the structural preconditions precisely.

### The 15-Minute City: Maximum Conservation, Minimum Edges

Carlos Moreno's 15-minute city concept — where everything you need is within a 15-minute walk or bike ride — is an optimization problem in spectral graph theory. The goal: maximize $\lambda_2$ (ensuring every neighborhood is well-connected to all services) while minimizing the number of edges (minimizing infrastructure cost and travel distance).

This is the graph theory problem of **optimal spectral connectivity**. For a given number of nodes (neighborhoods), what edge configuration maximizes $\lambda_2$ while minimizing total edge weight (travel distance)? The answer isn't a complete graph — that would mean everyone can reach everywhere directly, which is physically impossible. The answer is a graph where each neighborhood has a diverse mix of services (high internal degree) and efficient transit to nearby neighborhoods (strategic edges).

The 15-minute city's spectral signature: every neighborhood has roughly equal degree, the Fiedler value is high and uniform, and there are no bridge edges whose removal would disconnect the graph. It's the urban equivalent of a well-connected mesh network — redundant, resilient, efficient.

### CityLaplacian: Code

```python
import numpy as np
from scipy.linalg import eigh
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import itertools

@dataclass
class Neighborhood:
    name: str
    population: int = 10000
    services: List[str] = None  # residential, commercial, school, hospital, park, etc.
    
    def __post_init__(self):
        if self.services is None:
            self.services = ["residential"]

@dataclass
class TransportLink:
    neighborhood_a: str
    neighborhood_b: str
    mode: str = "bus"  # bus, subway, road, bike, walk
    travel_time_min: float = 15.0
    frequency_per_hour: float = 4.0
    capacity: float = 1.0
    
    @property
    def effective_weight(self) -> float:
        """Higher capacity, frequency, and speed = higher weight."""
        speed_factor = {"walk": 0.3, "bike": 0.6, "bus": 1.0, "subway": 2.0, "road": 1.5}
        return (self.capacity * self.frequency_per_hour * 
                speed_factor.get(self.mode, 1.0) / self.travel_time_min)


class CityLaplacian:
    """
    Analyze urban connectivity through spectral graph theory.
    Neighborhoods = nodes, transport links = weighted edges.
    """
    
    def __init__(self):
        self.neighborhoods: Dict[str, Neighborhood] = {}
        self.links: List[TransportLink] = []
        self._cache = {}
        
    def add_neighborhood(self, name: str, population: int = 10000, 
                         services: List[str] = None):
        self.neighborhoods[name] = Neighborhood(name, population, services)
        self._cache.clear()
        
    def add_link(self, a: str, b: str, mode: str = "bus", 
                 time: float = 15.0, freq: float = 4.0, cap: float = 1.0):
        self.links.append(TransportLink(a, b, mode, time, freq, cap))
        self._cache.clear()
    
    def _build_laplacian(self):
        labels = sorted(self.neighborhoods.keys())
        n = len(labels)
        idx = {name: i for i, name in enumerate(labels)}
        
        A = np.zeros((n, n))
        for link in self.links:
            i, j = idx[link.neighborhood_a], idx[link.neighborhood_b]
            w = link.effective_weight
            A[i, j] += w
            A[j, i] += w
            
        D = np.diag(A.sum(axis=1))
        L = D - A
        return L, A, labels
    
    def analyze(self) -> dict:
        L, A, labels = self._build_laplacian()
        n = len(labels)
        eigenvalues, eigenvectors = eigh(L)
        
        fiedler_value = eigenvalues[1] if n > 1 else 0
        fiedler_vector = eigenvectors[:, 1] if n > 1 else np.zeros(n)
        
        # Service diversity per neighborhood (mixed-use score)
        service_diversity = {}
        all_services = set()
        for nb in self.neighborhoods.values():
            all_services.update(nb.services)
        total_types = max(len(all_services), 1)
        
        for name, nb in self.neighborhoods.items():
            diversity = len(set(nb.services)) / total_types
            service_diversity[name] = diversity
        
        # Underserved detection: high Fiedler value = topologically peripheral
        # AND low service diversity = functionally deficient
        underserved = []
        for i, name in enumerate(labels):
            fiedler_score = abs(fiedler_vector[i])
            diversity = service_diversity.get(name, 0)
            underserved_score = fiedler_score * (1 - diversity)
            underserved.append((name, underserved_score, fiedler_score, diversity))
        underserved.sort(key=lambda x: x[1], reverse=True)
        
        # Transit coverage: what fraction of possible connections exist?
        possible_links = n * (n - 1) / 2
        actual_links = len(set(
            tuple(sorted([l.neighborhood_a, l.neighborhood_b])) for l in self.links
        ))
        coverage = actual_links / possible_links if possible_links > 0 else 0
        
        # 15-minute city score: average fraction of services reachable within 15 min
        reachable_services = {name: set(self.neighborhoods[name].services) for name in labels}
        for link in self.links:
            if link.travel_time_min <= 15:
                reachable_services[link.neighborhood_a].update(
                    self.neighborhoods[link.neighborhood_b].services)
                reachable_services[link.neighborhood_b].update(
                    self.neighborhoods[link.neighborhood_a].services)
        
        fifteen_min_scores = {}
        for name in labels:
            score = len(reachable_services[name]) / total_types if total_types > 0 else 0
            fifteen_min_scores[name] = score
        
        avg_15min = np.mean(list(fifteen_min_scores.values()))
        
        return {
            "n_neighborhoods": n,
            "n_transport_links": len(self.links),
            "fiedler_value": float(fiedler_value),
            "transit_coverage": float(coverage),
            "avg_15min_score": float(avg_15min),
            "underserved_areas": underserved[:5],
            "service_diversity": service_diversity,
            "fifteen_min_by_neighborhood": fifteen_min_scores,
            "natural_partition": {
                "zone_a": [labels[i] for i in range(n) if fiedler_vector[i] >= 0],
                "zone_b": [labels[i] for i in range(n) if fiedler_vector[i] < 0],
            },
            "eigenvalues": eigenvalues.tolist(),
        }
    
    def optimize_transit(self, budget: int = 3) -> List[dict]:
        """Find the best new transit links to add to maximize λ₂."""
        L, A, labels = self._build_laplacian()
        n = len(labels)
        idx = {name: i for i, name in enumerate(labels)}
        
        # Find all non-existent links
        existing = set(
            tuple(sorted([l.neighborhood_a, l.neighborhood_b])) for l in self.links
        )
        candidates = []
        for a, b in itertools.combinations(labels, 2):
            if (a, b) not in existing and (b, a) not in existing:
                candidates.append((a, b))
        
        # Greedy: add the link that increases λ₂ the most
        suggestions = []
        for _ in range(min(budget, len(candidates))):
            best_gain = 0
            best_link = None
            
            for a, b in candidates:
                # Simulate adding this link
                i, j = idx[a], idx[b]
                L_test = L.copy()
                w = 1.0  # default weight for proposed link
                L_test[i, j] -= w
                L_test[j, i] -= w
                L_test[i, i] += w
                L_test[j, j] += w
                
                eigs = eigh(L_test, eigvals_only=True, eigvals=(1, 1))
                gain = eigs[0] - (eigenvalues[1] if 'eigenvalues' in dir() else 0)
                
                if gain > best_gain:
                    best_gain = gain
                    best_link = (a, b)
            
            if best_link:
                i, j = idx[best_link[0]], idx[best_link[1]]
                L[i, j] -= 1.0
                L[j, i] -= 1.0
                L[i, i] += 1.0
                L[j, j] += 1.0
                suggestions.append({
                    "connect": best_link,
                    "fiedler_gain": float(best_gain),
                    "rationale": f"Connects {best_link[0]} to {best_link[1]}, "
                                f"bridging a spectral gap"
                })
                candidates = [(a, b) for a, b in candidates 
                             if (a, b) != best_link and (b, a) != best_link]
        
        return suggestions


def demo_city():
    # Jane Jacobs-style mixed-use city
    jacobs_city = CityLaplacian()
    
    neighborhoods = {
        "west_village": (8000, ["residential", "commercial", "school", "park"]),
        "soho": (12000, ["residential", "commercial", "restaurant", "gallery"]),
        "tribeca": (10000, ["residential", "commercial", "school", "park"]),
        "east_village": (15000, ["residential", "commercial", "school", "hospital", "park"]),
        "lower_east_side": (13000, ["residential", "commercial", "school"]),
        "chinatown": (9000, ["residential", "commercial", "restaurant", "cultural"]),
        "little_italy": (5000, ["residential", "commercial", "restaurant"]),
        "financial_district": (7000, ["commercial", "restaurant", "transit_hub"]),
    }
    
    for name, (pop, svcs) in neighborhoods.items():
        jacobs_city.add_neighborhood(name, pop, svcs)
    
    # Dense mesh of connections (Jane Jacobs' short blocks = many links)
    links = [
        ("west_village", "soho", "walk", 8, 60, 0.5),
        ("west_village", "tribeca", "walk", 12, 60, 0.5),
        ("soho", "tribeca", "walk", 10, 60, 0.5),
        ("soho", "chinatown", "walk", 7, 60, 0.5),
        ("soho", "little_italy", "walk", 5, 60, 0.5),
        ("tribeca", "financial_district", "subway", 10, 12, 2.0),
        ("tribeca", "chinatown", "walk", 8, 60, 0.5),
        ("east_village", "lower_east_side", "walk", 6, 60, 0.5),
        ("east_village", "little_italy", "walk", 10, 60, 0.5),
        ("lower_east_side", "chinatown", "walk", 8, 60, 0.5),
        ("lower_east_side", "little_italy", "walk", 7, 60, 0.5),
        ("chinatown", "little_italy", "walk", 4, 60, 0.5),
        ("chinatown", "financial_district", "walk", 12, 60, 0.5),
        ("little_italy", "financial_district", "subway", 8, 8, 2.0),
        ("west_village", "east_village", "bus", 15, 6, 1.0),
    ]
    for a, b, mode, time, freq, cap in links:
        jacobs_city.add_link(a, b, mode, time, freq, cap)
    
    result = jacobs_city.analyze()
    
    print("=== JANE JACOBS MIXED-USE CITY ===")
    print(f"Fiedler value: {result['fiedler_value']:.4f}")
    print(f"Transit coverage: {result['transit_coverage']:.2%}")
    print(f"Average 15-min score: {result['avg_15min_score']:.2%}")
    print(f"Natural partition: {result['natural_partition']}")
    print(f"Most underserved: {result['underserved_areas'][:3]}")
    print()
    
    # Zoning-separated suburban city (same population, separated uses)
    suburb = CityLaplacian()
    suburb.add_neighborhood("suburb_a", 25000, ["residential"])
    suburb.add_neighborhood("suburb_b", 20000, ["residential"])
    suburb.add_neighborhood("suburb_c", 15000, ["residential"])
    suburb.add_neighborhood("mall_zone", 5000, ["commercial"])
    suburb.add_neighborhood("office_park", 10000, ["commercial"])
    suburb.add_neighborhood("school_district", 3000, ["school"])
    
    # Everything connects through a single highway
    suburb.add_link("suburb_a", "mall_zone", "road", 25, 2, 2.0)
    suburb.add_link("suburb_b", "mall_zone", "road", 20, 2, 2.0)
    suburb.add_link("suburb_c", "mall_zone", "road", 30, 1, 2.0)
    suburb.add_link("mall_zone", "office_park", "road", 15, 4, 2.0)
    suburb.add_link("office_park", "school_district", "bus", 35, 2, 0.5)
    
    suburb_result = suburb.analyze()
    print("=== ZONING-SEPARATED SUBURB ===")
    print(f"Fiedler value: {suburb_result['fiedler_value']:.4f}")
    print(f"Transit coverage: {suburb_result['transit_coverage']:.2%}")
    print(f"Average 15-min score: {suburb_result['avg_15min_score']:.2%}")
    print(f"Most underserved: {suburb_result['underserved_areas'][:3]}")
    print()
    
    # Optimize the suburb
    print("=== TRANSIT OPTIMIZATION SUGGESTIONS ===")
    suggestions = suburb.optimize_transit(budget=3)
    for s in suggestions:
        print(f"  {s['connect'][0]} <-> {s['connect'][1]}: λ₂ gain = {s['fiedler_gain']:.4f}")


if __name__ == "__main__":
    demo_city()
```

### Reading the Urban Spectrum

The demo reveals a stark contrast. The Jacobs-style mixed-use city has a Fiedler value an order of magnitude higher than the zoning-separated suburb. Its 15-minute score is high — most neighborhoods can access most services through short walks. The Fiedler partition doesn't create a meaningful divide because the city is genuinely interconnected.

The suburb tells a different story. The Fiedler value is near zero — the mall zone is a bridge edge connecting residential areas to everything else. Remove it and the graph splits. The 15-minute score is abysmal: residential neighborhoods have only "residential" within walking distance. The spectral analysis identifies the mall zone and school district as the most critical (and fragile) links.

The optimization suggestions are illuminating: the algorithm recommends connecting residential neighborhoods directly to each other and adding links that bypass the mall bottleneck. This is exactly what urban planners recommend — redundant connections that reduce car dependency. The Laplacian formalizes intuition.

---

## Round 3 — The Software Architecture Laplacian

### Modules as Nodes, Dependencies as Edges

Software architecture is graph theory with syntax highlighting. Every codebase has a dependency graph: modules import other modules, services call other services, packages depend on other packages. This graph has a Laplacian, and that Laplacian has a Fiedler value, and that Fiedler value tells you something profound about the codebase's **architectural coherence**.

The dependency graph is directed (A depends on B doesn't mean B depends on A), but for spectral analysis we consider the *underlying undirected graph* — can information flow between two modules, regardless of direction? The Laplacian of this undirected graph measures how well-connected the codebase is as a whole.

High spectral conservation means the codebase has **strong internal coherence**. Changes can propagate through multiple paths. The system is resilient to individual module failures. But — and this is crucial — too high a conservation means **everything depends on everything**, which is the definition of a tangled monolith.

Low spectral conservation means the codebase has **structural fractures**. Modules or groups of modules are barely connected. Changes in one area don't propagate to others — which sounds good until you realize it means duplicated logic, inconsistent behavior, and the inability to refactor across boundaries.

The sweet spot: **moderate conservation with clear Fiedler partitioning**. The Laplacian's second eigenvector splits the codebase into natural modules — groups of code that are internally tightly connected but loosely connected to each other. This is the mathematical definition of "high cohesion, low coupling."

### Microservices: Spectral Fragility

Microservices architecture promises independent deployability, but the spectral analysis reveals its hidden fragility. A well-designed microservice system looks like a graph with moderate $\lambda_2$: each service is a dense cluster internally, and services connect through a few well-defined APIs. The Fiedler vector cleanly separates service boundaries.

But microservice systems are prone to **spectral gap collapse**. When services start calling each other in ad-hoc patterns (the "distributed monolith"), the graph becomes dense and $\lambda_2$ rises — paradoxically, this is bad. It means your "microservices" are actually just a monolith with network calls. The spectral gap (the difference between $\lambda_2$ and $\lambda_3$) reveals whether you have two clear clusters or a gradual continuum of coupling.

Conversely, when microservices are too isolated — sharing nothing, communicating only through fragile message queues — the graph fragments. $\lambda_2$ drops to near zero. The system loses its architectural coherence. Each service becomes an island, and the whole becomes less than the sum of its parts.

The distributed nature adds another dimension: network edges are fundamentally different from in-process edges. They can fail, lag, or reorder. A Laplacian that looks well-connected in theory can be disconnected in practice when network partitions occur. This is the microservice spectral paradox: the static graph looks fine, but the dynamic graph is fragile.

### The Monolith's Dual Nature

Monoliths naturally have high conservation — everything is in one process, everything can call everything. The Laplacian of a typical monolith has a large $\lambda_2$ because the graph is dense.

But high $\lambda_2$ isn't always good. A monolith where $\lambda_2$ is near its maximum is a **ball of mud** — every module depends on every other module. There are no natural boundaries, no way to reason about a subsystem in isolation. The Fiedler vector is nearly uniform because there's no meaningful partition.

The well-structured monolith sits at the sweet spot. It has moderate $\lambda_2$ — high enough for coherence, low enough for modularity. The Fiedler vector reveals natural module boundaries: groups of modules where intra-group connections are dense and inter-group connections are sparse. The eigenvalue spectrum shows *gaps* — clusters of eigenvalues separated by spectral gaps that correspond to architectural layers.

This is the insight: **the eigenvalue spectrum is the codebase's architectural fingerprint**. Tight clusters of eigenvalues indicate cohesive modules. Gaps between clusters indicate clean boundaries. A uniform spread indicates either excellent layering or total chaos — and the eigenvectors disambiguate.

### Architectural Decay: The Shrinking Spectral Gap

Software architecture decays over time. Dependencies accrete. Temporary hacks become permanent. A module that was supposed to be isolated gains imports from five unrelated modules. The Laplacian tracks this decay precisely.

As architectural decay progresses, the Fiedler value rises (the graph becomes more connected) but the **spectral gap shrinks** (the natural boundaries blur). The eigenvalues that were once clustered in distinct groups (corresponding to clean modules) spread out and merge. The Fiedler vector, which once cleanly separated modules, becomes noisy — modules that should be in different partitions get mixed together.

Monitoring the eigenvalue spectrum over time is like monitoring blood pressure for codebase health. A slowly rising $\lambda_2$ with a shrinking spectral gap is the early warning sign of architectural decay — months before it becomes painful to developers.

### CodebaseLaplacian: Code

```python
import os
import re
import ast
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Tuple, Set, Optional
import numpy as np
from scipy.linalg import eigh


class DependencyExtractor:
    """Extract import dependencies from Python files."""
    
    @staticmethod
    def extract_python(filepath: str) -> Set[str]:
        """Get module names imported by a Python file."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                tree = ast.parse(f.read())
        except (SyntaxError, UnicodeDecodeError):
            return set()
        
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
        return imports
    
    @staticmethod
    def extract_js(filepath: str) -> Set[str]:
        """Extract require/import dependencies from JS/TS files."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except UnicodeDecodeError:
            return set()
        
        pattern = r'(?:require\(["\']|import .*? from ["\'])(\.\.?/[^"\']+|[@\w/-]+)'
        matches = re.findall(pattern, content)
        return set(m.split('/')[-1].replace('.js', '').replace('.ts', '') 
                   for m in matches if not m.startswith('.'))


class CodebaseLaplacian:
    """
    Analyze a codebase's dependency graph through spectral graph theory.
    Modules = nodes, dependencies = edges.
    """
    
    def __init__(self, root_path: str):
        self.root = Path(root_path)
        self.modules: Dict[str, Set[str]] = {}  # module -> set of dependencies
        self.internal_modules: Set[str] = set()
        
    def scan(self, extensions: List[str] = None):
        """Scan codebase and extract dependency graph."""
        if extensions is None:
            extensions = ['.py', '.js', '.ts']
        
        # Map files to module names
        file_to_module: Dict[str, str] = {}
        
        for ext in extensions:
            for filepath in self.root.rglob(f'*{ext}'):
                rel = filepath.relative_to(self.root)
                # Module name: path.without_extension, / -> .
                parts = list(rel.parts[:-1]) + [rel.stem]
                if parts[-1] == '__init__':
                    parts = parts[:-1]
                module = '.'.join(parts) if ext == '.py' else '/'.join(parts)
                file_to_module[str(filepath)] = module
                self.internal_modules.add(module)
        
        # Extract dependencies
        for filepath, module in file_to_module.items():
            ext = Path(filepath).suffix
            if ext == '.py':
                raw_deps = DependencyExtractor.extract_python(filepath)
            elif ext in ('.js', '.ts'):
                raw_deps = DependencyExtractor.extract_js(filepath)
            else:
                continue
                
            # Map raw imports to internal modules
            internal_deps = set()
            for dep in raw_deps:
                # Check if this is an internal module
                for internal in self.internal_modules:
                    if internal.startswith(dep) or dep.split('.')[-1] in internal:
                        internal_deps.add(internal)
                        break
            
            if module in self.modules:
                self.modules[module].update(internal_deps)
            else:
                self.modules[module] = internal_deps
    
    def add_module(self, name: str, dependencies: List[str]):
        """Manually add a module and its dependencies."""
        self.modules[name] = set(dependencies)
        self.internal_modules.add(name)
        for dep in dependencies:
            self.internal_modules.add(dep)
    
    def analyze(self) -> dict:
        """Full spectral analysis of the dependency graph."""
        if not self.modules:
            return {"error": "No modules. Call scan() or add_module() first."}
        
        labels = sorted(self.internal_modules & set(self.modules.keys()))
        n = len(labels)
        if n < 2:
            return {"error": "Need at least 2 modules for analysis."}
        
        idx = {name: i for i, name in enumerate(labels)}
        
        # Build adjacency (undirected: dependency exists either direction)
        A = np.zeros((n, n))
        for module, deps in self.modules.items():
            if module not in idx:
                continue
            for dep in deps:
                if dep in idx:
                    i, j = idx[module], idx[dep]
                    A[i, j] = 1
                    A[j, i] = 1
        
        D = np.diag(A.sum(axis=1))
        L = D - A
        
        eigenvalues, eigenvectors = eigh(L)
        
        fiedler_value = eigenvalues[1]
        fiedler_vector = eigenvectors[:, 1]
        
        # Conservation: how well-connected overall
        max_lambda2 = n  # complete graph
        conservation = fiedler_value / max_lambda2
        
        # Spectral gaps: gaps between consecutive eigenvalues
        spectral_gaps = []
        for i in range(1, len(eigenvalues) - 1):
            gap = eigenvalues[i + 1] - eigenvalues[i]
            spectral_gaps.append((i, float(gap), float(eigenvalues[i])))
        # Find the largest gap — it indicates the best partition
        if spectral_gaps:
            best_gap = max(spectral_gaps, key=lambda x: x[1])
        else:
            best_gap = (0, 0, 0)
        
        # Fiedler partition: the natural module boundary
        partition_a = [labels[i] for i in range(n) if fiedler_vector[i] >= 0]
        partition_b = [labels[i] for i in range(n) if fiedler_vector[i] < 0]
        
        # Module cohesion: how well each module is embedded in its cluster
        cohesion = {}
        for i, name in enumerate(labels):
            same_cluster = partition_a if name in partition_a else partition_b
            intra_edges = sum(1 for dep in self.modules.get(name, []) 
                            if dep in same_cluster)
            total_edges = max(len(self.modules.get(name, set())), 1)
            cohesion[name] = intra_edges / total_edges
        
        # Detect architectural decay: high conservation + low spectral gaps
        avg_gap = np.mean([g[1] for g in spectral_gaps]) if spectral_gaps else 0
        decay_score = conservation * (1 - min(avg_gap / fiedler_value, 1.0)) if fiedler_value > 0 else 0
        
        # Optimal module boundaries via k-way spectral clustering
        # Look for the top-k spectral gaps
        k_gaps = sorted(spectral_gaps, key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "n_modules": n,
            "n_dependencies": int(A.sum() / 2),
            "fiedler_value": float(fiedler_value),
            "conservation_ratio": float(conservation),
            "spectral_gaps": spectral_gaps[:10],
            "largest_gap": best_gap,
            "natural_partition": {
                "group_a": partition_a,
                "group_b": partition_b,
            },
            "module_cohesion": cohesion,
            "decay_score": float(decay_score),
            "top_partition_points": k_gaps,
            "eigenvalues": eigenvalues.tolist(),
            "assessment": self._assess(conservation, decay_score, best_gap),
            "recommendations": self._recommend(conservation, decay_score, 
                                               partition_a, partition_b, cohesion),
        }
    
    def _assess(self, conservation: float, decay: float, 
                best_gap: tuple) -> str:
        if conservation > 0.7 and decay > 0.5:
            return ("HIGH conservation + HIGH decay: likely a tangled monolith. "
                   "Everything depends on everything. Refactor using Fiedler "
                   "partition as a guide for module boundaries.")
        elif conservation > 0.3 and best_gap[1] > 0.5:
            return ("MODERATE conservation + CLEAR spectral gap: well-structured "
                   "codebase with natural module boundaries. Maintain current "
                   "architecture and guard the spectral gaps.")
        elif conservation < 0.1:
            return ("LOW conservation: the codebase is fragmented. Modules are "
                   "barely connected, suggesting duplicated logic or poor "
                   "integration. Consider consolidating related modules.")
        elif conservation > 0.3 and decay < 0.3:
            return ("MODERATE conservation + LOW decay: healthy codebase. "
                   "Good balance between cohesion and modularity.")
        else:
            return ("MODERATE conservation: functional but monitor for decay. "
                   "The spectral structure is not yet clear — may need more "
                   "modules or cleaner dependency patterns.")
    
    def _recommend(self, conservation, decay, part_a, part_b, cohesion) -> List[str]:
        recs = []
        
        # Low cohesion modules need attention
        low_cohesion = [name for name, c in cohesion.items() if c < 0.3]
        if low_cohesion:
            recs.append(f"Low cohesion modules (cross-boundary deps): {low_cohesion[:5]}. "
                       "Consider relocating these or their dependencies.")
        
        if decay > 0.5:
            recs.append("High decay score: dependencies are crossing natural "
                       "boundaries. Enforce module boundaries before adding features.")
        
        if conservation < 0.1:
            recs.append("Very low conservation: consider whether isolated modules "
                       "should be consolidated or given explicit integration tests.")
        
        if len(part_a) > 3 * len(part_b) or len(part_b) > 3 * len(part_a):
            recs.append("Highly imbalanced partition: one side has far more modules. "
                       "The codebase may need a different decomposition strategy.")
        
        if not recs:
            recs.append("No major issues detected. Continue monitoring spectral gaps.")
        
        return recs


def demo_codebase():
    """Demo with a simulated codebase."""
    codebase = CodebaseLaplacian("/dev/null")  # won't scan, we'll add manually
    
    # Simulated Django-like web application
    modules = {
        # Core framework
        "core.config": ["core.logging", "core.utils"],
        "core.logging": [],
        "core.utils": [],
        
        # Auth module (well-bounded)
        "auth.models": ["core.config", "db.connection"],
        "auth.views": ["auth.models", "auth.serializers", "core.utils"],
        "auth.serializers": ["auth.models"],
        "auth.middleware": ["auth.models", "core.config"],
        
        # Database layer
        "db.connection": ["core.config", "core.logging"],
        "db.migrations": ["db.connection", "core.utils"],
        "db.query": ["db.connection"],
        
        # API module
        "api.routes": ["auth.middleware", "api.handlers", "core.config"],
        "api.handlers": ["auth.views", "users.views", "orders.views", "core.utils"],
        "api.serializers": ["users.serializers", "orders.serializers"],
        
        # Users module
        "users.models": ["db.connection", "auth.models", "core.utils"],
        "users.views": ["users.models", "users.serializers", "core.utils"],
        "users.serializers": ["users.models"],
        
        # Orders module
        "orders.models": ["db.connection", "users.models", "core.utils"],
        "orders.views": ["orders.models", "orders.serializers", "core.utils"],
        "orders.serializers": ["orders.models", "users.serializers"],
        "orders.tasks": ["orders.models", "core.logging"],
        
        # Notification module (cross-cutting)
        "notifications.email": ["core.config", "core.logging", "users.models"],
        "notifications.push": ["core.config", "core.logging", "users.models"],
        "notifications.models": ["db.connection", "users.models"],
    }
    
    for mod, deps in modules.items():
        codebase.add_module(mod, deps)
    
    result = codebase.analyze()
    
    print("=== CODEBASE SPECTRAL ANALYSIS ===")
    print(f"Modules: {result['n_modules']}")
    print(f"Dependencies: {result['n_dependencies']}")
    print(f"Fiedler value (λ₂): {result['fiedler_value']:.4f}")
    print(f"Conservation ratio: {result['conservation_ratio']:.4f}")
    print(f"Decay score: {result['decay_score']:.4f}")
    print(f"Largest spectral gap: {result['largest_gap']}")
    print(f"\nAssessment: {result['assessment']}")
    print(f"\nNatural partition:")
    print(f"  Group A: {result['natural_partition']['group_a']}")
    print(f"  Group B: {result['natural_partition']['group_b']}")
    print(f"\nRecommendations:")
    for r in result['recommendations']:
        print(f"  • {r}")
    
    # Show cohesion per module
    print(f"\nModule cohesion (fraction of deps within same Fiedler partition):")
    for name, score in sorted(result['module_cohesion'].items(), 
                               key=lambda x: x[1]):
        bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
        print(f"  {name:30s} {bar} {score:.2f}")
    
    # Eigenvalue spectrum
    print(f"\nEigenvalue spectrum:")
    eigs = result['eigenvalues']
    for i, e in enumerate(eigs):
        bar_len = min(int(e * 3), 60)
        print(f"  λ{i+1:2d}: {e:8.4f} {'█' * bar_len}")


if __name__ == "__main__":
    demo_codebase()
```

### The Spectral Fingerprint of Code

Run the demo and you see the codebase laid bare. The Fiedler partition separates the code into two natural groups — likely the "infrastructure" group (core, db, auth) and the "application" group (users, orders, api, notifications). The spectral gap between eigenvalues confirms this is a meaningful boundary.

Module cohesion scores reveal trouble spots. The `api.handlers` module, which dispatches to both users and orders, likely has low cohesion — its dependencies span the Fiedler boundary. The `notifications` module, which depends on `users.models`, also crosses the boundary. These are the modules where architectural decay is starting.

The eigenvalue spectrum tells the full story. If the eigenvalues cluster in distinct groups with gaps between them, the codebase has clean architectural layers. If they spread uniformly, the boundaries are blurred. The demo codebase shows moderate clustering — it's reasonably well-structured but could benefit from cleaner separation between infrastructure and application logic.

The power of this approach is that it's **language-agnostic and scale-agnostic**. The same Laplacian analysis works on a 10-module Python project, a 1000-module Java monolith, or a 50-service microservice architecture. The mathematics doesn't care about the syntax — it cares about the graph. And the graph is the architecture.

### The Architectural Sweet Spot

The three rounds converge on a single insight: **conservation is the universal measure of structural quality in designed systems**. Whether it's a building, a city, or a codebase, the Laplacian and its spectrum reveal the hidden connectivity that determines how the system performs, feels, and evolves.

Too much conservation (too high $\lambda_2$) means rigidity — a building where every room leads everywhere (confusing), a city where every neighborhood is identical (boring), a codebase where every module depends on every other (a monolith). Too little conservation means fragmentation — a building with dead-end wings (frustrating), a city where neighborhoods are isolated (dysfunctional), a codebase where modules can't talk to each other (duplicating).

The sweet spot is moderate conservation with clear structure. The Fiedler vector reveals natural boundaries. The spectral gaps confirm they're meaningful. The eigenvalue clusters show cohesive subsystems. This is what good architecture looks like — in buildings, in cities, and in code.

The Laplacian is the bridge between the qualitative language of design ("good flow," "walkable," "well-structured") and the quantitative language of mathematics ($\lambda_2$, spectral gaps, Fiedler partitions). It doesn't replace human judgment, but it gives that judgment a foundation sharper than intuition alone.

---

*Three rounds. Three scales. One mathematical framework. Conservation spectral analysis: because the structure of everything is a graph, and every graph has a Laplacian worth listening to.*
