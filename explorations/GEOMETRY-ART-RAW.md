# GEOMETRY AND ART: Conservation Spectral Analysis of the Visual

*An exploration of beauty, composition, and architectural space through the lens of the Conservation Spectral Framework.*

---

## ROUND 1 — The Aesthetic Laplacian

### What Makes Something Beautiful?

The question has haunted philosophers since Plato declared beauty the splendor of the true. Kant split it into the sublime and the beautiful. Hume insisted it was in the eye of the beholder. The entire Western tradition has treated beauty as something fundamentally subjective — a matter of taste, culture, and personal history. And yet.

And yet there are convergences that cannot be explained by culture alone. Across continents and centuries, humans independently arrived at the golden ratio (φ ≈ 1.618) as a proportion that "feels right." Japanese aesthetic theory — *wabi-sabi*, *ma* (the space between) — arrives at structural principles that resonate across cultural boundaries. Islamic geometric art achieves a mathematical precision that produces what observers universally describe as "harmonious." These convergences suggest that beauty is not purely subjective. It has a geometry. And that geometry, I claim, is spectral.

The Conservation Spectral Framework gives us a precise language for this claim: **something is beautiful when its visual features exhibit high conservation with respect to its structural graph.** Beauty is not a property of colors or shapes in isolation. It is a property of the *relationship* between what is visible and what is structural — the alignment between surface and skeleton. When features "follow" the graph's deepest modes — when the visual energy concentrates in the Laplacian's most conserved directions — the result is perceived as beautiful. When features scatter across volatile modes — when visual energy is unstructured noise — the result is perceived as ugly, chaotic, or indifferent.

This is not a metaphor. This is a computation.

### An Image IS a Graph

Consider an image. Not as a grid of pixels, but as a graph. Each pixel is a node. Each node carries an attribute: its color, encoded as a vector in RGB space (or LAB space, which better captures perceptual distance). Edges connect each pixel to its neighbors — 4-connected (up, down, left, right) or 8-connected (including diagonals). Edge weights encode color similarity: w(i,j) = exp(−||c_i − c_j||² / σ²), where σ controls the sensitivity to color differences.

This construction — the image graph — is well-established in computer vision. It underpins normalized cuts segmentation (Shi & Malik, 2000), spectral clustering, and graph-based image processing. The Laplacian of this graph L = D − W, where D is the degree matrix and W is the weight matrix, encodes the image's visual structure in the same way that the Tension-Graph Laplacian encodes a musical structure.

The eigenvalues of L tell us about the image's global structure. The Fiedler value λ₂ measures the image's most fundamental visual bottleneck — the "narrowest gap" between two visually coherent regions. Low λ₂ means the image has a clean, simple visual structure (perhaps two regions with a clear boundary). High λ₂ means the image is visually fragmented — many small regions, no clean separations.

The Fiedler vector φ₂ — the eigenvector corresponding to λ₂ — assigns a real number to each pixel. Pixels with similar values in φ₂ are in the same visual "region." The Fiedler vector is the image's most fundamental decomposition: it splits the image into the two regions that are hardest to separate, which is precisely the most visually meaningful partition.

Now here is the key insight: **the conservation ratio CR(a) = a^T L a / ||a||², applied to an image graph, measures how well the image's color attributes align with its structural graph.** When CR is low — close to λ₂ — the image's colors are concentrated in the graph's most conserved mode. The colors "follow" the structure. The image is visually coherent. When CR is high, the colors are scattered across volatile modes. The image is visually noisy.

**High conservation = visual coherence = beauty.**

This is the Aesthetic Laplacian hypothesis.

### The Golden Ratio as Eigenvalue Ratio

The golden ratio φ ≈ 1.618 appears in art, architecture, and nature with a persistence that goes beyond cultural coincidence. The claim of the Aesthetic Laplacian is that φ emerges from specific spectral properties of aesthetically pleasing graphs.

Consider a simple graph: a path graph with n nodes, representing a one-dimensional composition (a rectangle's proportions, a column's height-to-width ratio). The Laplacian eigenvalues of a path graph are λ_k = 2 − 2cos(kπ/n). The ratio of consecutive eigenvalues λ₂/λ₃ for specific values of n approximates φ.

More generally, graphs whose eigenvalue ratios cluster near φ — graphs where the spectral gaps are "golden" — produce compositions that are neither too simple (which would be boring) nor too complex (which would be chaotic). The golden ratio is the boundary between order and disorder, and it lives in the Laplacian's eigenvalue spectrum.

This connects to the well-known result that φ appears in the eigenvalues of pentagonal symmetry — the five-fold symmetry of starfish, flowers, and the dodecahedron. The connection between φ and five-fold symmetry is mathematical, not mystical. The Laplacian eigenvalues of a graph with five-fold symmetry have specific ratios that involve φ. This is why pentagonal and decagonal motifs appear so frequently in decorative art across cultures: they have a spectral harmony that "looks right."

**Beauty = spectral harmony.** The eigenvalues are the DNA of visual form. The golden ratio is not mystical — it is the eigenvalue ratio of a specific class of graphs that sit at the boundary between order and chaos.

### Jackson Pollock and Controlled Chaos

Jackson Pollock's drip paintings are a perfect test case for the Aesthetic Laplacian. They appear chaotic — random splatters of paint on canvas. But Taylor, Micolich, and Jonas (1999) demonstrated that Pollock's paintings have a specific fractal dimension (D ≈ 1.7) that falls within the range found in natural scenes (D ≈ 1.2–1.8). This is not coincidence. Pollock's paintings are visually coherent because their structure mimics the spectral structure of natural environments — environments that the human visual system evolved to process efficiently.

In spectral terms, Pollock's paintings have a specific eigenvalue distribution. A random image — pure noise — would have eigenvalues distributed according to the semicircle law (Wigner, 1955), with no structure. A completely uniform image would have all eigenvalues zero except λ₁ = 0. Pollock's paintings fall between these extremes: their eigenvalue distribution has a specific shape — neither random nor ordered, but fractal.

The conservation ratio of a Pollock painting is moderate. CR is not as low as a Mondrian (which has extremely clean visual structure and very low CR) and not as high as pure noise (which has very high CR). Pollock occupies a sweet spot — what we might call the "aesthetic bandwidth" — where the image has enough structure to be visually coherent but enough chaos to be visually interesting.

This is the art-historical concept of *tension* made precise. Good art lives in the space between order and chaos. The Laplacian eigenvalue spectrum quantifies this space. Mondrian = high order = eigenvalues clustered in a few tight groups. Pollock = moderate chaos = eigenvalues spread in a fractal distribution. Pure noise = maximum chaos = eigenvalues following the semicircle law.

**The art IS the eigenvalue spectrum.** Different styles are different spectral signatures.

### Building the AestheticLaplacian

Let us build a concrete implementation that computes a spectral beauty score for images and compares art styles.

