"""Agent with persistent memory and fleet capabilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .memory import AgentMemory
from .exceptions import AgentNotFoundError


@dataclass
class AgentConfig:
    """Configuration for an agent."""
    name: str
    model: str = "default"
    temperature: float = 0.7
    max_tokens: int = 4096
    tools: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)


class Agent:
    """An agent with persistent memory.
    
    Memory is stored as markdown files in ~/.superinstance/agents/{name}/
    
    Example:
        >>> agent = Agent("researcher")
        >>> agent.remember("User prefers Python examples")
        >>> agent.recall("Python")
        'User prefers Python examples'
    """

    def __init__(
        self,
        name: str,
        memory_dir: str | Path | None = None,
        config: AgentConfig | None = None,
    ):
        self.config = config or AgentConfig(name=name)
        self.name = name
        self.memory = AgentMemory(name, base_dir=memory_dir)
        self._spawned: list[Agent] = []
        self._created_at = datetime.now().isoformat()

    def remember(self, fact: str, category: str = "general") -> None:
        """Store a fact in long-term memory."""
        self.memory.remember(fact, category)

    def recall(self, query: str | None = None) -> str:
        """Retrieve memories matching a query."""
        return self.memory.recall(query)

    def ask(self, question: str) -> str:
        """Answer based on memory (keyword search).
        
        In production, this calls an LLM API with memory context.
        """
        stop_words = {"what", "does", "the", "user", "is", "are", "how", 
                      "why", "when", "where", "who", "a", "an", "do", 
                      "you", "have", "about", "that", "yet"}
        words = [w.lower() for w in question.replace("?", "").replace(".", "").split() 
                 if w.lower() not in stop_words and len(w) > 2]
        
        for word in words:
            memory = self.memory.recall(word)
            if memory and memory != "No memories match.":
                return f"Based on my memory: {memory.strip()}"
        return "I don't have any memories about that yet."

    def spawn(self, task: str, name: str | None = None) -> Agent:
        """Spawn a subagent for a specific task."""
        sub_name = name or f"{self.name}_sub_{len(self._spawned)}"
        subagent = Agent(sub_name, memory_dir=self.memory.base_dir)
        subagent.memory._files["SOUL.md"] = self.memory._files["SOUL.md"]
        subagent.remember(f"Spawned from {self.name} for task: {task}", "system")
        self._spawned.append(subagent)
        return subagent

    def status(self) -> dict[str, Any]:
        """Return agent status."""
        return {
            "name": self.name,
            "created_at": self._created_at,
            "memory": self.memory.stats(),
            "spawned_count": len(self._spawned),
            "spawned": [s.name for s in self._spawned],
            "config": {
                "model": self.config.model,
                "temperature": self.config.temperature,
                "tools": self.config.tools,
                "tags": self.config.tags,
            },
        }

    def __repr__(self) -> str:
        return f"Agent(name={self.name!r}, memories={self.memory.stats()['entries']})"
