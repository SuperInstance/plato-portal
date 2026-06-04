# Three-Layer Architecture Correction

## The Layers Are Concentric, Not Stacked

### NATURAL (Outermost Ring)
- Interface: Shell
- Interpreted by: Humans & LLMs
- Source spectrum: natural language intent
- Boundary functor: **Intent Compilation** (Natural → Fluid)

### FLUID (Middle Ring — The Hot Path)
- A proper programming language, NOT natural language
- Sits between natural and machine
- Transforms into both
- Lives in the **transformation graph**
- Adaptive, context-sensitive, compiled-but-parameterized
- Boundary functor (up): **Semantic Extraction** (Fluid → Natural)
- Boundary functor (down): **Expression Compilation** (Fluid → Machine)

### MACHINE (Innermost Ring — The Cold Path / Fixed Point)
- Compiled binary. SIMD kernels. PTX. AVX-512.
- Stable, bit-identical, slow-to-change
- The fixed point that the fluid code targets
- Boundary functor (up): **Result Extraction** (Machine → Fluid)

## Key Difference from Previous Draft

The shell is NOT the fallback. The shell is the **natural layer interface** — the outermost ring.

Fallback doesn't mean "shell takes over when machine fails."
It means: the system can always express itself in a language the next ring out understands.

- Machine can't compute? → Fluid re-parameterizes
- Fluid can't decide? → Natural (shell) provides intent
- Natural can't interpret? → This is the human's problem, not the system's

## Every Boundary is a Dual Aspect Functor

Each boundary runs in BOTH directions:
- Natural → Fluid: intent compilation
- Fluid → Machine: expression compilation  
- Machine → Fluid: result extraction
- Fluid → Natural: explanation extraction

The fluid layer is the transformation graph. It translates up to natural (explanation) and down to machine (computation). Neither direction is primary.

## Fluidity

The quality of fluid code is measured by:
1. **Compilability**: can it become machine code?
2. **Expressibility**: can it render to natural language?
3. **Transformability**: can it morph between representations without losing semantics?
