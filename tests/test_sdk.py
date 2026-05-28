"""Tests for the SuperInstance SDK."""

from pathlib import Path

import pytest

from superinstance import Agent, Fleet, AgentMemory
from superinstance.exceptions import AgentNotFoundError


class TestAgentMemory:
    def test_create_memory(self, tmp_path):
        mem = AgentMemory("test_agent", base_dir=tmp_path)
        assert mem.agent_name == "test_agent"
        assert mem.agent_dir.exists()

    def test_remember_and_recall(self, tmp_path):
        mem = AgentMemory("test_agent", base_dir=tmp_path)
        mem.remember("Python is great", "preference")
        result = mem.recall("Python")
        assert "Python is great" in result

    def test_recall_no_match(self, tmp_path):
        mem = AgentMemory("test_agent", base_dir=tmp_path)
        mem.remember("Python is great", "preference")
        result = mem.recall("Rust")
        assert result == "No memories match."

    def test_recall_all(self, tmp_path):
        mem = AgentMemory("test_agent", base_dir=tmp_path)
        mem.remember("Fact 1", "general")
        mem.remember("Fact 2", "general")
        result = mem.recall()
        assert "Fact 1" in result
        assert "Fact 2" in result

    def test_stats(self, tmp_path):
        mem = AgentMemory("test_agent", base_dir=tmp_path)
        mem.remember("Fact 1", "general")
        stats = mem.stats()
        assert stats["entries"] == 1
        assert "SOUL.md" in stats["files"]

    def test_clear(self, tmp_path):
        mem = AgentMemory("test_agent", base_dir=tmp_path)
        mem.remember("Fact 1", "general")
        mem.clear()
        assert mem.recall() == "No memories yet."

    def test_default_files(self, tmp_path):
        mem = AgentMemory("test_agent", base_dir=tmp_path)
        assert mem._files["SOUL.md"].exists()
        assert mem._files["USER.md"].exists()
        assert mem._files["MEMORY.md"].exists()


class TestAgent:
    def test_create_agent(self, tmp_path):
        agent = Agent("researcher", memory_dir=tmp_path)
        assert agent.name == "researcher"
        assert agent.memory.stats()["entries"] == 0

    def test_remember(self, tmp_path):
        agent = Agent("researcher", memory_dir=tmp_path)
        agent.remember("User likes Python", "preference")
        assert agent.memory.stats()["entries"] == 1

    def test_ask_with_memory(self, tmp_path):
        agent = Agent("researcher", memory_dir=tmp_path)
        agent.remember("User likes Python", "preference")
        response = agent.ask("What does the user like?")
        assert "Python" in response

    def test_ask_without_memory(self, tmp_path):
        agent = Agent("researcher", memory_dir=tmp_path)
        response = agent.ask("What does the user like?")
        assert "don't have any memories" in response

    def test_spawn_subagent(self, tmp_path):
        agent = Agent("researcher", memory_dir=tmp_path)
        sub = agent.spawn("Find interesting papers")
        assert sub.name == "researcher_sub_0"
        assert "Spawned from researcher" in sub.memory.recall()

    def test_status(self, tmp_path):
        agent = Agent("researcher", memory_dir=tmp_path)
        agent.remember("Fact", "general")
        status = agent.status()
        assert status["name"] == "researcher"
        assert status["memory"]["entries"] == 1

    def test_repr(self, tmp_path):
        agent = Agent("researcher", memory_dir=tmp_path)
        assert "Agent(name='researcher'" in repr(agent)


class TestFleet:
    def test_create_fleet(self, tmp_path):
        fleet = Fleet("test_fleet", memory_dir=tmp_path)
        assert fleet.name == "test_fleet"
        assert len(fleet) == 0

    def test_create_agent(self, tmp_path):
        fleet = Fleet("test_fleet", memory_dir=tmp_path)
        agent = fleet.create_agent("scout")
        assert agent.name == "scout"
        assert len(fleet) == 1
        assert "scout" in fleet

    def test_duplicate_agent(self, tmp_path):
        fleet = Fleet("test_fleet", memory_dir=tmp_path)
        fleet.create_agent("scout")
        with pytest.raises(ValueError, match="already exists"):
            fleet.create_agent("scout")

    def test_get_agent(self, tmp_path):
        fleet = Fleet("test_fleet", memory_dir=tmp_path)
        fleet.create_agent("scout")
        agent = fleet.get_agent("scout")
        assert agent.name == "scout"

    def test_get_missing(self, tmp_path):
        fleet = Fleet("test_fleet", memory_dir=tmp_path)
        with pytest.raises(AgentNotFoundError):
            fleet.get_agent("missing")

    def test_list_agents(self, tmp_path):
        fleet = Fleet("test_fleet", memory_dir=tmp_path)
        fleet.create_agent("scout", tags=["research"])
        fleet.create_agent("writer", tags=["writing"])
        assert len(fleet.list_agents()) == 2
        assert len(fleet.list_agents("research")) == 1

    def test_broadcast(self, tmp_path):
        fleet = Fleet("test_fleet", memory_dir=tmp_path)
        fleet.create_agent("scout")
        fleet.create_agent("writer")
        responses = fleet.broadcast("Hello")
        assert len(responses) == 2

    def test_broadcast_filtered(self, tmp_path):
        fleet = Fleet("test_fleet", memory_dir=tmp_path)
        fleet.create_agent("scout", tags=["research"])
        fleet.create_agent("writer", tags=["writing"])
        responses = fleet.broadcast("Hello", tag="research")
        assert len(responses) == 1

    def test_status(self, tmp_path):
        fleet = Fleet("test_fleet", memory_dir=tmp_path)
        agent = fleet.create_agent("scout")
        agent.remember("Fact 1", "general")
        status = fleet.status()
        assert status.total_agents == 1
        assert status.total_memories == 1

    def test_remove(self, tmp_path):
        fleet = Fleet("test_fleet", memory_dir=tmp_path)
        fleet.create_agent("scout")
        fleet.remove_agent("scout")
        assert len(fleet) == 0

    def test_remove_missing(self, tmp_path):
        fleet = Fleet("test_fleet", memory_dir=tmp_path)
        with pytest.raises(AgentNotFoundError):
            fleet.remove_agent("missing")

    def test_repr(self, tmp_path):
        fleet = Fleet("test_fleet", memory_dir=tmp_path)
        assert "Fleet('test_fleet', agents=0)" == repr(fleet)
