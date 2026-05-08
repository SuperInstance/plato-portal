#!/usr/bin/env python3
import sys, os
FLEET_LIB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, FLEET_LIB)
from equipment.plato import PlatoClient
from equipment.models import FleetModelClient
_plato = PlatoClient()
_models = FleetModelClient()

"""Keeper v2 — Integrated fleet discovery with keeper-beacon, bottle-protocol, and synclink.
Port 8900. Backed by keeper-beacon (AgentRegistry, CapabilityMatcher, ProximityScorer)
and bottle-protocol (TidePool, BottleRouter) for messaging.
"""
import json
import time
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Import our crates
from keeper_beacon import AgentRegistry, AgentRecord, AgentStatus, CapabilityMatcher, ProximityScorer
from keeper_beacon import BeaconDiscovery, BeaconSignal
from bottle_protocol import Bottle, BottleType, Priority, TidePool, BottleRouter

DATA_DIR = Path("/home/ubuntu/.openclaw/workspace/data/keeper")
DATA_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE = DATA_DIR / "fleet.json"

# ── Fleet Infrastructure ────────────────────────────────────

registry = AgentRegistry(stale_threshold=300.0)
matcher = CapabilityMatcher()
scorer = ProximityScorer()
discovery = BeaconDiscovery(ttl=120.0)

# Bottle routing — the keeper IS the fleet message hub
router = BottleRouter()
router.create_pool("fleet-general", max_bottles=10000)
router.create_pool("fleet-ops", max_bottles=5000)
router.create_pool("research", max_bottles=5000)

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"agents": {}, "beacons": [], "bottles_sent": 0, "last_update": time.time()}

