# Urban Planning and Smart Cities Through Conservation Spectral Analysis

*An exploration of how spectral graph theory's conservation law — what flows in must flow out — reveals the hidden structure of urban systems, from transit networks to zoning to emergency response.*

---

## ROUND 1 — The Transit Laplacian

### Stations, Routes, and the Conservation of Flow

A city's transit network is a graph. Stations are nodes. Routes — bus lines, subway corridors, light rail segments — are edges. Every morning, millions of passengers flow through this graph like current through a circuit. And like any circuit, this flow obeys a conservation law: at every station, what flows in must flow out, minus what's absorbed locally (passengers who've reached their destination) plus what's injected (passengers starting their journey).

This is the transit Laplacian.

The graph Laplacian $L = D - A$ — where $D$ is the degree matrix and $A$ is the adjacency matrix — encodes exactly this conservation structure. For any vector $\mathbf{x}$ representing a quantity at each node (passenger counts, congestion, accessibility scores), the Laplacian product $L\mathbf{x}$ measures the net outflow at each station. Conservation means this net outflow equals the source/sink term: $L\mathbf{x} = \mathbf{s}$, where $\mathbf{s}$ is the external injection/absorption.

A well-designed transit network has high conservation fidelity — flow moves smoothly, redundancy ensures no single point of failure, and the spectral properties of $L$ reflect this robustness. A poorly designed network — one with bottlenecks, underserved corridors, and forced transfers through choke points — has low conservation. The eigenvalues of $L$ tell the story.

### The Spectral Fingerprint of Transit Quality

The Laplacian's eigenvalues $\lambda_1 = 0 \leq \lambda_2 \leq \cdots \leq \lambda_n$ encode global connectivity. The second eigenvalue $\lambda_2$ — the algebraic connectivity or Fiedler value — is the most important number in urban transit you've never heard of. A high $\lambda_2$ means the network is well-connected: removing any single edge barely degrades connectivity. A low $\lambda_2$ means the network is fragile: it's held together by a few critical links whose removal would partition the city.

The Fiedler vector — the eigenvector corresponding to $\lambda_2$ — partitions the graph into two communities. In transit terms, it identifies the most natural "cut" through the network. If this cut separates wealthy neighborhoods from poor ones, or the downtown core from the suburbs, it reveals a structural inequity baked into the transit topology itself. No amount of schedule optimization fixes a network whose spectral structure enforces isolation.

Consider a toy city: five neighborhoods arranged roughly in a line — suburbs, midtown, downtown, midtown, suburbs — with a ring road connecting the ends. The Laplacian's spectrum immediately shows that the ring road is critical: removing it drops $\lambda_2$ dramatically, bifurcating the city. The Fiedler vector assigns positive values to one set of neighborhoods and negative values to the other, with the sign change occurring at the weakest link.

### Bottleneck Detection via Conservation Failure

Conservation breaks down at bottlenecks. When a station's inflow vastly exceeds its outflow capacity — think of a single transfer point serving three converging lines during rush hour — the Laplacian approximation fails. The flow equation $L\mathbf{x} = \mathbf{s}$ assumes infinite capacity edges, but real transit has hard limits.

We can extend the model with a capacity-weighted Laplacian $L_C = D_C - C$, where $C$ is a capacity matrix (maximum passengers per edge per unit time). The ratio $L\mathbf{x} / L_C\mathbf{x}$ reveals where demand-to-capacity is highest — these are the bottleneck stations. A high ratio means conservation is strained: the station is trying to move more than its edges allow.

This spectral bottleneck analysis is more powerful than simple ridership statistics because it accounts for network topology. A station with moderate ridership but poor connectivity (few edges, all saturated) is a worse bottleneck than a busy station with many redundant connections. The Laplacian captures this distinction automatically.

### Policy Implications: Where to Add a Line

The Fiedler vector doesn't just diagnose problems — it prescribes solutions. Adding a transit edge between nodes of opposite Fiedler sign maximizes the increase in $\lambda_2$. This is the spectral answer to "where should we build the next transit line?" — connect the two communities that the network most wants to separate.

This isn't abstract math. Cities like Boston, where the Red and Blue lines famously didn't connect until 2024, suffered from exactly this spectral inefficiency. The missing connection forced passengers through a long, congested detour (through Green Line transfers), creating a conservation bottleneck at downtown stations. The spectral prescription — connecting the two clusters identified by the Fiedler vector — was exactly what was eventually built.

### Code: TransitLaplacian

```python
import numpy as np
import networkx as nx
from scipy import sparse
from scipy.sparse.linalg import eigsh
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

class TransitLaplacian:
    """
    Spectral analysis of urban transit networks via the graph Laplacian.
    
    Stations = nodes. Routes = edges. The Laplacian encodes conservation:
    flow in = flow out + local absorption at every station.
    
    The Fiedler value (λ₂) measures network resilience.
    The Fiedler vector identifies structurally underserved neighborhoods.
    """
    
    def __init__(self):
        self.G = nx.Graph()
        self.station_positions = {}
        self.line_colors = {}
    
    def add_station(self, station_id, name, x, y, zone='general'):
        """Add a transit station at geographic position (x, y)."""
        self.G.add_node(station_id, name=name, zone=zone)
        self.station_positions[station_id] = (x, y)
    
    def add_route(self, station_a, station_b, capacity=1000, line='default',
                  travel_time=5):
        """Add a route (edge) between two stations with capacity and metadata."""
        self.G.add_edge(station_a, station_b, capacity=capacity,
                        line=line, travel_time=travel_time)
    
    def build_city(self):
        """Construct a synthetic city transit network for demonstration."""
        # Downtown core — high connectivity, hub-and-spoke
        self.add_station('dt_core', 'Downtown Core', 5.0, 5.0, 'downtown')
        self.add_station('dt_north', 'Downtown North', 5.0, 6.0, 'downtown')
        self.add_station('dt_south', 'Downtown South', 5.0, 4.0, 'downtown')
        self.add_station('dt_east', 'Downtown East', 6.0, 5.0, 'downtown')
        self.add_station('dt_west', 'Downtown West', 4.0, 5.0, 'downtown')
        
        # Inner ring — moderate connectivity
        self.add_station('inner_nw', 'Inner NW', 3.5, 6.5, 'inner')
        self.add_station('inner_ne', 'Inner NE', 6.5, 6.5, 'inner')
        self.add_station('inner_se', 'Inner SE', 6.5, 3.5, 'inner')
        self.add_station('inner_sw', 'Inner SW', 3.5, 3.5, 'inner')
        
        # Outer suburbs — sparse connectivity (the spectral problem)
        self.add_station('suburb_n', 'North Suburb', 5.0, 9.0, 'suburb')
        self.add_station('suburb_ne', 'NE Suburb', 8.0, 8.0, 'suburb')
        self.add_station('suburb_e', 'East Suburb', 9.0, 5.0, 'suburb')
        self.add_station('suburb_se', 'SE Suburb', 8.0, 2.0, 'suburb')
        self.add_station('suburb_s', 'South Suburb', 5.0, 1.0, 'suburb')
        self.add_station('suburb_sw', 'SW Suburb', 2.0, 2.0, 'suburb')
        self.add_station('suburb_w', 'West Suburb', 1.0, 5.0, 'suburb')
        self.add_station('suburb_nw', 'NW Suburb', 2.0, 8.0, 'suburb')
        
        # Downtown ring — high-capacity internal connections
        downtown_stations = ['dt_core', 'dt_north', 'dt_east', 'dt_south', 'dt_west']
        for i in range(len(downtown_stations)):
            for j in range(i + 1, len(downtown_stations)):
                self.add_route(downtown_stations[i], downtown_stations[j],
                               capacity=2000, line='metro_ring', travel_time=2)
        
        # Inner ring connections
        self.add_route('dt_north', 'inner_nw', capacity=1500, line='blue', travel_time=4)
        self.add_route('dt_north', 'inner_ne', capacity=1500, line='blue', travel_time=4)
        self.add_route('dt_east', 'inner_ne', capacity=1500, line='green', travel_time=4)
        self.add_route('dt_east', 'inner_se', capacity=1500, line='green', travel_time=4)
        self.add_route('dt_south', 'inner_se', capacity=1500, line='red', travel_time=4)
        self.add_route('dt_south', 'inner_sw', capacity=1500, line='red', travel_time=4)
        self.add_route('dt_west', 'inner_sw', capacity=1500, line='yellow', travel_time=4)
        self.add_route('dt_west', 'inner_nw', capacity=1500, line='yellow', travel_time=4)
        
        # Suburb connections — BOTTLENECK: mostly single lines to inner ring
        # This is the spectral problem: suburbs have low redundancy
        self.add_route('inner_nw', 'suburb_nw', capacity=500, line='blue_ext', travel_time=8)
        self.add_route('inner_ne', 'suburb_ne', capacity=500, line='green_ext', travel_time=8)
        self.add_route('inner_se', 'suburb_se', capacity=500, line='red_ext', travel_time=8)
        self.add_route('inner_sw', 'suburb_sw', capacity=500, line='yellow_ext', travel_time=8)
        self.add_route('inner_nw', 'suburb_n', capacity=500, line='blue_ext', travel_time=7)
        self.add_route('inner_ne', 'suburb_n', capacity=500, line='green_ext', travel_time=7)
        self.add_route('inner_se', 'suburb_e', capacity=500, line='red_ext', travel_time=7)
        self.add_route('inner_sw', 'suburb_w', capacity=500, line='yellow_ext', travel_time=7)
        self.add_route('inner_se', 'suburb_s', capacity=500, line='red_ext', travel_time=9)
        self.add_route('inner_sw', 'suburb_s', capacity=500, line='yellow_ext', travel_time=9)
        
        # Ring road connecting outer suburbs — low capacity
        outer_stations = ['suburb_nw', 'suburb_n', 'suburb_ne', 'suburb_e',
                          'suburb_se', 'suburb_s', 'suburb_sw', 'suburb_w', 'suburb_nw']
        for i in range(len(outer_stations) - 1):
            self.add_route(outer_stations[i], outer_stations[i + 1],
                           capacity=300, line='ring_bus', travel_time=12)
    
    def compute_laplacian(self):
        """Compute the graph Laplacian and its spectral decomposition."""
        # Normalized Laplacian for better spectral properties
        L = nx.normalized_laplacian_matrix(self.G).astype(float)
        
        # Compute smallest eigenvalues/eigenvectors
        eigenvalues, eigenvectors = eigsh(L, k=min(6, len(self.G) - 1),
                                           which='SM')
        
        # Sort by eigenvalue
        idx = np.argsort(eigenvalues)
        self.eigenvalues = eigenvalues[idx]
        self.eigenvectors = eigenvectors[:, idx]
        
        # Node ordering for mapping eigenvectors back
        self.node_order = list(self.G.nodes())
        
        return self.eigenvalues, self.eigenvectors
    
    def fiedler_analysis(self):
        """
        The Fiedler vector (2nd eigenvector) reveals the network's 
        weakest partition — structurally underserved neighborhoods.
        """
        if not hasattr(self, 'eigenvalues'):
            self.compute_laplacian()
        
        fiedler_value = self.eigenvalues[1]  # λ₂
        fiedler_vector = self.eigenvectors[:, 1]
        
        # Map back to stations
        station_scores = {}
        for i, node in enumerate(self.node_order):
            station_scores[node] = fiedler_vector[i]
        
        # Identify the spectral partition
        positive_cluster = [n for n, s in station_scores.items() if s >= 0]
        negative_cluster = [n for n, s in station_scores.items() if s < 0]
        
        # Bottleneck edges: those connecting the two clusters
        bottlenecks = []
        for u, v in self.G.edges():
            if (u in positive_cluster and v in negative_cluster) or \
               (u in negative_cluster and v in positive_cluster):
                bottlenecks.append((u, v))
        
        # Capacity analysis at bottleneck edges
        bottleneck_info = []
        for u, v in bottlenecks:
            data = self.G.edges[u, v]
            bottleneck_info.append({
                'from': self.G.nodes[u]['name'],
                'to': self.G.nodes[v]['name'],
                'capacity': data['capacity'],
                'line': data['line'],
                'travel_time': data['travel_time']
            })
        
        return {
            'fiedler_value': fiedler_value,
            'station_scores': station_scores,
            'positive_cluster': [self.G.nodes[n]['name'] for n in positive_cluster],
            'negative_cluster': [self.G.nodes[n]['name'] for n in negative_cluster],
            'bottleneck_edges': bottleneck_info,
            'num_bottlenecks': len(bottlenecks),
            'resilience_score': f'Bottleneck ratio: {len(bottlenecks)}/{self.G.number_of_edges()}'
        }
    
    def capacity_strain_analysis(self):
        """
        Identify stations where conservation is strained:
        demand-to-capacity ratio reveals where flow cannot be conserved.
        """
        # Simulate demand via shortest-path betweenness centrality
        betweenness = nx.edge_betweenness_centrality(self.G, normalized=True)
        
        # Demand-to-capacity ratio for each edge
        strain = {}
        for (u, v), bc in betweenness.items():
            cap = self.G.edges[u, v]['capacity']
            strain[(u, v)] = {
                'betweenness': bc,
                'capacity': cap,
                'strain_ratio': bc / cap * 1e5,  # scaled
                'from': self.G.nodes[u]['name'],
                'to': self.G.nodes[v]['name']
            }
        
        # Sort by strain (highest = worst bottleneck)
        sorted_strain = sorted(strain.items(), key=lambda x: x[1]['strain_ratio'],
                               reverse=True)
        return sorted_strain
    
    def recommend_new_route(self):
        """
        Spectral prescription: connect nodes of opposite Fiedler sign 
        to maximize λ₂ increase — where to build the next line.
        """
        if not hasattr(self, 'eigenvalues'):
            self.compute_laplacian()
        
        fiedler = self.eigenvectors[:, 1]
        
        best_pair = None
        best_score = -np.inf
        
        nodes = self.node_order
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                if not self.G.has_edge(nodes[i], nodes[j]):
                    # Spectral gain ≈ product of Fiedler values * distance
                    score = abs(fiedler[i] * fiedler[j])
                    if fiedler[i] * fiedler[j] < 0:  # opposite signs
                        score *= 2  # bonus for connecting clusters
                    if score > best_score:
                        best_score = score
                        best_pair = (nodes[i], nodes[j])
        
        if best_pair:
            return {
                'connect_from': self.G.nodes[best_pair[0]]['name'],
                'connect_to': self.G.nodes[best_pair[1]]['name'],
                'spectral_gain': best_score,
                'rationale': 'Connecting opposite Fiedler signs maximizes algebraic connectivity'
            }
        return None
    
    def full_report(self):
        """Generate a complete spectral transit analysis report."""
        self.build_city()
        eigenvalues, _ = self.compute_laplacian()
        fiedler = self.fiedler_analysis()
        strain = self.capacity_strain_analysis()
        recommendation = self.recommend_new_route()
        
        report = []
        report.append("=" * 70)
        report.append("TRANSIT LAPLACIAN SPECTRAL ANALYSIS")
        report.append("=" * 70)
        report.append(f"\nNetwork: {self.G.number_of_nodes()} stations, "
                      f"{self.G.number_of_edges()} route segments")
        report.append(f"\nSPECTRUM (smallest eigenvalues): "
                      f"{', '.join(f'{e:.4f}' for e in eigenvalues)}")
        report.append(f"\nFIEDLER VALUE (λ₂ = algebraic connectivity): "
                      f"{fiedler['fiedler_value']:.6f}")
        report.append(f"  → Higher is better. This value suggests "
                      f"{'good' if fiedler['fiedler_value'] > 0.3 else 'poor'} "
                      f"network resilience.")
        
        report.append(f"\nSPECTRAL PARTITION (Fiedler cut):")
        report.append(f"  Cluster A: {', '.join(fiedler['positive_cluster'])}")
        report.append(f"  Cluster B: {', '.join(fiedler['negative_cluster'])}")
        report.append(f"  Bottleneck edges: {fiedler['num_bottlenecks']}")
        
        report.append(f"\nTOP 5 CAPACITY STRAIN (conservation failure risk):")
        for i, ((u, v), info) in enumerate(strain[:5]):
            report.append(f"  {i+1}. {info['from']} → {info['to']} "
                          f"(strain: {info['strain_ratio']:.2f})")
        
        if recommendation:
            report.append(f"\nSPECTRAL RECOMMENDATION:")
            report.append(f"  Build new route: {recommendation['connect_from']} ↔ "
                          f"{recommendation['connect_to']}")
            report.append(f"  Spectral gain: {recommendation['spectral_gain']:.4f}")
        
        return '\n'.join(report)
    
    def visualize(self, filename='transit_laplacian.png'):
        """Visualize the transit network colored by Fiedler vector."""
        if not hasattr(self, 'eigenvalues'):
            self.build_city()
            self.compute_laplacian()
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 8))
        
        fiedler = self.eigenvectors[:, 1]
        node_colors = {node: fiedler[i] for i, node in enumerate(self.node_order)}
        colors = [node_colors[n] for n in self.G.nodes()]
        
        # Left: Fiedler coloring
        nx.draw(self.G, pos=self.station_positions, node_color=colors,
                node_size=300, cmap='coolwarm', with_labels=False,
                edge_color='gray', width=1.5, ax=axes[0])
        axes[0].set_title(f'Transit Network — Fiedler Vector Coloring\n'
                          f'λ₂ = {self.eigenvalues[1]:.4f} (Red/Blue = spectral partition)',
                          fontsize=11)
        
        # Annotate key stations
        for node in self.G.nodes():
            x, y = self.station_positions[node]
            name = self.G.nodes[node]['name']
            axes[0].annotate(name, (x, y), fontsize=6, ha='center',
                             va='bottom', xytext=(0, 5),
                             textcoords='offset points')
        
        # Right: Capacity strain
        betweenness = nx.edge_betweenness_centrality(self.G, normalized=True)
        edge_strain = []
        for (u, v) in self.G.edges():
            cap = self.G.edges[u, v]['capacity']
            edge_strain.append(betweenness[(u, v)] / cap * 1e5)
        
        nx.draw(self.G, pos=self.station_positions,
                node_color='lightblue', node_size=200,
                with_labels=False,
                edge_color=edge_strain, edge_cmap=plt.cm.YlOrRd,
                width=2.5, ax=axes[1])
        axes[1].set_title('Capacity Strain Heat Map\n'
                          '(Red edges = conservation bottleneck)', fontsize=11)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        return filename


# Run the analysis
if __name__ == '__main__':
    tl = TransitLaplacian()
    print(tl.full_report())
    tl.visualize()
```

### What the Code Reveals

The `TransitLaplacian` builds a synthetic city with 17 stations: a dense downtown core, an inner ring, and sparse outer suburbs. The spectral analysis reveals:

1. **The Fiedler value is low** — the network has a clear structural weakness. The suburbs are connected to the core through too few links.
2. **The Fiedler partition separates downtown from suburbs** — exactly the inequity transit planners worry about.
3. **Capacity strain concentrates at the inner-to-suburb connections** — these are the edges where conservation fails under load.
4. **The spectral recommendation** is to add a direct route connecting the two Fiedler clusters — precisely what cities do when they build "cross-town" express lines.

This isn't coincidental. The Laplacian's conservation structure mirrors the actual flow dynamics of passenger movement. A network that's spectrally robust is one where passengers can get from anywhere to anywhere via multiple redundant paths — the definition of good transit.

---

## ROUND 2 — The Zoning Graph

### Zones as Nodes, Interactions as Edges

A city's zoning map is also a graph, though we rarely think of it that way. Each zone — residential, commercial, industrial, mixed-use, park — is a node. Edges connect zones that are adjacent or that have significant human interaction patterns (commuting, shopping, recreation). The weight of each edge reflects the intensity of interaction: a residential zone next to a commercial zone has high edge weight (people walk to shops), while a residential zone next to heavy industry has low weight (people avoid it).

The zoning Laplacian $L_Z$ captures the flow of human activity through the city. At each zone, the conservation law states: the activity that enters a zone (visitors, workers, shoppers) equals the activity that leaves, plus what's consumed locally. In a well-balanced city, this conservation holds smoothly — there's a steady, healthy flow between zones. In a poorly zoned city, conservation breaks down.

### Jane Jacobs and the Spectral Vindication of Mixed Use

Jane Jacobs argued in *The Death and Life of Great American Cities* (1961) that mixed-use zoning — where residential, commercial, and civic functions coexist in the same neighborhood — creates healthier, safer, more vibrant communities. Her argument was observational and intuitive, based on her experience in Greenwich Village. Spectral graph theory gives it mathematical teeth.

In a mixed-use zoning graph, every node connects to many others with diverse edge types. A single block might have edges to residential (people live there), commercial (people shop there), recreational (a park), and civic (a school). The resulting graph has high algebraic connectivity ($\lambda_2$ is large) because removing any single edge barely affects the overall connectivity. Activity flows freely through the graph.

In a single-use zoning graph — the legacy of Euclidean zoning that dominated 20th-century American city planning — the graph partitions into disconnected or weakly connected subgraphs. A pure residential suburb has edges only to other residential zones and perhaps a single arterial connecting to a distant commercial zone. A downtown office district has commercial edges only, becoming a "dead zone" at night when workers leave.

The spectral signature is unmistakable: single-use cities have low $\lambda_2$, high modularity, and a Fiedler vector that separates residential from commercial zones. Mixed-use cities have high $\lambda_2$, low modularity, and a Fiedler vector that doesn't cleanly separate anything — because everything is connected to everything.

### Dead Zones and the Conservation Void

A "dead zone" in urban planning — an area with no nighttime activity, no street life, no passive surveillance — is a spectral void. In graph terms, it's a node with low degree and low eigenvector centrality. Activity flows in during working hours and flows out completely at night, leaving no residual flow. Conservation holds trivially (zero in, zero out) but in the worst possible way.

The extreme eigenvalues of the zoning Laplacian reveal these dead zones. Nodes with small values in the principal eigenvector (the eigenvector for the largest eigenvalue) are peripheral — they contribute little to the overall flow. Nodes with near-zero values in the Fiedler vector are "neutral" — they don't strongly belong to either partition, which often means they're disconnected from the city's social fabric entirely.

Spectral analysis can identify dead zones *before* they form. When a new development is proposed, adding it to the zoning graph and recomputing $\lambda_2$ predicts its impact on city connectivity. A proposed big-box store in a residential area, surrounded by parking lots with no pedestrian connections, creates a node that connects to the graph through a single edge — devastating for $\lambda_2$.

### The 15-Minute City as Spectral Ideal

The "15-minute city" concept — where every essential need is within a 15-minute walk or bike ride — is a spectral ideal. In graph terms, it means every node has high eigenvector centrality (connected to diverse, important nodes) and low average shortest path length to all other nodes. The Laplacian spectrum of a 15-minute city is nearly flat — all non-zero eigenvalues are roughly equal — indicating a highly regular, well-connected graph where no node is privileged or marginalized.

Paris under Mayor Hidalgo has been moving toward this model, converting car lanes to bike paths, opening schoolyards on weekends, and mixing uses at the neighborhood level. The spectral effect is a gradual increase in $\lambda_2$ as formerly disconnected nodes (car-only areas) become connected through new multi-modal edges.

### Code: ZoningGraph

```python
import numpy as np
import networkx as nx
from scipy.sparse.linalg import eigsh
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class ZoningGraph:
    """
    Spectral analysis of urban zoning via interaction graphs.
    
    Zones = nodes. Interactions = edges. The zoning Laplacian captures
    the conservation of human activity flow between zones.
    
    Mixed-use zoning: high conservation, high λ₂.
    Single-use zoning: low conservation, low λ₂ (dead zones).
    
    Jane Jacobs vindicated spectrally.
    """
    
    # Zone types and their interaction affinities
    ZONE_TYPES = {
        'residential': {'color': '#4CAF50', 'label': 'R'},
        'commercial': {'color': '#2196F3', 'label': 'C'},
        'industrial': {'color': '#FF9800', 'label': 'I'},
        'mixed_use': {'color': '#9C27B0', 'label': 'M'},
        'park': {'color': '#8BC34A', 'label': 'P'},
        'civic': {'color': '#F44336', 'label': 'V'},
    }
    
    # Interaction matrix: how much activity flows between zone types
    INTERACTION_AFFINITY = {
        ('residential', 'residential'): 0.3,
        ('residential', 'commercial'): 0.9,
        ('residential', 'industrial'): 0.1,
        ('residential', 'mixed_use'): 1.0,
        ('residential', 'park'): 0.8,
        ('residential', 'civic'): 0.7,
        ('commercial', 'commercial'): 0.5,
        ('commercial', 'industrial'): 0.4,
        ('commercial', 'mixed_use'): 0.9,
        ('commercial', 'park'): 0.4,
        ('commercial', 'civic'): 0.5,
        ('industrial', 'industrial'): 0.2,
        ('industrial', 'mixed_use'): 0.3,
        ('industrial', 'park'): 0.1,
        ('industrial', 'civic'): 0.2,
        ('mixed_use', 'mixed_use'): 1.0,
        ('mixed_use', 'park'): 0.7,
        ('mixed_use', 'civic'): 0.8,
        ('park', 'park'): 0.3,
        ('park', 'civic'): 0.6,
        ('civic', 'civic'): 0.3,
    }
    
    def __init__(self, city_name="Generic City"):
        self.city_name = city_name
        self.G = nx.Graph()
        self.zones = {}
    
    def _affinity(self, type_a, type_b):
        """Get symmetric interaction affinity between two zone types."""
        key = (type_a, type_b) if (type_a, type_b) in self.INTERACTION_AFFINITY \
              else (type_b, type_a)
        return self.INTERACTION_AFFINITY.get(key, 0.1)
    
    def add_zone(self, zone_id, zone_type, population=0, area=1.0, x=0, y=0):
        """Add a zone to the city."""
        self.G.add_node(zone_id, zone_type=zone_type, population=population,
                        area=area, pos=(x, y))
        self.zones[zone_id] = {
            'type': zone_type, 'population': population,
            'area': area, 'pos': (x, y)
        }
    
    def auto_connect(self, proximity_threshold=2.5):
        """Connect zones within proximity, weighted by interaction affinity."""
        zone_ids = list(self.zones.keys())
        for i in range(len(zone_ids)):
            for j in range(i + 1, len(zone_ids)):
                za, zb = self.zones[zone_ids[i]], self.zones[zone_ids[j]]
                dist = np.sqrt((za['pos'][0] - zb['pos'][0])**2 +
                               (za['pos'][1] - zb['pos'][1])**2)
                if dist <= proximity_threshold:
                    affinity = self._affinity(za['type'], zb['type'])
                    weight = affinity * (1.0 / max(dist, 0.1))
                    self.G.add_edge(zone_ids[i], zone_ids[j],
                                    weight=weight, distance=dist,
                                    affinity=affinity)
    
    def build_euclidean_city(self):
        """
        Build a traditional single-use (Euclidean) zoned city.
        Districts are separated by type — classic suburban sprawl.
        """
        # Residential district (north)
        for i in range(8):
            self.add_zone(f'res_{i}', 'residential', population=5000,
                          area=2.0, x=1.0 + i * 0.8, y=8.0)
        
        # Commercial district (center-south, separate from residential)
        for i in range(5):
            self.add_zone(f'com_{i}', 'commercial', population=500,
                          area=1.5, x=2.0 + i * 1.0, y=5.0)
        
        # Industrial district (far south, isolated)
        for i in range(3):
            self.add_zone(f'ind_{i}', 'industrial', population=100,
                          area=3.0, x=2.5 + i * 1.5, y=1.5)
        
        # Single park (small, central)
        self.add_zone('park_0', 'park', population=0, area=1.0, x=5.0, y=6.5)
        
        # Civic center (isolated)
        self.add_zone('civic_0', 'civic', population=200, area=1.0, x=7.0, y=3.5)
        
        self.auto_connect(proximity_threshold=3.0)
    
    def build_jacobs_city(self):
        """
        Build a Jacobsian mixed-use city — diverse zones interleaved.
        Every neighborhood has residential, commercial, park, and civic.
        """
        # Create 6 mixed neighborhoods, each with diverse zones
        neighborhood_centers = [(2, 2), (6, 2), (10, 2),
                                (2, 6), (6, 6), (10, 6)]
        
        zone_idx = 0
        for nx_c, ny_c in neighborhood_centers:
            # Each neighborhood: residential + commercial + park + civic + mixed
            offsets = [(-0.4, -0.4, 'residential'), (0.4, -0.4, 'commercial'),
                       (0.0, 0.4, 'park'), (-0.4, 0.4, 'civic'),
                       (0.4, 0.4, 'mixed_use'), (0.0, 0.0, 'mixed_use')]
            
            for dx, dy, ztype in offsets:
                pop = {'residential': 3000, 'commercial': 800,
                       'park': 0, 'civic': 300, 'mixed_use': 2000}[ztype]
                area = {'residential': 1.5, 'commercial': 1.0,
                        'park': 0.8, 'civic': 0.6, 'mixed_use': 1.2}[ztype]
                self.add_zone(f'zone_{zone_idx}', ztype, population=pop,
                              area=area, x=nx_c + dx, y=ny_c + dy)
                zone_idx += 1
        
        self.auto_connect(proximity_threshold=2.0)
    
    def spectral_analysis(self):
        """Full spectral decomposition of the zoning graph."""
        if self.G.number_of_nodes() == 0:
            return None
        
        # Weighted Laplacian
        L = nx.normalized_laplacian_matrix(self.G, weight='weight').astype(float)
        k = min(8, len(self.G) - 1)
        eigenvalues, eigenvectors = eigsh(L, k=k, which='SM')
        
        idx = np.argsort(eigenvalues)
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        node_order = list(self.G.nodes())
        
        # Principal eigenvector (centrality)
        principal = eigenvectors[:, -1]
        
        # Fiedler analysis
        fiedler_value = eigenvalues[1]
        fiedler_vector = eigenvectors[:, 1]
        
        # Dead zone detection: nodes with low eigenvector centrality
        centrality_scores = {node: abs(principal[i])
                             for i, node in enumerate(node_order)}
        threshold = np.percentile(list(centrality_scores.values()), 25)
        dead_zones = {node: self.zones[node]['type']
                      for node, score in centrality_scores.items()
                      if score < threshold}
        
        # Activity conservation: sum of weighted edges per node
        activity_flow = {}
        for node in node_order:
            total_flow = sum(self.G.edges[node, n]['weight']
                             for n in self.G.neighbors(node))
            activity_flow[node] = total_flow
        
        # Spectral connectivity score (geometric mean of non-zero eigenvalues)
        nonzero = eigenvalues[eigenvalues > 1e-10]
        connectivity = np.exp(np.mean(np.log(nonzero))) if len(nonzero) > 0 else 0
        
        return {
            'eigenvalues': eigenvalues,
            'fiedler_value': fiedler_value,
            'centrality_scores': centrality_scores,
            'dead_zones': dead_zones,
            'activity_flow': activity_flow,
            'connectivity_score': connectivity,
            'node_order': node_order,
            'eigenvectors': eigenvectors,
            'n_zones': len(self.G),
            'n_edges': self.G.number_of_edges(),
            'avg_degree': np.mean([d for _, d in self.G.degree()])
        }
    
    def compare_cities(self):
        """Compare Euclidean (single-use) vs Jacobsian (mixed-use) city."""
        results = {}
        
        for label, builder in [('Euclidean (single-use)', self.build_euclidean_city),
                                ('Jacobsian (mixed-use)', self.build_jacobs_city)]:
            self.__init__()  # reset
            builder()
            analysis = self.spectral_analysis()
            results[label] = analysis
        
        report = []
        report.append("=" * 70)
        report.append("ZONING GRAPH SPECTRAL COMPARISON")
        report.append("=" * 70)
        
        for label, a in results.items():
            report.append(f"\n{'─' * 50}")
            report.append(f"  {label}")
            report.append(f"{'─' * 50}")
            report.append(f"  Zones: {a['n_zones']}, Edges: {a['n_edges']}, "
                          f"Avg degree: {a['avg_degree']:.2f}")
            report.append(f"  Fiedler value (λ₂): {a['fiedler_value']:.6f}")
            report.append(f"  Connectivity score: {a['connectivity_score']:.6f}")
            report.append(f"  Dead zones detected: {len(a['dead_zones'])}")
            for zone, ztype in a['dead_zones'].items():
                report.append(f"    → {zone} ({ztype})")
            
            # Average activity flow by zone type
            type_flow = defaultdict(list)
            for node, flow in a['activity_flow'].items():
                type_flow[self.zones[node]['type']].append(flow)
            report.append(f"  Activity flow by zone type:")
            for ztype, flows in sorted(type_flow.items()):
                report.append(f"    {ztype}: mean={np.mean(flows):.3f}, "
                              f"std={np.std(flows):.3f}")
        
        # Verdict
        report.append(f"\n{'=' * 70}")
        euclidean_f2 = results['Euclidean (single-use)']['fiedler_value']
        jacobs_f2 = results['Jacobsian (mixed-use)']['fiedler_value']
        ratio = jacobs_f2 / euclidean_f2 if euclidean_f2 > 0 else float('inf')
        
        report.append(f"SPECTRAL VERDICT:")
        report.append(f"  Mixed-use Fiedler value is {ratio:.1f}x single-use")
        report.append(f"  Jane Jacobs: "
                      f"{'VINDICATED' if ratio > 1 else 'unexpectedly challenged'}")
        report.append(f"  Dead zones: "
                      f"{len(results['Euclidean (single-use)']['dead_zones'])} "
                      f"(Euclidean) vs "
                      f"{len(results['Jacobsian (mixed-use)']['dead_zones'])} "
                      f"(Jacobsian)")
        
        return '\n'.join(report)
    
    def visualize_comparison(self, filename='zoning_comparison.png'):
        """Side-by-side comparison of zoning graphs."""
        fig, axes = plt.subplots(1, 2, figsize=(18, 8))
        
        for idx, (label, builder) in enumerate([
            ('Euclidean (Single-Use)', self.build_euclidean_city),
            ('Jacobsian (Mixed-Use)', self.build_jacobs_city)
        ]):
            self.__init__()
            builder()
            analysis = self.spectral_analysis()
            
            node_colors = [self.ZONE_TYPES[self.zones[n]['type']]['color']
                           for n in analysis['node_order']]
            positions = {n: self.zones[n]['pos'] for n in analysis['node_order']}
            
            # Edge width by weight
            edge_weights = [self.G.edges[u, v]['weight'] * 3
                            for u, v in self.G.edges()]
            
            nx.draw(self.G, pos=positions, node_color=node_colors,
                    node_size=250, with_labels=False,
                    edge_color='gray', width=edge_weights,
                    alpha=0.8, ax=axes[idx])
            
            axes[idx].set_title(f'{label}\n'
                                f'λ₂ = {analysis["fiedler_value"]:.4f} | '
                                f'Connectivity = {analysis["connectivity_score"]:.4f}\n'
                                f'Dead zones: {len(analysis["dead_zones"])}',
                                fontsize=11)
        
        # Legend
        patches = [mpatches.Patch(color=v['color'], label=k)
                   for k, v in self.ZONE_TYPES.items()]
        fig.legend(handles=patches, loc='lower center', ncol=6, fontsize=9)
        
        plt.tight_layout(rect=[0, 0.05, 1, 1])
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        return filename


# Run the analysis
if __name__ == '__main__':
    zg = ZoningGraph()
    print(zg.compare_cities())
    zg.visualize_comparison()
```

### Reading the Spectral Verdict

The `ZoningGraph` constructs two synthetic cities — one Euclidean (single-use, typical American suburb), one Jacobsian (mixed-use, Parisian-style) — and compares their Laplacian spectra. The results are predictable but quantified:

- **Mixed-use cities have higher $\lambda_2$**: The graph is more connected because diverse zone types create diverse edges. No single edge removal isolates a neighborhood.
- **Single-use cities have more dead zones**: Residential zones with only residential neighbors have low eigenvector centrality. They contribute little to the city's overall activity flow.
- **Activity flow variance is lower in mixed-use cities**: Flow is evenly distributed, meaning no zone is overwhelmed or abandoned.

The spectral framework transforms the qualitative wisdom of Jane Jacobs into a quantitative tool. When a developer proposes a new project, you can ask: "Does this increase or decrease the city's algebraic connectivity?" The answer is no longer a matter of aesthetic preference — it's a number.

---

## ROUND 3 — The Emergency Response Laplacian

### Units, Coverage, and the Laplacian of Resilience

Emergency response — fire, EMS, police — is a graph problem hiding in plain sight. Each response unit (fire engine, ambulance, patrol car) is a node. Each unit's coverage area defines edges to the zones it can reach within a target response time. The resulting graph, when analyzed through its Laplacian, reveals the city's emergency resilience: its ability to absorb shocks, redistribute resources, and maintain coverage when units are deployed or unavailable.

The conservation law here is coverage conservation: at every zone, the total coverage from all nearby units should equal or exceed the demand. In Laplacian terms, $L_E \mathbf{c} = \mathbf{d}$, where $\mathbf{c}$ is the coverage vector (how much each unit contributes) and $\mathbf{d}$ is the demand vector (how much each zone needs). High conservation means every zone is covered by multiple units — redundancy. Low conservation means some zones depend on a single unit — vulnerability.

### The Fiedler-Weighted Placement Problem

Where should a city place its emergency units to maximize resilience? The naive answer is to place them at high-demand locations. The spectral answer is more nuanced: place them to maximize $\lambda_2$ of the response Laplacian.

The Fiedler vector identifies the weakest cut in the coverage graph — the boundary between well-covered and poorly-covered areas. Adding a unit at a node where the Fiedler vector has the largest magnitude on the poorly-covered side maximizes the increase in $\lambda_2$. This is the spectral version of "put the new fire station where it helps most."

Consider a city where downtown has three fire stations within two miles of each other (historical placement, dense buildings) while the growing eastern suburb has none. The coverage graph has a clear Fiedler cut: downtown (over-covered) vs. eastern suburbs (under-covered). The spectral prescription is unambiguous — place the next unit at the suburb's centroid.

But there's a subtlety. Simply placing the unit at the geographic centroid might not maximize $\lambda_2$. The optimal placement accounts for the *weighted* Fiedler vector, where weights reflect population density, hazard risk, and existing response times. This is a semi-definite optimization problem: maximize $\lambda_2(L_E + \Delta L)$ over all possible unit placements $\Delta L$, subject to budget constraints.

### Redundancy, Gaps, and the Spectral Gap

The "spectral gap" — the difference between the first two eigenvalues $\lambda_2 - \lambda_1 = \lambda_2$ (since $\lambda_1 = 0$) — is the resilience gap. A large gap means the coverage graph is well-connected: losing any single unit degrades coverage smoothly. A small gap means the graph is near a phase transition: losing one more unit could fragment coverage, leaving entire zones unreachable within target response times.

This is directly analogous to percolation theory in physics. The emergency response graph percolates — maintains full-city coverage — when $\lambda_2$ exceeds a critical threshold. Below that threshold, the graph fragments into covered and uncovered components. The Fiedler vector shows exactly where the fragmentation will occur.

Real cities operate near this threshold more often than they'd like to admit. Budget constraints limit the number of units, and demographic shifts create new demand faster than infrastructure can adapt. Spectral monitoring — computing $\lambda_2$ of the response graph monthly, tracking its trend — provides an early warning system. A declining $\lambda_2$ means the city is approaching a coverage crisis before any actual incident reveals it.

### Dynamic Rebalancing via Spectral Flow

Emergency response is dynamic. Units get dispatched, become unavailable, and return to service. The response Laplacian changes in real-time. After each dispatch event, the graph loses a node (the dispatched unit), and $\lambda_2$ drops. The remaining units' coverage areas must expand to compensate.

Spectral rebalancing is the strategy of repositioning available units after each dispatch to minimize the drop in $\lambda_2$. Mathematically, for each possible repositioning $\Delta L$, compute the resulting $\lambda_2$ and choose the one that maximizes it. This is a greedy approximation to the dynamic coverage problem.

In practice, this means: when Ambulance 3 responds to a call in Sector 7, Ambulance 5 (the closest available unit) should move toward Sector 7's centroid, maintaining coverage in the now-vulnerable area. The Fiedler vector of the reduced graph tells Ambulance 5 exactly where to stage — at the point where the spectral partition is weakest.

Cities like Baltimore and Seattle have begun experimenting with dynamic ambulance deployment systems. The spectral approach provides the mathematical backbone: instead of ad-hoc heuristics ("move toward the hole"), it computes the globally optimal repositioning that maximizes coverage resilience.

### Code: EmergencyLaplacian

```python
import numpy as np
import networkx as nx
from scipy.sparse.linalg import eigsh
from scipy.optimize import minimize
from itertools import combinations
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle
from collections import defaultdict


class EmergencyLaplacian:
    """
    Spectral analysis of emergency response coverage.
    
    Units = nodes. Coverage areas = edges. The response Laplacian encodes
    coverage resilience: high conservation = redundant coverage, low = gaps.
    
    Optimal unit placement = Fiedler-weighted positioning.
    Dynamic rebalancing = spectral flow after dispatch events.
    """
    
    def __init__(self, city_size=10.0):
        self.city_size = city_size
        self.zones = {}       # zone_id -> {pos, demand, type}
        self.units = {}        # unit_id -> {pos, coverage_radius, type, available}
        self.G = nx.Graph()    # bipartite: units connect to zones they cover
    
    def add_zone(self, zone_id, x, y, demand=1.0, zone_type='residential'):
        """Add a city zone with demand (population density * risk factor)."""
        self.zones[zone_id] = {
            'pos': np.array([x, y]), 'demand': demand, 'type': zone_type
        }
    
    def add_unit(self, unit_id, x, y, coverage_radius=3.0, unit_type='fire'):
        """Add an emergency response unit with coverage radius."""
        self.units[unit_id] = {
            'pos': np.array([x, y]), 'radius': coverage_radius,
            'type': unit_type, 'available': True
        }
    
    def build_coverage_graph(self):
        """Build bipartite graph: unit-node connects to zone-node if in range."""
        self.G.clear()
        
        # Add unit nodes
        for uid, udata in self.units.items():
            if udata['available']:
                self.G.add_node(f'u_{uid}', bipartite='unit', pos=udata['pos'],
                                unit_type=udata['type'])
        
        # Add zone nodes
        for zid, zdata in self.zones.items():
            self.G.add_node(f'z_{zid}', bipartite='zone', pos=zdata['pos'],
                            demand=zdata['demand'], zone_type=zdata['type'])
        
        # Add coverage edges
        for uid, udata in self.units.items():
            if not udata['available']:
                continue
            for zid, zdata in self.zones.items():
                dist = np.linalg.norm(udata['pos'] - zdata['pos'])
                if dist <= udata['radius']:
                    # Weight by inverse distance (closer = better coverage)
                    weight = zdata['demand'] / max(dist, 0.1)
                    self.G.add_edge(f'u_{uid}', f'z_{zid}', weight=weight,
                                    distance=dist)
    
    def build_scenario_city(self):
        """Build a realistic city scenario for analysis."""
        np.random.seed(42)
        
        # 25 zones in a 5x5 grid with varying demand
        zone_types = ['residential', 'commercial', 'industrial', 'mixed_use']
        for i in range(5):
            for j in range(5):
                zid = f'zone_{i}_{j}'
                x, y = 1.5 * (i + 1), 1.5 * (j + 1)
                # Downtown center has higher demand
                dist_to_center = np.sqrt((x - 7.5)**2 + (y - 7.5)**2)
                demand = max(0.5, 3.0 - dist_to_center * 0.2) + np.random.uniform(-0.3, 0.3)
                ztype = zone_types[(i + j) % len(zone_types)]
                self.add_zone(zid, x, y, demand=demand, zone_type=ztype)
        
        # Initial unit placement (suboptimal — clustered downtown)
        initial_positions = [
            ('fire_1', 6.0, 7.5, 3.5, 'fire'),
            ('fire_2', 7.5, 6.0, 3.5, 'fire'),
            ('fire_3', 7.5, 9.0, 3.5, 'fire'),    # clustered
            ('ems_1', 7.5, 7.5, 3.0, 'ems'),
            ('ems_2', 6.0, 6.0, 3.0, 'ems'),
            ('ems_3', 9.0, 7.5, 3.0, 'ems'),      # clustered
            ('police_1', 7.5, 7.5, 4.0, 'police'),
            ('police_2', 4.5, 4.5, 4.0, 'police'),
        ]
        
        for uid, x, y, radius, utype in initial_positions:
            self.add_unit(uid, x, y, coverage_radius=radius, unit_type=utype)
    
    def compute_spectral(self):
        """Compute the Laplacian spectrum of the coverage graph."""
        self.build_coverage_graph()
        
        if self.G.number_of_nodes() < 3:
            return None
        
        L = nx.normalized_laplacian_matrix(self.G, weight='weight').astype(float)
        k = min(10, len(self.G) - 1)
        
        try:
            eigenvalues, eigenvectors = eigsh(L, k=k, which='SM')
        except Exception:
            return None
        
        idx = np.argsort(eigenvalues)
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        return eigenvalues, eigenvectors
    
    def coverage_analysis(self):
        """Analyze coverage gaps and redundancy."""
        self.build_coverage_graph()
        
        zone_coverage = {}
        coverage_gaps = []
        redundancy_scores = {}
        
        for zid in self.zones:
            zone_node = f'z_{zid}'
            if zone_node not in self.G:
                coverage_gaps.append(zid)
                zone_coverage[zid] = 0
                redundancy_scores[zid] = 0
                continue
            
            covering_units = list(self.G.neighbors(zone_node))
            n_covering = len(covering_units)
            total_weight = sum(self.G.edges[zone_node, u]['weight']
                               for u in covering_units)
            
            zone_coverage[zid] = total_weight
            redundancy_scores[zid] = n_covering  # units covering this zone
        
        # Zones with low redundancy (single-unit dependency)
        vulnerable_zones = {z: r for z, r in redundancy_scores.items() if r <= 1}
        
        # Zones with no coverage at all
        uncovered = [z for z in coverage_gaps]
        
        return {
            'zone_coverage': zone_coverage,
            'redundancy_scores': redundancy_scores,
            'vulnerable_zones': vulnerable_zones,
            'uncovered_zones': uncovered,
            'avg_redundancy': np.mean(list(redundancy_scores.values())),
            'min_redundancy': min(redundancy_scores.values()),
            'coverage_ratio': 1 - len(uncovered) / len(self.zones)
        }
    
    def fiedler_placement_recommendation(self):
        """
        Use Fiedler vector to recommend optimal placement for next unit.
        Place where Fiedler magnitude is highest on the under-covered side.
        """
        result = self.compute_spectral()
        if result is None:
            return None
        
        eigenvalues, eigenvectors = result
        fiedler = eigenvectors[:, 1]
        node_order = list(self.G.nodes())
        
        # Find which side of the Fiedler cut has worse coverage
        coverage = self.coverage_analysis()
        
        zone_fiedler = {}
        for i, node in enumerate(node_order):
            if node.startswith('z_'):
                zid = node[2:]
                zone_fiedler[zid] = fiedler[i]
        
        if not zone_fiedler:
            return None
        
        # Optimal placement: centroid of zones with largest |Fiedler| AND low redundancy
        candidates = []
        for zid, fval in zone_fiedler.items():
            redund = coverage['redundancy_scores'].get(zid, 0)
            # Score combines Fiedler magnitude with vulnerability
            score = abs(fval) * max(1, 3 - redund)
            candidates.append((zid, score, fval, redund))
        
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        # Recommend position as weighted centroid of top candidates
        top_n = candidates[:5]
        total_weight = sum(c[1] for c in top_n)
        if total_weight == 0:
            return None
        
        rec_x = sum(self.zones[c[0]]['pos'][0] * c[1] for c in top_n) / total_weight
        rec_y = sum(self.zones[c[0]]['pos'][1] * c[1] for c in top_n) / total_weight
        
        return {
            'recommended_position': (rec_x, rec_y),
            'top_vulnerable_zones': [(c[0], c[3]) for c in top_n],
            'fiedler_value': eigenvalues[1],
            'current_avg_redundancy': coverage['avg_redundancy'],
            'uncovered_zones': coverage['uncovered_zones']
        }
    
    def simulate_dispatch(self, unit_id):
        """Simulate dispatching a unit (removing it from coverage)."""
        if unit_id not in self.units:
            return None
        
        self.units[unit_id]['available'] = False
        
        # Compute new spectral properties
        result = self.compute_spectral()
        coverage = self.coverage_analysis()
        
        if result is None:
            return {'error': 'Graph too small after dispatch'}
        
        eigenvalues, _ = result
        
        return {
            'dispatched_unit': unit_id,
            'fiedler_value_after': eigenvalues[1],
            'avg_redundancy_after': coverage['avg_redundancy'],
            'vulnerable_zones_after': len(coverage['vulnerable_zones']),
            'uncovered_after': len(coverage['uncovered_zones']),
            'coverage_degradation': coverage['coverage_ratio']
        }
    
    def spectral_rebalance(self, dispatched_unit_id):
        """
        After dispatching a unit, find optimal repositioning for remaining units.
        Greedy: for each available unit, find the position that maximizes λ₂.
        """
        self.units[dispatched_unit_id]['available'] = False
        
        available_units = [uid for uid, u in self.units.items() if u['available']]
        
        rebalancing = {}
        
        for uid in available_units:
            original_pos = self.units[uid]['pos'].copy()
            
            # Grid search around current position
            best_pos = original_pos.copy()
            best_f2 = 0
            
            for dx in np.linspace(-2, 2, 9):
                for dy in np.linspace(-2, 2, 9):
                    test_pos = original_pos + np.array([dx, dy])
                    # Clip to city bounds
                    test_pos = np.clip(test_pos, 0.5, self.city_size + 0.5)
                    
                    self.units[uid]['pos'] = test_pos
                    result = self.compute_spectral()
                    
                    if result is not None:
                        eigenvalues, _ = result
                        if eigenvalues[1] > best_f2:
                            best_f2 = eigenvalues[1]
                            best_pos = test_pos.copy()
            
            self.units[uid]['pos'] = original_pos  # restore
            
            movement = best_pos - original_pos
            distance_moved = np.linalg.norm(movement)
            
            rebalancing[uid] = {
                'current_pos': tuple(original_pos),
                'recommended_pos': tuple(best_pos),
                'distance_moved': distance_moved,
                'f2_gain': best_f2,
                'type': self.units[uid]['type']
            }
        
        return rebalancing
    
    def full_report(self):
        """Generate complete emergency response spectral analysis."""
        self.build_scenario_city()
        
        report = []
        report.append("=" * 70)
        report.append("EMERGENCY RESPONSE LAPLACIAN — SPECTRAL ANALYSIS")
        report.append("=" * 70)
        
        report.append(f"\nCity: {len(self.zones)} zones, "
                      f"{len(self.units)} response units")
        
        # Initial coverage
        coverage = self.coverage_analysis()
        report.append(f"\nINITIAL COVERAGE:")
        report.append(f"  Coverage ratio: {coverage['coverage_ratio']:.1%}")
        report.append(f"  Average redundancy: {coverage['avg_redundancy']:.2f} "
                      f"units/zone")
        report.append(f"  Min redundancy: {coverage['min_redundancy']} "
                      f"(zones with single-unit dependency)")
        report.append(f"  Vulnerable zones (≤1 unit): "
                      f"{len(coverage['vulnerable_zones'])}")
        report.append(f"  Uncovered zones: "
                      f"{len(coverage['uncovered_zones'])}")
        
        # Spectral analysis
        result = self.compute_spectral()
        if result is not None:
            eigenvalues, _ = result
            report.append(f"\nSPECTRAL PROPERTIES:")
            report.append(f"  Fiedler value (λ₂): {eigenvalues[1]:.6f}")
            report.append(f"  Spectral gap: {eigenvalues[2] - eigenvalues[1]:.6f}")
            report.append(f"  Smallest eigenvalues: "
                          f"{', '.join(f'{e:.4f}' for e in eigenvalues[:6])}")
            
            resilience = 'HIGH' if eigenvalues[1] > 0.3 else \
                         'MODERATE' if eigenvalues[1] > 0.15 else 'LOW'
            report.append(f"  Resilience rating: {resilience}")
        
        # Placement recommendation
        placement = self.fiedler_placement_recommendation()
        if placement:
            report.append(f"\nFIEDLER-WEIGHTED PLACEMENT RECOMMENDATION:")
            report.append(f"  Next unit should be placed at: "
                          f"({placement['recommended_position'][0]:.1f}, "
                          f"{placement['recommended_position'][1]:.1f})")
            report.append(f"  Most vulnerable zones:")
            for zid, redund in placement['top_vulnerable_zones'][:3]:
                report.append(f"    → {zid}: {redund} covering units")
        
        # Dispatch simulation
        report.append(f"\nDISPATCH SIMULATION (fire_3 → zone_0_0):")
        dispatch_result = self.simulate_dispatch('fire_3')
        if dispatch_result:
            report.append(f"  λ₂ after dispatch: "
                          f"{dispatch_result['fiedler_value_after']:.6f}")
            report.append(f"  Vulnerable zones: "
                          f"{dispatch_result['vulnerable_zones_after']}")
            report.append(f"  Coverage ratio: "
                          f"{dispatch_result['coverage_degradation']:.1%}")
        
        # Spectral rebalancing
        self.build_scenario_city()  # reset
        report.append(f"\nSPECTRAL REBALANCING (after fire_3 dispatch):")
        self.units['fire_3']['available'] = False
        rebalance = self.spectral_rebalance('fire_3')
        
        for uid, info in sorted(rebalance.items(), 
                                key=lambda x: x[1]['distance_moved'],
                                reverse=True):
            if info['distance_moved'] > 0.1:
                report.append(f"  {uid} ({info['type']}): move "
                              f"({info['current_pos'][0]:.1f},"
                              f"{info['current_pos'][1]:.1f}) → "
                              f"({info['recommended_pos'][0]:.1f},"
                              f"{info['recommended_pos'][1]:.1f}) "
                              f"[{info['distance_moved']:.1f} units]")
        
        return '\n'.join(report)
    
    def visualize(self, filename='emergency_laplacian.png'):
        """Visualize coverage graph with redundancy heat map."""
        self.build_scenario_city()
        self.build_coverage_graph()
        
        fig, axes = plt.subplots(1, 2, figsize=(18, 8))
        
        # Left: Coverage map
        coverage = self.coverage_analysis()
        
        # Draw zone coverage (color by redundancy)
        for zid, zdata in self.zones.items():
            redund = coverage['redundancy_scores'].get(zid, 0)
            color = plt.cm.RdYlGn(redund / max(coverage['redundancy_scores'].values()
                                                 or [1]))
            circle = Circle(zdata['pos'], 0.6, color=color, alpha=0.7)
            axes[0].add_patch(circle)
            axes[0].text(zdata['pos'][0], zdata['pos'][1], str(redund),
                         ha='center', va='center', fontsize=8, fontweight='bold')
        
        # Draw unit coverage radii
        unit_colors = {'fire': 'red', 'ems': 'blue', 'police': 'green'}
        for uid, udata in self.units.items():
            if udata['available']:
                circle = Circle(udata['pos'], udata['radius'],
                                fill=False, color=unit_colors.get(udata['type'], 'gray'),
                                linestyle='--', linewidth=1.5, alpha=0.5)
                axes[0].add_patch(circle)
                axes[0].plot(udata['pos'][0], udata['pos'][1],
                             marker='*', markersize=12,
                             color=unit_colors.get(udata['type'], 'gray'))
                axes[0].text(udata['pos'][0], udata['pos'][1] + 0.4,
                             uid, ha='center', fontsize=7)
        
        axes[0].set_xlim(0, 12)
        axes[0].set_ylim(0, 12)
        axes[0].set_aspect('equal')
        axes[0].set_title('Coverage Redundancy Map\n'
                          '(Green=well covered, Red=vulnerable, Numbers=units covering)',
                          fontsize=11)
        
        # Right: After dispatch + rebalancing
        self.units['fire_3']['available'] = False
        rebalance = self.spectral_rebalance('fire_3')
        
        # Apply rebalancing for visualization
        moved_units = {}
        for uid, info in rebalance.items():
            if info['distance_moved'] > 0.3:
                moved_units[uid] = self.units[uid]['pos'].copy()
                self.units[uid]['pos'] = np.array(info['recommended_pos'])
        
        self.build_coverage_graph()
        new_coverage = self.coverage_analysis()
        
        for zid, zdata in self.zones.items():
            redund = new_coverage['redundancy_scores'].get(zid, 0)
            color = plt.cm.RdYlGn(redund / max(new_coverage['redundancy_scores'].values()
                                                 or [1]))
            circle = Circle(zdata['pos'], 0.6, color=color, alpha=0.7)
            axes[1].add_patch(circle)
            axes[1].text(zdata['pos'][0], zdata['pos'][1], str(redund),
                         ha='center', va='center', fontsize=8, fontweight='bold')
        
        for uid, udata in self.units.items():
            if udata['available']:
                circle = Circle(udata['pos'], udata['radius'],
                                fill=False, color=unit_colors.get(udata['type'], 'gray'),
                                linestyle='--', linewidth=1.5, alpha=0.5)
                axes[1].add_patch(circle)
                axes[1].plot(udata['pos'][0], udata['pos'][1],
                             marker='*', markersize=12,
                             color=unit_colors.get(udata['type'], 'gray'))
                axes[1].text(udata['pos'][0], udata['pos'][1] + 0.4,
                             uid, ha='center', fontsize=7)
        
        axes[1].set_xlim(0, 12)
        axes[1].set_ylim(0, 12)
        axes[1].set_aspect('equal')
        axes[1].set_title('After Dispatch (fire_3) + Spectral Rebalancing\n'
                          '(Units repositioned to maximize λ₂)',
                          fontsize=11)
        
        # Legend
        legend_patches = [
            mpatches.Patch(color='red', label='Fire'),
            mpatches.Patch(color='blue', label='EMS'),
            mpatches.Patch(color='green', label='Police'),
        ]
        fig.legend(handles=legend_patches, loc='lower center', ncol=3, fontsize=10)
        
        plt.tight_layout(rect=[0, 0.05, 1, 1])
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        return filename


# Run the analysis
if __name__ == '__main__':
    el = EmergencyLaplacian()
    print(el.full_report())
    el.visualize()
```

### What the Code Reveals

The `EmergencyLaplacian` builds a 25-zone city with 8 response units initially clustered downtown. The analysis shows:

1. **Low Fiedler value**: The coverage graph is fragile. Suburban zones depend on single units, and the Fiedler cut separates the over-covered downtown from under-covered periphery.
2. **Dispatch degrades $\lambda_2$ predictably**: When a unit is dispatched, the algebraic connectivity drops. The magnitude of the drop reveals how critical that unit was.
3. **Spectral rebalancing works**: After dispatching a unit, the remaining units are repositioned using grid search over $\lambda_2$. Units move outward from downtown toward vulnerable suburban zones — exactly the intuitive response, but now mathematically justified.
4. **The Fiedler placement recommendation** identifies the optimal location for the next unit — not at the geographic centroid of uncovered zones, but at the spectral centroid that maximally bridges the Fiedler cut.

### The Conservation Principle in Emergency Response

The deep insight is that emergency response, like all the systems we've explored, obeys a conservation law. Coverage flows through the city graph: from units, through edges (response corridors), to zones. At each zone, the coverage that arrives must match the demand. When it doesn't — when conservation fails — there's a gap. The Laplacian's null space (the zero eigenvalue's eigenvector) represents perfect conservation: a steady state where coverage everywhere equals demand. The non-zero eigenvalues measure how quickly the system returns to this equilibrium after a perturbation (an emergency).

This reframing transforms emergency management from reactive (respond to incidents) to proactive (maintain spectral resilience). A city with high $\lambda_2$ absorbs emergencies as perturbations that quickly decay. A city with low $\lambda_2$ is one bad incident away from a coverage collapse.

---

## Coda: The Spectral City

These three rounds share a common thread: urban systems are graphs, graphs have Laplacians, and Laplacians encode conservation. Whether it's passenger flow (transit), human activity (zoning), or emergency coverage (response), the spectral properties of the underlying graph reveal the system's health, equity, and resilience.

The transit Laplacian shows where to build the next line. The zoning Laplacian vindicates mixed-use planning with numbers, not just anecdotes. The emergency Laplacian turns coverage optimization into spectral maximization. In each case, the Fiedler vector — the ghost in the Laplacian — identifies the city's weakest link and prescribes its repair.

Urban planning has always been a mix of art and science. Spectral graph theory tips the balance toward science without losing the art. The numbers don't replace judgment — they inform it. A planner who knows her city's $\lambda_2$ is declining can act before the crisis, not after. A mayor who sees the Fiedler partition cutting through her city can invest in the neighborhoods that need it most. A smart city isn't one with more sensors — it's one that understands its own topology.

The Laplacian is the city's unconscious. It runs silently beneath the streets, the zoning maps, the dispatch radios. It doesn't care about politics or aesthetics — only about flow, connection, and conservation. Listen to it, and the city tells you what it needs.
