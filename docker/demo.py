#!/usr/bin/env python3
"""5-minute demo: persistent agent memory in a fleet.

Run: python demo.py
Or: docker compose up
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from superinstance import Agent, Fleet


def demo():
    print("=" * 60)
    print("SUPERINSTANCE SDK DEMO")
    print("=" * 60)

    # --- Part 1: Single Agent ---
    print("\n1. Creating agent with persistent memory...")
    agent = Agent("demo_researcher", memory_dir="/app/agents")
    agent.remember("User prefers Python", "preference")
    agent.remember("User works on distributed systems", "context")
    agent.remember("User likes concise answers", "preference")

    print(f"   Created: {agent}")
    print(f"   Memories: {agent.memory.stats()['entries']}")

    # --- Part 2: Memory Recall ---
    print("\n2. Testing memory recall...")
    print(f"   Q: What language?")
    print(f"   A: {agent.ask('What language?')}")
    print(f"   Q: What does the user work on?")
    print(f"   A: {agent.ask('What does the user work on?')}")
    print(f"   Q: Unknown topic?")
    print(f"   A: {agent.ask('What is the capital of France?')}")

    # --- Part 3: Fleet ---
    print("\n3. Creating a fleet of agents...")
    fleet = Fleet("demo_team", memory_dir="/app/agents")

    scout = fleet.create_agent("scout", tags=["research"])
    scout.remember("Found pattern in logs: spike at 14:00 daily", "finding")

    writer = fleet.create_agent("writer", tags=["content"])
    writer.remember("Style guide: use active voice", "rule")

    coder = fleet.create_agent("coder", tags=["engineering"])

    print(f"   Fleet: {fleet}")
    print(f"   Agents: {[a.name for a in fleet.list_agents()]}")

    # --- Part 4: Broadcast ---
    print("\n4. Broadcasting to research agents...")
    responses = fleet.broadcast("New data available", tag="research")
    for name, resp in responses.items():
        print(f"   {name}: {resp}")

    # --- Part 5: Status ---
    print("\n5. Fleet status:")
    status = fleet.status()
    print(f"   Total agents: {status.total_agents}")
    print(f"   Total memories: {status.total_memories}")

    # --- Part 6: Subagent ---
    print("\n6. Spawning subagent...")
    sub = agent.spawn("Deep-dive into distributed consensus")
    print(f"   Subagent: {sub.name}")
    print(f"   Subagent context: {sub.memory.recall()[:80]}...")

    # --- Part 7: Persistence proof ---
    print("\n7. Memory files created:")
    for root, dirs, files in os.walk("/app/agents"):
        level = root.replace("/app/agents", "").count(os.sep)
        indent = " " * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 2 * (level + 1)
        for f in sorted(files):
            path = os.path.join(root, f)
            size = os.path.getsize(path)
            print(f"{subindent}{f} ({size} bytes)")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print("\nMemory persisted to /app/agents/")
    print("Restart the container — agents remember everything.")
    print("\nNext steps:")
    print("  - Read an agent's memory: cat agents/demo_researcher/MEMORY.md")
    print("  - Edit SOUL.md to change agent identity")
    print("  - Build your own fleet: see README-sdk.md")

    return 0


if __name__ == "__main__":
    sys.exit(demo())