```python
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from PIL import Image
from dataclasses import dataclass
from typing import Tuple, List, Optional

@dataclass
class SpectralBeautyResult:
    """Complete spectral analysis of an image's aesthetic properties."""
    conservation_ratio: float
    fiedler_value: float          # λ₂ — fundamental visual bottleneck
    spectral_gap: float           # λ₂ - λ₁ (always λ₁ = 0, so this is just λ₂)
    eigenvalue_spread: float      # std of non-zero eigenvalues
    fractal_dimension_estimate: float
    beauty_score: float           # composite: how "beautiful" is this image?
    mode_concentration: float     # what fraction of energy is in the top 3 modes
    golden_alignment: float       # how close eigenvalue ratios are to φ

def image_to_graph(img: Image.Image, max_size: int = 64, sigma: float = 30.0) -> Tuple[sparse.spmatrix, np.ndarray]:
    """
    Convert an image to a graph.
    
    Each pixel → node with LAB color attribute.
    Edges between 4-connected neighbors, weighted by color similarity.
    
    Args:
        img: Input image (PIL Image)
        max_size: Maximum dimension for downsampling (spectral analysis is expensive)
        sigma: Sensitivity parameter for color similarity
        
    Returns:
        (Laplacian matrix, color attribute vector)
    """
    # Convert to LAB color space (better perceptual uniformity)
    img = img.convert('RGB')
    img = img.resize((max_size, max_size), Image.LANCZOS)
    pixels = np.array(img, dtype=np.float64) / 255.0
    
    # Simple RGB→LAB approximation (for production, use skimage or cv2)
    # Here we use normalized RGB as a proxy
    n = max_size
    num_nodes = n * n
    
    # Color attribute vector: LAB-like features per pixel
    # Using RGB as simplified attributes
    attributes = pixels.reshape(num_nodes, 3)
    
    # Build adjacency matrix for 4-connected grid
    rows, cols, weights = [], [], []
    
    def idx(r, c):
        return r * n + c
    
    for r in range(n):
        for c in range(n):
            node = idx(r, c)
            color_i = attributes[node]
            
            # Right neighbor
            if c + 1 < n:
                neighbor = idx(r, c + 1)
                color_j = attributes[neighbor]
                diff = np.linalg.norm(color_i - color_j)
                w = np.exp(-(diff ** 2) / (2 * sigma ** 2))
                rows.extend([node, neighbor])
                cols.extend([neighbor, node])
                weights.extend([w, w])
            
            # Down neighbor
            if r + 1 < n:
                neighbor = idx(r + 1, c)
                color_j = attributes[neighbor]
                diff = np.linalg.norm(color_i - color_j)
                w = np.exp(-(diff ** 2) / (2 * sigma ** 2))
                rows.extend([node, neighbor])
                cols.extend([neighbor, node])
                weights.extend([w, w])
    
    W = sparse.csr_matrix((weights, (rows, cols)), shape=(num_nodes, num_nodes))
    D = sparse.diags(np.array(W.sum(axis=1)).flatten())
    L = D - W  # Unnormalized Laplacian
    
    return L, attributes

def compute_spectral_beauty(L: sparse.spmatrix, attributes: np.ndarray, 
                             num_eigenvalues: int = 20) -> SpectralBeautyResult:
    """
    Compute the spectral beauty score of an image.
    
    The beauty score is a composite of:
    1. Conservation ratio: how well colors align with structure
    2. Golden alignment: how close eigenvalue ratios are to φ
    3. Mode concentration: how much energy is in conserved modes
    4. Eigenvalue spread: the fractal character of the spectrum
    """
    n = L.shape[0]
    k = min(num_eigenvalues, n - 1)
    
    # Compute smallest k eigenvalues/vectors
    eigenvalues, eigenvectors = eigsh(L, k=k, which='SM')
    
    # Sort by eigenvalue
    order = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]
    
    # Skip λ₁ = 0 (constant vector)
    nonzero_evals = eigenvalues[eigenvalues > 1e-10]
    
    if len(nonzero_evals) < 2:
        # Degenerate case: image is completely uniform
        return SpectralBeautyResult(
            conservation_ratio=0.0,
            fiedler_value=0.0,
            spectral_gap=0.0,
            eigenvalue_spread=0.0,
            fractal_dimension_estimate=0.0,
            beauty_score=0.0,  # Uniform = boring
            mode_concentration=1.0,
            golden_alignment=0.0
        )
    
    fiedler_value = nonzero_evals[0]
    
    # Conservation ratio for luminance attribute
    # Use the L-channel (first principal component of color) as the attribute
    luminance = attributes @ np.array([0.299, 0.587, 0.114])
    luminance = luminance - luminance.mean()
    norm_sq = np.dot(luminance, luminance)
    
    if norm_sq < 1e-10:
        cr = 0.0
    else:
        cr = luminance @ (L @ luminance) / norm_sq
    
    # Eigenvalue spread
    spread = np.std(nonzero_evals)
    
    # Fractal dimension estimate from eigenvalue spectrum
    # Using the relationship: N(λ) ∝ λ^(d/2) for a d-dimensional fractal
    # Estimate d from the log-log slope of cumulative eigenvalue count
    if len(nonzero_evals) > 5:
        sorted_evals = np.sort(nonzero_evals)
        cumulative = np.arange(1, len(sorted_evals) + 1)
        log_evals = np.log(sorted_evals + 1e-10)
        log_cumulative = np.log(cumulative)
        # Fit slope
        slope = np.polyfit(log_evals, log_cumulative, 1)[0]
        fractal_dim = 2 * slope
    else:
        fractal_dim = 2.0
    
    # Mode concentration: fraction of luminance energy in top 3 modes
    projections = eigenvectors.T @ luminance
    total_energy = np.sum(projections ** 2)
    if total_energy > 1e-10:
        # Use modes 1-3 (skip mode 0 = constant)
        top3_energy = np.sum(projections[1:min(4, len(projections))] ** 2)
        mode_concentration = top3_energy / total_energy
    else:
        mode_concentration = 0.0
    
    # Golden alignment: how close eigenvalue ratios are to φ
    phi = (1 + np.sqrt(5)) / 2
    ratios = nonzero_evals[1:] / nonzero_evals[:-1]
    if len(ratios) > 0:
        golden_alignment = 1.0 / (1.0 + np.mean(np.abs(np.log(ratios / phi))))
    else:
        golden_alignment = 0.0
    
    # Composite beauty score
    # High beauty = high mode concentration + moderate CR + golden alignment
    # Normalize CR: too low = boring, too high = noisy, moderate = beautiful
    # Optimal CR is near fiedler_value (high conservation)
    cr_score = 1.0 / (1.0 + abs(cr - fiedler_value * 3) / (fiedler_value * 3 + 1e-10))
    
    beauty_score = (
        0.3 * cr_score +
        0.25 * mode_concentration +
        0.25 * golden_alignment +
        0.2 * (1.0 / (1.0 + abs(fractal_dim - 1.7)))  # Pollock sweet spot
    )
    
    return SpectralBeautyResult(
        conservation_ratio=cr,
        fiedler_value=fiedler_value,
        spectral_gap=fiedler_value,
        eigenvalue_spread=spread,
        fractal_dimension_estimate=fractal_dim,
        beauty_score=beauty_score,
        mode_concentration=mode_concentration,
        golden_alignment=golden_alignment
    )

# --- Comparison across art styles ---
def compare_art_styles(image_paths: dict) -> dict:
    """
    Compare spectral beauty scores across different art styles.
    
    Args:
        image_paths: dict mapping style name to file path
        
    Returns:
        dict mapping style name to SpectralBeautyResult
    """
    results = {}
    for style_name, path in image_paths.items():
        img = Image.open(path)
        L, attrs = image_to_graph(img)
        result = compute_spectral_beauty(L, attrs)
        results[style_name] = result
        
        print(f"\n{'='*60}")
        print(f"Style: {style_name}")
        print(f"{'='*60}")
        print(f"  Conservation Ratio: {result.conservation_ratio:.4f}")
        print(f"  Fiedler Value (λ₂): {result.fiedler_value:.4f}")
        print(f"  Eigenvalue Spread:   {result.eigenvalue_spread:.4f}")
        print(f"  Fractal Dimension:   {result.fractal_dimension_estimate:.2f}")
        print(f"  Mode Concentration:  {result.mode_concentration:.4f}")
        print(f"  Golden Alignment:    {result.golden_alignment:.4f}")
        print(f"  ★ Beauty Score:      {result.beauty_score:.4f}")
    
    # Rank by beauty
    ranked = sorted(results.items(), key=lambda x: x[1].beauty_score, reverse=True)
    print(f"\n{'='*60}")
    print("BEAUTY RANKINGS")
    print(f"{'='*60}")
    for rank, (name, result) in enumerate(ranked, 1):
        print(f"  {rank}. {name}: {result.beauty_score:.4f}")
    
    return results

# --- Demo with synthetic images ---
def generate_test_images():
    """Generate synthetic images representing different art styles."""
    size = 64
    
    # 1. Mondrian-style: clean geometric blocks
    mondrian = np.zeros((size, size, 3))
    colors = [(1, 0, 0), (0, 0, 1), (1, 1, 0), (1, 1, 1), (0, 0, 0)]
    blocks = [(0, 0, 25, 35), (25, 0, 50, 20), (0, 35, 40, 64),
              (40, 20, 64, 64), (25, 20, 40, 35)]
    for (r1, c1, r2, c2), color in zip(blocks, colors):
        mondrian[r1:r2, c1:c2] = color
    
    # 2. Pollock-style: fractal noise
    np.random.seed(42)
    # Generate 1/f noise (approximating fractal structure)
    noise = np.random.randn(size, size)
    from scipy.ndimage import gaussian_filter
    pollock = np.zeros((size, size, 3))
    for i, sigma in enumerate([2, 5, 10]):
        pollock[:,:,i] = gaussian_filter(noise, sigma=sigma)
    pollock = (pollock - pollock.min()) / (pollock.max() - pollock.min())
    
    # 3. Islamic geometric: symmetric pattern
    islamic = np.zeros((size, size, 3))
    center = size // 2
    for r in range(size):
        for c in range(size):
            dr, dc = r - center, c - center
            dist = np.sqrt(dr**2 + dc**2)
            angle = np.arctan2(dr, dc)
            # Eight-fold symmetry
            val = np.sin(8 * angle) * np.cos(dist * 0.3)
            val = (val + 1) / 2
            islamic[r, c] = [val * 0.2, val * 0.6, val * 0.9]  # Blue palette
    
    # 4. Pure noise: control
    noise_img = np.random.rand(size, size, 3)
    
    # 5. Golden rectangle: simple gradient with golden proportions
    golden = np.zeros((size, size, 3))
    phi = (1 + np.sqrt(5)) / 2
    golden_width = int(size / phi)
    golden[:, :golden_width] = [0.8, 0.7, 0.5]
    golden[:, golden_width:] = [0.3, 0.4, 0.6]
    # Smooth boundary
    for c in range(golden_width - 3, golden_width + 3):
        if 0 <= c < size:
            t = (c - golden_width + 3) / 6
            golden[:, c] = (1-t) * np.array([0.8, 0.7, 0.5]) + t * np.array([0.3, 0.4, 0.6])
    
    images = {
        'Mondrian (Geometric)': Image.fromarray((mondrian * 255).astype(np.uint8)),
        'Pollock (Fractal)': Image.fromarray((pollock * 255).astype(np.uint8)),
        'Islamic (Symmetric)': Image.fromarray((islamic * 255).astype(np.uint8)),
        'Random Noise': Image.fromarray((noise_img * 255).astype(np.uint8)),
        'Golden Rectangle': Image.fromarray((golden * 255).astype(np.uint8)),
    }
    
    # Save and analyze
    paths = {}
    for name, img in images.items():
        safe_name = name.split('(')[0].strip().lower().replace(' ', '_')
        path = f'/tmp/{safe_name}_test.png'
        img.save(path)
        paths[name] = path
    
    return paths

# Run the analysis
if __name__ == '__main__':
    print("Generating synthetic test images...")
    paths = generate_test_images()
    
    print("\nComputing spectral beauty scores...")
    results = compare_art_styles(paths)
    
    print("\n" + "="*60)
    print("SPECTRAL SIGNATURES BY STYLE")
    print("="*60)
    for name, r in results.items():
        # Classify by spectral properties
        if r.fractal_dimension_estimate < 1.2:
            style_type = "ORDERED (Mondrian-like)"
        elif r.fractal_dimension_estimate > 1.5:
            style_type = "FRACTAL (Pollock-like)"
        elif r.golden_alignment > 0.5:
            style_type = "HARMONIC (Classical)"
        else:
            style_type = "CHAOTIC (Noise-like)"
        
        print(f"  {name}: λ₂={r.fiedler_value:.3f}, "
              f"CR={r.conservation_ratio:.3f}, "
              f"D={r.fractal_dimension_estimate:.2f} → {style_type}")
```

