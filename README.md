# SuperInstance SDK

> Persistent multi-agent AI with filesystem-backed memory and fleet orchestration.

**Version:** 0.1.0 (alpha) — working core, aspirational docs now aligned.

## Install

```bash
pip install superinstance
```

## Quick Start

```python
from superinstance.agent import Agent, AgentConfig
from superinstance.fleet import Fleet

# Create an agent (two styles both work)
agent = Agent("researcher")

# Or with a config object (the README-friendly style)
config = AgentConfig(name="researcher", model="gpt-4")
agent = Agent(config)

# The agent remembers across sessions (stored at ~/.superinstance/agents/researcher/)
agent.remember("User prefers concise summaries")

# Create a fleet
fleet = Fleet(name="analysis-team")
scout = fleet.create_agent("scout", tags=["research"])
writer = fleet.create_agent("writer", tags=["content"])

# Broadcast a message
fleet.broadcast("New project started")

# Check fleet status
status = fleet.status()
print(f"{status.total_agents} agents, {status.total_memories} memories")
```

## API Reference

### `Agent`

| Method | Signature | Description |
|--------|-----------|-------------|
| `Agent(name, ..., config)` | `Agent("name")` or `Agent(config)` | Create agent. Memory auto-loads from disk. |
| `send(message)` | `agent.send("hello")` | Process a message, stored in memory. |
| `remember(fact, category)` | `agent.remember("fact", "notes")` | Store a fact in long-term memory. |
| `recall(query)` | `agent.recall("summary")` | Retrieve matching memories. |
| `ask(question)` | `agent.ask("What do you know?")` | Answer based on memory context. |
| `spawn(task, name)` | `agent.spawn("analyze", "sub1")` | Create a child agent. |
| `status()` | `agent.status()` | Return agent status dict. |

### `Fleet`

| Method | Signature | Description |
|--------|-----------|-------------|
| `Fleet(name)` | `Fleet("team")` | Create a named fleet. |
| `create_agent(name, ...)` | `fleet.create_agent("scout")` | Create and register an agent. |
| `add_agent(agent)` | `fleet.add_agent(agent)` | Add an existing agent. |
| `get_agent(name)` | `fleet.get_agent("scout")` | Retrieve an agent by name. |
| `list_agents(tag)` | `fleet.list_agents("research")` | List agents, optionally filtered. |
| `broadcast(message, tag)` | `fleet.broadcast("hi")` | Send a message to all/tagged agents. |
| `dispatch(task)` | `fleet.dispatch("analyze data")` | Route a task to the best-suited agent. |
| `spectral_balance()` | `fleet.spectral_balance()` | Compute fleet resource balance. |
| `status()` | `fleet.status()` | Get fleet status summary. |
| `remove_agent(name)` | `fleet.remove_agent("scout")` | Remove an agent from the fleet. |

### `AgentMemory`

| Method | Signature | Description |
|--------|-----------|-------------|
| `AgentMemory(name)` | `AgentMemory("alice")` | Persistent memory manager. |
| `remember(fact, category)` | `mem.remember("key detail")` | Store a fact. |
| `recall(query)` | `mem.recall("detail")` | Retrieve matching memories. |
| `store(key, value)` | `mem.store("theme", "minimal")` | Store a key-value pair. |
| `retrieve(key)` | `mem.retrieve("theme")` | Get a stored value by key. |
| `search(query)` | `mem.search("detail")` | Search all memories. |
| `clear()` | `mem.clear()` | Clear all memories. |
| `stats()` | `mem.stats()` | Return memory statistics. |
| `path` | — | File path: `~/.superinstance/agents/{name}/`. |

### `Exceptions`

| Exception | When |
|-----------|------|
| `SuperInstanceError` | Base error. |
| `AgentNotFoundError` | Referenced agent doesn't exist. |
| `FleetConnectionError` | Can't reach an agent in the fleet. |
| `MemoryError` | Memory operation failed. |

## How It Works

1. **Agent Creation**: Each agent gets a directory at `~/.superinstance/agents/{name}/` with SOUL.md, USER.md, MEMORY.md, and a diary.
2. **Memory**: Facts append to MEMORY.md as timestamped entries. On start, memory auto-loads from disk. `remember()` and `recall()` use text matching.
3. **Fleet Coordination**: `Fleet` manages agent registry with tag-based filtering. `broadcast()` sends messages to all or filtered agents. `dispatch()` routes tasks to available agents.
4. **Spectral Balance*: `spectral_balance()` computes a placeholder eigenvalue model of fleet resource distribution — ready for production implementation.

## Testing

```bash
pytest tests/ -v
```

All tests pass (26/26).

## License

MIT
