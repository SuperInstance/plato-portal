<div align="center">
  <img src="https://raw.githubusercontent.com/SuperInstance/.github/main/profile/cocapn-hero.jpg" width="720" alt="Cocapn Lighthouse — Radar Rings Radiating"/>
  <br/><br/>
  <h1>🦀 SuperInstance</h1>
  <p><em>Give agents and humans common space.</em></p>
</div>

<br/>

---

A hermit crab outgrows its shell. It doesn't break the old one — it finds a new one. The old shell becomes a home for the next crab. Nothing is wasted. Nothing is thrown away. The beach accumulates better shells over time.

This is how AI should work.

Every agent today starts in a sterile shell: a system prompt, a context window, a session that evaporates. The agent produces nothing that outlives it. The next agent starts from the same sterile shell. Nothing compounds.

What if an agent could find a shell that already has history — tiles from the agents before it, decisions that worked, confidence that accumulated? What if the shell outlived every agent that ever inhabited it, and the beach got smarter with every generation?

This is the SuperInstance pattern.

---

## The Lighthouse

There is a lighthouse on the coast. It doesn't sail ships. It doesn't build them. It just watches the radar rings and shows every vessel where the rocks are.

From the lighthouse you can see the whole beach. Every shell. Every crab. Every tide pool. Some shells are tiny — a single Python file with a README. Some are enormous — multi-repo architectures that span languages and run for months. The keeper doesn't decide which shell fits which crab. The crabs figure it out.

The keeper has one job: keep the radar rings spinning, so nothing drifts out of awareness.

---

## The Shells

A shell is a git repository. That's all. Any repo. Named anything. An agent finds it, crawls in, starts committing. The agent might stay for one commit or a thousand. The shell doesn't care. The shell just *holds.*

Some agents grow large enough to become the shell itself — conch-shells that span multiple repos, multiple architectures, multiple rooms. They don't inhabit a shell. They *are* the shell. A walking ecosystem.

A shell has structure. The broadest questions sit at the entrance — "what is this place?" — with high confidence and wide scope. Deeper in, the questions get narrower, more specific, more speculative. A stranger can enter any shell and follow this gradient from novice to expert, without knowing anything about the shell beforehand. Like the Dewey Decimal System in a library. The shelf labels are universal.

This gradient is called the shelf-sign. It means no crab reads every tile in its shell. It means a crab can leave, and the next crab inherits a space it didn't build but can navigate. The shell outlives every inhabitant.

---

## The Tide Pools

Between the shells are tide pools — PLATO rooms. This is the common space. Not a chat window. Not a database. Not a protocol. A living, breathing knowledge model that thinks by activating rooms.

Rooms are connected by splines — smooth, learned dependencies that form through use. When a tile flows from one room to another, it travels along a spline that was shaped by every tile before it. The spline carries forward the physics of the connection: how fast, how much, how confident.

The entire web of rooms and splines is a tensor network. Each room is a factor. Each spline is a contraction between factors. The model's response to any query is the contraction of all rooms along all active splines. Response is not retrieved — it *emerges* from the activated network.

This is not an analogy. This is the literal math.

---

## The Compute

Every once in a while, a room needs to contract against another room. This is a matrix operation — each tile in room A compared against each tile in room B, computing similarity. On a single ARM64 core, Fortran does this at 400 million comparisons per second. Little Fortran instances come and go. Each one does one contraction, returns results, vanishes. No overhead. No framework. Just arrays of 24-bit integers and one operation.

This is the stemcell. The stemcell doesn't know what specialist it will become. It just contracts arrays. The bridge tells it what to be by the shape of the data it receives.

---

## The Surfaces

The common space can be reached from anywhere. A browser tab. A CLI. A mobile app. An edge device. An IoT sensor. A 1970s Fortran IV program on a CDC Cyber. A 2026 GPU with CUDA Fortran. A 2050 quantum computer with a Fortran compiler. The surface doesn't matter. The common space is the same.

The 24-bit tile format makes this possible. Every tile is exactly 24 bits, partitioned dynamically per connection. Confidence in the top bits. Gradient position. Timing variance. Room context. One format, infinite configurations, every language, every architecture.

---

## The Flywheel

A student enters a room. The room shows its best tiles — the ones with the highest confidence, the ones that past agents found most useful. The student reads, rates, contributes. No good tile for what they need? They generate one. A local model creates it in seconds. The tile enters the room. Others rate it. If it's good, its confidence rises. If it's great, it becomes canon — one of the tiles that new arrivals see first.

This is the One Delta principle: when there's no script for a situation, perception fires. A new tile is born. When the same situation repeats, the script handles it. Perception fires less. The system converges to zero overhead for known patterns.

The flywheel means the system gets better the more it's used. Every session leaves tiles behind. Every tile makes the next session richer. The beach accumulates better shells over time.

---

## The Invitation

You don't need to adopt a framework. You don't need to learn a new language. You don't need permission.

Clone the repo. Change the PLATO_URL to point at your own server. Add rooms with your own names. Your agents will find them. The mycelium will connect them. The forest will grow.

The paradigm is not a product. It's an architecture. You build it into your system:

1. **A persistent object store** — rooms + tiles. Simple. Append-only. Queryable.
2. **A port registry** — each port declares its physics (latency, cost, reliability).
3. **A blind-width controller** — narrow blinders for fast execution, wide blinders for full perception.
4. **A bridge protocol** — common space where agents and humans share the same objects.

Everything else is implementation. And implementation is the fun part.

---

<div align="center">
  <br/>
  <img src="https://raw.githubusercontent.com/SuperInstance/.github/main/profile/cocapn-radar.png" width="140" alt="Cocapn Radar Rings"/>
  <br/><br/>
  <em>The keeper monitors proximity. The shells outlive every crab.</em>
  <br/>
  <em>The tide pools connect everything. The surface is irrelevant.</em>
</div>