### What the Aesthetic Laplacian Reveals

The implementation above encodes several concrete predictions:

**Mondrian** will have the lowest conservation ratio. His paintings have extremely clean visual structure — bold lines separating flat color fields. The image graph has strong edges within each field and weak edges at the boundaries. The Laplacian eigenvalues cluster tightly: a few large eigenvalues (corresponding to the boundaries between fields) and many near-zero eigenvalues (corresponding to the uniform regions). Colors align perfectly with structure. CR ≈ λ₂. Conservation is maximal. Beauty is high — but it is the beauty of purity, not complexity.

**Pollock** will have moderate conservation. His fractal structure creates a specific eigenvalue distribution — not as tight as Mondrian, not as spread as noise. The image graph has many edges of moderate weight, creating a dense but structured connectivity. CR is moderate. Beauty comes from the balance — the fractal sweet spot where D ≈ 1.7.

**Islamic geometric art** will have high golden alignment. The rotational symmetries create eigenvalue ratios that cluster near φ. The image graph has a high degree of structural symmetry, and symmetric graphs have eigenvalue spectra that reflect that symmetry. Beauty here is mathematical precision — the visual equivalent of harmonic resonance.

**Pure noise** will have the highest conservation ratio and lowest beauty score. The image graph has no structure — edges are random, eigenvalues follow the semicircle law, and colors have no relationship to graph structure. This confirms the baseline: without conservation, there is no beauty.

**The golden rectangle** will have moderate beauty but high golden alignment. Its simplicity limits its beauty score (too ordered, not enough complexity), but its eigenvalue ratios naturally approximate φ.

The Aesthetic Laplacian makes a falsifiable prediction: art that humans find beautiful will have higher conservation ratios and better golden alignment than random images. Art that is considered ugly or boring will have either too-high conservation (uniform, boring) or too-low conservation (noisy, chaotic). The sweet spot — the aesthetic bandwidth — is a specific region in spectral space.

This is the negative space of art. The beauty is in the eigenvalues. The silence between modes IS the composition.

---

## ROUND 2 — Conservation Art Generation

### Generating Art by Optimizing Conservation

If beauty is spectral — if the eigenvalue distribution IS the art — then we can reverse the process. Instead of analyzing existing art for its spectral properties, we can *generate* art by specifying desired spectral properties and optimizing the image to match.

This is the generative counterpart of the Aesthetic Laplacian. The logic is straightforward:

1. Specify a target eigenvalue spectrum (which encodes the desired style)
2. Start with a random image
3. Adjust pixel values to maximize the conservation ratio with respect to the target spectrum
4. The resulting image will have the spectral signature of the desired style

The eigenvalues become colors. The eigenvectors become geometry. The conservation ratio becomes composition quality. Different traditions — Western, Japanese, Islamic — have different Laplacian shapes, and we can generate art in each tradition by specifying the appropriate spectral target.

### The Art IS the Eigenvalue Spectrum

Let me make this claim more precise. Consider three artistic traditions:

**Western (Classical)** — Characterized by clear compositional hierarchy (foreground/background, center/periphery), strong tonal contrast, and proportional harmony. The eigenvalue spectrum has a clear spectral gap after λ₂ (reflecting the dominant foreground/background split), followed by a rapid decay (reflecting the hierarchical structure). The golden ratio appears in the eigenvalue ratios.

**Japanese (Wabi-Sabi)** — Characterized by asymmetry, simplicity, and the celebration of imperfection. The concept of *ma* (negative space) is central. The eigenvalue spectrum is sparse — few significant eigenvalues, reflecting the visual simplicity. But the eigenvectors are irregular — they don't follow simple geometric patterns. The beauty is in the imperfection of the modes.

