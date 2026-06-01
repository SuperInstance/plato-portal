"""
Protocol message types and handlers for the A2A Conservation Protocol.
"""

import time
import uuid
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

from conservation_agent import ConservationAgent
from agent_directory import AgentDirectory


class MessageType(Enum):
    IDENTITY_BROADCAST = "IDENTITY_BROADCAST"
    IDENTITY_ACK = "IDENTITY_ACK"
    ALIGNMENT_QUERY = "ALIGNMENT_QUERY"
    ALIGNMENT_RESPONSE = "ALIGNMENT_RESPONSE"
    COLLABORATION_PROPOSE = "COLLABORATION_PROPOSE"
    COLLABORATION_ACCEPT = "COLLABORATION_ACCEPT"
    COLLABORATION_REJECT = "COLLABORATION_REJECT"
    TASK_ROUTE = "TASK_ROUTE"
    TASK_ACK = "TASK_ACK"
    CONSERVATION_CHECK = "CONSERVATION_CHECK"
    CONSERVATION_REPORT = "CONSERVATION_REPORT"


@dataclass
class ProtocolMessage:
    """A protocol message with type, sender, receiver, and payload."""
    msg_type: MessageType
    sender: str
    receiver: str
    payload: Dict[str, Any]
    message_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            'msg_type': self.msg_type.value,
            'sender': self.sender,
            'receiver': self.receiver,
            'payload': self.payload,
            'message_id': self.message_id,
            'timestamp': self.timestamp,
        }


@dataclass
class CollaborationResult:
    """Result of a collaboration proposal and routing."""
    agent_a: str
    agent_b: str
    alignment: float
    conservation_ratio: float
    predicted_success: float
    routing: Dict[str, List[int]]
    fiedler_vector: List[float]
    composed_eigenvalues: List[float]
    messages: List[ProtocolMessage] = field(default_factory=list)


