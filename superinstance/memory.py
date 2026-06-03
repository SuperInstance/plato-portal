"""Filesystem-based persistent memory for agents."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any


class AgentMemory:
    """Persistent memory stored as markdown files.
    
    Directory structure:
        {base_dir}/{agent_name}/
            SOUL.md      - identity
            USER.md      - user context
            MEMORY.md    - long-term facts
            diary/       - session logs
    """

    def __init__(self, agent_name: str, base_dir: str | Path | None = None):
        self.agent_name = agent_name
        self.base_dir = Path(base_dir) if base_dir else Path.home() / ".superinstance" / "agents"
        self.agent_dir = self.base_dir / agent_name
        self.agent_dir.mkdir(parents=True, exist_ok=True)

        self._files = {
            "SOUL.md": self.agent_dir / "SOUL.md",
            "USER.md": self.agent_dir / "USER.md",
            "MEMORY.md": self.agent_dir / "MEMORY.md",
        }
        self.diary_dir = self.agent_dir / "diary"
        self.diary_dir.mkdir(exist_ok=True)
        self._ensure_files()

    def _ensure_files(self) -> None:
        """Create default files if missing."""
        now = datetime.now().isoformat()
        defaults = {
            "SOUL.md": f"# {self.agent_name}\n\nCreated: {now}\n",
            "USER.md": "# User Profile\n\n",
            "MEMORY.md": "# Long-Term Memory\n\n",
        }
        for key, path in self._files.items():
            if not path.exists():
                path.write_text(defaults[key])

    def remember(self, fact: str, category: str = "general") -> None:
        """Store a fact."""
        timestamp = datetime.now().isoformat()
        entry = f"- [{timestamp}] [{category}] {fact}\n"
        
        with open(self._files["MEMORY.md"], "a") as f:
            f.write(entry)
        
        today = datetime.now().strftime("%Y-%m-%d")
        with open(self.diary_dir / f"{today}.md", "a") as f:
            f.write(f"- [{timestamp}] {fact}\n")

    def recall(self, query: str | None = None) -> str:
        """Retrieve memories."""
        text = self._files["MEMORY.md"].read_text()
        lines = [l for l in text.split("\n") if l.strip().startswith("- [")]
        
        if not query:
            return "\n".join(lines) if lines else "No memories yet."
        
        matching = [l for l in lines if query.lower() in l.lower()]
        return "\n".join(matching) if matching else "No memories match."

    def read_soul(self) -> str:
        return self._files["SOUL.md"].read_text()

    def read_user(self) -> str:
        return self._files["USER.md"].read_text()

    def stats(self) -> dict[str, Any]:
        text = self._files["MEMORY.md"].read_text()
        entries = len([l for l in text.split("\n") if l.strip().startswith("- [")])
        return {
            "entries": entries,
            "diary_days": len(list(self.diary_dir.iterdir())),
            "agent_dir": str(self.agent_dir),
            "files": {k: str(v) for k, v in self._files.items()},
        }

    def store(self, key: str, value: str) -> None:
        """Store a key-value pair."""
        self.remember(f"key:{key} → {value}", "kvstore")

    def retrieve(self, key: str) -> str | None:
        """Retrieve a stored value by key."""
        text = self._files["MEMORY.md"].read_text()
        prefix = f"key:{key} → "
        for line in text.split("\n"):
            if prefix in line:
                return line.split(prefix, 1)[1].strip()
        return None

    def search(self, query: str) -> list[str]:
        """Semantic-style search over memories.
        
        Currently uses substring matching. In production this
        would use embedding-based semantic search.
        """
        text = self._files["MEMORY.md"].read_text()
        return [l.strip() for l in text.split("\n") 
                if l.strip().startswith("- [") and query.lower() in l.lower()]

    def clear(self) -> None:
        """Clear all memories."""
        self._files["MEMORY.md"].write_text("# Long-Term Memory\n\n")
        for f in self.diary_dir.iterdir():
            f.unlink()

    def __repr__(self) -> str:
        return f"AgentMemory({self.agent_name!r}, entries={self.stats()['entries']})"