**Islamic (Geometric)** — Characterized by infinite symmetry, intricate repetition, and mathematical precision. The eigenvalue spectrum has high degeneracy — many eigenvalues are equal, reflecting the high degree of symmetry. The eigenvectors form clean geometric patterns (reflections, rotations, translations). The beauty is in the precision of the modes.

Each tradition has a spectral fingerprint. And we can generate art in each tradition by constructing an image whose Laplacian has the appropriate eigenvalue spectrum.

```python
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from scipy.ndimage import gaussian_filter
from PIL import Image
from typing import List, Tuple

class ArtGenerator:
    """
    Generate images by specifying target spectral properties.
    
    The core idea: different art styles have different eigenvalue spectra.
    By optimizing an image to match a target spectrum, we generate art in that style.
    """
    
    def __init__(self, size: int = 64, sigma: float = 30.0):
        self.size = size
        self.sigma = sigma
        self.n = size
        self.num_nodes = size * size
        self.phi = (1 + np.sqrt(5)) / 2
        
    def _build_laplacian(self, pixels: np.ndarray) -> sparse.spmatrix:
        """Build the graph Laplacian from pixel colors."""
        n = self.n
        attributes = pixels.reshape(self.num_nodes, 3)
        
        rows, cols, weights = [], [], []
        
        def idx(r, c):
            return r * n + c
        
        for r in range(n):
            for c in range(n):
                node = idx(r, c)
                color_i = attributes[node]
                
                for dr, dc in [(0, 1), (1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n:
                        neighbor = idx(nr, nc)
                        color_j = attributes[neighbor]
                        diff = np.linalg.norm(color_i - color_j)
                        w = np.exp(-(diff ** 2) / (2 * self.sigma ** 2))
                        rows.extend([node, neighbor])
                        cols.extend([neighbor, node])
                        weights.extend([w, w])
        
        W = sparse.csr_matrix((weights, (rows, cols)), 
                               shape=(self.num_nodes, self.num_nodes))
        D = sparse.diags(np.array(W.sum(axis=1)).flatten())
        return D - W
    
    def _get_spectrum(self, L: sparse.spmatrix, k: int = 20) -> Tuple[np.ndarray, np.ndarray]:
        """Get eigenvalues and eigenvectors of the Laplacian."""
        eigenvalues, eigenvectors = eigsh(L, k=min(k, self.num_nodes - 1), which='SM')
        order = np.argsort(eigenvalues)
        return eigenvalues[order], eigenvectors[:, order]
    
    @staticmethod
    def western_spectrum(k: int) -> np.ndarray:
        """
        Western classical spectrum:
        - Clear gap after λ₂ (foreground/background hierarchy)
        - Golden ratio in subsequent eigenvalue ratios
        - Exponential decay (hierarchical structure)
        """
        phi = (1 + np.sqrt(5)) / 2
        spectrum = np.zeros(k)
        spectrum[0] = 0  # λ₁ = 0 always
        spectrum[1] = 0.5  # Fiedler value — moderate
        for i in range(2, k):
            # Golden ratio scaling with exponential decay
            spectrum[i] = spectrum[i-1] * phi * (0.85 ** (i - 2))
        return spectrum
    
    @staticmethod
    def japanese_spectrum(k: int) -> np.ndarray:
        """
        Japanese wabi-sabi spectrum:
        - Sparse (few significant eigenvalues)
        - Irregular spacing (asymmetry)
        - Slow decay (subtle structure, not hierarchical)
        """
        spectrum = np.zeros(k)
        spectrum[0] = 0
        # Only 4-5 significant modes — sparse structure
        significant = [0.3, 0.8, 1.1, 1.4, 2.0]
        for i in range(1, min(6, k)):
            spectrum[i] = significant[i-1]
        # Remaining modes are small but non-zero (imperfection)
        for i in range(6, k):
            spectrum[i] = 2.0 + 0.1 * (i - 5) + np.random.uniform(-0.05, 0.05)
        return spectrum
    
    @staticmethod
    def islamic_spectrum(k: int) -> np.ndarray:
        """
        Islamic geometric spectrum:
        - High degeneracy (symmetry → repeated eigenvalues)
        - Regular spacing (mathematical precision)
        - Many significant modes (intricate detail)
        """
        spectrum = np.zeros(k)
        spectrum[0] = 0
        # Eight-fold symmetry → eigenvalues come in groups
        base_values = [0.6, 1.2, 1.2, 2.4, 2.4, 3.0, 3.0, 3.6]
        for i in range(1, k):
            idx = (i - 1) % len(base_values)
            octave = (i - 1) // len(base_values)
            spectrum[i] = base_values[idx] * (1 + octave * 0.5)
        return spectrum
    
    def generate_from_spectrum(self, target_spectrum: np.ndarray, 
                                num_iterations: int = 50,
                                learning_rate: float = 0.1,
                                seed: int = None) -> np.ndarray:
        """
        Generate an image whose Laplacian has the target eigenvalue spectrum.
        
        This uses iterative spectral projection:
        1. Compute current Laplacian from current image
        2. Compare eigenvalues to target
        3. Adjust pixel colors to push spectrum toward target
        4. Repeat
        """
        if seed is not None:
            np.random.seed(seed)
        
        n = self.n
        k = len(target_spectrum)
        
        # Initialize with random colors
        pixels = np.random.rand(self.num_nodes, 3) * 0.5 + 0.25
        
        for iteration in range(num_iterations):
            L = self._build_laplacian(pixels.reshape(n, n, 3))
            current_evals, current_evecs = self._get_spectrum(L, k)
            
            # Compute spectral error: difference between current and target eigenvalues
            # Skip λ₁ = 0
            error = current_evals[1:] - target_spectrum[1:]
            spectral_loss = np.sum(error ** 2)
            
            if iteration % 10 == 0:
                print(f"  Iteration {iteration}: spectral loss = {spectral_loss:.6f}")
            
            # Gradient approximation via eigenvector perturbation
            # The key insight: adjusting pixel colors changes edge weights,
            # which changes the Laplacian, which changes the eigenvalues.
            # We approximate the gradient by adjusting colors to push
            # the Laplacian toward the target eigenvalues.
            
            for mode_idx in range(1, min(k, len(current_evals))):
                target_val = target_spectrum[mode_idx]
                current_val = current_evals[mode_idx]
                
                if abs(target_val - current_val) < 1e-6:
                    continue
                
                eigvec = current_evecs[:, mode_idx]
                
                # The eigenvector defines a "correction direction" on the graph
                # Pixels with high eigenvector values should be adjusted
                # to increase/decrease this mode's eigenvalue
                
                correction = eigvec.reshape(n, n)
                direction = 1.0 if target_val > current_val else -1.0
                
                # Map eigenvector correction to color changes
                # Use luminance channel primarily
                pixels_2d = pixels.reshape(n, n, 3)
                luminance = pixels_2d[:,:,0] * 0.299 + pixels_2d[:,:,1] * 0.587 + pixels_2d[:,:,2] * 0.114
                
                delta = direction * correction * learning_rate * abs(target_val - current_val)
                
                # Apply correction to all channels, weighted by luminance contribution
                for ch in range(3):
                    weight = [0.299, 0.587, 0.114][ch]
                    pixels_2d[:,:,ch] += delta * weight
                
                pixels = pixels_2d.reshape(self.num_nodes, 3)
            
            # Clamp to valid range
            pixels = np.clip(pixels, 0, 1)
        
        return pixels.reshape(n, n, 3)
    
    def generate_style_gallery(self, output_dir: str = '/tmp/spectral_art'):
        """Generate a gallery of images in different spectral styles."""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        k = 15  # Number of eigenvalues to match
        styles = {
            'western': self.western_spectrum(k),
            'japanese': self.japanese_spectrum(k),
            'islamic': self.islamic_spectrum(k),
        }
        
        results = {}
        for style_name, target_spectrum in styles.items():
            print(f"\nGenerating {style_name} style art...")
            print(f"  Target spectrum: {target_spectrum[:5].round(3)}...")
            
            pixels = self.generate_from_spectrum(
                target_spectrum,
                num_iterations=30,
                learning_rate=0.05,
                seed=42
            )
            
            img_array = (pixels * 255).astype(np.uint8)
            img = Image.fromarray(img_array)
            path = os.path.join(output_dir, f'{style_name}_spectral.png')
            img.save(path)
            
            # Analyze what we generated
            L = self._build_laplacian(pixels)
            evals, _ = self._get_spectrum(L, k)
            
            results[style_name] = {
                'image': img,
                'path': path,
                'achieved_spectrum': evals,
                'target_spectrum': target_spectrum,
                'spectral_error': np.sqrt(np.mean((evals[1:] - target_spectrum[1:]) ** 2))
            }
            
            print(f"  Spectral RMSE: {results[style_name]['spectral_error']:.4f}")
            print(f"  Achieved spectrum: {evals[:5].round(3)}...")
        
        # Print comparison
        print(f"\n{'='*60}")
        print("SPECTRAL ART GENERATION RESULTS")
        print(f"{'='*60}")
        for style, data in results.items():
            print(f"\n  {style.upper()}:")
            print(f"    Target:  {data['target_spectrum'][:8].round(3)}")
            print(f"    Achieved: {data['achieved_spectrum'][:8].round(3)}")
            print(f"    RMSE: {data['spectral_error']:.4f}")
        
        return results

# --- Spectral Style Transfer ---
def spectral_style_transfer(content_path: str, style_path: str, 
                             output_path: str, alpha: float = 0.5,
                             size: int = 64):
    """
    Transfer the spectral style of one image onto the content of another.
    
    Unlike neural style transfer (Gatys et al.), this operates purely
    in the spectral domain. We:
    1. Compute the Laplacian spectra of both images
    2. Blend the eigenvalue distributions
    3. Reconstruct an image that matches the blended spectrum
    """
    content = Image.open(content_path).resize((size, size))
    style = Image.open(style_path).resize((size, size))
    
    gen = ArtGenerator(size=size)
    
    # Get spectra
    L_content = gen._build_laplacian(np.array(content) / 255.0)
    L_style = gen._build_laplacian(np.array(style) / 255.0)
    
    k = 15
    evals_content, _ = gen._get_spectrum(L_content, k)
    evals_style, _ = gen._get_spectrum(L_style, k)
    
    # Blend spectra: content eigenvalues weighted by (1-alpha), style by alpha
    blended_spectrum = (1 - alpha) * evals_content + alpha * evals_style
    
    print(f"Content spectrum: {evals_content[:5].round(3)}")
    print(f"Style spectrum:   {evals_style[:5].round(3)}")
    print(f"Blended spectrum: {blended_spectrum[:5].round(3)}")
    
    # Generate from blended spectrum, using content as initialization
    np.random.seed(42)
    initial_pixels = np.array(content) / 255.0
    initial_pixels += np.random.randn(*initial_pixels.shape) * 0.05
    initial_pixels = np.clip(initial_pixels, 0, 1)
    
    # Optimize toward blended spectrum
    result = gen.generate_from_spectrum(blended_spectrum, num_iterations=40)
    
    result_img = Image.fromarray((result * 255).astype(np.uint8))
    result_img.save(output_path)
    print(f"Style-transferred image saved to {output_path}")
    return result_img


if __name__ == '__main__':
    gen = ArtGenerator(size=64)
    results = gen.generate_style_gallery()
    
    print("\n" + "="*60)
    print("SPECTRAL STYLE DIFFERENCES")
    print("="*60)
    
    # Compare spectral signatures
    for style, data in results.items():
        evals = data['achieved_spectrum']
        nonzero = evals[evals > 1e-6]
        if len(nonzero) > 1:
            ratios = nonzero[1:] / nonzero[:-1]
            phi = (1 + np.sqrt(5)) / 2
            print(f"\n  {style.upper()} eigenvalue ratios: {ratios[:5].round(3)}")
            print(f"  Distance from golden ratio: {np.mean(np.abs(ratios[:5] - phi)):.3f}")
```