class ConservationProtocol:
    """
    The A2A Conservation Protocol handler.
    
    Manages the spectral handshake, collaboration proposals,
    Fiedler routing, and conservation monitoring.
    """

    def __init__(self, directory: AgentDirectory):
        self.directory = directory
        self._message_log: List[ProtocolMessage] = []
        self._active_collaborations: Dict[str, CollaborationResult] = {}

    def broadcast_identity(self, agent: ConservationAgent) -> ProtocolMessage:
        """Agent broadcasts its spectral fingerprint to the directory."""
        msg = ProtocolMessage(
            msg_type=MessageType.IDENTITY_BROADCAST,
            sender=agent.name,
            receiver="directory",
            payload={'fingerprint': agent.spectral_fingerprint.to_dict()},
        )
        self.directory.register(agent)
        self._message_log.append(msg)

        ack = ProtocolMessage(
            msg_type=MessageType.IDENTITY_ACK,
            sender="directory",
            receiver=agent.name,
            payload={'registered': True},
        )
        self._message_log.append(ack)
        return ack

    def query_collaborators(self, agent: ConservationAgent,
                            min_alignment: float = 0.15) -> ProtocolMessage:
        """Query the directory for potential collaborators."""
        candidates = self.directory.find_collaborators(agent, min_alignment)

        msg = ProtocolMessage(
            msg_type=MessageType.ALIGNMENT_QUERY,
            sender=agent.name,
            receiver="directory",
            payload={'min_alignment': min_alignment},
        )
        self._message_log.append(msg)

        response = ProtocolMessage(
            msg_type=MessageType.ALIGNMENT_RESPONSE,
            sender="directory",
            receiver=agent.name,
            payload={
                'candidates': [
                    {
                        'agent_id': cid,
                        'alignment': alpha,
                    }
                    for cid, alpha in candidates
                ],
            },
        )
        self._message_log.append(response)
        return response

    def propose_collaboration(self, agent_a: ConservationAgent,
                              agent_b: ConservationAgent,
                              task_description: str = "general",
                              cross_weight: float = 0.3) -> CollaborationResult:
        """
        Full spectral handshake: compute alignment, predict conservation,
        route via Fiedler partitioning.
        """
        # Compute alignment
        alignment = agent_a.can_collaborate_with(agent_b)

        # Compose graphs
        composition = agent_a.compose_with(agent_b, cross_weight)

        # Predict success
        predicted_success = 1.0 - np.exp(-3.0 * max(alignment, 0))

        # Routing via Fiedler partition
        fiedler = np.array(composition['fiedler_vector'])
        n_a = agent_a.tension_graph['n']
        n_b = agent_b.tension_graph['n']
        n_total = n_a + n_b

        # Partition based on Fiedler vector sign
        routing_a = [i for i in range(n_total) if fiedler[i] >= 0 and i < n_a]
        routing_b = [i for i in range(n_total) if fiedler[i] < 0 and i >= n_a]

        # If Fiedler doesn't split well, use natural partition
        if not routing_a:
            routing_a = list(range(n_a))
        if not routing_b:
            routing_b = list(range(n_a, n_total))

        # Protocol messages
        propose_msg = ProtocolMessage(
            msg_type=MessageType.COLLABORATION_PROPOSE,
            sender=agent_a.name,
            receiver=agent_b.name,
            payload={
                'task': task_description,
                'alignment': alignment,
                'predicted_conservation': composition['conservation_ratio'],
                'predicted_success': predicted_success,
            },
        )
        self._message_log.append(propose_msg)

        # Accept or reject based on alignment
        if alignment >= agent_a.spectral_fingerprint.alignment_threshold:
            response_type = MessageType.COLLABORATION_ACCEPT
            response_payload = {
                'accepted': True,
                'routing': {
                    agent_a.name: routing_a,
                    agent_b.name: routing_b,
                },
            }
        else:
            response_type = MessageType.COLLABORATION_REJECT
            response_payload = {
                'accepted': False,
                'reason': f'alignment {alignment:.3f} below threshold {agent_a.spectral_fingerprint.alignment_threshold}',
            }

        response_msg = ProtocolMessage(
            msg_type=response_type,
            sender=agent_b.name,
            receiver=agent_a.name,
            payload=response_payload,
        )
        self._message_log.append(response_msg)

        result = CollaborationResult(
            agent_a=agent_a.name,
            agent_b=agent_b.name,
            alignment=alignment,
            conservation_ratio=composition['conservation_ratio'],
            predicted_success=predicted_success,
            routing={
                agent_a.name: routing_a,
                agent_b.name: routing_b,
            },
            fiedler_vector=composition['fiedler_vector'],
            composed_eigenvalues=composition['eigenvalues'],
            messages=[propose_msg, response_msg],
        )

        collab_id = f"{agent_a.name}+{agent_b.name}"
        self._active_collaborations[collab_id] = result
        return result

    def find_collaborators(self, agent: ConservationAgent,
                           min_alignment: float = 0.15):
        """Convenience: find collaborators from directory."""
        return self.directory.find_collaborators(agent, min_alignment)

    def compose_and_route(self, agent_a: ConservationAgent,
                          agent_b: ConservationAgent,
                          task: str = "general",
                          cross_weight: float = 0.3) -> CollaborationResult:
        """Alias for propose_collaboration."""
        return self.propose_collaboration(agent_a, agent_b, task, cross_weight)

    def conservation_check(self, result: CollaborationResult) -> Dict:
        """
        Mid-collaboration health check.
        In a real system, this would re-compute alignment from live data.
        Here we simulate by checking the stored metrics.
        """
        healthy = result.alignment > 0.15 and result.predicted_success > 0.3
        return {
            'collaboration': f"{result.agent_a}+{result.agent_b}",
            'alignment': result.alignment,
            'conservation_ratio': result.conservation_ratio,
            'predicted_success': result.predicted_success,
            'healthy': healthy,
        }

    def message_summary(self) -> str:
        """Summary of all protocol messages exchanged."""
        lines = ["Protocol Messages", "=" * 50]
        for msg in self._message_log:
            lines.append(
                f"  [{msg.msg_type.value}] {msg.sender} → {msg.receiver}"
            )
        return "\n".join(lines)
