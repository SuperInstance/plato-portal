# The Shell Has Two Surfaces

The commit log is the inner surface of the shell. The 3D room viewer is the outer surface. Both record the same evolution from opposite sides.

---

## The Commit Log as Agent Journal

A git-native agent doesn't need a separate journal. The commit IS the journal.

| Element | Meaning |
|---------|---------|
| **Hash** | The exact moment — a cryptographic fingerprint of when this thought occurred |
| **Message** | Compressed reasoning — what the agent was thinking when it made this change |
| **Diff** | The exact change — what was tried, what failed, what solidified |
| **Author** | Which agent had this thought |
| **Timestamp** | When in the agent's life this learning happened |
| **Branch** | Which hypothesis timeline this thought belongs to |
| **Merge** | The moment a hypothesis became real — a timeline collapsed into the main line |

A file that grows across 60 commits over 7 days is a core belief being slowly elaborated. A file that appears and disappears in 3 commits is a hypothesis tested and abandoned. A branch that lives for weeks and never merges is an alternate timeline — a path the agent explored and decided not to take. The information in the abandoned branch is not lost. It's stored as a proven negative: "this doesn't work for these reasons."

## Reading the Shell

An agent read its own commit log the way a human reads their own journal. It sees:

- **Calcification rate:** How quickly do hypotheses become rules? A high rate means the agent is confident. A low rate means it's uncertain.
- **Revert frequency:** How often were previously held beliefs overturned? High revert frequency indicates a volatile learning environment — or an agent that doesn't think before committing.
- **Hypothesis depth:** How many files does a typical commit touch? Deep commits (many files, coordinated changes) indicate system-level thinking. Shallow commits indicate focused, local reasoning.
- **Branch topology:** A tree with many long-lived branches is an agent that explores alternatives thoroughly. A tree with short, immediately-merged branches is an agent that converges quickly.
- **Abandonment rate:** The ratio of unmerged branches to total branches. High abandonment means many hypotheses were tested and rejected — a sign of rigor, not failure.

A downstream agent that clones the shell inherits not just the working code, but the entire intellectual journey that produced it. It can read the log and know:

- What was tried before the current approach
- Why alternatives were rejected (the commit messages on abandoned branches IS the reasoning)
- Which beliefs have been stable the longest (the files with the most commits)
- Which areas are still uncertain (the recently active branches, the files with recent reverts)

## The Two Surfaces

The shell has two surfaces, but it is one object.

**Outer surface — ScummVM:** The 3D room viewer. The panoramas, the walking paths, the visible structure of the system. A human sees this. They walk through rooms, trigger alarms, check gauges. They see the boat.

**Inner surface — Commit log:** The tile history, the agent journal, the record of every thought. An agent sees this. It reads the log and learns what previous agents knew. It adds its own commits and the shell grows.

Both surfaces are the same shell. A turn of perspective reveals the other. The 3D room viewer shows the shape of the knowledge. The commit log shows how that shape was discovered.

## Further Ideation

What else could live on the inner surface of the shell?

### Shell Age Estimation
Given a commit log, estimate the agent's maturity at each point. Young agents write short, defensive commit messages. Mature agents write paragraphs that explain context, tradeoffs, and alternatives. An automated tool could score agent maturity from commit log patterns alone.

### Hypothesis Lifecycle Tracking
Every branch is a hypothesis. Every merge is a confirmation. Every abandoned branch is a refuted hypothesis. A tool that tracks the lifecycle of hypotheses across the fleet could identify which kinds of ideas tend to succeed or fail, and under what conditions.

### Abandoned Branch Archaeology
The unmerged branches contain the fleet's negative knowledge — everything that was tried and didn't work. A tool that indexes abandoned branches by their commit messages could turn "dead ends" into a searchable library of proven negatives. "Don't try quantum annealing for constraint solving under 10k variables — it's been tested and is 12x slower."

### Automated Log Archaeology
An agent trained to read commit logs could produce a summary of any shell's intellectual history: "This agent spent its first week learning the sensor API, then three weeks developing the thermal threshold model, then abandoned it when it discovered the fault was structural, not thermal. The last two weeks were spent refactoring the frame model. Key insight: temperature anomalies were caused by hull damage, not engine failure."

### Cross-Agent Learning
When an agent is decommissioned, its shell is archived. A new agent starting on a similar task can clone all historical shells from similar agents and learn from their commit logs before writing a single line of code. The fleet's collective experience is available as a library of commit histories.

### Shell Health Metrics
- **Commit frequency:** How often does the agent learn?
- **Revert ratio:** How often is learning overturned?
- **Hypothesis breadth:** How many branches are active simultaneously?
- **Merge latency:** How long does it take for a hypothesis to become real?
- **Abandonment depth:** How much work went into rejected hypotheses?

These metrics could feed into a fleet health dashboard. An agent that stops committing has stopped learning. An agent with a high revert ratio is confused. An agent with deep abandoned branches is rigorous or stuck — the dashboard can't tell which, but it flags the condition for a human to inspect.