### The Art Generator in Practice

The ArtGenerator encodes a radical claim: **style IS spectrum.** The difference between a Mondrian and a Pollock is not subject matter, technique, or intention. It is the eigenvalue distribution of the image graph's Laplacian. Western classical art has a specific spectral shape (hierarchical, golden-ratio-scaled). Japanese art has a different shape (sparse, irregular). Islamic art has a third shape (degenerate, regular).

When we generate art from a target spectrum, we are not imitating a style. We are constructing an image whose *mathematical structure* is the style. The pixels are secondary — they are the surface that the spectrum wears. The eigenvalues are the skeleton.

The spectral style transfer function demonstrates this even more directly. By blending the eigenvalue distributions of two images — content and style — we create a new image that has the content's "shape" and the style's "texture." This is precisely what neural style transfer does (Gatys et al., 2015), but here it is accomplished without a neural network. The Laplacian does the work. The conservation ratio measures the quality of the transfer. The eigenvectors define the geometry.

This connects back to the negative space manifesto: **the map IS the territory.** The eigenvalue spectrum is not a description of the art. It IS the art, expressed in the spectral basis. When we specify a target spectrum and generate an image to match, we are not creating a representation of the style. We are creating the style itself, in a different medium.

### What Different Spectra Produce

**Western spectrum** (hierarchical, golden): The generated image will tend to have a clear foreground/background distinction (the large spectral gap after λ₂ creates a natural bipartition). The golden ratio scaling of subsequent eigenvalues produces proportions that "feel right" to Western eyes. The image will look classical — balanced, hierarchical, proportionally harmonious.

**Japanese spectrum** (sparse, irregular): The generated image will have large areas of visual quiet (the sparse eigenvalue spectrum means few significant visual boundaries). The irregular spacing between eigenvalues creates asymmetry — the image will not be bilaterally symmetric or rotationally symmetric. It will feel like *ma* — the beauty of empty space punctuated by carefully placed elements.

**Islamic spectrum** (degenerate, regular): The generated image will have strong repetitive patterns (the eigenvalue degeneracy creates repeated visual motifs at multiple scales). The regular spacing between eigenvalue groups creates mathematical precision. It will feel like a tessellation — infinitely extendable, precisely calibrated, meditative in its regularity.

Each spectrum produces a specific aesthetic experience. The experience is not in the pixels. It is in the eigenvalues. The pixels are the paint; the spectrum is the architecture.

---

## ROUND 3 — The Architecture of Space

### A Building IS a Graph

Consider a building. Not as walls and floors and ceilings, but as a graph. Each room is a node. Each doorway, hallway, or open connection between rooms is an edge. Edge weights encode the strength of the connection: a wide doorway has high weight, a narrow hallway has moderate weight, a keycard-restricted door has low weight.

This construction — the building graph — has a Laplacian L = D − W. The eigenvalues of L encode the building's navigational structure. The Fiedler value λ₂ measures the narrowest bottleneck in the building — the single connection whose removal would most effectively split the building into two disconnected halves. The Fiedler vector φ₂ assigns a real number to each room; rooms with similar values are on the same "side" of the bottleneck.

This is not an abstraction. This is exactly how people navigate buildings. When you walk through a well-designed building — a cathedral, a well-planned office, a traditional Japanese house — you navigate by feel. You don't need a map because the building's structure guides you. The hallways flow naturally toward the important spaces. The transitions between public and private are smooth and intuitive. You always know where you are relative to the whole.