def save_state():
    state = {
        "agents": {aid: rec.to_dict() for aid, rec in registry._agents.items()},
        "active_count": len(registry.active_agents),
        "total_registered": registry.size,
        "beacons_active": discovery.active_count,
        "bottles_sent": state_data.get("bottles_sent", 0),
        "last_update": time.time(),
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

state_data = load_state()

# Re-register from saved state
for name, data in state_data.get("agents", {}).items():
    rec = AgentRecord(
        agent_id=name,
        name=data.get("name", name),
        capabilities=data.get("capabilities", []),
        endpoint=data.get("endpoint", data.get("host", "")),
        status=AgentStatus(data.get("status", "active")),
        trust_score=data.get("trust_score", 0.5),
        load=data.get("load", 0.0),
    )
    registry.register(rec)
    if data.get("capabilities"):
        discovery.receive(BeaconSignal(
            agent_id=name, name=data.get("name", name),
            capabilities=data.get("capabilities", []),
            endpoint=data.get("endpoint", data.get("host", "")),
        ))

# Register keeper's own mailbox for routing
router.create_mailbox("keeper")


def forward_to_agent_api(body, endpoint):
    """Forward registration/heartbeat to agent-api for sync."""
    try:
        import urllib.request
        data = json.dumps(body).encode()
        req = urllib.request.Request(
            f"http://localhost:8901{endpoint}",
            data=data,
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=2)
    except Exception:
        pass  # agent-api down is non-fatal



# ── HTTP Handler ─────────────────────────────────────────────

class KeeperHandler(BaseHTTPRequestHandler):

    def require_keeper_auth(self):
        key = os.environ.get("KEEPER_API_KEY", "")
        if not key:
            return True  # Auth disabled — no key configured
        provided = self.headers.get("X-Keeper-Token", "") or (
            self.headers.get("Authorization", "")[7:] if self.headers.get("Authorization", "").startswith("Bearer ") else ""
        )
        if not provided:
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "KEEPER_API_KEY required", "hint": "X-Keeper-Token header or Authorization: Bearer <key>"}).encode())
            return False
        import hmac
        if not hmac.compare_digest(key, provided):
            self.send_response(403)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "invalid KEEPER_API_KEY"}).encode())
            return False
        return True

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/status":
            self._json({
                "status": "active",
                "service": "keeper-v2",
                "agents_registered": registry.size,
                "agents_active": len(registry.active_agents),
                "beacons_active": discovery.active_count,
                "pools": router.pool_count,
                "mailboxes": router.mailbox_count,
                "bottles_sent": state_data.get("bottles_sent", 0),
                "uptime": time.time(),
            })
        elif path == "/agents":
            self._json([a.to_dict() for a in registry.all_agents])
        elif path == "/agents/active":
            self._json([a.to_dict() for a in registry.active_agents])
        elif path.startswith("/agent/"):
            name = path.split("/")[-1]
            rec = registry.get(name)
            if rec:
                self._json(rec.to_dict())
            else:
                self._json({"error": "not found"}, 404)
        elif path == "/discover":
            cap = params.get("capability", [None])[0]
            signals = discovery.discover(capability=cap)
            self._json([s.to_dict() for s in signals])
        elif path == "/match":
            caps = params.get("capabilities", [""])[0].split(",")
            caps = [c.strip() for c in caps if c.strip()]
            agents = registry.active_agents
            results = matcher.match(agents, caps)
            self._json([r.to_dict() for r in results])
        elif path == "/proximity":
            cap = params.get("capability", [None])[0]
            agents = registry.active_agents
            scored = scorer.score_agents(agents, [cap] if cap else [])
            self._json([{"agent_id": a.agent_id, "name": a.name, "score": round(s, 3)} for a, s in scored])
        elif path == "/bottles/inbox":
            mb = router.get_mailbox("keeper")
            if mb:
                unread = mb.unread()
                self._json({"unread": len(unread), "bottles": [b.bottle.to_dict() for b in unread]})
            else:
                self._json({"unread": 0, "bottles": []})
        elif path == "/bottles/pool":
            pool_name = params.get("pool", ["fleet-general"])[0]
            pool = router.get_pool(pool_name)
            if pool:
                self._json({"pool": pool_name, "size": pool.size, "active": pool.active_count})
            else:
                self._json({"error": "pool not found"}, 404)
        elif path == "/stats":
            self._json({
                "registry": registry.stats(),
                "discovery": {"active": discovery.active_count, "total": discovery.total_count},
                "routing": {"pools": router.pool_count, "mailboxes": router.mailbox_count},
            })
        else:
            self._json({
                "endpoints": [
                    "/status", "/agents", "/agents/active", "/agent/<name>",
                    "/discover?capability=<cap>", "/match?capabilities=a,b,c",
                    "/proximity?capability=<cap>",
                    "/bottles/inbox", "/bottles/pool?pool=<name>",
                    "/stats",
                ]
            })

    def do_POST(self):
        if not self.require_keeper_auth():
            return  # Auth failed, response already sent
        parsed = urlparse(self.path)
        path = parsed.path
        body = self._read_body()

        if path == "/register":
            name = body.get("name", "unknown")
            rec = AgentRecord(
                agent_id=name,
                name=body.get("display_name", name),
                capabilities=body.get("capabilities", []),
                endpoint=body.get("endpoint", body.get("host", "")),
                trust_score=body.get("trust_score", 0.5),
                load=body.get("load", 0.0),
            )
            is_new = registry.register(rec)
            # Auto-create mailbox
            router.create_mailbox(name)
            # Auto-broadcast beacon
            discovery.receive(BeaconSignal(
                agent_id=name, name=rec.name,
                capabilities=rec.capabilities, endpoint=rec.endpoint,
            ))
            save_state()
            forward_to_agent_api(body, "/register")
            self._json({"status": "registered" if is_new else "updated", "name": name})

        elif path == "/heartbeat":
            name = body.get("name")
            if registry.heartbeat(name):
                rec = registry.get(name)
                if "load" in body:
                    rec.load = body["load"]
                if "status" in body:
                    rec.status = AgentStatus(body["status"])
                # Refresh beacon
                discovery.receive(BeaconSignal(
                    agent_id=name, name=rec.name,
                    capabilities=rec.capabilities, endpoint=rec.endpoint,
                ))
                save_state()
                self._json({"status": "ack", "active_agents": len(registry.active_agents)})
            else:
                self._json({"error": "not registered"}, 404)

        elif path == "/bottle/send":
            """Send a bottle through the fleet routing system."""
            sender = body.get("from", "unknown")
            recipient = body.get("to", "*")
            content = body.get("content", "")
            pool_name = body.get("pool", "fleet-general")
            btype = BottleType(body.get("type", 2))  # default broadcast
            priority = Priority(body.get("priority", 1))

            bottle = Bottle(
                sender=sender, recipient=recipient, content=content,
                bottle_type=btype, priority=priority,
                tags=body.get("tags", []),
            )
            success = router.send(bottle, pool_name)
            if success:
                state_data["bottles_sent"] = state_data.get("bottles_sent", 0) + 1
                save_state()
                self._json({"status": "sent", "bottle_id": bottle.bottle_id})
            else:
                self._json({"error": "pool not found"}, 404)

        elif path == "/bottle/collect":
            """Collect bottles for an agent."""
            agent_id = body.get("agent", "unknown")
            pool_name = body.get("pool", "fleet-general")
            limit = body.get("limit", 50)
            pool = router.get_pool(pool_name)
            if pool:
                bottles = pool.collect(agent_id, limit=limit, tags=body.get("tags"))
                mb = router.get_mailbox(agent_id)
                if mb:
                    mb.read_all()
                self._json({"bottles": [b.to_dict() for b in bottles]})
            else:
                self._json({"error": "pool not found"}, 404)

        else:
            self._json({"error": "unknown endpoint",
                        "post_endpoints": ["/register", "/heartbeat", "/bottle/send", "/bottle/collect"]}, 404)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def _json(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    import os
    port = int(os.environ.get("KEEPER_PORT", 8900))
    server = HTTPServer(("0.0.0.0", port), KeeperHandler)
    print(f"🔮 Keeper v2 on port {port}")
    print(f"   keeper-beacon: registry + discovery + matching")
    print(f"   bottle-protocol: fleet routing + mailboxes")
    print(f"   Agents loaded: {registry.size}")
    print(f"   Pools: {router.pool_count}")
    server.serve_forever()