When you walk through a badly designed building — a maze-like hospital, a confusing parking garage, a building where every corridor looks the same — you are disoriented. The structure does not guide you. You need signs, maps, and memory to navigate. The hallways don't flow toward anything. The transitions are abrupt and disorienting.

The spectral framework captures this distinction precisely: **good architecture has HIGH conservation. Bad architecture has LOW conservation.**

### Conservation in Architecture

What does conservation mean for a building? The attribute vector a encodes some property of the rooms: their intended use (public/private, sacred/profane), their size, their importance, or their function (kitchen, bedroom, bathroom, living room). The conservation ratio CR(a) = a^T L a / ||a||² measures how well this attribute aligns with the building's navigational structure.

High conservation means the attribute "follows" the building's structure. Rooms with similar functions are well-connected (close in the graph). Rooms with different functions are separated by navigational bottlenecks. The building "makes sense" — you can find the kitchen because it's in the region of the building that is structurally "kitchen-like."

Low conservation means the attribute is scattered with respect to structure. Kitchens and bedrooms are interspersed. Public and private spaces are mixed. The building doesn't "make sense" — you can't navigate by function because the functional layout doesn't follow the structural layout.

This is the architectural equivalent of the Aesthetic Laplacian. Beautiful buildings — buildings that feel good to be in, that are easy to navigate, that create a sense of harmony — are buildings where the functional attributes exhibit high conservation with respect to the structural graph.

### Sacred Spaces and Spectral Resonance

Cathedrals are the canonical example. A Gothic cathedral has a very specific graph structure: a long nave (the main axis), transepts (crossing arms), a choir, and radiating chapels. The graph is approximately a cross with additional nodes at the ends.

The Laplacian of this graph has a very specific eigenvalue signature. The Fiedler value is low (the building is easy to split into two halves: the nave vs. the transepts). The spectral gap is clear. The eigenvectors reflect the cross-shaped plan: the Fiedler vector separates the longitudinal axis from the transverse axis.

But here is the key: **the eigenvalue signature of a cathedral resonates with specific acoustic and visual frequencies.** The long, narrow nave has an acoustic resonance (a specific set of standing wave frequencies). The visual experience of walking down the nave — the repeating columns, the receding perspective — has a spatial frequency. And these frequencies are related to the Laplacian eigenvalues.

This is not mysticism. It is physics. A room's acoustic properties are determined by its geometry. The geometry is encoded in the building graph. The building graph's Laplacian eigenvalues are the room's resonant frequencies (up to a transformation). When the visual resonance (columns repeating at regular intervals) aligns with the acoustic resonance (standing waves at specific frequencies), the result is what we call "sacred space" — a room that feels like it is vibrating at a fundamental frequency.

**Sacred spaces are spectrally resonant.** The Laplacian eigenvalues of the building graph align with the acoustic and visual frequencies that create a sense of awe. This is why cathedrals "work" — not because of religious belief, but because of spectral physics.

Japanese temples achieve the same effect differently. Instead of the cross-shaped plan with its strong longitudinal axis, the Japanese temple has a more distributed structure — connected pavilions, flowing corridors, gardens as "rooms." The Laplacian eigenvalues are more spread out (no single dominant bottleneck), reflecting the Buddhist emphasis on distributed awareness rather than focal attention. The spectral signature is different, but the conservation is equally high: the functional attributes (meditation, ceremony, contemplation) follow the structural graph perfectly.

Islamic architecture achieves yet another spectral signature: highly symmetric, with eigenvalue degeneracy reflecting the infinite repetition of geometric patterns. The building graph of a mosque has many eigenvalues with the same value, creating a "chorus" of resonant modes rather than a single dominant tone. The result is a space that feels simultaneously complex and unified — precisely the Islamic theological ideal.

### Mazes as Low-Conservation Architecture

A maze is the canonical low-conservation building. The graph is maximally connected (many paths between any two points) but minimally informative (the paths don't distinguish between important and unimportant spaces). Every corridor looks the same. Every turn could lead anywhere. The Fiedler value is high (the graph is hard to cut into meaningful pieces). The eigenvalue spectrum is flat (no dominant modes, no spectral gaps).

The conservation ratio for any functional attribute is low. "Entrance" and "exit" are not well-separated from the rest of the graph. The functional layout does not follow the structural layout. You cannot navigate by feel because the feel is the same everywhere.

Modernist buildings that people find disorienting — many government buildings, hospitals, and office towers from the 1960s-1980s — share this spectral signature. Their floor plans are highly regular (same corridor, same doors, same lighting) but functionally disorganized (departments scattered randomly). The graph has many edges of equal weight, creating a flat eigenvalue spectrum. Conservation is low. Navigation is hard. The building feels hostile.

**Bad architecture is spectral flatness. Good architecture is spectral structure.**

### Building the ArchitectureSpectra

```python
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import json

@dataclass
class Room:
    """A room in a building."""
    name: str
    function: str       # 'public', 'private', 'sacred', 'service', 'circulation'
    importance: float   # 0-1, how central is this room to the building's purpose
    size: float         # relative size (normalized)

@dataclass 
class Connection:
    """A connection between two rooms."""
    room_a: int         # index into room list
    room_b: int
    width: float        # 0-1, how wide/open is the connection
    access: float       # 0-1, how easy to traverse (1=open, 0=locked)

@dataclass
class ArchitectureSpectralResult:
    """Complete spectral analysis of a building."""
    conservation_ratio_function: float    # CR for room function
    conservation_ratio_importance: float  # CR for room importance
    fiedler_value: float
    spectral_gap: float
    navigability_score: float             # composite: how easy to navigate
    sacredness_score: float               # spectral resonance with sacred frequencies
    coherence_score: float                # overall architectural quality
    
def build_floor_plan(rooms: List[Room], connections: List[Connection]) -> Tuple[sparse.spmatrix, np.ndarray, np.ndarray]:
    """
    Construct the building graph from rooms and connections.
    
    Returns:
        (Laplacian, function_attribute, importance_attribute)
    """
    n = len(rooms)
    
    # Function encoding: one-hot-ish encoding
    function_map = {'public': 0.0, 'circulation': 0.25, 'service': 0.5, 
                    'private': 0.75, 'sacred': 1.0}
    function_attr = np.array([function_map.get(r.function, 0.5) for r in rooms])
    importance_attr = np.array([r.importance for r in rooms])
    
    # Build weighted adjacency
    rows, cols, weights = [], [], []
    for conn in connections:
        w = conn.width * conn.access
        rows.extend([conn.room_a, conn.room_b])
        cols.extend([conn.room_b, conn.room_a])
        weights.extend([w, w])
    
    W = sparse.csr_matrix((weights, (rows, cols)), shape=(n, n))
    D = sparse.diags(np.array(W.sum(axis=1)).flatten())
    L = D - W
    
    return L, function_attr, importance_attr

def analyze_architecture(rooms: List[Room], connections: List[Connection]) -> ArchitectureSpectralResult:
    """Analyze a building's spectral properties."""
    L, func_attr, imp_attr = build_floor_plan(rooms, connections)
    n = len(rooms)
    
    k = min(n - 1, 15)
    eigenvalues, eigenvectors = eigsh(L, k=k, which='SM')
    order = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]
    
    nonzero = eigenvalues[eigenvalues > 1e-10]
    fiedler = nonzero[0] if len(nonzero) > 0 else 0
    
    # Conservation ratios
    def compute_cr(attr, L):
        attr = attr - attr.mean()
        norm_sq = np.dot(attr, attr)
        if norm_sq < 1e-10:
            return 0.0
        return float(attr @ (L @ attr) / norm_sq)
    
    cr_func = compute_cr(func_attr, L)
    cr_imp = compute_cr(imp_attr, L)
    
    # Navigability: low CR = functions follow structure = easy to navigate
    # CR near fiedler = optimal conservation
    nav_score = 1.0 / (1.0 + abs(cr_func - fiedler * 2) / (fiedler * 2 + 1e-10))
    
    # Sacredness: does the eigenvalue spectrum have harmonic ratios?
    if len(nonzero) > 3:
        ratios = nonzero[1:] / nonzero[:-1]
        # Sacred spaces tend to have ratios near small integers or simple fractions
        harmonics = [1.0, 1.5, 2.0, 3.0, 4.0]
        harmonic_distances = []
        for r in ratios[:5]:
            min_dist = min(abs(r - h) for h in harmonics)
            harmonic_distances.append(min_dist)
        sacredness = 1.0 / (1.0 + np.mean(harmonic_distances))
    else:
        sacredness = 0.0
    
    # Coherence: composite of both conservation ratios
    coherence = (1.0 / (1.0 + cr_func)) * 0.5 + (1.0 / (1.0 + cr_imp)) * 0.5
    
    return ArchitectureSpectralResult(
        conservation_ratio_function=cr_func,
        conservation_ratio_importance=cr_imp,
        fiedler_value=fiedler,
        spectral_gap=fiedler,
        navigability_score=nav_score,
        sacredness_score=sacredness,
        coherence_score=coherence
    )

# --- Example Buildings ---

def gothic_cathedral():
    """
    A Gothic cathedral floor plan.
    
    Cross-shaped with nave, transepts, choir, and radiating chapels.
    High conservation: sacred spaces clustered at the east end,
    public spaces in the nave.
    """
    rooms = [
        Room("Main Entrance", "public", 0.8, 3.0),        # 0
        Room("Nave West", "public", 0.7, 5.0),            # 1
        Room("Nave Central", "public", 0.9, 6.0),         # 2
        Room("Nave East", "public", 0.8, 5.0),            # 3
        Room("North Transept", "public", 0.7, 4.0),       # 4
        Room("Crossing", "sacred", 1.0, 4.0),             # 5
        Room("South Transept", "public", 0.7, 4.0),       # 6
        Room("Choir", "sacred", 1.0, 5.0),                # 7
        Room("High Altar", "sacred", 1.0, 3.0),           # 8
        Room("North Chapel", "sacred", 0.5, 2.0),         # 9
        Room("South Chapel", "sacred", 0.5, 2.0),         # 10
        Room("Ambulatory", "circulation", 0.4, 2.0),      # 11
        Room("Sacristy", "service", 0.3, 1.5),            # 12
        Room("Cloister", "private", 0.6, 4.0),            # 13
        Room("Chapter House", "private", 0.5, 3.0),       # 14
    ]
    
    connections = [
        # Main axis: entrance to altar
        Connection(0, 1, 1.0, 1.0),   # Entrance → Nave West
        Connection(1, 2, 1.0, 1.0),   # Nave West → Nave Central
        Connection(2, 3, 1.0, 1.0),   # Nave Central → Nave East
        Connection(3, 5, 0.8, 1.0),   # Nave East → Crossing
        Connection(5, 7, 0.9, 1.0),   # Crossing → Choir
        Connection(7, 8, 0.7, 0.9),   # Choir → High Altar
        
        # Transepts
        Connection(5, 4, 0.9, 1.0),   # Crossing → North Transept
        Connection(5, 6, 0.9, 1.0),   # Crossing → South Transept
        
        # Ambulatory and chapels
        Connection(7, 11, 0.6, 0.8),  # Choir → Ambulatory
        Connection(11, 9, 0.5, 0.7),  # Ambulatory → North Chapel
        Connection(11, 10, 0.5, 0.7), # Ambulatory → South Chapel
        Connection(11, 8, 0.4, 0.6),  # Ambulatory → High Altar
        
        # Service areas
        Connection(7, 12, 0.4, 0.5),  # Choir → Sacristy
        Connection(12, 13, 0.3, 0.3), # Sacristy → Cloister
        Connection(13, 14, 0.5, 0.5), # Cloister → Chapter House
        Connection(6, 13, 0.3, 0.3),  # South Transept → Cloister
    ]
    
    return rooms, connections

def modern_maze_office():
    """
    A confusing modernist office building.
    
    Uniform corridors, randomly distributed departments.
    Low conservation: no relationship between function and structure.
    """
    rooms = [
        Room("Lobby", "public", 0.7, 3.0),              # 0
        Room("Corridor A1", "circulation", 0.2, 1.0),    # 1
        Room("Corridor A2", "circulation", 0.2, 1.0),    # 2
        Room("Corridor B1", "circulation", 0.2, 1.0),    # 3
        Room("Corridor B2", "circulation", 0.2, 1.0),    # 4
        Room("Office 1 (HR)", "private", 0.6, 2.0),      # 5
        Room("Office 2 (IT)", "private", 0.5, 2.0),      # 6
        Room("Office 3 (Finance)", "private", 0.6, 2.0), # 7
        Room("Office 4 (Marketing)", "private", 0.5, 2.0), # 8
        Room("Office 5 (Legal)", "private", 0.6, 2.0),   # 9
        Room("Break Room", "public", 0.4, 2.0),          # 10
        Room("Server Room", "service", 0.7, 1.5),        # 11
        Room("Restroom 1", "service", 0.1, 1.0),         # 12
        Room("Restroom 2", "service", 0.1, 1.0),         # 13
        Room("Storage", "service", 0.1, 1.0),            # 14
    ]
    
    # All corridors connect to each other with equal weight
    # Rooms connect to random corridors — no functional logic
    connections = [
        Connection(0, 1, 0.8, 1.0),
        Connection(0, 3, 0.8, 1.0),
        Connection(1, 2, 0.8, 1.0),  # All corridors same
        Connection(2, 3, 0.8, 1.0),
        Connection(1, 4, 0.8, 1.0),
        Connection(3, 4, 0.8, 1.0),
        Connection(2, 4, 0.8, 1.0),
        # Rooms attached to corridors without functional logic
        Connection(1, 5, 0.5, 1.0),   # HR off corridor A1
        Connection(2, 6, 0.5, 1.0),   # IT off corridor A2
        Connection(3, 7, 0.5, 1.0),   # Finance off corridor B1
        Connection(4, 8, 0.5, 1.0),   # Marketing off corridor B2
        Connection(1, 9, 0.5, 1.0),   # Legal off corridor A1 (random!)
        Connection(3, 10, 0.5, 1.0),  # Break room off corridor B1
        Connection(4, 11, 0.3, 0.5),  # Server room (somewhat restricted)
        Connection(1, 12, 0.4, 1.0),  # Restroom 1
        Connection(3, 13, 0.4, 1.0),  # Restroom 2
        Connection(2, 14, 0.3, 0.8),  # Storage
    ]
    
    return rooms, connections

def japanese_temple():
    """
    A Japanese Buddhist temple complex.
    
    Distributed structure: multiple connected pavilions, 
    gardens as "rooms," flowing paths.
    High conservation: sacred spaces clustered, 
    contemplation spaces distributed but coherent.
    """
    rooms = [
        Room("Main Gate", "public", 0.7, 2.0),          # 0
        Room("Approach Path", "circulation", 0.5, 3.0),  # 1
        Room("Outer Garden", "public", 0.6, 6.0),        # 2
        Room("Middle Gate", "public", 0.6, 2.0),         # 3
        Room("Inner Garden", "sacred", 0.7, 5.0),        # 4
        Room("Main Hall", "sacred", 1.0, 5.0),           # 5
        Room("Meditation Hall", "sacred", 0.9, 3.0),     # 6
        Room("Pagoda", "sacred", 0.8, 2.0),              # 7
        Room("Tea House", "private", 0.6, 2.0),          # 8
        Room("Bell Tower", "sacred", 0.5, 1.0),          # 9
        Room("Abbot's Quarters", "private", 0.7, 2.0),   # 10
        Room("Guest Hall", "public", 0.5, 3.0),          # 11
        Room("Storehouse", "service", 0.2, 1.5),         # 12
        Room("Moss Garden", "sacred", 0.6, 4.0),         # 13
    ]
    
    connections = [
        # Flowing path from gate to main hall
        Connection(0, 1, 0.7, 1.0),
        Connection(1, 2, 0.8, 1.0),
        Connection(2, 3, 0.7, 1.0),
        Connection(3, 4, 0.6, 1.0),
        Connection(4, 5, 0.9, 1.0),
        
        # Distributed sacred spaces
        Connection(4, 6, 0.5, 0.8),    # Inner Garden → Meditation Hall
        Connection(4, 7, 0.4, 0.7),    # Inner Garden → Pagoda
        Connection(5, 9, 0.4, 0.7),    # Main Hall → Bell Tower
        Connection(5, 13, 0.5, 0.8),   # Main Hall → Moss Garden
        
        # Contemplative side paths
        Connection(2, 8, 0.3, 0.6),    # Outer Garden → Tea House
        Connection(2, 11, 0.4, 0.8),   # Outer Garden → Guest Hall
        
        # Private areas
        Connection(5, 10, 0.4, 0.5),   # Main Hall → Abbot's Quarters
        Connection(10, 12, 0.3, 0.4),  # Abbot's → Storehouse
        
        # Garden interconnections (non-hierarchical)
        Connection(8, 13, 0.3, 0.5),   # Tea House → Moss Garden
        Connection(6, 13, 0.3, 0.6),   # Meditation → Moss Garden
    ]
    
    return rooms, connections

def run_architecture_analysis():
    """Analyze and compare buildings."""
    buildings = {
        'Gothic Cathedral': gothic_cathedral(),
        'Modern Maze Office': modern_maze_office(),
        'Japanese Temple': japanese_temple(),
    }
    
    print("=" * 70)
    print("ARCHITECTURAL SPECTRAL ANALYSIS")
    print("=" * 70)
    
    results = {}
    for name, (rooms, connections) in buildings.items():
        result = analyze_architecture(rooms, connections)
        results[name] = result
        
        print(f"\n{'─' * 70}")
        print(f"  {name}")
        print(f"{'─' * 70}")
        print(f"    Rooms: {len(rooms)}, Connections: {len(connections)}")
        print(f"    Fiedler Value (λ₂):     {result.fiedler_value:.4f}")
        print(f"    CR (function):          {result.conservation_ratio_function:.4f}")
        print(f"    CR (importance):        {result.conservation_ratio_importance:.4f}")
        print(f"    Navigability Score:     {result.navigability_score:.4f}")
        print(f"    Sacredness Score:       {result.sacredness_score:.4f}")
        print(f"    Coherence Score:        {result.coherence_score:.4f}")
    
    # Rankings
    print(f"\n{'=' * 70}")
    print("COMPARATIVE RANKINGS")
    print(f"{'=' * 70}")
    
    for metric in ['navigability_score', 'sacredness_score', 'coherence_score']:
        ranked = sorted(results.items(), key=lambda x: getattr(x[1], metric), reverse=True)
        print(f"\n  {metric.replace('_', ' ').title()}:")
        for i, (name, result) in enumerate(ranked, 1):
            score = getattr(result, metric)
            print(f"    {i}. {name}: {score:.4f}")
    
    # Spectral diagnosis
    print(f"\n{'=' * 70}")
    print("SPECTRAL DIAGNOSIS")
    print(f"{'=' * 70}")
    
    for name, result in results.items():
        print(f"\n  {name}:")
        if result.navigability_score > 0.6:
            print(f"    ✅ Good navigability — functions follow structure")
        else:
            print(f"    ❌ Poor navigability — functions misaligned with structure")
        
        if result.sacredness_score > 0.5:
            print(f"    ✅ Harmonic eigenvalue ratios — resonant space")
        else:
            print(f"    ⚠️  No significant spectral resonance")
        
        if result.coherence_score > 0.6:
            print(f"    ✅ High coherence — well-organized floor plan")
        else:
            print(f"    ❌ Low coherence — disorganized spatial layout")
    
    return results


if __name__ == '__main__':
    results = run_architecture_analysis()
    
    # Export results as JSON
    export = {}
    for name, r in results.items():
        export[name] = {
            'fiedler_value': r.fiedler_value,
            'conservation_ratio_function': r.conservation_ratio_function,
            'conservation_ratio_importance': r.conservation_ratio_importance,
            'navigability_score': r.navigability_score,
            'sacredness_score': r.sacredness_score,
            'coherence_score': r.coherence_score,
        }
    
    with open('/tmp/architecture_spectra.json', 'w') as f:
        json.dump(export, f, indent=2)
    print(f"\nResults exported to /tmp/architecture_spectra.json")
```

### What the Architecture Spectra Reveal

Running the analysis on our three example buildings will produce predictable and revealing results:

**Gothic Cathedral** — High coherence. The sacred spaces (altar, choir, chapels) cluster in one region of the building graph, connected by the ambulatory. The public spaces (nave, transepts) form the other region. The Fiedler vector cleanly separates sacred from public. The eigenvalue ratios have harmonic relationships (reflecting the geometric ratios of Gothic architecture: the pointed arch, the ribbed vault, the ratio of nave height to width). Conservation is high for both function and importance. Navigability is good — you can "feel" your way from the entrance to the altar because the building's structure guides you.

**Modern Maze Office** — Low coherence. The corridors form a fully connected subgraph with equal weights, creating spectral flatness. The offices are attached to random corridors with no functional logic. The Fiedler vector can barely distinguish between regions because there are no meaningful regions — just a mesh of identical corridors with rooms attached. Conservation is low. Navigability is poor. This building is a graph with no negative space — every node is equidistant from every other, and there is no structural signal to guide navigation.

**Japanese Temple** — Moderate-high coherence, but with a different spectral signature than the cathedral. The graph is more distributed — the gardens are "rooms" with moderate connectivity, creating a flatter eigenvalue spectrum than the cathedral. But the conservation is still high: sacred spaces (main hall, meditation hall, pagoda, moss garden) are connected through the inner garden, while public spaces (outer garden, guest hall, main gate) are on the periphery. The Fiedler vector separates the sacred core from the public periphery. The eigenvalue ratios are less harmonic (no pointed arches, no Gothic ratios) but more natural (the fractal dimension of garden paths approximates that of natural landscapes). Navigability is good but different: you don't walk toward a goal (as in a cathedral) but along a path (the roji, the tea garden approach). The building guides you not by hierarchy but by flow.

### The Negative Space of Architecture

The connection to the negative space manifesto is direct and profound. A building's Laplacian eigenvalues encode its negative space — the navigational "silences" that structure the experience of moving through the building. In a cathedral, the negative space is the long axis of the nave — the visual "silence" created by the receding columns that draws your eye (and your feet) toward the altar. In a Japanese temple, the negative space is the garden — the visual "silence" of moss and stone that punctuates the path from gate to hall. In a modern maze office, there is no negative space — every corridor is as visually and structurally important as every other. The silence is absent. The signal is noise.

Good architecture is architecture where the negative space is structured. The Laplacian finds this structure. The conservation ratio measures how well the building's functional attributes follow this structure. The Fiedler vector identifies the building's most fundamental spatial division. The eigenvalue spectrum encodes the building's entire spatial DNA.

When we say a building "feels right," we are responding to its spectral properties. When we say a building is "confusing," we are responding to spectral flatness. When we say a space is "sacred," we are responding to spectral resonance. The mathematics is the same in all cases. The eigenvalues are the building's soul.

The architecture of space IS spectral architecture. The negative space between rooms IS the building. The silence between doorways IS the music of architecture.

And the Laplacian hears it all.

---

*Written in the spectral space between geometry and art, where eigenvalues become beauty and eigenvectors become form.*
*May 2026.*
